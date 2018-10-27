Create or clean DB
Go to settings file and change the database configuration
python manage.py makemigrations
python manage.py migrate
python manage.py runserver



After the above command you'll be able to see html page by running following url in browser:
http://127.0.0.1:8000/

if you want json end result you have to run following url in browser:

http://127.0.0.1:8000/search?word=input

Note: input is variable you have to pass string instead of input