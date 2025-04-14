# read the toc file and extract the href and name pairs

import yaml
import pandas as pd

dir = 'c:/gitprivate/azure-ai-docs-pr/articles/ai-foundry'
csvfile = 'ai-foundry-toc.csv'

# Load the YAML file
with open(f'{dir}/toc.yml', 'r') as file:
    toc = yaml.safe_load(file)

# Initialize an empty list to store the pairs
pairs = []

# Function to recursively extract href and name pairs
def extract_pairs(items):
    for item in items:
        if 'href' in item and 'name' in item:
            pairs.append({'href': item['href'], 'name': item['name']})
        if 'items' in item:
            extract_pairs(item['items'])

# Extract pairs from the top-level items
extract_pairs(toc['items'])

# Convert the list of pairs to a DataFrame
df = pd.DataFrame(pairs)

# Save the DataFrame to a CSV file
df.to_csv(csvfile, index=False)
print(f"Saved to {csvfile}")