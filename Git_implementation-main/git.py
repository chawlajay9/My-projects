"""
Build the minimal git impletation based on Zipfile

- Create Repository
- Create Commits
- Clone Commits (Reset your project to previous commit)
- List all Respositories
- List all Commits
"""

import os
from pickle import DICT
import sys
import json
from typing import List, Dict
import zipfile


# define directories for Git
BASE_DIR = os.path.expanduser("./git/")
REPOS_DIR = os.path.expanduser("./git/repo/")

# Check if the repositories folder already exists. if not, we create it.
if not os.path.isdir(os.path.normpath(REPOS_DIR)):
    os.makedirs(os.path.normpath(REPOS_DIR))


# Create empty directory as Database and load the content og "git.db" if it exists
db: Dict[str, List] = {}

if os.path.isfile(os.path.normpath(os.path.expanduser(BASE_DIR + "git.db"))):
    db = dict(
        json.load(
            open(os.path.normpath(os.path.expanduser(BASE_DIR + "git.db")), "r")
        )
    )


def dump():
    """
    This function writes the contents of our dictionry 'db' to a file using json
    so that it can be read later
    """

    path: str = os.path.normpath(os.path.expanduser(BASE_DIR + "git.db"))
    try:
        json.dump(db, open(path, "w"), indent=4)
    except Exception as e:
        print("Could not save database: ", e)


def create_repo(name: str):
    """
    Create a new repository.
    It basically adds the repository's name to the database and creates the directory for it.
    """
    if name not in db:
        db[name] = []
        os.makedirs(os.path.normpath(REPOS_DIR + name))
    else:
        print(f" Repository {name} already exists")
    dump()


def list_repos():
    """
    Lists all the respositories there are so far
    """
    if len(db) > 0:
        for key in db:
            print(str(key))
    else:
        print("There are no repositories, created")


def list_commits(repo: str):
    """
    Lists all the 
    """
    if repo in db:
        print("\n".join(db[repo]))
    else:
        print("Sorry there is no such repository")


def zipdir(path: str, repo: str, commit_name: str):
    """
    Create a zipfil containing the contents of a folder and saves it be the folder specified in the commit_name argument.
    """
    # we represent the contents of gitignore to a list
    gitignore: List[str] = []
    if os.path.isfile(".gitignore"):
        with open(".gitignore", "r") as f:
            gitignore = [line.strip() for line in f.readlines()]

    # the folder must exist for this to work
    with zipfile.ZipFile(
        os.path.normpath(REPOS_DIR + repo + f"/{commit_name}.zip"),
        "w",
        zipfile.ZIP_DEFLATED,
    ) as ziph:
        for root, dirs, files in os.walk(path):
            for file_ in files:
                if file_ not in gitignore:
                    # files whose names are in gitignore are not added
                    ziph.write(os.path.join(root, file_))


def commit(repo: str, commit_name: str):
    """
    Creates a commit and saves the new contents of the folder to the repository folder with name as commit_name
    """
    if repo in db:
        commits = db[repo]
        if not commit_name in commits:
            zipdir(".", repo, commit_name)
            commits.append(f"{commit_name}")
            db[repo] = commits
            dump()
        else:
            print("Commit with the name already exists")
    else:
        print(f"Repository {repo} does not exist. Please create it first.")


def clone(repo: str, commit_name: str):
    """
    Clones the contents of a commit in a repository to the current directory
    This is archieved by copying the zipfile related to the commit and expanding the contents to our directory
    replacing the already exist content
    """
    if repo in db:
        if commit_name in db[repo]:
            try:
                path = os.path.normpath(
                    REPOS_DIR + f"{repo}/{commit_name}.zip")
                with zipfile.ZipFile(path, "r") as zipf:
                    zipf.extractall(path=os.curdir)
            except Exception as e:
                print(f"Error closing commit_name {commit_name} \n", e)
        else:
            print("Commit does not exist")
    else:
        print("Respository does not exist")


if __name__ == "__main__":
    # BAsic commands info to print in console
    commands = """
                Your command was not understood.
                Try command such as
                git list
                git list <Repository_name>
                git clone <respository_name> <commit_name> 
                git create <repository_name>   
                git commit <repository_name> <commit_name>           
                """
    commit_name: str
    repo: str
    if len(sys.argv) > 1:
        if sys.argv[1] == "clone" and len(sys.argv) == 4:
            repo = sys.argv[2]
            commit_name = sys.argv[3]
            clone(repo, commit_name)
            print(f"cloning {commit_name} from repository {repo}")
        elif sys.argv[1] == "commit" and len(sys.argv) == 4:
            repo = sys.argv[2]
            commit_name = sys.argv[3]
            commit(repo, commit_name)
            print(
                f"Commiting directory with {commit_name} to repository {repo}")
        elif sys.argv[1] == "list" and len(sys.argv) == 2:
            list_repos()
        elif sys.argv[1] == "list" and len(sys.argv) >= 2:
            list_commits(sys.argv[2])
        elif sys.argv[1] == "create" and len(sys.argv) == 3:
            create_repo(sys.argv[2])
        else:
            print(commands)
    else:
        print(commands)
