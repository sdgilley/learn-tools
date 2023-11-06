'''
This script reads through the files in your local repo and finds code snippets from azureml-examples
See readme for details of the columns in the output file.
'''
import os
import re
import utilities as h

###################### INPUT HERE ############################
# Name the file and the path to your repo.
repo_path = 'c:\\GitPrivate\\azure-docs-pr\\articles\\machine-learning'
result_fn = "snippets.csv"
############################ DONE ############################

# open the file to write the results to.
f = open(result_fn, 'w+')
f.write("from_file, match, branch, path, ref_file, notebook_cell \n")
# iterate through the files in the folder.  

files = os.listdir(repo_path)

# find the file names from the directory.  
for file in files:
    if file.endswith('.md'):
        file_path = os.path.join(repo_path,file)
        lines = h.read_file(file_path)
        for line in lines:
            # snippets have ~\azureml-examples in them.  Find all snippets and write them to the file.
            match_snippet = re.findall(r'\(~\/azureml-examples[^)]*\)|source="~\/azureml-examples[^"]*"', line)
            if match_snippet:
                for match in match_snippet:
                    path, ref_file, branch, match, name = h.cleanup_matches(match)
                f.write(f"{file}, {match}, {branch}, {path}, {ref_file}, {name} \n")    
# close the csv file.
f.close()

# I usually open the .csv in Excel and create some pivot tables to summarize.  

### NOTE TO SELF
# This finds named cells for notebooks, but not snippet ids for :::code blocks.  Need to add that at some point.
# code blocks look like this:
# :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/online/deploy-with-packages/mlflow-model/deploy.sh" ID="create_deployment_inline" :::


