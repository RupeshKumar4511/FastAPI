# ASGI 
ASGI stands for Asynchronous Server Gateway Interface.
<br>
It actually converts the http request to that format which is understandable to python(FastAPI).

# uvicorn 
It is a webserver for the FastAPI application. It listens the request for the FastAPI.

# Why FastAPI is preferred instead of Flask : 
Because in flask, Every Component like webserver,WSGI and api code are synchronous and blocking in nature whereas in FastAPI, every component is async in nature.

# How to work with FastAPI

```bash 
# create virtual environment 
python -m venv myenv
// It makes a folder named "myenv" the where the isolated environment is created.

# activates our virtual environment on Operating System.
./myenv/Scripts/activate

From now on:

python uses myenv’s Python

pip install installs packages only inside myenv

# Inside myenv : 
pip install fastapi uvicorn pydantic

# create "main.py" file outside the "myenv" folder. 
create an instance of FastAPI and define routes for different type of http request.

# To run server 
uvicorn main:app --reload 
// app is the instance of FastAPI which is defined in the "main.py" file.

// --reload : It automatically restarts the server when any changes were made.

```

# Problem with simple python : 
1. Type validation : we need to do type validation by using manual code like checking the type of data. 
<br>
2. Data Validation : we need to do type validation by using manual code.

# Pydantic 
Pydantic is a Python library used for type validation, data validation, parsing, and serialization using type hints.


# To get the requirement.txt file 
It contains all the libraries used for project.
<br>
pip freeze > requirements.txt

# How to install the libraries written in requirement.txt file
pip install -r requirements.txt


# How to stop uvicorn server : 
If "Ctrl+c" does not work : 
<br>

```bash 
# It gives the process id of uvicorn
tasklist | findstr uvicorn

# kill process
taskkill /PID <PID> /F

```


