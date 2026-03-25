# Overview

This is a project with a focus on developing a web application which allows for sellers to post food bundles and consumers to reserve them, with the intent to reduce food waste. The core functionality involves:

- User creation and authentication.
- Marketplace with bundle postings, reservations and an issue report feature.
- Overselling prevention.
- Seller analytics.
- Forecast on reservation demands and no-shows.
- Security.
- Accessibility.

For frontend styling, Bootstrap is used to build simple design templates for the web application. For backend development, Django is also used to implement the front-end and the back-end, such as database models, administration, commands, views, urls and much more. The only programming language used in this project is Python.

## Roles

- Brian Stadnicki 740061452 Project Lead / Project Owner
- Ben Hambleton 740040694 Technical Lead / Scrum Master
- Rose Burston 730036689 Data Lead
- Livia Banyai 740008028  QA and Testing
- Tang Liang Li 740009122 DevOps / Software Developer
- Edward Naylor 740008590 Data Lead
- Laura Bonnelame 740008028 Documentation
- Hazel Gillam  740024206 Software Developer

## Initial setup

Create the virtual environment:

```sh
cd food-waste-rescue
python -m venv .env
```

If on Linux:

```sh
source .env/bin/activate
```

If on Windows:

```sh
Set-ExecutionPolicy Unrestricted -Scope Process
.env\Scripts\activate
```

Installing requirements and initial setup

```sh
python -m pip install -r requirements.txt
python manage.py migrate
```

Setting up the demo:

```sh
python manage.py seed --mode=refresh --seed=123
```

Running the development server:

```sh
python manage.py runserver
```

Running the production server:

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
python manage.py migrate
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