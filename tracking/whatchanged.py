import pandas as pd
import os

# yearly summary
# to form the file, execute the following in a git bsh window in the directory of the repo:
# change to your name.  omit --until if you want till now
# git  whatchanged --author='Sheri Gilley' --since '04/01/2023' --until '04/01/2024' --oneline --pretty=format: | sort | uniq >> mychanges.csv
# put the file in the same directory as this script

# fix truncation
pd.set_option('display.max_colwidth', 500)
# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Join the directory with the filename
file_path = os.path.join(script_dir, "mychanges.csv")

# # Read the csv file
column_names = ['V1', 'V2', 'V3', 'V4', 'ChangeType', 'Filename', 'Filename2']
changed = pd.read_csv(file_path, header=None, sep="\s+", names=column_names)
# print(changed[['ChangeType', 'Filename', 'Filename2']])
# keep only the necessary columns
changed = changed[['ChangeType', 'Filename', 'Filename2']]
# print(changed)
# find the unique filename/type combos
unique = changed.drop_duplicates().copy()

# some lines had two filenames, split them out and then append them to the unique list
extra = unique[unique['Filename2'].notnull()][['ChangeType','Filename2']].copy()
# now drop filename2 from unique
unique = unique[['ChangeType','Filename']]
# Rename 'Filename2' to 'Filename' in extra
extra = extra.rename(columns={'Filename2': 'Filename'})
# Append extra to unique
# print(f'unique {type(unique)} extra {type(extra)}')
# print(f'unique {unique.shape} extra {extra.shape}')
unique = pd.concat([unique, extra])

## Ready to process the files
# get file type from filename
unique['FileType'] = unique['Filename'].apply(lambda x: os.path.splitext(x)[1])

# show counts for unique files
print(pd.crosstab(index=unique['ChangeType'], columns=unique['FileType']))

# show the added files
print("Added:")
print(unique[(unique['FileType'] == ".md") & (unique['ChangeType'] == 'A')]['Filename'])

# show the deleted files
print("Deleted:")
print(unique[(unique['FileType'] == ".md") & (unique['ChangeType'] == 'D')]['Filename'])


# If you want to investigate the files further, write a csv file:
unique.to_csv("filechanges.csv", index=False)