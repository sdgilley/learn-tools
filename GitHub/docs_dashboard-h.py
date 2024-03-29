import os

def get_notebooks(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()  
        lines = [line.split('@')[0] for line in lines] # all we need is the file name, not the codeowners
    return lines

def write_html(notebooks):
    html_file = os.path.join("docs","dashboard.html")
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

        file = notebook.split('/')[-1].replace('.', '&#46;') # last part of the path is the file name
        file_name = os.path.splitext(file)[0]
        # now put back the spaces and dots in the file name for better readability
        file = file.replace('%20', ' ').replace('&#46;', '.')
        status = f'<a href="{wf_link}/{workflow}"><img src="{wf_link}/{workflow}/badge.svg?branch=main" alt="{file_name}"></a>'
        row = f'<tr><td>{status}</td><td><a href="{gh_link}/{notebook}">{file}</a></td></tr>\n'
        rows_by_extension[extension].append(row)

    # read the top part of the html file from top.html 
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Get the directory that the script is in
    with open(os.path.join(script_dir,'top.html'), 'r') as top_file:
        top_contents = top_file.read()
    with open(os.path.join(script_dir,'jumps.html'), 'r') as jumps:
        jumps = jumps.read()
    for extension in sorted(rows_by_extension.keys()):
        rows = rows_by_extension[extension]      
        ext = extension[1:].strip() # get rid of the leading dot
        if extension != '':
            with open(f'docs/{ext}.html', 'w') as file:
                file.write(f'<html>\n<head>\n<title>{extension} code snippets dashboard</title>\n')
                file.write(top_contents)
                file.write(f'<h1> {extension} code snippets dashboard</h1>\n')
                file.write(jumps)
                rows = rows_by_extension[extension]      
                file.write(f'<a name={extension}></a><h2>{extension}</h2>\n')
                file.write('<table>\n')
                for row in rows:
                    file.write(row)
                file.write('</table>\n')
                file.write('</body>\n</html>')

# This is the main function
if __name__=="__main__": 
    # get the notebook names
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Get the directory that the script is in
    file_path = os.path.join(script_dir, "CODEOWNERS.txt")  # Join it with the file name
    # file_path = os.path.join(script_dir, "test.txt")  # Join it with the file name

    notebooks = get_notebooks(file_path)
    notebooks = [notebooks.replace('\\ ','%20') for notebooks in notebooks] # replace space with &nbsp;
    # print(notebooks)
    write_html(notebooks)