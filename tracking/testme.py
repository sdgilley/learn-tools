import os


# git  whatchanged --author='Sheri Gilley' --since '04/01/2023' --until '03/31/2024' --oneline --pretty=format: | sort | uniq >> ../MonthlyReport/sherichanges.csv
command = "cd c:/GitPrivate/azure-docs-pr && git checkout main && git pull"
os.system(command)
command = "git whatchanged --author='Sheri Gilley' --since '04/01/2023' --until '03/31/2024' --oneline --pretty=format: | sort | uniq >> newchanges.csv"
os.system(command)