"""
Change links in a file you're going to move to v1
usage: python move-to-v1.py <filename>

To move a file from machine-learning to machine-learning/v1:

* First, open a terminal and run this script on the file you're going to move.
* After running this script, check diffs to verify changes. (If you move it first, 
  you won't be able to see diffs as the whole file will be new.)
* Then move to v1.  Also move the associated media folder.
* Search for other articles that link to the file you moved move and update the links
* Create PR to get a build and make sure you didn't miss any files in our folders that need updating.
* Finally, add redirect to catch links from elsewhere.  
  (Wait until after that first build to add the redirect.)

"""
import sys

# read the file argument
filename = sys.argv[1]

# read the contents of the file
with open(filename, "r") as file:
    content = file.read()

# replace all occurrences of a string in the file
import re

# first, remove occurrences of "./" in the links to normalize the links
pattern = r"(?<!\.\./)\((?!\.\./)[^)]*?\./"  # thank you Copilot for creating this regex
content = re.sub(pattern, "", content, flags=re.MULTILINE)

# now shift local links up one level if they don't start with v1/
pattern = r"\((?!v1/)([^)]*\.md)\)"  # thank you Copilot for creating this regex
replace = r"(../\1)"
content = re.sub(pattern, replace, content, flags=re.MULTILINE)

# finally, remove the v1/ from the links to other v1 articles
pattern = r"\(v1/([^)]*\.md)\)"  # thank you Copilot for creating this regex
replace = r"(\1)"
content = re.sub(pattern, replace, content, flags=re.MULTILINE)

# write the result back to the same file
with open(filename, "w") as file:
    file.write(content)
