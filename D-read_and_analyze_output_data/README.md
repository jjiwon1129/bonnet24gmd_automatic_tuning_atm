In this folder, three jupyter notebooks are available:

- `0_Plotting_PPEs_parameters_and_outputs.ipynb` plots the parameters and outputs of the PPEs.
- `1_Hyperparameter_tuning_SobolAnalysis.ipynb` conducts a hyperparameter tuning and the Sobol Analysis.
- `2_Implausibility.ipynb` runs the History Matching technique: emulator training, hyperparameter tuning, 
implausibility metrics estimation and selection of the next sampling
- `3_Param-to-output-map-1st-2nd-3rd_4thdPPE.ipynb` generates parameter-to-output maps for the 1st and 2nd PPE together, and for the 3rd and 4th PPE together (appendix of the paper) and an other plot with subsets of these two plots. 
- `4_Evaluation.ipynb` to generate the evaluation plots with additional metrics


### What the user has to do:

The user should successively run the five notebooks. The three first notbooks (0_, 1_, 2_) should be ran in the numbering order for each iteration of the history matching technique. The two last notebooks (3_, 4_) can be ran at anytime.
The user can update: the name of the table files to be read (in 0_ ), the implausilibility metrics threshold (in 2_) so that the new selected sampling is large enough to explore the parameter space and small enough to focus on the are of interest of the parameter-to-output map.
