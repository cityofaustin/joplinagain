# joplinagain
Joplin... again (starting fresh to help debug)


## Why does this exist?
Joplin has moved far enough away from base wagtail that it's getting hard to figure out where issues are coming from.

## What's here?
So far I've run the default wagtail init within pipenv, meaning:
```
pipenv install wagtail
pipenv run wagtail start joplin
cd joplin
pipenv install -r requirements.txt
pipenv run python manage.py migrate 
pipenv run python manage.py createsuperuser
pipenv run python manage.py runserver
```

After that, I updated the models to include ServicePage, then ran migrations:
```
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate
```

## What's next?
Trying to add in the models from joplin and see if we can figure out any problems.
