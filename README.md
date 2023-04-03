# Content-Management-System

Installation

1. Clone the repository to your local machine using the following command:

- git clone https://github.com/joylan21/Content-Management-System.git


2. Navigate to the project directory:

- cd Content-Management-System/Backend


3. Create a virtual environment and activate it:

- conda create -n my_env python=3.7
- conda activate my_env


4. Install the project dependencies:

pip install -r requirements.txt


5. Create the database tables:

- python manage.py makemigrations
- python manage.py makemigrations main
- python manage.py migrate


6. To run the project, execute the following command:

- python manage.py runserver


7. superuser or admin will be auto created after successful migrations
- email: admin@gmail.com
- Password: admin


8. admin panel url
- http://localhost:{port}/admin/


9. swagger api endpoint
- http://localhost:{port}/

10. Unit test Coverage report folder

- cd htmlcov
- run index.html on live server
