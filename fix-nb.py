# Change notebook links and images to markdown syntax
# usage: python fix-notebook-links.py <filename>

import sys
import re

# read the file argument
filename = sys.argv[1]

# read the contents of the file
with open(filename, 'r') as file:
    content = file.read()

# remove any /en-us/ from links
pattern = 'https://learn.microsoft.com/en-us/'
replacement = 'https://learn.microsoft.com/'
content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

# remove https://docs.microsoft.com/azure/machine-learning/ from links
pattern = r'https://docs\.microsoft\.com/azure/machine-learning/(.*?)'
replacement = r'\1.md'
content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

# change image links
#  ![explain text](image.png) -> :::image type="content" source="image.png" alt-text="explain text":::

pattern = r'!\[(.*?)\]\((.*?)\)' # thank you Copilot for creating this regex
replacement = r':::image type="content" source="\2" alt-text="\1":::'
content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

# write the result back to the same file
with open(filename, 'w') as file:
    file.write(content)

