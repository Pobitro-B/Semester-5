--- q3
CREATE TABLE Students (StudentID INT PRIMARY KEY, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, Discipline TEXT);

CREATE TABLE Faculty (FacultyID INT PRIMARY KEY, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, Department TEXT);

--- q4
INSERT INTO Students (StudentID, FirstName, LastName, Discipline) VALUES (12340010, 'Ajay', 'Chikate', 'DSAI');
INSERT INTO Students (StudentID, FirstName, LastName, Discipline) VALUES (12340020, 'Aviral', 'Saxena', 'CSE');
INSERT INTO Students (StudentID, FirstName, LastName, Discipline) VALUES (12340040, 'Kishor', 'Koppikar', 'CSE');
INSERT INTO Students (StudentID, FirstName, LastName, Discipline) VALUES (12340030, 'Pobitro', 'Bhattacharya', 'DSAI');
Insert into Students values (12340050, 'Arnav', 'Mishra', 'CSE'),(12340060, 'Sourav', 'Gupta', 'CSE');

INSERT INTO Faculty (FacultyID, FirstName, LastName, Department) VALUES (23450010, 'Kishor', 'Gupta', 'CSE');
INSERT INTO Faculty (FacultyID, FirstName, LastName, Department) VALUES (23450020, 'Ajay', 'Chandra', 'DSAI');
INSERT INTO Faculty (FacultyID, FirstName, LastName, Department) VALUES (23450030, 'Sanjay', 'Mishra', 'DSAI');
INSERT INTO Faculty (FacultyID, FirstName, LastName, Department) VALUES (23450040, 'Anirudh', 'Yadav', 'CSE');

--- q5
Select * from Students where Discipline='CSE';

Select * from Faculty where Department='CSE';

--- q6
select FirstName, LastName from Students;

select LastName, Department from Faculty;

--- q7
Select DISTINCT FirstName from Students Union Select Distinct FirstName from Faculty;

Select DISTINCT LastName from Students Union Select DISTINCT LastName from Faculty;

--- q8
Select FirstName from Students intersect Select FirstName from Faculty;


Select LastName from Students intersect Select LastName from Faculty;