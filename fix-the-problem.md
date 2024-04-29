# Fix the problem 

When the pr-report shows a problem in a PR, you need to fix the problem before you can approve the PR.

The problems that will break our build are:

* A file that we reference is being deleted.
* An id or notebook cell name is being deleted.

Before the PR can be approved, we need to make sure that the docs that reference these files or ids are updated.  The PR report gives the name of the referencing file(s) that need to be fixed.

## No fix necessary

In some cases, the name of the notebook cell or id that was deleted is not actually used in the referencing file.  In that case, you can approve the PR without making any changes.  

### Example

You'll see the following output from `python GitHub/pr-report.py 2779`:

```
MODIFIED FILES: 4
Modified File: sdk/python/endpoints/batch/deploy-pipelines/hello-batch/sdk-deploy-and-test.ipynb 
  Referenced in:
   https://github.com/MicrosoftDocs/azure-docs-pr/edit/main/articles/machine-learning/how-to-use-batch-pipeline-deployments.md
   Notebook cells deleted: 1
   * previews
*azureml-examples temp-fix branch has the same version of this file as main

Fix these references in our docs before approving this PR.

Modified File: sdk/python/endpoints/batch/deploy-pipelines/training-with-components/sdk-deploy-and-test.ipynb 
  Referenced in:
   https://github.com/MicrosoftDocs/azure-docs-pr/edit/main/articles/machine-learning/how-to-use-batch-training-pipeline.md
   Notebook cells deleted: 1
   * python38-azureml
*azureml-examples temp-fix branch has the same version of this file as main

Fix these references in our docs before approving this PR.
```

But when you go to https://github.com/MicrosoftDocs/azure-docs-pr/edit/main/articles/machine-learning/how-to-use-batch-pipeline-deployments.md, you won't find the cell name "previews" referenced anywhere in the document. So there's nothing to fix here.

Likewise, when you go to https://github.com/MicrosoftDocs/azure-docs-pr/edit/main/articles/machine-learning/how-to-use-batch-training-pipeline.md, you won't find a reference to a cell named "python38-azureml".  So again, there is nothing to fix here.

## Quick fix in azure-docs-pr

If you can quickly fix the reference in azure-docs-pr, do so.  For example, if the reference is no longer necessary, remove it.  Or perhaps if it is a single line of code, replace the reference with the hard-coded line.  (Don't do this for anything longer than one or two lines, though.)

* Create a PR in azure-docs-pr to apply this fix.  
* After your azure-docs-pr PR with the fix is merged, you can approve the azureml-examples PR.

## Move to a temporary branch

If you can't do a quick fix, follow this process:

1. If the file in question is the same as the one on the temp-fix branch, skip 2 and go on to step 3.  (You'll see this information in the PR report.)
1. If the file is not the same as on the temp-fix branch, check to see if the temp-fix branch is currently in use in azure-docs-pr.  Search for ~/azureml-examples-temp-fix in our directory (on the main branch, after pulling from upstream main).  Or run find-snippets. - it will report on all active branches in our docs.  
	1. If temp-fix is not in use, checkout the branch temp-fix in azureml-docs.  Then pull from upstream main.  Push your changes to upstream/temp-fix. This will update all the files in the temp-fix branch to the latest versions. 
	1. If temp-fix IS in use, you don't want to mess with other referenced files that haven't been fixed yet, so you can't just pull all of upstream main. In this case, COPY the file(s) from azureml-examples, **main branch** that are causing you to reject the PR.  Checkout temp-fix in azureml-examples and paste those files into the branch.  Push your changes to upstream/temp-fix. This will update the files in the temp-fix branch to the latest versions prior to the new PR.
1. Create a PR in azure-docs-pr to use **~/azureml-examples-temp-fix** instead of **~/azureml-examples-main** for the reference(s) to the problem file/id(s).
1. Once your PR in azure-docs-pr is merged to main, you can approve the azureml-examples PR.
> NOTE FOR RELEASE BRANCHES: During Build or Ignite, when there are release branches, this process is more complex. All those release branches also need your update.  Coordinate with the Build/Ignite roadshow owner before you approve the PR.  They'll need to sync main into the release branches before you can approve the original azureml-examples PR.
1. Create a work item to update these articles to again use ~/azureml-examples-main after the azureml-examples PR has merged.  We want to minimize the time that an article references a file on the temp-fix branch.

### Example

You'll see the following output from `python GitHub/pr-report.py 2888`:

```
MODIFIED FILES: 1
Modified File: cli/setup.sh 
  Referenced in:
   https://github.com/MicrosoftDocs/azure-docs-pr/edit/main/articles/machine-learning/how-to-deploy-automl-endpoint.md
   https://github.com/MicrosoftDocs/azure-docs-pr/edit/main/articles/machine-learning/how-to-configure-cli.md
   Code cells deleted: 2
   * # <az_configure_defaults>
   * # </az_configure_defaults>
*azureml-examples temp-fix branch has the same version of this file as main

Fix these references in our docs before approving this PR.
```

There are two docs that reference the file cli/setup.sh.  The ID `az_configure_defaults` is being deleted in the PR. 

My first question would to be ask the PR author why they are deleting this section.  Is it no longer necessary?  If so, delete the references to it in the docs as well, (https://github.com/MicrosoftDocs/azure-docs-pr/edit/main/articles/machine-learning/how-to-deploy-automl-endpoint.md & 
   https://github.com/MicrosoftDocs/azure-docs-pr/edit/main/articles/machine-learning/how-to-configure-cli.md)

If it was a mistake (they didn't think the comments mattered and just deleted them), ask them to put the comments back.

If the rename was for some good reason (the old name was confusing, perhaps), the temp-fix branch contains the same version of the file as main.  So you can switch the references in the docs to point to the temp-fix branch (instead of main) for this particular id.  That is, change:

:::code language="azurecli" source="~/azureml-examples-**main**/cli/setup.sh" id="az_configure_defaults":::

to:

:::code language="azurecli" source="~/azureml-examples-**temp-fix**/cli/setup.sh" id="az_configure_defaults":::

Once your change has merged to main in azure-docs-pr, you can approve the PR in azureml-examples.

Once the azureml-examples change has merged, you can go back to the docs and update the references to point back to main.  This is a temporary fix, so we want to minimize the time that the docs reference the temp-fix branch.