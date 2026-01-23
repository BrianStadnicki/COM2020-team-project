## Initial setup

```sh
python -m venv .env
source .env/bin/activate
cd food-waste-rescue
python -m pip install -r requirements.txt
python manage.py migrate
```

## Running server

```sh
source .env/bin/activate
cd food-waste-rescue
python manage.py migrate
python manage.py runserver
```

## Development resources

[Django topic docs](https://docs.djangoproject.com/en/6.0/topics/)

[Bootstrap styling docs](https://getbootstrap.com/docs/5.3/getting-started/introduction/)

[Guide to Git](https://beej.us/guide/bggit/html/split/index.html)

[Guide to Git - conflicts](https://beej.us/guide/bggit/html/split/merge.html)

## Development workflow

- On GitHub:
- Create a github issue
- Assign yourself and any others
- Label appropriately (new stuff is enhancement, docs, bug etc)
- Assign COM2020 work
- Assign milestone (sprint 1, 2 or demo)
- Assign relationships (what it's blocking or blocked by)
- Create a branch (the option is in the "Development" section on the github issue) for it, based off of the current sprint branch
- On VSCode:
- Git fetch from all remotes
- Switch to your new branch
- When committing, include your issue number in the title e.g. "fix misspelling #4"
- If you overwrite your git branch history i.e. undo and change your previous commit, and have already pushed to GitHub, then you should force push to prevent a mess from your previous commit being re-added. (NOTE: never force push to a branch anyone else is working on)
- Before making a pull request, you need to update your branch to the latest state of the current sprint branch. Also useful during development. First pull all remotes, then merge the sprint branch into your current one.
- Once ready, open a pull request against the current sprint branch and assign the relevant reviewers
- Ensure your python code has been ran through the linter before merging, and that your branch is up to date with the sprint branch, and test it.

### Running the linter

```sh
ruff format
```
