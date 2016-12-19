###Requirements

Python (2.7.x, 3.x), python-pip, virtualenv

###Installation

- Create a virtual enviroment 
```bash
$ virtualenv env 
$ source env/bin/activate
```
- Install the required packages as such:
```
$ pip install -r requirements.txt
```
###Running the Application

```bash
$ python app/application.py
```
- Access this url in your browser:

http://localhost:5000/navigator?search_term=<search_term>

###Third party packages used

1. Flask (http://flask.pocoo.org/)
2. Requests (http://docs.python-requests.org/)


###Rundown

1. Using the navigator view the app extracts the search term from the get request.
2. Using requests the app calls for github api to get repos that matches the search term.
3. The app sorts the repos based on creation date then slice the first five.
4. Per repo the app starts calling for each repo last commit info.
5. A serialized structure is created as results, and passed as context to the html template that renders it.


###Constraint

This application is limited to 10 requests per minute, since it calls for the github api using unauthenticated requests. 

