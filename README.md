Requirements:
    Python 3.2+
    Django 1.8
    httplib2

Installation:
    currently we have an issue with User model from Django as it's cannot be used in an app with no migrations, please follow these steps
    1. comment out the crowdsourcing app in the crowdresearch.settings file INSTALLED_APPS
    2. run python3.4 manage.py syncdb
    3. uncomment the commented app from step 1
    4. run python3.4 manage.py syncdb
    5. if prompted to create a new user, please don't do so, use the web frontend to create a user, this will create a profile as well


To run the app:
    python3.4 manage.py runserver 0.0.0.0:8000

