// generate the workflow and file links based on the user input

document.getElementById('form').addEventListener('submit', function(event) {
    event.preventDefault();

    let userInput = document.getElementById('user_input').value.trim();

    // if (!userInput.startsWith('~/azureml-examples-')) {
    //     console.log(userInput);
    //     alert('Please enter a valid code snippet starting with ~/azureml-examples-');
    //     return;
    // }
    // Replace spaces in the name with %20 for the URL
    userInput = userInput.replace(/ /g, "%20");

    //figure out if it is a code snippet or full url
    if (userInput.includes('~/azureml-examples-')){
        //this is a code snippet
        // Remove the ~/azureml-examples- prefix and any arguments after the ?
        userInput = userInput.split('?')[0].replace('~/azureml-examples-', '')
    }

    else if (userInput.includes('https://github.com/Azure/azureml-examples')){
        //this is a full url
        // Remove the url
        userInput = userInput.split('?')[0].replace('https://github.com/Azure/azureml-examples/blob/','');
        // also remove double slashes
        userInput = userInput.replace('//','/');
    }
    // The first part of the path is the branch
    const branch = userInput.split('/')[0].trim(); 
    // The rest of the path is the file path
    let file = userInput.replace(`${branch}/`, '').trim(); 
    // replace all / with - to form the workflow name
    let wf = file.replace(/\//g, '-');

    // if the path was sdk-python, workflow just used python.
    wf = wf.replace('sdk-python', 'sdk');

    // now split out the extension to get the name. 
    // There might be multiple splits because the filename may have a . in it.
    let fileParts = wf.split('.');
    fileParts.pop();  // last part is the extension, so remove it. Then put the rest back together.
    let wfname = fileParts.join('.');

    // Finally, form the links
    const wfLink = `https://github.com/Azure/azureml-examples/actions/workflows/${wfname}.yml`;
    const ghLink = `https://github.com/Azure/azureml-examples/blob/${branch}/${file}`;

    // populate the document with the links
    document.getElementById('workflow_link').innerHTML = `Workflow: <a href="${wfLink}"><img src="${wfLink}/badge.svg?branch=main" alt="${wfLink}"</a>`;
    document.getElementById('file_link').innerHTML = `File: <a href="${ghLink}">${ghLink}</a>`;
    // un-hide any element(s) with the class 'explain'
    let explainElements = document.getElementsByClassName('explain');
    for (let i = 0; i < explainElements.length; i++) {
        explainElements[i].style.display = 'block';  
    }
});