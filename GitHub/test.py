import utilities as h

repo_name = "Azure/azureml-examples"
repo_branch = "main"
repo = h.connect_repo(repo_name)
contents = repo.get_contents('.github/CODEOWNERS', ref=repo_branch).decoded_content.decode().splitlines()

start_index = 0
end_index = 0
for i, line in enumerate(contents):
    if line.startswith('#### files'):
        start_index = i
    if line.startswith('# End of docs'):
        end_index = i
        break

contents = contents[start_index+1:end_index]

# print(contents)
# print(len(contents))

codeowners = h.read_codeowners()
print(codeowners)
print(len(codeowners))
