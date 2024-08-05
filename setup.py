import os

os.system('pip install -r requirements.txt')

os.system('python manage.py makemigrations')

os.system('python manage.py migrate sessions')

os.system('python manage.py migrate')

os.system('python manage.py migrate --fake')

os.system('python manage.py createsuperuser')