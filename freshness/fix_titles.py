# Read work items 
def fix_titles(df, freshness_title=None):
    import re
    new = df.copy()
    if freshness_title:
        pattern = f"^{re.escape(freshness_title)}"
        new.loc[:, 'Title'] = new['Title'].str.replace(pattern, '', regex=True)
        # also remove quotes in the title
    # remove quotes from titles
    new['Title'] = new['Title'].str.replace(r'"', '')
    new['Title'] = new['Title'].str.replace(r"'", '')
    # remove - Azure Machine Learning from the title
    new['Title'] = new['Title'].str.replace(r' - Azure Machine Learning$', '', regex=True)
    # strip  - Azure AI Foundry from the title
    new['Title'] = new['Title'].str.replace(r' - Azure AI Foundry$', '', regex=True)
    # remove leading blanks
    new['Title'] = new['Title'].str.strip()
    # remove trailing blanks
    new['Title'] = new['Title'].str.rstrip()
    return new

if __name__ == "__main__":
    import os
    import pandas as pd

    script_dir = os.path.dirname(__file__)
    work_items = pd.read_excel(os.path.join(script_dir, "Jan-engagement.xlsx"))
    work_items['before'] = work_items['Title']
    work_items = fix_titles(work_items)
    csvfile = os.path.join(script_dir, 'fixing.csv')
    temp = work_items[['before','Title']]
    temp.to_csv(csvfile)