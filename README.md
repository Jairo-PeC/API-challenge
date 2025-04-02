                 
# Globant-challenge

Jairo Peña implementation of the globant challenge for data engineering job. 
 
## Getting Started

Get into the repository (https://github.com/Jairo-PeC/Globant-challenge).   
Clone the project with url.
 
### Prerequisites

##### Requirements for running project
- [Install python](https://www.python.org/downloads/) I ran it in version 3.9.2
- [Install conda enviroment](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
- [Install postman](https://www.postman.com/downloads/)<br /><br />
In your local shell run next commands to install needed libraries:
- pip install Flask
- pip install pathlib
 
## Running app



### Run employee/app.py

<your python library>/python.exe <your path>/globant/employee/app.py

### Run service endpoints. Port 5000

<h6>POST<h6/> http://127.0.0.1:5000//employees_schema/insert/hired_employees 
<h6>POST<h6/> http://127.0.0.1:5000//employees_schema/insert/departments 
<h6>POST<h6/> http://127.0.0.1:5000//employees_schema/insert/jobs 
<h6>GET<h6/> http://127.0.0.1:5000//employees_schema/jobsByQuarter 
<h6>GET<h6/> http://127.0.0.1:5000//employees_schema/departmentsAboveTheMean 

 
## Versioning

1.0
 
## Authors

Jairo Enrique Peña Cruz
[Linkedin](https://www.linkedin.com/in/jairo-pena-cruz/)


