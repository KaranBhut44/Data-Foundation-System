# Group1 Team4

# Private dataset access workflow (Python)
#### Team Members: 
 - 2020201049  - Nisarg Sheth
 - 2020201083  - Pujan Ghelani
 - 2020202015  - Karan Bhut

# 1. About Project:
#### -> Requirements:
 - Make a Web-Application(python) providing a way to access private datasets.

#### -> Functionalities: 
 - Users should be able to request access of private datasets and they should be able to access public datasets without any permission.
 - Dataset owners should be able to accept/reject access requests of their datasets.

#### -> Deliverables:
 - Registration/ Login page for Dataset Admins and users.
 - An Admin page containing facility to view/accept/reject access requests.
 - A user page having list of datasets and their types.

# 2. Technology stack:
 - Flask
 - SQL
 - HTML
 - CSS 
 - Javascript

# 3. Resources:
 - https://flask.palletsprojects.com/en/2.0.x/quickstart/#a-minimal-application
 - https://www.youtube.com/watch?v=oA8brF3w5XQ
 - https://www.youtube.com/watch?v=Qr4QMBUPxWo&t=21969s

# 4. Related Projects:
#### -> Publishing datasets and versions (Python)
 - After the dataset is published by this project, it should be updated in our project's dataset list. 

#### -> Standard analytics on datasets (Python) & Studies on datasets (like notebooks) (Python)
 - If dataset is public or user's access request is approved then only he/she should be able to perform Analytics or Study on any dataset.

#### -> User authentication service
 - This project will be used to register/login different dataset users and dataset owners of our project.

# 5. Steps to run the project

 - Execute this command: `python manage.py runserver`
 - Open this URL in Any browser: `127.0.0.1:8000`

# 6. Project Code structure:
For Django project, Project name is 'mysite' and Application name is 'dfs'.
 - `mysite/settings.py`: configured for MySQL.
 - `dfs/models.py`: Contains Models for different MySQL tables.
 - `dfs/urls.py`: Contains routes information.
 - `dfs/views.py`: It is the main python file for handling backend.
 - `static`: It contains static files like js,css and images for the UI.
 - `templates/admin.html`: Dataset publisher page
 - `templates/home.html`: Dataset consumer page
 - `templates/login.html`: Login page
 - `templates/registration.html`: Registration page
