import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
from SALib.sample import latin
from SALib.analyze import sobol


def constant_kernel_params(Y_train_column):
    """Y_train의 출력값 스케일을 기반으로 ConstantKernel 초기값과 범위 추천"""
    y_range = np.max(Y_train_column) - np.min(Y_train_column)
    y_std = np.std(Y_train_column)

    init = max(1e-3, y_std)  # 너무 작으면 0으로 수렴하므로 하한 설정
    lower = init / 100
    upper = init * 100

    return init, (lower, upper)


def train_gpr_models(X_train, Y_train):
    """Train independent Gaussian Process Regressors for each output."""
    n_features = X_train.shape[1]

    length_scale_bounds = [
        (1e-4, 1e-1),   # c0_c1
        (1e-5, 5e-2),   # xlamdd_xlamde
        (1e-2, 5.0),    # clam
        (1e-4, 0.5),   # cxlamu
        (1e-3, 0.5),   # ssolar
        (1.0, 1e3),     # ALPHA0
    ]

    models = []

    for i in range(Y_train.shape[1]):
        y_col = Y_train[:, i]
        const_init, const_bounds = constant_kernel_params(y_col)

        kernel = ConstantKernel(const_init, const_bounds) * RBF(
            length_scale=np.ones(n_features),
            length_scale_bounds=length_scale_bounds
        )

        model = GaussianProcessRegressor(
            kernel=kernel,
            normalize_y=True,
            n_restarts_optimizer=5,
            random_state=0  # 재현성 확보
        )

        model.fit(X_train, y_col)
        models.append(model)

    return models

def predict_gpr_models(models, X):
    """Predict mean and std for each model over ``X``."""
    means = []
    stds = []
    for m in models:
        mean, std = m.predict(X, return_std=True)
        means.append(mean)
        stds.append(std)
    return np.column_stack(means), np.column_stack(stds)


def sample_lhs(parameter_bounds, n_samples, seed=None):
    """Generate LHS samples using SALib."""
    names = list(parameter_bounds)
    bounds = [parameter_bounds[name] for name in names]
    problem = {
        "num_vars": len(names),
        "names": names,
        "bounds": bounds,
    }
    X = latin.sample(problem, N=n_samples, seed=seed)
    return X, problem


def compute_implausibility(pred_mean, pred_std, y_obs, sigma_obs):
    """Return the implausibility score for emulator predictions."""
    return np.abs(pred_mean - y_obs) / np.sqrt(pred_std ** 2 + sigma_obs ** 2)


def filter_samples(X, implausibility, n_keep, group1_indices=[0, 1, 2]):
    """Select ``n_keep`` non-implausible samples using an automatic threshold.

    Parameters
    ----------
    X : ndarray, shape (n_samples, n_features)
    implausibility : ndarray, shape (n_samples, n_outputs)
    group1_indices : sequence of int
        Indices of core output metrics.
    n_keep : int
        Desired number of samples to retain.

    Returns
    -------
    X_keep : ndarray
        Selected non-implausible samples.
    mask : ndarray of bool
        Boolean mask of ``X`` indicating selected rows.
    rho1 : float
        The smallest threshold value satisfying the ``n_keep`` requirement.
    """
    if n_keep <= 0:
        return np.empty((0, X.shape[1])), np.zeros(X.shape[0], dtype=bool), 0.0

    n_outputs = implausibility.shape[1]
    group1 = np.array(group1_indices, dtype=int)
    group2 = np.setdiff1d(np.arange(n_outputs), group1)

    core_max = implausibility[:, group1].max(axis=1) if group1.size else np.zeros(len(X))
    other_max = implausibility[:, group2].max(axis=1) if group2.size else np.zeros(len(X))

    required_rho = np.maximum(core_max, other_max / 2)
    sorted_rho = np.sort(required_rho)

    idx = min(n_keep - 1, len(sorted_rho) - 1)
    rho1 = sorted_rho[idx]

    candidate_mask = required_rho <= rho1
    candidate_idx = np.where(candidate_mask)[0]

    # Choose n_keep samples with lowest overall maximum implausibility
    if candidate_idx.size > n_keep:
        max_impl = np.max(implausibility[candidate_idx], axis=1)
        order = np.argsort(max_impl)
        candidate_idx = candidate_idx[order][:n_keep]

    mask = np.zeros(X.shape[0], dtype=bool)
    mask[candidate_idx] = True
    return X[mask], mask, float(rho1)


def perform_sobol_analysis(problem, X, Y):
    """Run Sobol sensitivity analysis on non-implausible data."""
    return sobol.analyze(problem, Y, calc_second_order=False)


def history_matching_iteration(
    X_train,
    Y_train,
    parameter_bounds,
    y_obs,
    sigma_obs,
    n_samples=300000,
    seed=None,
    n_keep=30,
    group1_indices=[0, 1, 2],
):
    """Perform one iteration of emulator-based history matching"""
    if group1_indices is None:
        group1_indices = []

    # Train emulator(s)
    models = train_gpr_models(X_train, Y_train)

    # Generate candidate samples
    X_test, problem = sample_lhs(parameter_bounds, n_samples, seed)
    pred_mean, pred_std = predict_gpr_models(models, X_test)

    # Implausibility calculation
    impl = compute_implausibility(pred_mean, pred_std, y_obs, sigma_obs)
    X_keep, mask, rho1 = filter_samples(X_test, impl, n_keep, group1_indices)
    Y_keep = pred_mean[mask]

    return models, X_keep, Y_keep, impl, rho1, mask


def run_multi_iteration_history_matching(
    X_train,
    Y_train,
    parameter_bounds,
    y_obs,
    sigma_obs,
    n_iterations=1,
    n_samples=300000,
    seed=None,
    n_keep=30,
    group1_indices=[0, 1, 2],
):
    """Run multiple iterations of history matching"""
    print("\u25B6 Start: Running multi-iteration history matching")
    rng = np.random.default_rng(seed)
    bounds = parameter_bounds.copy()
    results = []
    final_models = None

    for i in range(n_iterations):
        print(f"\n [Iteration {i+1}/{n_iterations}] started")
        iter_seed = int(rng.integers(0, 2**32 - 1))
        print(" - Generating samples and training emulator...")
        models, X_keep, Y_keep, impl, rho1, mask = history_matching_iteration(
            X_train,
            Y_train,
            bounds,
            y_obs,
            sigma_obs,
            n_samples=n_samples,
            seed=iter_seed,
            n_keep=n_keep,
            group1_indices=group1_indices,
        )
        print(f" - Number of non-implausible samples: {len(X_keep)} (rho1={rho1:.3f})")

        results.append(
            {
                "models": models,
                "X_keep": X_keep,
                "Y_keep": Y_keep,
                "implausibility": impl,
                "parameter_bounds": bounds.copy(),
                "rho1": rho1,
                "mask": mask,
            }
        )

        final_models = models

        # Update bounds based on retained samples
        if X_keep.size:
            bounds = {
                name: [X_keep[:, j].min(), X_keep[:, j].max()]
                for j, name in enumerate(bounds)
            }
            print(" - Parameter bounds updated")
        else:
            print(" - No samples retained; bounds unchanged")

        if i == n_iterations - 1 or X_keep.size == 0:
            print(" - Stopping condition reached")
            break

    print("\n Performing final Sobol sensitivity analysis...")
    # Sobol analysis using the final emulator on a new sample
    sobol_seed = int(rng.integers(0, 2**32 - 1))
    X_sobol, problem = sample_lhs(parameter_bounds, n_samples, sobol_seed)
    pred_mean, _ = predict_gpr_models(final_models, X_sobol)

    output_names = ["TOASW", "TOALW", "TOAnet", "tcld_CLARA", "tcld_ESA", "pwat"]
    sobol_all = {}
    for i, name in enumerate(output_names):
        indices = perform_sobol_analysis(problem, X_sobol, pred_mean[:, i])
        sobol_all[name] = indices
    print(" Done: Completed full process including sensitivity analysis\n")

    return results, sobol_all, bounds


# 1. 사용자 정의: 초기 학습 데이터
df = pd.read_csv("training_data.csv")

X_train = df[["c0_c1", "xlamdd_xlamde", "clam", "cxlamu", "ssolar", "ALPHA0"]].to_numpy()

Y_train = df[["TOASW", "TOALW", "TOAnet", "tcld_CLARA", "tcld_ESA", "pwat"]].to_numpy()

# 2. 관측값과 오차
# TOASW, TOALW, TOAnet, tcld_CLARA, tcld_ESA, pwat
y_obs = np.array([240.5, -240.5, 0.5, 62.7, 65.1, 24.1])         # 각 output의 관측 목표값
sigma_obs = np.array([0.5, 0.5, 0.5, 1e-6, 1e-6, 1e-6])                   # 각 output의 관측 오차

# 3. 파라미터 경계
parameter_bounds = {
    "c0_c1": [1e-3, 5e-3],
    "xlamdd_xlamde": [5e-5, 6e-4],
    "clam": [0.05, 0.2],
    "cxlamu": [5e-4, 6e-3],
    "ssolar": [0.99, 1.2],
    "ALPHA0": [50, 100],
}

# 4. history matching
results, sobol_all, bounds = run_multi_iteration_history_matching(
    X_train,
    Y_train,
    parameter_bounds,
    y_obs,
    sigma_obs,
    n_iterations=1,
    n_samples=300000,
    seed=42,
    n_keep=30,
    group1_indices=[0, 1, 2],
)

# 5. 저장
import pickle

output_data = {
    "results": results,
    "sobol_all": sobol_all,
    "bounds": bounds,
}

with open("PPE2.pkl", "wb") as f:
    pickle.dump(output_data, f)





