'''
Functions to work with Azure DevOps (ADO) API
This module contains functions to authenticate with Azure DevOps and perform operations
!IMPORTANT - sign in with az login --use-device-code before running this script
''' 

# Import necessary libraries
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.identity import DefaultAzureCredential
import os
import pandas as pd
from azure.devops.v7_0.work_item_tracking.models import Wiql

## Function to authenticate with Azure DevOps
## and return a connection object
def authenticate_ado(ado_url="https://dev.azure.com/msft-skilling"):  
    try:
        # Authenticate with Azure Active Directory (Entra ID)
        credential = DefaultAzureCredential()
        access_token = credential.get_token("499b84ac-1321-427f-aa17-267ca6975798/.default").token

        # Create a BasicAuthentication object with the access token
        credentials = BasicAuthentication('', access_token)

        # Connect to Azure DevOps
        connection = Connection(base_url=ado_url, creds=credentials)
        return connection
    except Exception as e:
        print("Error connecting to Azure DevOps:")
        print("Run `az login --use-device-code` before running this script.")
        exit(1)


def query_work_items(query, columns):
    # Authenticate with Azure DevOps
    connection = authenticate_ado()
    wit_client = connection.clients.get_work_item_tracking_client()

    # Define the WIQL query
    wiql_query = Wiql(query)

    # Execute the WIQL query
    wiql_result = wit_client.query_by_wiql(wiql=wiql_query)

    if not wiql_result.work_items:
        print("No work items found.")
        return pd.DataFrame()
    
    # Fetch work item details
    work_item_ids = [item.id for item in wiql_result.work_items]
    work_items = wit_client.get_work_items(ids=work_item_ids)

    # Create a dataframe from the work items
    work_items_df = pd.DataFrame([{
        column.replace('System.', ''): (work_item.fields.get(column, {}).get('displayName', '') if column == 'System.AssignedTo' else work_item.fields.get(column, ''))
        for column in columns
    } for work_item in work_items])

    # Convert 'CreatedDate' to datetime if it exists in columns
    if 'CreatedDate' in columns:
        work_items_df['CreatedDate'] = pd.to_datetime(work_items_df['CreatedDate'], errors='coerce')
        # Remove closed items last changed more than 90 days ago - need freshness again.
        cutoff_date = pd.Timestamp.now(tz='UTC') - pd.Timedelta(days=90)
        work_items_df = work_items_df[~((work_items_df['State'] == 'Closed') & (work_items_df['CreatedDate'] < cutoff_date))]

    return work_items_df

## function to query for freshness, supply the title you're looking for
def query_freshness(title_string, days=90):
    project_name = "Content"

    # Define the WIQL query
    columns = ['System.Id', 'System.Title', 'System.State', 
               'System.CreatedDate', 'System.IterationPath', 'System.AssignedTo']
    # limit to work items created in the last 365 days, otherwise will be too large for ML queries
    query=f"""
        SELECT {','.join(columns)}
        FROM workitems
        WHERE [System.TeamProject] = '{project_name}'
        AND [System.CreatedDate] >= @StartOfMonth('-365d')
        AND [System.Title] CONTAINS '{title_string}'
        AND [System.State] <> 'Removed'
        """

    # execute the query
    work_items_df = query_work_items(query, columns)
    # convert to datetime for implementing the cutoff date check
    work_items_df['CreatedDate'] = pd.to_datetime(work_items_df['CreatedDate'], errors='coerce')
    # Remove closed items Created before the freshness time period 
    # These need freshness again!
    start_of_month = pd.Timestamp.now(tz='UTC').replace(day=1)
    cutoff_date = start_of_month - pd.Timedelta(days=days)
    cutoff_date = cutoff_date.replace(day=1) # start at first of month
    work_items_df = work_items_df[~((work_items_df['State'] == 'Closed') & (work_items_df['CreatedDate'] < cutoff_date))]
    return work_items_df

# Call the function
if __name__ == "__main__":
    project_name = "Content"
    # provide vars needed for query
    title_string = "Freshness - over 90:  "
    # call the query_freshness function:
    work_items_df = query_freshness(title_string)
    print(f"Freshness query, total work items found: {work_items_df.shape[0]}")
