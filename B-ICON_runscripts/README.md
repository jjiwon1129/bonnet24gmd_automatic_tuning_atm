[for the reader: this is exactly the same info as in the main ../README.md file]

This step uses the sampling generated above to create an ensemble of ICON runs. These scripts start from a template ICON run file, copies it the same number of times as the size of the parameter sampling, and replaces the values of the parameters with the values in the sampling. In this folder, one template file has been included: this template is designed for the PPE_1 of the paper. It contains default tags "ParameterParameterParameter" that are replaced with the sampling values for the 6 parameters of PPE_1 using the script 1_LHCPPE_make_runfile_PaperExample.sh.

### What the user has to do:

In your ICON repository `Path-to-your-ICON-repository\`, in the `run\` folder, copy the following script:

> cp A-ICON_runscripts\1_LHCPPE_make_runfile_PaperExample.sh Path-to-your-ICON-repository\run

/!\ You will need to modify the path in the template file: at each line where the following comment is written : 
`[here_a_path_is_defined_and_should_be_changed_by_the_user]` **#TODO: update that path**  

and then run that script in `Path-to-your-ICON-repository\run`:

> bash 1_LHCPPE_make_runfile_PaperExample.sh

Run the ICON runs:
In the ICON repository, in the `run\` folder (not in a subfolder), run the following script: 

> bash 2_LHCPPE_submit_runfiles_PaperExample

This step produces the log and error files, as well as the outputs of the ICON run in the folder `..\experiments`.