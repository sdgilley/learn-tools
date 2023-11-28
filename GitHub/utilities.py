# some functions to use for find-snippets, pr-report, and merge-report

# function to clean up the matches
# syntax of a match is different if it is from a notebook vs. code files.
# returns info about the match:
#       path to the file in azureml-examples
#       file name of the file being referenced
#       branch used to find the file(i.e., azureml-examples-main)
#       match - the full match
#       name - the name of the notebook cell 
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
    if "?" in ref_file: # split out the id name from the ref_file if it exists
        ref_file, name = ref_file.split('?',1)
    else:
        name = ''
    if path != '': # if the path is empty, we don't want a beginning slash.  
        ref_file = f"{path}/{ref_file}" # add the path to the ref_file
    ref_file = ref_file.replace('///', '/').replace('//','/') # get rid of triple or double slashes
    return(path, ref_file, branch, match, name) # right now, not using match and name.  But might in the future


# this function gets the changes for a specific file in a PR.
# Then searches for notebook cells or code snippets the were added/deleted.
# Returns a tuple with a boolean for whether the file is a notebook, 
# a list of added cells, and a list of deleted cells.
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

# function to read local file - try utf-8 first, then latin-1
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

def read_snippets():
    import os
    import pandas as pd
    # read the snippets file
    fn = "refs-found.csv"
    mydir = os.path.abspath(__file__)
    snippet_fn = os.path.join(os.path.dirname(mydir), fn)
    # Check if snippets file exists
    if os.path.exists(snippet_fn):
        snippets = pd.read_csv(snippet_fn)
    else:
        print(f"{snippet_fn} does not exist.")
        print("Run 'find-snippets.py' to create the file.")
        sys.exit()
    return snippets