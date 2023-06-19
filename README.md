# Hackathon_App

A submissions app where one can submit their hackathon submissions & see the list. 
The hackathon can be posted by anyone and they will be authorized before they are allowed to post hackathons. Users can submit some code or files as hackathon submissions. 


**TechStack Used**
1. Python (Programming Language)
2. Django and Django Rest Framework (Web Framework)
3. PostgreSQL (Database)

**How to setup and run locally**

1. Clone the Repository
2. Create and Activate Python Virtual Environment
3. After activating the virtual enviornment, redirect to project base directory.
4. Run the following command for installing dependencies. 
  ```
  $ pip install -r requirements.txt
  ```
5. Now before running the server, we have to setup database. To do so, follow the following steps -
      i) Install postreSQl and pgAdmin.
      ii) Create a database in pgAdmin.
      iii) Link the database django project by setting the name, user and password fileds of "DATABASE" section of settings.py file.
      iv) Migrate the database by running the following commands.
          ```
          $ python manage.py makemigrations
          ```
          ```
          $ python manage.py migrate
          ```

6. Now create superuser for accessing the admin panel.
  ```
  $ python manage.py createsuperuser
  ```
7. After completeing of all the entries while creating superuser, we are ready to test the whole project.
8. Now run the following command for starting the server
  ```
  $ python manage.py runserver
  ```
9. To access the application checkout http://127.0.0.1:8000
10. Follow the steps given [Link]([https://mypadhai.herokuapp.com/](https://docs.google.com/document/d/10BV1MMT7DcFWb5PdTFSJyLFMsaQ2oHKooI9fMDN1CkM/edit?usp=sharing)) to run and test the various APIs.

