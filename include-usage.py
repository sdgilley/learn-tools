# Script to count the number of times an include file is used in a set of articles
# Usage: python include-usage.py
# Before usage, set the include_path and doc_path variables to the appropriate values

import os, glob

# Define the directory path for your include files
include_path = 'c:/work/azure-docs-pr/articles/machine-learning/includes/*.md'
# Define the directory path for your articles
doc_path = 'c:/work/azure-docs-pr/articles/machine-learning'

# Get the list of filenames in the include file directory
filenames = [os.path.basename(include) for include in glob.glob(include_path)]

# Create a dictionary so we can keep a count.
include_files = {el:0 for el in filenames}

# Loop through the doc files; note that this doesn't recurse through sub-folders
docs = glob.glob(doc_path + '/*.md')
for doc in docs:
    # Open the file
    with open(doc, 'r', encoding='utf-8') as f:
        # Loop through the lines
        for line in f:
            # Look for the include statement (note that this is case sensitive)
            if line.startswith('[!INCLUDE'):
                # Get the filepath out of the include statement
                filepath = line.split('(')[1].split(')')[0]
                # Strip the path off so we just have the filename
                filename = os.path.basename(filepath)
                # Is the filename in the include_files dictionary?
                if filename in include_files:
                    # Increment the count
                    include_files[filename] += 1


# Print the results
for key, value in include_files.items():
    print(key, value)