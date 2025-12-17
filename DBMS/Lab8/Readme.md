Student Database Management System (PostgreSQL + Python)

This program demonstrates how to connect a Python application to a PostgreSQL database, perform DDL and DML operations, execute queries, and provide a text-based user interface for interaction.
It fulfills the lab requirements for database programming using PostgreSQL.

## Overview
The project includes:
* Creation of database tables using SQL (DDL)
* Data insertion, updating, and deletion (DML)
* Querying and displaying results using various SQL clauses
* A simple terminal-based menu for user interaction
* Proper cleanup and error handling on termination

## Files Included
* student_lab.py
* requirements.txt
* README.md

## Prerequisites

Before running this program, ensure the following:
Docker is installed and running.
Python 3.8 or higher is installed.
The PostgreSQL Docker container is set up and accessible.
The Python dependencies listed in requirements.txt are installed.
Setting Up PostgreSQL Using Docker
Pull the official PostgreSQL image:
docker pull postgres

Run the PostgreSQL container:
docker run --name pg_lab -e POSTGRES_PASSWORD=admin123 -p 5432:5432 -d postgres
Access the PostgreSQL shell:
docker exec -it pg_lab psql -U postgres

Create the database:
CREATE DATABASE studentdb;
\q
Installing Dependencies
Install the required Python package using pip:
pip install -r requirements.txt

If you encounter issues on Windows, use:
pip install psycopg2-binary
Running the Program
Ensure the PostgreSQL container is running:
docker ps


Run the Python program:
python student_lab.py

The program will display a text-based menu:

Student Database Management System

1. Create Table
2. Insert Student(s)
3. Update Student
4. Delete Student
5. Query Data
6. Exit
Enter your choice:

Example Table Schema

When you select the “Create Table” option, the program creates a table named students with the following schema:

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    department VARCHAR(50)
);

Query Options

The program supports the following query operations:

Retrieve and display all student records.

Display students belonging to a specified department.

Display the average age of students per department (using GROUP BY).

Display students whose names start with a user-specified letter (pattern matching).

Termination and Cleanup

When the user selects “Exit”:

All database connections are closed gracefully.

The program terminates without leaving open connections.

To stop and remove the PostgreSQL container:

docker stop pg_lab
docker rm pg_lab

Troubleshooting

If the program cannot connect to PostgreSQL, ensure that the Docker container is running.

Check if the port 5432 is accessible on localhost.

If installation of psycopg2 fails, use psycopg2-binary instead.