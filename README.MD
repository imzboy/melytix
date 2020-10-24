
# How to setup the project

> 1. git clone https://github.com/imzboy/melytix.git
> 2. cd melytix
> 3. python -m venv .venv
> 4. linux - source .venv/bin/activate windows - .venv\scripts\activate
> 5. pip install -r requirements.txt
> 6. linux - export FLASK_APP=app.py windows - set FLASK_APP=app.py
> 7. linux - export FLASK_ENV=development windows - set FLASK_ENV=development
> 8. flask run

# Development flow

For every feature/bugfix/hotfix/refactoring/etc. create a separate branch with self explanatory name.
After the development and initial tests are done, create a pull request to master.
If any merge conflicts arise, resolve them.

> 1. git pull
> 2. git checkout -b <**branch name**>
