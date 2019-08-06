# website-riot
Requirements:
1) Python 3
2) sqlserver
3) Django Module
4) MySQL Workbench/XAMPP/etc.
5) Requests module (pip install requests)

Start mysqlserver on port 3306.

Open a PowerShell/CMD/Terminal in the folder where the file manage.py is and then execute:
1) pip install mysqlclient
2) python manage.py makemigrations
3) python manage.py migrate
https://docs.djangoproject.com/en/2.0/topics/migrations/
4) python manage.py runserver
5) Open localhost:8000