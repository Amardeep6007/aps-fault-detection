# neurolab-mongo-python

![image](https://user-images.githubusercontent.com/57321948/196933065-4b16c235-f3b9-4391-9cfe-4affcec87c35.png)

### Step 1 - Install the requirements

```bash
pip install -r requirements.txt
```

### Step 2 - Run main.py file

```bash
python main.py
```

This changes are made by Amardeep Kumar in neuro lab


Useful Git Commands

step 1: if we are starting with project and want to use git in our project then use the below command

```
git init 
```
The above command is going to initialize the git in our source code

Alternate method to start can be --
Clone the existing git hub repository

```
git clone <github_url>
```

The above command will clone or download the github repository in our system

Step 2: Add the changes made in the file to git stagging area

```
git add "file_name"
```
Note: In the above command,  We can use filename to add a specific file or the "."(dot) to add all the files to the git stagging area

Step 3: commit
```
git commit -m "Your message"
```

Step 4:
```
git push origin "branch_name"
```
Note: In the above code "origin" contains the url of your gtihub repo.

(OR)
If we want to forcefully push the changes in to the github then , 

```
git push origin main -f
```

Step 5: To pull the changes from the git hub repo
```
git pull origin "branch_name"
```
