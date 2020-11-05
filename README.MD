
# How to setup the project

> 1. git clone https://github.com/imzboy/melytix.git
> 2. cd melytix
> 3. python -m venv .venv
> 4. linux - source .venv/bin/activate windows - .venv\scripts\activate
> 5. pip install -r requirements.txt
> 6. create a .env file and write DEBUG=True FLASK_ENV=development FLASK_APP=app.py
> 7. flask run

# Development flow

For every feature/bugfix/hotfix/refactoring/etc. create a separate branch with self explanatory name.
After the development and initial tests are done, create a pull request to master.
If any merge conflicts arise, resolve them.

if you have not yet cloned the repository use > git clone

> 1. git pull
> 2. git checkout -b <**branch name**>
