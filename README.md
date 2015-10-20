# DjangoBokeh

Dummy sample of a plot rendered by Bokeh in Django

# Django Architecture

![Django architecture and the Model View Controller.](https://eggslaking.files.wordpress.com/2013/03/django2.png?w=580)

# To start the project

```
django-admin startproject site1
cd site1/
python manage.py startapp plot1
python manage.py migrate
```
# Run:
```
python manage.py runserver
```
Open the browser: [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

# Tested:
with:
- Django 1.8.5
- Bokeh 0.10

# Instalation:
```
virtualenv env
pip install -r requirements.txt
source env/bin/activate
 python site1/manage.py runserver 8001
```

# Deployment

Assuming Apache 2 installed with ```mod_wsgi```.

```
# Copy static files to STATIC_ROOT (in settings)
sudo ./site1/manage.py collectstatic  --noinput

# Copy apache config:
sudo cp apache/django-bokeh.conf /etc/apache2/conf-enabled/

# Copy the env and site1 to /var/www/django_bokeh.
# The structure will look like this
$ tree -d -L 3 /var/www/django_bokeh
/var/www/django_bokeh
├── env
│   ├── bin
│   ├── include
│   │   └── python2.7 -> /usr/include/python2.7
│   ├── lib
│   │   └── python2.7
│   ├── local
│   │   ├── bin -> /home/leal/git/DjangoBokeh/env/bin
│   │   ├── include -> /home/leal/git/DjangoBokeh/env/include
│   │   └── lib -> /home/leal/git/DjangoBokeh/env/lib
│   └── man
│       └── man1
├── site1
│   ├── data
│   ├── plot1
│   │   └── migrations
│   ├── site1
│   ├── static
│   └── templates
│       └── plot1
└── static
    └── admin
        ├── css
        ├── img
        └── js


```
