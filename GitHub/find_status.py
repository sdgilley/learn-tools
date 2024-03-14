# input a ~/azureml-examples link and find the workflow status
# example: ~/azureml-examples-main/sdk/python/jobs/single-step/scikit-learn/train-hyperparameter-tune-deploy-with-sklearn/train-hyperparameter-tune-with-sklearn.ipynb?name=credential

# test cases - first one  has no workflow
# user_input = "~/azureml-examples-main/sdk/python/jobs/single-step/scikit-learn/train-hyperparameter-tune-deploy-with-sklearn/train-hyperparameter-tune-with-sklearn.ipynb?name=credential"
# user_input = "~/azureml-examples-main/cli/assets/component/train.yml"
if 'user_input' not in globals():
    user_input = input("Enter the file path: ")
#strip out the query string and ~/azureml-examples- from the input
user_input = user_input.split('?')[0].replace('~/azureml-examples-','')
# the first part of the string is now the branch
branch = user_input.split('/')[0]
file = user_input.replace(f'{branch}/','')
wf = file.replace('/','-') # workflow file name uses - for each / in the file path

wf_link = "https://github.com/Azure/azureml-examples/actions/workflows" # where to find the workflows
gh_link = f"https://github.com/Azure/azureml-examples/blob/{branch}" # where to find the files
print(f'** Workflow: {wf_link}/{wf}')
print(f'** File: {gh_link}/{file}')