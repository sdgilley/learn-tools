# Read work items 
def fix_titles(df, suffix, prefix=None):
    import re
    new = df.copy()
    if prefix:
        pattern = f"^{re.escape(prefix)}"
        new.loc[:, 'Title'] = new['Title'].str.replace(pattern, '', regex=True)
    # remove quotes from titles
    new['Title'] = new['Title'].str.replace(r'"', '').str.replace(r"'", '')
    # remove suffix from the title
    new['Title'] = new['Title'].str.replace(f"r'{suffix}$'", '', regex=True)
    # remove leading & trailing blanks
    new['Title'] = new['Title'].str.strip().str.rstrip()
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