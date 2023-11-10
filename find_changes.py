# for modified files - see if they are referenced
# if so, print along with where it is refrenced from
# also, print all notebook cells that were modified (added or deleted)
def find_changes(thisfile, prfiles):
    import re
    patch = [file['patch'] for file in prfiles if file['filename'] == thisfile]
    nb_cell = r'(\\n[\+-]\s*"name":\s*"[^"]*")'
    print("checking for cells")
    # print(patch)
    matches = re.findall(nb_cell, str(patch))
    for match in matches:
        print(f"** Notebook cell modified: {match}")