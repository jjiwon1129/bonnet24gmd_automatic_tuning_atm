# This folder gathers all the scripts to conduct the automatic tuning routine presented in Bonnet, Pastori et al 2024. See paper preprint: https://doi.org/10.5194/egusphere-2024-2508

## Authors
Pauline Bonnet (1)

(1) Deutsches Zentrum für Luft- und Raumfahrt (DLR), Institut für Physik der Atmosphäre, Oberpfaffenhofen, Germany


## Description
This repository contains bash scripts, python scripts and jupyter notebooks that were used for the paper Bonnet, Pastori et al 2024. The following successive steps can be done using these scripts: (A) generate a parameter sampling (of a chosen set of parameters in a given range of maximum and minimum values), (B) create ICON run scripts for each of the parameter values, (C) postprocesses the ICON outputs, (D) fits a Gaussian Process emulator to the parameter-to-output map, runs a large PPE with the emulator, calculates an error function on the outputs of that emulator, and selects the new set of parameters to use for the next ICON PPE.

Note that for the purpouse of scripts sharing and saving computational ressources in a test phase, the first steps (A) and (B) where slightly modified relatively to the used version: instead of generating a size 30 ensemble, here we show the example for a size 3 ensemble, and instead of running the ICON run on 2 or 11 years, we show a template file for a 1 year long simulation. The user can simply change the end year of the simulation from 1980 to 1981 or 1989. Note also that all the experiment folders containing the ICON outputs are not included (to save storage ressources). All the tables (created in step (C)) containing the output metrics of all the ICON PPEs used in the paper are already included in the folder C-Postprocessing_PaperExample/table.

This method is adapted from the History Matching Technique presented in Couvreux et al. 2021. This method was initially presented by Williamson et al., 2017, and has been applied in Hourdin et al., 2021, 2023.

The ICON version used is: ICON-A 2.6.4
The python version used is: python 3.8.13

## How to

The routine is split into the following steps:

1. **A-Generate_a_LHC_sampling**: 
	run the notebook: `0_generate_a_LHC_sampling_and_save_parameter_values.ipynb`
	This notebook generates a Latin Hypercube sampling, creates one file per parameter, which contains the values of the parameter sampling (e.g. the 1st line of all parameter files corresponds to the 1st set of parameters, the 2nd line to the 2nd set, etc.) and saves them in `B-ICON_runscripts\PARAMETER_SAMPLES\`

2. **B-ICON_runscripts**:
	This step uses the sampling generated above to create an ensemble of ICON runs. These scripts start from a template ICON run file, copies it the same number of times as the size of the parameter sampling, and replaces the values of the parameters with the values in the sampling. In this folder, one template file has been included: this template is designed for the PPE_1 of the paper. It contains default tags "ParameterParameterParameter" that are replaced with the sampling values for the 6 parameters of PPE_1 using the script 1_LHCPPE_make_runfile_PaperExample.sh.
	In your ICON repository `Path-to-your-ICON-repository\`, in the `run\` folder, copy the following script:

	> cp A-ICON_runscripts\1_LHCPPE_make_runfile_PaperExample.sh Path-to-your-ICON-repository\run

	/!\ You will need to modify the path in the template file: at each line where the following comment is written : 
	`[here_a_path_is_defined_and_should_be_changed_by_the_user]` #TODO: update that path 

	and then run that script in `Path-to-your-ICON-repository\run`:

	> bash 1_LHCPPE_make_runfile_PaperExample.sh

	Run the ICON runs:
	In the ICON repository, in the `run\` folder (not in a subfolder), run the following script: 

	> bash 2_LHCPPE_submit_runfiles_PaperExample

	This step produces the log and error files, as well as the outputs of the ICON run in the folder `..\experiments`.

3. **C-Postprocessing_PaperExample**:
	Run Postprocessing scripts:

	>>>		
	bash run\1_LHCPPE_create_analysis_runfiles_PaperExample.sh \
	bash run\2_LHCPPE_submit_analysis_runfiles_PaperExample.sh
	>>>

	This step produces _.ps_ tables with all the output metrics for each runs in the folder `\table`. See the `README.md` file in `C-Postprocessing_PaperExample` for more info.

4. **D-read_and_analyze_output_data**:
	- run the notebook: `0_Plotting_PPEs_parameters_and_outputs.ipynb` to plot the parameters and outputs of the PPEs.
	- run the notebook: `1_Hyperparameter_tuning_SobolAnalysis.ipynb` to conduct a hyperparameter tuning and the Sobol Analysis.
	- run the notebook: `2_Implausibility.ipynb` to run the History Matching technic: emulator training, hyperparameter tuning, implausibility metrics estimation and selection of the next sampling 
	- run the notebook: `3_Param-to-output-map-1st-2nd-3rd_4thdPPE.ipynb` to generate parameter-to-output maps
	- run the notebook: `4_Evaluation.ipynb` to generate the evaluation plots with additional metrics

5. **Start again at step 2-**
Using the sampling selected at step 4-, run an ICON PPE in step 2 and continue the following steps, until a converged version of ICON, according to expert knowledge, is reached.

## Licensing
This code is under Creative Commons Attribution 4.0 International 

