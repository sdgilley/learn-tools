# Import necessary libraries
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.identity import DefaultAzureCredential
## Function to authenticate with Azure DevOps
## and return a connection object
def authenticate_ado(ado_url = "https://dev.azure.com/msft-skilling"):  
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