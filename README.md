# BUDGET WEB APP
## Video Demo: https://youtu.be/45339iAgM_k
## Description:

###### What project is about?
On my daily basis, in my family we continually register our expenses to keep our finances on track. Before developing this app, my wife and I, used to use a whatsapp group to record any expense that we make. Afterwards, every saturday we record all the expenses on a spreadsheet in Google.
With all that in mind, i developed this app, to make easier the process of registering expenses online and saving in to a database.

###### Files explanation:
The project tree is composed by the main directory FINAL_PROJECT. Inside it, we have a file named "run.py". This is the executable file to run with the cmd "python run.py".

On the same folder, we have another folder named "budgetapp". Inside this folder, we have our main files like: "init.py". Inside it we have all the app.config commands to initialize flask, configure the secret key for the password hash, database and mail management. 

Then we have our "routes.py" were we have all the decorators to run our webapp. We have register, login, logout, "/" or index, account, reset password and reset password token, transaction, budget, delete budget, results and delete transaction. They all comprise the main functioning of the webapp.

Then we have "models.py". By using Flask-sqlalchemy to manage the database, here i create the classes to manage the database and its tables such as: User, Transactions, Budget. I started the project using CS50 Library but had some problems with reseting the password so i migrated to SQLAlchemy to solve this.

Then we have "forms.py". I used flask-wtf library to manage all forms. Being the ones created Registration Form, Login Form, Update Account Form, Request Reset Form, Reset Password, Transaction Form and Budget Form. Each one was created as a Class and i also created some functions to manage custom validation error method in case the user made an error inputting information.

Also on this directory, we have the the database, budget.db were all info is stored, created with SQLAlchemy. 
On this directory, we have the templates folder. Our main file is the layout, were i set the parameters for the scheme of every other page on the webapp, separating info for logged users and non-logged. In order of operation, we have the following html files: register, login, index, reset_request, reset_token, account, transaction, budget and results.
On the directory we also have static/images where the logo is saved.

###### Design choices:
All the CSS design was made using Bootstrap classes. As i previously stated, i started using the CS50 library but at some stage i found i had the need to migrate to another way of managing database and forms so i started using Flask-sqlAlchemy.

###### Final words:
It has been a challenge trying to learn how to use different flask functionalities in order to get my ideas going on the project. I think it has prepared me to started the next course CS50w where i'll be able to go deep into learning web development. Thanks CS50 team!