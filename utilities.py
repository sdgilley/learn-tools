# some functions to use for create-codeowners and find-snippets

# function to clean up the matches
def cleanup_matches(match):
    import os
    match= match.replace('(', '').replace(')', '').replace('"', '').replace(',', '').replace('source=', '')
     # split up the match into parts here.
    path = os.path.dirname(match)
    ref_file = os.path.basename(match)
    # the first part of the path, after ~/, is the "path-to-root"  which includes the branch name
    # path-to-root is configured in azure-docs-pr/.openpublishing.publish.config.json
    branch = path.split('/')[1] 
    # remove the branch info to get the path to the file in azureml-examples
    path = path.replace('~/', '').replace(f"{branch}/",'')
    if "?" in ref_file:
        ref_file, name = ref_file.split('?',1)
    else:
        name = ''
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
