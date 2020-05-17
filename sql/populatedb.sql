\connect student_advisor_db

insert into occupation (occupation_name, median_sal) values
    ('Help Desk Operator', 30000),
    ('Financial Advisor', 50000),
    ('Pharmacist', 110000)
;

-- inserting dummy student data (50 rows); generated via https://mockaroo.com/
insert into student (fname, lname, dob, grad_year, gpa, occupation_id) values
    ('Debi', 'McGarry', '8/30/1990', 2010, 3.31, 1),
    ('Adiana', 'Deluce', '9/2/1990', 2008, 3.74, 1),
    ('Zara', 'Henstridge', '12/3/1991', 2008, 2.32, 1),
    ('Eve', 'Guiness', '4/29/1994', 1986, 3.82, 2),
    ('Maitilde', 'Hartlebury', '6/16/1996', 2012, 2.55, 2),
    ('Arleyne', 'Bonnesen', '8/12/1992', 1991, 3.03, 2),
    ('Graham', 'Goldstraw', '10/5/1990', 2010, 3.28, 3),
    ('Sheridan', 'Markham', '11/26/1996', 1998, 3.14, 3),
    ('Adair', 'Harold', '12/23/1993', 2002, 3.82, 3)
;
