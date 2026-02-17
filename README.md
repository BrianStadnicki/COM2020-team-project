# Overview

This is a project with a focus on developing a web application which allows for sellers to post food bundles and consumers to reserve them, with the intent to reduce food waste. The core functionality involves:

- User creation and authentication.
- Marketplace with bundle postings, reservations and an issue report feature.
- Overselling prevention.
- Seller analytics.
- Forecast on reservation demands and no-shows.
- Security.
- Accessibility.

For frontend development, Bootstrap is used to build simple design templates for the web application. For backend development, Django is also used to implement the front-end and the back-end, such as database models, administration, commands, views, urls and much more. The only programming language used in this project is Python.

## Initial setup

Linux:

```sh
cd food-waste-rescue
python -m venv .env
source .env/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

Windows:

```sh
cd food-waste-rescue
python -m venv .env
windows: Set-ExecutionPolicy Unrestricted -Scope Process
.env\Scripts\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```


## Running server

Windows:
```sh
cd food-waste-rescue
windows: Set-ExecutionPolicy Unrestricted -Scope Process
.env\Scripts\activate
python manage.py migrate
python manage.py runserver
```

Linux:

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

### After changing the database schema

```sh
python manage.py makemigrations
python manage.py migrate
```

### Add demo data

```sh
python manage.py seed --mode=refresh --seed=123
```

### Add happy path test data

```sh
python manage.py init_happy_path_test --mode=refresh --seed=123
```

### Export data

```sh
python manage.py export
```

### Demo run config

Also disables debug mode

```sh
SECRET_KEY="CHANGE_ME" python manage.py runserver
```

### Running Unit Tests

This project uses Django's built-in test runner.
All tests are located inside the main/tests/ directory.

1. Navigate to the project root (where manage.py lives)
```sh
cd food-waste-rescue
```

2. Activate the virtual environment:

```sh
python -m venv .env
windows: Set-ExecutionPolicy Unrestricted -Scope Process
.env\Scripts\activate
```

3. Run a test suite, e.g.:
```sh
python manage.py test main.tests.test_public_pages
```

4. You should see something like:
```sh
Ran 3 tests in ...
OK
```