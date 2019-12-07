# Releaser
This app can be used to to create a release file for SQL code. Basicaly you can select one or more merge commits (tipicaly to a master branch) and all updated/modified SQL scripts will be combined (appended) in one SQL script (split by "Go" command). This release script can be then run in PROD environment.

**Steps**:
1) Run the code (python Releaser.py). The following dialog will pop up:

![Gui](https://github.com/VankatPetr/Python/blob/master/Releaser/sreenshots/gui.png)

2) Select your local repository and an SQL file into which all SQL scripts will be copied:

![Gui Repo and File](https://github.com/VankatPetr/Python/blob/master/Releaser/sreenshots/gui_repo_and_file.png)

3) Click on Load Commits. This will list last 30 merge commits on your current Git branch (you can adjust the code to automaticaly checkout the desired branch - typicaly your master branch)

4) Select the merges you want to release and click on Update Release File. This will copy all upadated/modified SQL scripts into the selected release file (separated by 'Go').
