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

def query_work_items(query, columns):
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
    wiql_query = Wiql(query)

    # Execute the WIQL query
    wiql_result = wit_client.query_by_wiql(wiql=wiql_query)

    # Fetch the details of each work item
    work_item_ids = [item.id for item in wiql_result.work_items]
    work_items = wit_client.get_work_items(ids=work_item_ids)

    # Create a dataframe from the work items
    work_items_df = pd.DataFrame([{
        column: (work_item.fields.get(column, {}).get('displayName', '') if column == 'System.AssignedTo' else work_item.fields.get(column, ''))
        for column in columns
    } for work_item in work_items])


    # Convert 'ChangedDate' to datetime if it exists in columns
    if 'ChangedDate' in columns:
        work_items_df['ChangedDate'] = pd.to_datetime(work_items_df['ChangedDate'], errors='coerce')
        # Remove closed items last changed more than 90 days ago - need freshness again.
        cutoff_date = pd.Timestamp.now(tz='UTC') - pd.Timedelta(days=90)
        work_items_df = work_items_df[~((work_items_df['State'] == 'Closed') & (work_items_df['ChangedDate'] < cutoff_date))]

    return work_items_df

# Call the function
if __name__ == "__main__":
    project_name = "Content"
    # provide vars needed for quer
    title_string = "Freshness - over 90:  "
    # make sure you list all the columns you want returned from the query
    columns = ['System.Id', 'System.Title', 'System.State', 
               'System.AssignedTo', 'System.IterationPath', 'System.ChangedDate']
    query = f"""
        SELECT {','.join(columns)}
        FROM workitems
        WHERE [System.TeamProject] = '{project_name}'
        AND [System.Title] CONTAINS '{title_string}'
        AND [System.State] <> 'Removed'
        """
    work_items = query_work_items(query, columns)
    script_dir = os.path.dirname(__file__)
    csv_file = os.path.join(script_dir, 'work_items.csv')
    work_items.to_csv(csv_file, index=False)
    print(f"Saved to {csv_file}")