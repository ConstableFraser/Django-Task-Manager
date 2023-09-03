### Hexlet tests and linter status:
[![Actions Status](https://github.com/ConstableFraser/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/ConstableFraser/python-project-52/actions)
[![Linter](https://github.com/ConstableFraser/python-project-52/actions/workflows/linter.yml/badge.svg)](https://github.com/ConstableFraser/python-project-52/actions/workflows/linter.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/0592caf9f3efcb116c40/maintainability)](https://codeclimate.com/github/ConstableFraser/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/0592caf9f3efcb116c40/test_coverage)](https://codeclimate.com/github/ConstableFraser/python-project-52/test_coverage)

# TASK MANAGER
ticket management system
## useful features:
1. create a ticket and display list of tickets
2. ticket editing and specify status, label and executor
3. create and display list of: statuses, label и users
4. authentication system

## how it works:
1. the user must log in or create a new account
2. authorized user can create and update tickets, statuses and labels
3. only the author can delete tickets and own account

## demo version:
https://task-managet-django.onrender.com/

or watch the video:

[![Watch the video](staticfiles/images/Figaro_preview.png)](https://youtu.be/aBok39kZT9Q)

## technical information

### info about structure of db
![database](staticfiles/images/structure_db.png)

### tech stack
djnago, python, poetry, gunicorn, jinja2, bootstrap, rollbar, whitenoise
