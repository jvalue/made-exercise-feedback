# AMSE Automatic Exercise Feedback
This repository contains code to automatically give feedback for exercise submissions for the AMSE/SAKI course at FAU Erlangen-Nürnberg.

# Install
Grading code is tested and supposed to run with the latest Python LTS version (3.11 at the time of writing, check https://devguide.python.org/versions/).

[Pip](https://pypi.org/project/pip/) is used for dependency management.

Use [venv](https://docs.python.org/3/library/venv.html) to manage a virtual environment for the project. If it is not already installed, install it on your machine using pip: `pip install virtualenv`

1. Create a virtual env: `python -m virtualenv env`
2. Activate the virtual env: `source env/bin/activate`
3. Install dependencies using pip (inside the virtual env): `pip install -r requirements.txt`.

# Execute
To run the automated grading, first activate the virtual env, then execute grading.py with an optional work directory as first argument.

1. `source env/bin/activate`
2. `python grading.py`

# Use with CI
To use the automated grading feedback in student repositories in AMSE, use the GitHub Actions workflow in`ci/grading-feedback.yml`. It sets up a GitHub action with Python 11 and Jayvee and then executes `./run_grading.sh`.

# Notes
- The SQLAlchemy version <2 in requirements.txt is by design, see https://levelup.gitconnected.com/how-to-fix-attributeerror-optionengine-object-has-no-attribute-execute-in-pandas-eb635fbb89e4.
