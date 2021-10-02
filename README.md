## Dynamic Portfolio using Python and Flask

This website was created using Python 3.x and Flask API.

<hr />

Before running this application make sure to follow the steps as follows:

* Setup the python environment where the isolated Flask environment would run.
  For Windows:
  `python -m venv env `  

  For Linux:
  `sudo apt-get install python3-venv`
  `python3 -m venv env` 

  For macOS:
  `python3 -m venv env`

* After that install Flask:
  `python -m pip install --upgrade pip`
  `python -m pip install flask`

* Once Flask has been successfully installed, you need to setup the Flask API to read main.py as the main file. Flask generally searches for `app.py` for the main file, but in this case, we have to choose `main.py`

  To do that, in case of Windows command prompt use:
  `set FLASK_APP=main`

  For Bash use:
  `export FLASK_APP=main`

  For PowerShell use:
  `$env:FLASK_APP="main"`

* Make sure you have the extra dependencies:

  * Flask login
    `python -m pip install flask_login`
  * Flask SQL Alchemy
    `python -m pip install flask_sqlalchemy`

* Once all is done, simply run the app:
  `flask run` and the app will be running on `http://127.0.0.1:5000/`port