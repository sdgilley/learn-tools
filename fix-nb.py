'''
Change notebook links and images to markdown syntax
usage: python fix-nb.py <filename>

When you use Import Jupyter Notebook to add content to your .md file, the
links and images will need to be updated to work in the .md file.

Run this script in your terminal to apply some common fixes.  You'll still need
to read through the updated content to see if there are other changes you need to make.
'''

import sys
import re

# read the file argument
filename = sys.argv[1]

# read the contents of the file
with open(filename, 'r') as file:
    content = file.read()

# remove any /en-us/ from links
pattern = '/en-us/'
replace = '/'
content = re.sub(pattern, replace, content, flags=re.MULTILINE)

# replace https://learn.microsoft.com/azure/ links with /azure/ links
pattern = r'https://learn.microsoft.com/azure/'
replace = r'/azure/'
content = re.sub(pattern, replace, content, flags=re.MULTILINE)

# replace machine-learning links with relative links
pattern = r'/azure/machine-learning/(.*?)\?view=azureml-api-2'
replace = r'\1.md'
content = re.sub(pattern, replace, content, flags=re.MULTILINE)

# change image links
#  ![explain text](image.png) -> :::image type="content" source="image.png" alt-text="explain text":::

pattern = r'!\[(.*?)\]\((.*?)\)' # thank you Copilot for creating this regex
replace = r':::image type="content" source="\2" alt-text="\1":::'
content = re.sub(pattern, replace, content, flags=re.MULTILINE)

## OR THIS for <img> tags
# <img src="image.png" title="explain text" /> -> :::image type="content" source="image.png" alt-text="explain text":::
# regex pattern to match the img tag
pattern = r'<img.*?src="(.*?)".*?title="(.*?)".*?>'
replace = r':::image type="content" source="\1" alt-text="\2":::'
content = re.sub(pattern, replace, content, flags=re.MULTILINE)

# write the result back to the same file
with open(filename, 'w') as file:
    file.write(content)

# write the result back to the same file
with open(filename, 'w') as file:
    file.write(content)

