# Django website template (production ready)
Tired of writing Django project from scratch? use this template to speed up your Django development and deliver your project within few hours, instead of weeks or months.

### Why use Django website template?
Using a Django template can save you a lot of time, which is a huge benefit. Most clients don't care if you start from scratch or use a template; they just want their problem solved quickly. Whether you use Django or another framework usually doesn't matter to them as long as the job gets done efficiently.

This template can help you save hours of work, allowing you to deliver a production-ready website in just a few hours.

### What features does Django template include?
- Production ready, you can immediately deploy this to cloud such as Railway.app, Render.com etc.
- Comes with a landing page that you can modify.
- Responsive design, forget about making things responsive yourself.
- Contact us page.
- 404 page
- Has blog with Trix WYSIWYG editor built into the admin panel.
- Technical SEO optimization.
- Dynamic Sitemap.xml
- Robots.txt
- Google analytics
- Custom user model.
- Tailwind css setup for rapid development (note: the tailwind classes are prefixed with `tw-`, to differentiate them)

### Do I need to be an expert in Django to use this?
A basic understanding of HTML, CSS, and JavaScript is all you need to get started. However, if you want to add custom pages or make more advanced modifications, having at least some foundational knowledge will be really helpful.

### Demo
Visit the demo site: [Django Demo website](https://django-website-template.vercel.app/)

For admin use
```
demo@mail.com
demo123*
```
### Table of contents

- [Django website template (production ready)](#django-website-template-production-ready)
  - [Why use Django website template?](#why-use-django-website-template)
  - [What features does Django template include?](#what-features-does-django-template-include)
  - [Do I need to be an expert in Django to use this?](#do-i-need-to-be-an-expert-in-django-to-use-this)
  - [Demo](#demo)
  
- [Local development](#local-development)
  - [Admin superuser](#admin-superuser)
- [Customizing](#customizing)
  - [Adding title, description to page](#adding-title-description-to-page)
- [Deployment:](#deployment)
    - [Create a firebase credential file](#create-a-firebase-credential-file)
    - [Deploying credential file to production](#deploying-credential-file-to-production)
- [Images credits](#images-credits)





## Local development

follow the below steps :
1. Star the repo: https://github.com/PaulleDemon/Django-website-template
   
2. Clone the repo
`git clone https://github.com/PaulleDemon/Django-website-template`

3. Install python 3.8 or above.
https://www.python.org/downloads/

4. Open the template folder and from the terminal change the
directory to the current working directory.
`cd home/Template`

5. Install dependencies in an environment (creating an
enviornment is optional, but recommended)
```
pip install -r requirements.txt
```

6. Add a `.env` file inside the project folder with the following
```py
DEBUG=1
PYTHON_VERSION=3.10
DOMAIN=""

ALLOWED_HOSTS=".up.railway.app"
ALLOWED_CORS=""

SECRET_KEY=""
PORD_SECRET_KEY=""

DJANGO_SUPERUSER_EMAIL="" # optonal use if you want to create supruser using --noinput
DJANGO_SUPERUSER_PASSWORD="" # optonal use if you want to create supruser using --noinput

EMAIL_HOST="smtpout.server.net"
EMAIL_HOST_USER=""
EMAIL_HOST_PASSWORD=""

POSTGRES_DATABASE=""
POSTGRES_USER=""
POSTGRES_PASSWORD=""
POSTGRES_HOST=""

POSTGRES_URL=""

PROJECT_ID="" # firebase project id
BUCKET_NAME=".appspot.com" # firebase storage name
FIREBASE_CRED_PATH="project/firebase-cred.json"

FIREBASE_ENCODED=""
CLOUD_PLATFORM="RAILWAY"

GOOGLE_ANALYTICS="G-"
```

7. Now in your terminal Create databases and Tables using
```
python manage.py migrate
```
Your database is created and ready to use.

8. Now run the website from the terminal using.
```py
python manage.py runserver
```
Your website should be available at: http://localhost:8000/

9. To run Tailwind CSS open a new terminal and run
```py
python manage.py tailwind start
```

**Note:** If you are facing problems starting this program in windows OS, remove logging from project/settings.py

### Admin superuser
To create a admin superuser use the following in terminal
```py
python manage.py createsuperuser
```

## Customizing

All html, css, js and assets lies inside the templates.
- To modify the landing page, update `home.html`.
- To add link to header and footer or modify head tags, check `base.html`.
- extend `base.html` to have the same footer and header.

### Adding title, description to page
To add title to a page use the following tags
```py
{% block title %}lorem impsum {% endblock title %}
{% block description %}lorem impsum{% endblock description %} #meta description

{% block socialTitle %}{{blog.title}} | {% endblock socialTitle %} # open graph title, for socials
{% block socialDescription %}{{blog.meta_description}}{% endblock socialDescription %} # open graph description, for socials
{% block pageType %}article{% endblock pageType %}
{% block pageImage %}{% endblock pageImage %} # social image
```

To add additional head tags

```py
{% block head_tags %}lorem impsum {% endblock head_tags %}
```
To add scripts at the end of the elements
```
{% block scripts %}
    <script src="{% static "" %}" />
{% endblock scripts %}
```

## Deployment:

Deploy to vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FPaulleDemon%2FDjango-website-template&demo-title=Django%20website%20template&demo-description=A%20starters%20template%20for%20django%20developers%2C%20freelancers%20and%20agencies&demo-url=https%3A%2F%2Fdjango-website-template.vercel.app%2F)

or

You can make use of Railway to deploy your own instance. 

<a href="https://railway.app?referralCode=BfMDHP">
  <img src="railway.png" alt="railway icon" height="50px"/>
</a>

Link to deploy to [Railway.app](https://railway.app?referralCode=BfMDHP)

once you complete make sure to 
```
python manage.py collectstatic
```
and set
```
DEBUG=0
```
**Generate secret key**
To generate secret key use `from django.core.management.utils import get_random_secret_key` then `get_random_secret_key()` in your python shell

**Note:** don't forget to set the sites to your domain instead of example.com in the admin panel

### Create a firebase credential file

>**Note:** We'll be using firebase for persistent storage, to upload user files. Firebase is pre-configured as there are other firebase services developers may want to use. <br><br> You can also use any of the storage supported by [django-storages](https://github.com/jschneier/django-storages), if you don't want to use firebase.

To use Firebase

1. We use Google storage for storing files. Go to firebase -> storage -> create (make it public)

2. Now Go to firebase -> project settings -> service account -> Generate new private key.

Rename the private as `firebase-cred.json`

Use this private file as your credential file.

#### Deploying credential file to production
Sometimes your cloud provider may not provide you with storage for secret files. 
So convert the credential file to base64 using
```
base64 firebase-cred.json > encoded.txt
```
Now copy the contents of encoded.txt and paste it in `FIREBASE_ENCODED="wedde"` variable


## Images credits
Images are taken from free to use sites such as 
1. unsplash - https://unsplash.com/
2. Pexels - https://www.pexels.com/