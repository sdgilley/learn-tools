import os
from datetime import datetime

def get_snippet_files(file_path):
    """Reads a file and returns a list of file names."""
    with open(file_path, 'r') as file:
        lines = [line.split('@')[0] for line in file]  # Get the file name, not the codeowners
    return lines

def get_tutorial_files(file_path):
    # note the tutorials file is a csv file with different structure for the files
    # turn it into an ~/azureml-examples-path name 
    lines = []
    with open(file_path, 'r') as file:
        file.readline()  # Skip the first line
        for line in file:  # Read the rest of the lines
            line = line.split(',')[0]
            line = line.replace('https://raw.githubusercontent.com/Azure/azureml-examples/', '')
            # get rid of the branch name, which is the first part of the path
            line = '/'.join(line.split('/')[1:])
            line = '/' + line
            print(line)
            lines.append(line)
    return lines

def write_html(notebooks):
    """Writes an HTML file for each type of notebook."""
    wf_link = "https://github.com/Azure/azureml-examples/actions/workflows"  # Where to find the workflows
    gh_link = "https://github.com/Azure/azureml-examples/blob/main"  # Where to find the files
    rows_by_extension = {}
    today = datetime.now().strftime('%B %d, %Y')

    for notebook in notebooks:
        debug=False
        if notebook == '/tutorials/get-started-notebooks/quickstart.ipynb':
            print("Processing quickstart notebook")
            debug = True
        workflow = notebook.replace('/', '-')[1:]  # Get rid of leading '-'
        workflow = workflow.replace('sdk-python', 'sdk')  # Special case for python files
        workflow = os.path.splitext(workflow)[0] + ".yml"  # Replace extension with .yml

        extension = os.path.splitext(notebook)[1].strip()
        rows_by_extension.setdefault(extension, [])  # Initialize an empty list if this extension hasn't been seen before

        file = notebook.split('/')[-1].replace('.', '&#46;')  # Last part of the path is the file name
        file_name = os.path.splitext(file)[0]
        file = file.replace('%20', ' ').replace('&#46;', '.')  # Put back the spaces and dots in the file name for better readability

        status = f'<a href="{wf_link}/{workflow}"><img src="{wf_link}/{workflow}/badge.svg?branch=main" alt="{file_name}"></a>'
        row = f'<tr><td>{status}</td><td><a href="{gh_link}/{notebook}">{file}</a></td></tr>\n'
        rows_by_extension[extension].append(row)
        if debug:
            print(f'Here is the complete row: {row}')

    
    # Read the top part of the html file from top.html 
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Get the directory that the script is in
    repo_dir = script_dir #find the repo directory
    while not os.path.isdir(os.path.join(repo_dir, '.git')):
        repo_dir = os.path.dirname(repo_dir)
    file_dir = os.path.join(repo_dir, "docs")  # Where to put the dashboard files

    # write the dashboards.html page
    with open(os.path.join(script_dir, 'dashboard.html'), 'r') as file:
        dashboard_content = file.read()
    file_path = os.path.join(file_dir, 'dashboards.html')
    with open(file_path, 'w') as file:
        file.write(dashboard_content)
        file.write(f'<p class="update">Last update: {today}</p>\n')
        file.write("<div class='small-table'><table><tr><th>File type</th><th class='number'>#</th></tr>\n")
        for extension, rows in sorted(rows_by_extension.items()):
            if extension:
                ext = extension[1:].strip()  # Get rid of the leading dot
                file.write(f"<tr><td><a href='{ext}.html'>{extension}</a></td><td class='number'>{len(rows)}</td></tr>\n")  # Add the 'number' class to the cell
        file.write('</table></div>\n')
    
    # write the individual dashboard files

    # read top and jumps from the script directory
    with open(os.path.join(script_dir, 'top.html'), 'r') as file:
        top_contents = file.read()
    with open(os.path.join(script_dir, 'jumps.html'), 'r') as file:
        jumps_contents = file.read()
    with open(os.path.join(script_dir, 'disclaimer.html'), 'r') as file:
        disclaimer_contents = file.read()
    with open(os.path.join(script_dir, 'disclaimer2.html'), 'r') as file:
        disclaimer2_contents = file.read()

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
                file.write(f'<p class="update">{len(rows)} files. Last update: {today}</p>\n')
                if extension in ['.json', '.sh', '.py']:
                    file.write(disclaimer_contents)
                if extension in ['.yml', '.yaml']:
                    file.write(disclaimer2_contents)
                file.write('<table>\n')
                file.write('<tr><th>Workflow</th><th>File</th></tr>\n')

                for row in rows:
                    file.write(row)
                    file.flush()  # Flush the data to the file

                    if 'get-started-notebooks-quickstart' in row:
                        print(f'HERE IT IS: {row}')  # Print the row
                        print(f'WRITING IT IN {file_path}')  # Print the file path
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

    # Get the file names from the tutorials.csv file
    # Add the file names from the CODEOWNERS.txt file
    snippet_names = get_snippet_files(os.path.join(repo_dir, "GitHub", "CODEOWNERS.txt"))

    # tutorial_names by itself works correctly.  But for some reason, adding to 
    # the snippet_names list doesn't work.  So for now, just using snippet_names, which 
    # is all the files that are pulled into docs during build time.
    # tutorial_names = get_tutorial_files(os.path.join(repo_dir, "GitHub","tutorials.csv"))
    # file_names = tutorial_names + snippet_names
    file_names = snippet_names
    # Replace spaces with '%20' in notebook names
    file_names = [file.replace('\\ ', '%20') for file in file_names]

    # create the dashboards
    write_html(file_names)
