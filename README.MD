  
# Django Docker Full - by osw4l

![enter image description here](https://i.imgur.com/rsEw4yc.png)

It is a beautiful **Django** image simple to configure, run and deploy, it was made with a lot of love and dedicated for humans who love django and simple things.

this project contains the next libraries

 -  Python 3.8.10 
 - [Django==3.2](https://docs.djangoproject.com/en/4.0/releases/3.2/)    
 - [django-admin-interface](https://github.com/fabiocaccamo/django-admin-interface)    
 - [Channels](https://channels.readthedocs.io/en/stable/)    
 - [Celery](https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html)    
 - [django-celery-beat](https://django-celery-beat.readthedocs.io/en/latest/)    
 - [django-celery-results](https://github.com/celery/django-celery-results)    
 - [django-cors-headers](https://github.com/adamchainz/django-cors-headers)    
 - [django-environ](https://django-environ.readthedocs.io/en/latest/)    
 - [django-extensions](https://github.com/django-extensions/django-extensions)    
 - [drf-yasg (Swagger)](https://github.com/axnsan12/drf-yasg)  
 - [djangorestframework](https://www.django-rest-framework.org/)    
 - [djangorestframework-gis](https://github.com/openwisp/django-rest-framework-gis)    
 - [django-leaflet](https://github.com/makinacorpus/django-leaflet)    
 - [django-map-widgets](https://github.com/erdem/django-map-widgets)    
 - psycopg2    
 - Redis    
 - Pillow    
 - django-storages    
 - boto    
 - botocore    
 - s3transfer    
     
and more pretty stuff like    
 - Docker compose    
 - [Daphne](https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/daphne/)  
 - [UWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) (no gunicorn)  
 - [Postgis](https://postgis.net/) as Database  
 - [Geo Django](https://docs.djangoproject.com/en/3.2/ref/contrib/gis/)    
 - Leaflet and Google Maps    
 - Django Admin Themes
 - Celery Worker and Celery Beat    
 - Nginx with django static files support    
 - Static files working fine !    
 - AWS S3 Storage    
 - Natural structure, **like you weren't using docker**    
- Production deploy steps [click here](https://gist.github.com/osw4l/cbfbfb3f7a7f42ab31fa5083b358f316)    

**Django Rest Framework Swagger**

the project contains its own auth backend with register, login and reset password

![enter image description here](https://i.imgur.com/n2o2Fqo.png)

Each endpoint contains its own serializer and swagger collection
![enter image description here](https://i.imgur.com/Ynqm69w.png)

![enter image description here](https://i.imgur.com/BlnGLVU.png)

if you want to disable the register and the confirmation after register you have to go to setup in the admin

[http://localhost:4500/admin/](http://localhost:4500/admin/)

Go to main and then go to setup

![enter image description here](https://i.imgur.com/Q70P0FB.png)

![enter image description here](https://i.imgur.com/qbgi0dK.png)
Now go to the detail

I'll disabled the register for now

![enter image description here](https://i.imgur.com/WQo5C4v.png)

**Then if I try to register in the register endpoint this gonna be the result**

![enter image description here](https://i.imgur.com/1H8Zxum.png)

**Django Google Maps Widget**

![enter image description here](https://cloud.githubusercontent.com/assets/1518272/26807500/ad0af4ea-4a4e-11e7-87d6-632f39e438f7.gif)

**Django Leaflet**

![enter image description here](https://camo.githubusercontent.com/4744043b6b90dbac1d548f4bc4fea4b82d2859867334a85b44ff119b42f905b0/68747470733a2f2f662e636c6f75642e6769746875622e636f6d2f6173736574732f3534363639322f313034383833362f37386236616439342d313039342d313165332d383664382d6333653838363236613331642e706e67)

![enter image description here](https://fle.github.io/images/012-admin-widget.png)

**Django Admin custom themes by** [django-admin-interface](https://github.com/fabiocaccamo/django-admin-interface)    

![enter image description here](https://user-images.githubusercontent.com/1035294/35631521-64b0cab8-06a4-11e8-8f57-c04fdfbb7e8b.gif)


**Custom Commands**

![enter image description here](https://i.imgur.com/yHCPCTv.png)
 
 to use the custom commands just give permissions
 
 **Command to collect Statics**
```bash
chmod +x run_collect_static.sh
```

 **Command to make migrations and migrate**
```bash
chmod +x run_migrate.sh
```

 **Command to create super user**
 
```bash
chmod +x run_create_user.sh
```

 **Command to load django admin themes**
 
```bash
chmod +x run_theme.sh
```

Simple and beautiful structure

![enter image description here](https://i.imgur.com/rjlx88Y.png)    
to run  the image follow the next instructions, just for local environment    

## Create Environment file
```bash
cp env_template .env
```
## Build image
 
```bash
docker-compose build
```
## Up image
```bash
 docker-compose up -d
```
## Migrations

you can create migrations and migrate the new models changes using the custom commands

**this command just run migrate command**
```bash
 docker-compose exec backend python3 manage.py migrate
```

**this command just run makemigrations and migrate commands**
```bash
./run_migrate.sh
```

## Restart Celery Beat
```bash
 docker-compose restart beat
``` 
## Create Superuser 

 **command**
```bash
docker-compose exec backend python3 manage.py createsuperuser
```

**sh file**
```bash
./run_create_user.sh
```

## collect statics

this command just **works** in **local** doesn't work in production
```bash
docker-compose exec backend python3 manage.py collectstatic    
```

this command **works** in **local** and production

**sh file**
```bash
./run_collect_static.sh
```

## Load Django Admin Themes

```bash
./run_theme.sh
```

## Pycharm Support first, we need to setup the common stuff to active the autocomplete adding the Django Support choosing the manage.py and settings.py files location.
    
![enter image description here](https://i.imgur.com/yxaLtUc.png)    
 now we need add the python interpreter what live inside the docker container to the project    
    
Go to preferences and to click in Interpreter then in Project Interpreter and press add    
    
![enter image description here](https://i.imgur.com/DwKsssx.png)    
 now, do click in Docker, select the image what contains the project name, then write python3 and press ok    
    
![enter image description here](https://i.imgur.com/pI86DZb.png)    
 press apply and ok, done!.    
    
![enter image description here](https://i.imgur.com/lmpULSQ.png)    
 now we have configured the interpreter what lives inside our Docker Container in our project    
    
Please, DON'T UPDATE THE DEPENDENCIES ! **unless necessary**    

 if you wanna deploy this project in production, [go to here](https://gist.github.com/osw4l/cbfbfb3f7a7f42ab31fa5083b358f316)    
    
**Thanks for using my project, if you need something else, feel you free to contact me** **ioswxd@gmail.com**

## Enjoy the project 🥳 🟡 🔵 💛 💙 💟
