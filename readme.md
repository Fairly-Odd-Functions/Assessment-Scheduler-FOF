[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Fairly-Odd-Functions/Assessment-Scheduler-FOF)
[![Run in Postman](https://run.pstmn.io/button.svg)](https://documenter.getpostman.com/view/32883617/2sAYBaApxi)

![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Assessment Scheduler App

## Dependencies
* Python3/pip3
* Packages listed in requirements.txt


## Installing Dependencies
```bash
$ pip install -r requirements.txt
```


## Flask MVC
This flask application is structured using the Model View Controller pattern


## Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command.


```bash
$ flask init
```


## Flask Commands
wsgi.py is a utility script for performing various tasks related to the project.


### CSV Commands
```bash
$ flask csv users
```

```bash
$ flask csv courses
```

```bash
$ flask csv assessments
```

```bash
$ flask csv programmes
```

```bash
$ flask csv semesters
```

### Staff Commands
```bash
# COMMAND #1 - CREATE STAFF
$ flask staff create
```

```bash
# COMMAND #2 - UPDATE STAFF
$ flask staff update
```

```bash
# COMMAND #3 - DELETE STAFF
$ flask staff delete
```

```bash
# COMMAND #4 - LIST ALL STAFF
$ flask staff list-all
```

```bash
# COMMAND #5 - SEARCH STAFF PROFILE
$ flask staff search
```

```bash
# COMMAND #6 - ASSIGN STAFF TO A COURSE
$ flask staff add-course
```

```bash
# COMMAND #7 - REMOVE STAFF FROM A COURSE
$ flask staff remove-course
```

```bash
# COMMAND #8 - VIEW STAFF ASSIGNED COURSE/S
$ flask staff list-courses
```

### Course Commands

```bash
# Command #1 : CREATE COURSE
$ flask course create
```

```bash
# COMMAND #2 : UPDATE COURSE
$ flask course update
```

```bash
# COMMAND #3 : SEARCH COURSE
$ flask course search
```

```bash
# COMMAND #4 : VIEW ALL COURSES
$ flask course list-all
```

```bash
# COMMAND #5 : ADD ASSESSMENT TO A COURSE
$ flask course add-assessment
```

```bash
# COMMAND #6 : REMOVE ASSESSMENT FROM A COURSE
$ flask course remove-assessment
```

```bash
# COMMAND #7 : VIEW ALL ASSESSMENTS FOR A COURS
$ flask course list-assesssments
```

### Assessment Commands

```bash
# COMMAND #1 : CREATE ASSESSMENT
$ flask assessment create
```

```bash
# COMMAND #2 : SEARCH ASSESSMENT
$ flask assessment search
```

```bash
# COMMAND #2.5 : SEARCH ALL ASSESSMENTS BASED ON TYPE
$ flask assessment search-type
```

```bash
# COMMAND #3 : LIST ALL ASSESSMENTS
$ flask assessment list-all
```

```bash
# COMMAND #4 : UPDATE ASSESSMENT
$ flask assessment update
```

### Programme Commands

```bash
# COMMAND #1 : CREATE PROGRAMME
$ flask programme create
```

```bash
# COMMAND #2 : ADD A COURSE TO A PROGRAMME
$ flask programme add-course
```

```bash
# COMMAND #3 : UPDATE PROGRAMME
$ flask programme update
```

```bash
# COMMAND #4 : LIST ALL PROGRAMMES
$ flask programme list-all
```

```bash
# COMMAND #5 : LIST ALL COURSE WITHIN A PROGRAMME
$ flask programme list-courses
```

```bash
# COMMAND #6 : SEARCH PROGRAMME
$ flask programme search
```

```bash
# COMMAND #7 : REMOVE COURSE FROM A PROGRAMME
$ flask programme remove-course
```

### Semester Commands
```bash
# COMMAND #1 : CREATE SEMESTER
$ flask semester create
```

```bash
# COMMAND #2 : SEARCH SEMESTER
$ flask semester search
```

```bash
# COMMAND #3 : UPDATE SEMESTER
$ flask semester update
```

```bash
# COMMAND #4 : LIST ALL SEMESTERS
$ flask semester list-all
```

```bash
# COMMAND #4.5 : LIST ALL SEMESTERS BASED ON ACADEMIC YEAR
$ flask semester list-year
```

```bash
# COMMAND #5 : LIST ALL COURSES IN A SEMESTER
$ flask semester list-courses
```

```bash
# COMMAND #6 : ADD COURSE OFFERING TO SEMESTER
$ flask semester add-offering
```

```bash
# COMMAND #6.5 : UPDATE COURSE OFFERING
$ flask semester update-offering
```

```bash
# COMMAND #7 REMOVE COURSE OFFERING FROM SEMESTER
$ flask semester remove-offering
```

### Admin Commands
```bash
# COMMAND #1 : CREATE ADMIN
$ flask admin create
```

```bash
# COMMAND #2 : DELETE ADMIN
$ flask admin delete
```

```bash
# COMMAND #3 : UPDATE ADMIN
$ flask admin update
```

```bash
# COMMAND #4 - SEARCH STAFF PROFILE
$ flask admin search
```

```bash
# COMMAND #5 : LIST ALL ADMIN
$ flask admin list-all
```

## Running The Project
For development run the serve command (what you execute):
```bash
$ flask run
```

# Testing

## Unit & Integration
A total of fourteen (37) tests are created in the App/test. Located at test_app.py
You can then execute all all application as follows:

```bash
$ pytest
```

![Screenshot1](img\tests.png)

or run perform specific tests with the following convention:

```bash
# Run all User Unit Tests
$ flask test user unit
```

```bash
# Run all User Integration Tests
$ flask test user int
```

```bash
# Run all Staff Unit Tests
$ flask test staff unit
```

```bash
# Run all Staff Integration Tests
$ flask test staff int
```

```bash
# Run all Admin Unit Tests
$ flask test admin unit
```

```bash
# Run all Admin Integration Tests
$ flask test admin int
```

```bash
# Run all Course Unit Tests
$ flask test course unit
```

```bash
# Run all Course Integration Tests
$ flask test course int
```

```bash
# Run all Semester Unit Tests
$ flask test semester unit
```

```bash
# Run all Semester Integration Tests
$ flask test semester int
```

```bash
# Run all Programme Unit Tests
$ flask test programme unit
```

```bash
# Run all Assessment Unit Tests
$ flask test assessment unit
```