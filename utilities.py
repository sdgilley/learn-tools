# some functions to use for create-codeowners and find-snippets

# function to clean up the matches
def cleanup_matches(match):
    import os
    match= match.replace('(', '').replace(')', '').replace('"', '').replace(',', '').replace('source=', '')
    #print(f"** match is {match}")
     # split up the match into parts here.
    path = os.path.dirname(match)
    ref_file = os.path.basename(match)
    # the first part of the path, after ~/, is the "path-to-root"  which includes the branch name
    # path-to-root is configured in azure-docs-pr/.openpublishing.publish.config.json
    branch = path.split('/')[1] 
    # remove the branch info to get the path to the file in azureml-examples
    path = path.replace('~/', '')
    if path == branch:
        path = ''
    else:
        path = path.replace(f"{branch}/",'')
    if "?" in ref_file:
        ref_file, name = ref_file.split('?',1)
    else:
        name = ''
    if path != '': # if the path is empty, we don't want a beginning slash.  
        ref_file = f"{path}/{ref_file}"
    ref_file = ref_file.replace('///', '/').replace('//','/') # get rid of triple or double slashes
    return(path, ref_file, branch, match, name)

# function to read the file - try utf-8 first, then latin-1
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as target_file:
            lines = target_file.readlines()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as target_file:
                lines = target_file.readlines()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            lines = []
    return lines


# Function to delete duplicate rows in a file
def remove_duplicates_and_sort(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Remove duplicates by converting the list to a set and back to a list
    lines = list(set(lines))

    # Sort the lines
    lines.sort()

    with open(file_path, 'w') as f:
        f.writelines(lines)

# this function gets the changes for a specific file and looks through to see if 
# notebook cells or code snippet comments were deleted.

def find_changes(thisfile, prfiles):
    import re
    patch = [file['patch'] for file in prfiles if file['filename'] == thisfile]
    nb_cell = r'(\\n[\+-])\s*"name":\s*"([^"]*)"' # finds added or deleted cells with a name
    code_cell = r'(\\n[\+-])(#\s*<[^>]*>)' # finds lines that start with # <> or # </> 
                                         # only works for files that use # as comment.
    adds = []
    deletes = []
    nb = False

    if thisfile.endswith('.ipynb'):
        nb = True
        matches = re.findall(nb_cell, str(patch))
    else:
        matches = re.findall(code_cell, str(patch))

    for match in matches:
        if match[0] == "\\n+":
            adds.append(match[1]) 
        elif match[0 == "\\n-"]:
            deletes.append(match[1])
        else:
            print("ERROR in utilities.py find_changes. The match was not an add or delete.")

    return(nb, adds, deletes) 

