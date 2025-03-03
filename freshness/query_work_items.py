# !IMPORTANT - sign in with az login --use-device-code before running this script
# query work items from Azure DevOps using the Python SDK
# return a dataframe with the work items
# see bottom for example usage
import os
import pandas as pd
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.identity import DefaultAzureCredential
from azure.devops.v7_0.work_item_tracking.models import Wiql

def query_work_items(title_string, days=90):
    ado_url = "https://dev.azure.com/msft-skilling"
    project_name = "Content"
    
    # Authenticate with Azure Active Directory (Entra ID)
    credential = DefaultAzureCredential()
    access_token = credential.get_token("499b84ac-1321-427f-aa17-267ca6975798/.default").token

    # Create a BasicAuthentication object with the access token
    credentials = BasicAuthentication('', access_token)

    # Connect to Azure DevOps
    connection = Connection(base_url=ado_url, creds=credentials)
    wit_client = connection.clients.get_work_item_tracking_client()

    # Define the WIQL query
    wiql_query = Wiql(
        query=f"""
        SELECT [System.Id], [System.Title], [System.State], [System.ChangedDate], [System.IterationPath], [System.AssignedTo]
        FROM workitems
        WHERE [System.TeamProject] = '{project_name}'
        AND [System.Title] CONTAINS '{title_string}'
        AND [System.State] <> 'Removed'
        """
    )

    # Execute the WIQL query
    wiql_result = wit_client.query_by_wiql(wiql=wiql_query)

    # Fetch the details of each work item
    work_item_ids = [item.id for item in wiql_result.work_items]
    if not work_item_ids:
        print("No work items found.")
        return pd.DataFrame()

    work_items = wit_client.get_work_items(ids=work_item_ids)


    # Create a dataframe from the work items
    work_items_df = pd.DataFrame([{
        'ID': work_item.id, 
        'Title': work_item.fields['System.Title'], 
        'State': work_item.fields['System.State'],
        'Sprint': work_item.fields.get('System.IterationPath'),  # Use .get() to handle missing fields
        'ChangedDate': work_item.fields.get('System.ChangedDate'),  # Use .get() to handle missing fields
        'AssignedTo': work_item.fields.get('System.AssignedTo', {}).get('displayName', '') if work_item.fields.get('System.AssignedTo') else ''
    } for work_item in work_items])
    
    work_items_df['ChangedDate'] = pd.to_datetime(work_items_df['ChangedDate'], errors='coerce')
    # Remove closed items last changed more than 90 days ago - need freshness again.
    now_utc = pd.Timestamp.now(tz='UTC')
    cutoff_date = now_utc - pd.Timedelta(days=days)
    work_items_df = work_items_df[~((work_items_df['State'] == 'Closed') & (work_items_df['ChangedDate'] < cutoff_date))]

    return work_items_df

# Call the function
if __name__ == "__main__":
    title_string = "Freshness - over 360:  "
    work_items_df = query_work_items(title_string)
    # if state is closed, only keep if changed in the last 30 days
    script_dir = os.path.dirname(__file__)
    csv_file = os.path.join(script_dir, 'work_items.csv')
    work_items_df.to_csv(csv_file, index=False)
    print(f"Saved to {csv_file}")