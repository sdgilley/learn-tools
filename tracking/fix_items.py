# Read work items 
def fix_titles(work_items):
    if work_items['Title'].str.contains('Freshness - over 90:').any():
        over90 = work_items[work_items['Title'].str.contains('Freshness - over 90:')]
        over90.loc[:, 'Title'] = over90['Title'].str.replace(r'^Freshness - over 90:  ', '', regex=True)
        replace = " - Azure AI Foundry"
        over90.loc[:, 'Title'] = over90['Title'].str.replace(replace, '', regex=True)
    
    # we don't care about the over 180 here, this is for Foundry which is all over 90    
    # but if we did, it uses file name not title
    return over90

def fix_engagement(engagement):
    # # keep only the columns we need: Url, PageViews
    engagement = engagement[['Title','PageViews']]
    # strip  - Azure Machine Learning from the title
    engagement['Title'] = engagement['Title'].str.replace(r' - Azure Machine Learning$', '', regex=True)
    engagement['PageViews'] = engagement['PageViews'].str.replace(',', '')
    engagement['PageViews'] = pd.to_numeric(engagement['PageViews'])# # keep only the columns we need: Url, PageViews
    engagement = engagement[['Title','PageViews']]
    # strip  - Azure Machine Learning from the title
    engagement['Title'] = engagement['Title'].str.replace(r' - Azure Machine Learning$', '', regex=True)
    engagement['PageViews'] = engagement['PageViews'].str.replace(',', '')
    engagement['PageViews'] = pd.to_numeric(engagement['PageViews'])

if __name__ == "__main__":
    import os
    import pandas as pd

    script_dir = os.path.dirname(__file__)
    work_items = pd.read_csv(os.path.join(script_dir, "SE Content Freshness.csv"))
    work_items['before'] = work_items['Title']
    work_items = fix_titles(work_items)
    csvfile = os.path.join(script_dir, 'fixing.csv')
    temp = work_items[['before','Title']]
    temp.to_csv(csvfile)