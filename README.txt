Following configuration needs to be changed in settings.py 
•	Set PROJECT_BASE_PATH to the absolute path of the project
•	Set SITE_BASE_URL to the site URL
•	Change DATABASES as per the database used
•	Update the following variables as per your email host
	o	EMAIL_HOST
	o	EMAIL_HOST_USER
	o	EMAIL_HOST_PASSWORD
	o	EMAIL_PORT
	o	EMAIL_USE_TLS

Dependencies
The application is dependent on the following packages:
•	django-select-ajax (http://code.google.com/p/django-ajax-selects/updates/list) - This opensource django application is used extensively throughout the project to add AJAX based autocomplete features for various forms.

?	Database adapter - Use database adapter based on your database. For PostgreSQL, psycopg2 (http://initd.org/psycopg/) is the most popular one. Update the connection information accordingly in the setting.py file.
