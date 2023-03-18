# PowerDNS Admin

Power DNS Admin

## Installation

Setup a virtualenv and install requirements
(this example uses [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)):

```bash
mkvirtualenv pda -p python3.9
pip install -r requirements.txt
```

## Set up database

Create a database named `pdns_admin`.

```
createdb pdns_admin
```

Create database migrations:

```
./manage.py makemigrations
```

Create database tables:

```
./manage.py migrate
```

## Running server

```bash
./manage.py runserver
```

## Google Authentication Setup

To setup Google Authentication, follow the [instructions here](https://django-allauth.readthedocs.io/en/latest/providers.html#google).
