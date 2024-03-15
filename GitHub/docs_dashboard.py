import os

def get_notebooks(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()  
        lines = [line.split('@')[0] for line in lines] # all we need is the file name, not the codeowners
    return lines

def write_readme(notebooks):
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Get the directory that the script is in
    readme_file = os.path.join(script_dir,"DASHBOARD.md")

    wf_link = "https://github.com/Azure/azureml-examples/actions/workflows" # where to find the workflows
    gh_link = "https://github.com/Azure/azureml-examples/blob/main" # where to find the files
    rows_by_extension = {}

    for notebook in notebooks:
        workflow = notebook.replace('/', '-')
        workflow = workflow[1:] # get rid of leading '-'
        workflow = workflow.replace('sdk-python','sdk') # special case for python files
        workflow = os.path.splitext(workflow)[0] + ".yml" # replace extension with .yml

        extension = os.path.splitext(notebook)[1]
        # If this extension hasn't been seen before, initialize an empty list for it
        if extension not in rows_by_extension:
            rows_by_extension[extension] = []

        # print(workflow)
        file = notebook.split('/')[-1].replace('.', '&#46;') # last part of the path is the file name
        file_name = os.path.splitext(file)[0]
        # now put back the spaces and dots in the file name for better readability
        file = file.replace('%20', ' ').replace('&#46;', '.')
        # print(f"FILE: {file}, File name: {file_name}")
        status = f"[![{file_name}]({wf_link}/{workflow}/badge.svg?branch=main)]({wf_link}/{workflow})"
        row = f"|{status} | [{file}]({gh_link}/{notebook})|\n"
        # Add the row to the list for this extension
        rows_by_extension[extension].append(row)

    # Now, iterate over the dictionary to write each list of rows to a separate table
    with open(readme_file, 'w') as f:
        prefix = "# Files referenced in docs \n\n These files are referenced in https://learn.microsoft.com/azure/machine-learning \n\n"
        f.write(prefix)
        # f.write('Jump to:\n')
        # for extension in sorted(rows_by_extension.keys()):
        #     # Write a link to each section
        #     ext = extension.replace(".", "")
        #     f.write(f'[{ext}](#{ext})\n')

        for extension, rows in sorted(rows_by_extension.items()):
            # Write a header for each extension
            if extension != '': # ignore the files without extension
                f.write(f'## {extension} files\n')
                f.write('| Status | File |\n')
                f.write('| --- | --- |\n')
                for row in rows:
                    f.write(row)
    print("finished writing DASHBOARD...")


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