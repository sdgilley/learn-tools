# Read work items 
def fix_work_items(work_items, freshness_title):
    import re
    new = work_items.copy()
    pattern = f"^{re.escape(freshness_title)}"
    new.loc[:, 'Title'] = new['Title'].str.replace(pattern, '', regex=True)
        # also remove quotes in the title
    # remove quotes from titles
    new['Title'] = new['Title'].str.replace(r'"', '')
    new['Title'] = new['Title'].str.replace(r"'", '')
    return new

def fix_engagement(engagement):
    # strip  - Azure Machine Learning from the title
    engagement['Title'] = engagement['Title'].str.replace(r' - Azure Machine Learning$', '', regex=True)
 # strip  - Azure AI Foundry from the title
    engagement['Title'] = engagement['Title'].str.replace(r' - Azure AI Foundry$', '', regex=True)
   
    return engagement

if __name__ == "__main__":
    import os
    import pandas as pd

    script_dir = os.path.dirname(__file__)
    work_items = pd.read_csv(os.path.join(script_dir, "SE Content Freshness.csv"))
    work_items['before'] = work_items['Title']
    work_items = fix_work_items(work_items)
    csvfile = os.path.join(script_dir, 'fixing.csv')
    temp = work_items[['before','Title']]
    temp.to_csv(csvfile)