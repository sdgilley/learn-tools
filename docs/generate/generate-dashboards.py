import os
from datetime import datetime

def get_notebooks(file_path):
    """Reads a file and returns a list of notebook names."""
    with open(file_path, 'r') as file:
        lines = [line.split('@')[0] for line in file]  # Get the file name, not the codeowners
    return lines

def write_html(notebooks):
    """Writes an HTML file for each type of notebook."""
    wf_link = "https://github.com/Azure/azureml-examples/actions/workflows"  # Where to find the workflows
    gh_link = "https://github.com/Azure/azureml-examples/blob/main"  # Where to find the files
    rows_by_extension = {}
    today = datetime.now().strftime('%B %d, %Y')

    for notebook in notebooks:
        workflow = notebook.replace('/', '-')[1:]  # Get rid of leading '-'
        workflow = workflow.replace('sdk-python', 'sdk')  # Special case for python files
        workflow = os.path.splitext(workflow)[0] + ".yml"  # Replace extension with .yml

        extension = os.path.splitext(notebook)[1]
        rows_by_extension.setdefault(extension, [])  # Initialize an empty list if this extension hasn't been seen before

        file = notebook.split('/')[-1].replace('.', '&#46;')  # Last part of the path is the file name
        file_name = os.path.splitext(file)[0]
        file = file.replace('%20', ' ').replace('&#46;', '.')  # Put back the spaces and dots in the file name for better readability

        status = f'<a href="{wf_link}/{workflow}"><img src="{wf_link}/{workflow}/badge.svg?branch=main" alt="{file_name}"></a>'
        row = f'<tr><td>{status}</td><td><a href="{gh_link}/{notebook}">{file}</a></td></tr>\n'
        rows_by_extension[extension].append(row)

    # Read the top part of the html file from top.html 
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Get the directory that the script is in
    repo_dir = script_dir
    while not os.path.isdir(os.path.join(repo_dir, '.git')):
        repo_dir = os.path.dirname(repo_dir)
    file_dir = os.path.join(repo_dir, "docs")  # Where to put the dashboard files

    with open(os.path.join(script_dir, 'top.html'), 'r') as top_file:
        top_contents = top_file.read()
    with open(os.path.join(script_dir, 'jumps.html'), 'r') as jumps_file:
        jumps_contents = jumps_file.read()

    for extension, rows in sorted(rows_by_extension.items()):
        if extension:
            ext = extension[1:].strip()  # Get rid of the leading dot
            file_path = os.path.join(file_dir, f'{ext}.html')
            with open(file_path, 'w') as file:
                print("Writing", file_path)
                file.write(f'<html>\n<head>\n<title>{extension} code snippets dashboard</title>\n')
                file.write(top_contents)
                file.write(f'<h1> {extension} code snippets dashboard</h1>\n')
                file.write(jumps_contents)
                file.write(f'<p class="update">Last update: {today}</p>\n')
                file.write(f'<a name={extension}></a><h2>{extension}</h2>\n')
                file.write('<table>\n')
                for row in rows:
                    file.write(row)
                file.write('</table>\n')
                file.write('</body>\n</html>')
# This is the main function
if __name__ == "__main__":
    import os

    # Get the directory that the script is in
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Find the root directory of the repository
    repo_dir = script_dir
    while not os.path.isdir(os.path.join(repo_dir, '.git')):
        repo_dir = os.path.dirname(repo_dir)

    # Construct the path to the CODEOWNERS.txt file
    file_path = os.path.join(repo_dir, "GitHub", "CODEOWNERS.txt")

    # Get the notebook names
    notebook_names = get_notebooks(file_path)

    # Replace spaces with '%20' in notebook names
    notebook_names = [notebook.replace('\\ ', '%20') for notebook in notebook_names]
    # print the files
    write_html(notebook_names)