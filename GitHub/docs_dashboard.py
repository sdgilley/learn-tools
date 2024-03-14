import os

def get_notebooks(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()  
        lines = [line.split('@')[0] for line in lines] # all we need is the file name, not the codeowners
    return lines

def write_readme(notebooks):
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Get the directory that the script is in
    readme_file = os.path.join(script_dir,"DASHBOARD.md")
    f = open(readme_file, "w")
    prefix = "# Files referenced in docs \n\n These files are referenced in https://learn.microsoft.com/azure/machine-learning \n\n| status | file |\n |---|---|\n"
    f.write(prefix)

    wf_link = "https://github.com/Azure/azureml-examples/actions/workflows" # where to find the workflows
    gh_link = "https://github.com/Azure/azureml-examples/blob/main" # where to find the files

    for notebook in notebooks:
        workflow = notebook.replace('/', '-')
        workflow = workflow[1:] # get rid of leading '-'
        workflow_name = os.path.splitext(workflow)[0] + ".yml" # replace extension with .yml
        # print(workflow_name)
        file = notebook.split('/')[-1].replace('.', '&#46;') # last part of the path is the file name
        file_name = os.path.splitext(file)[0]
        # print(f"FILE: {file}, File name: {file_name}")
        status = f"[![{file_name}]({wf_link}/{workflow_name}/badge.svg?branch=main)]({wf_link}/{workflow})"
        row = f"|{status} | [{file}]({gh_link}/{notebook})|\n"
        f.write(row)
    print("finished writing DASHBOARD...")
    f.close()


# This is the main function
if __name__=="__main__": 
    # get the notebook names
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Get the directory that the script is in
    file_path = os.path.join(script_dir, "CODEOWNERS.txt")  # Join it with the file name
    # file_path = os.path.join(script_dir, "test.txt")  # Join it with the file name

    notebooks = get_notebooks(file_path)
    notebooks = [notebooks.replace('\\ ','%20') for notebooks in notebooks] # replace space with &nbsp;
    # print(notebooks)
    write_readme(notebooks)