from setuptools import setup

setup(
    name='pda',
    version='0.1.0',
    package_dir={'': 'src'},
    install_requires=[
        'amqp==5.1.1',
        'asgiref==3.6.0',
        'async-timeout==4.0.2',
        'attrs==22.2.0',
        'bcrypt==4.0.1',
        'billiard==3.6.4.0',
        'celery[redis]==5.2.7',
        'celery-progress==0.1.3',
        'certifi==2022.12.7',
        'cffi==1.15.1',
        'charset-normalizer==3.0.1',
        'click==8.1.3',
        'click-didyoumean==0.3.0',
        'click-plugins==1.1.1',
        'click-repl==0.2.0',
        'cryptography==39.0.1',
        'defusedxml==0.7.1',
        'django==4.1.7',
        'django-allauth==0.54.0',
        'django-allauth-2fa==0.10.0',
        'django-anymail[mailgun]==9.0',
        'django-environ==0.9.0',
        'django-otp==1.1.4',
        'django-waffle==3.0.0',
        'djangorestframework==3.14.0',
        'djangorestframework-api-key==2.3.0',
        'dnspython==2.3.0',
        'dotenv-cli==3.1.0',
        'drf-spectacular==0.25.1',
        'gunicorn==20.1.0',
        'idna==3.4',
        'inflection==0.5.1',
        'jinja2==3.1.2',
        'jsonschema==4.17.3',
        'kombu==5.2.4',
        'mysql==0.0.3',
        'oauthlib==3.2.2',
        'prompt-toolkit==3.0.38',
        'psycopg2-binary==2.9.5',
        'pycparser==2.21',
        'pydantic==1.10.2',
        'pyjwt[crypto]==2.6.0',
        'pypng==0.20220715.0',
        'pyrsistent==0.19.3',
        'python3-openid==3.2.0',
        'python-dotenv==0.21.0',
        'pytz==2022.7.1',
        'pyaml==21.10.1',
        'qrcode==7.4.2',
        'redis==4.5.1',
        'requests==2.28.2',
        'requests-oauthlib==1.3.1',
        'selenium==4.8.2',
        'sentry-sdk==1.15.0',
        'six==1.16.0',
        'sqlparse==0.4.3',
        'typing-extensions==4.5.0',
        'uritemplate==4.1.1',
        'urllib3==1.26.14',
        'vine==5.0.0',
        'wcwidth==0.2.6',
    ],
    entry_points={
        'console_scripts': [
            'pda = lib.cli.app:cli',
        ],
    },
)
