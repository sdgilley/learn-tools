// generate the workflow and file links based on the user input

document.getElementById('toggle-link').addEventListener('click', function(e) {
    e.preventDefault();
    toggleExample();
});

document.getElementById('form').addEventListener('submit', function(event) {
    event.preventDefault();
    // clear the previous results
    clearAll(); 
    let userInput = document.getElementById('user_input').value.trim();

    // if (!userInput.startsWith('~/azureml-examples-')) {
    //     console.log(userInput);
    //     alert('Please enter a valid code snippet starting with ~/azureml-examples-');
    //     return;
    // }
    // Replace spaces in the name with %20 for the URL
    userInput = userInput.replace(/ /g, "%20");

    //figure out if it is a code snippet or full url
    if (!userInput.startsWith('~/azureml-examples-') && !userInput.startsWith('https://github.com/Azure/azureml-examples/blob/')) {
        // if it is neither, show an error message and return
        document.getElementById('workflow_link').innerHTML = `Please enter a valid code snippet starting with <b>~/azureml-examples-</b> or a full URL starting with <b>https://github.com/Azure/azureml-examples/blob/</b>`;
        return;  
    }

    if (userInput.startsWith('~/azureml-examples-')){
        //this is a code snippet
        // Remove the ~/azureml-examples- prefix and any arguments after the ?
        userInput = userInput.split('?')[0].replace('~/azureml-examples-', '')
    }

    else if (userInput.startsWith('https://github.com/Azure/azureml-examples')){
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
    toggleExplain('show');
    // hide the example
    toggleExample('hide');
});

function clearAll() {
    document.getElementById('workflow_link').innerHTML = '';
    document.getElementById('file_link').innerHTML = '';
    toggleExample('hide');
    toggleExplain('hide');
}

function toggleExample(status) {
    var section = document.getElementById('toggle-section');
    var link = document.getElementById('toggle-link');

    if (status === 'show') {
        section.style.display = 'block';
        link.innerHTML = '<i class="fa-solid fa-caret-down"></i> Hide examples';
    } else if (status === 'hide') {
        section.style.display = 'none';
        link.innerHTML = '<i class="fa-solid fa-caret-right"></i> Show examples';
    } else {
        if (section.style.display === 'none') {
            section.style.display = 'block';
            link.innerHTML = '<i class="fa-solid fa-caret-down"></i> Hide examples';
        } else {
            section.style.display = 'none';
            link.innerHTML = '<i class="fa-solid fa-caret-right"></i> Show examples';
        }
    }
}
function toggleExplain(status) {
    let explainElements = document.getElementsByClassName('explain');
    for (let i = 0; i < explainElements.length; i++) {
        if (status === 'show') {
            explainElements[i].style.display = 'block';
        } else if (status === 'hide') {
            explainElements[i].style.display = 'none';
        } else {
            if (explainElements[i].style.display === 'none') {
                explainElements[i].style.display = 'block';
            } else {
                explainElements[i].style.display = 'none';
            }
        }
    }
}

