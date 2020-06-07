\connect student_advisor_db

insert into occupation (occupation_name, median_sal) values
    ('Help Desk Operator', 30000),
    ('Financial Advisor', 50000),
    ('Pharmacist', 110000)
;

insert into faculty (fname, lname) values
    ('Larry', 'Mathers'),
    ('Leonard', 'Gradewell'),
    ('Smokey', 'Sheauwork'),
    ('Ashley', 'Flunkerson')
;

insert into field (field_name, area) values
    ('Mathematics', 'STEM'),
    ('Biology', 'STEM'),
    ('English', 'Humanities'),
    ('Literature', 'Humanities'),
    ('Music', 'Humanities')
;

insert into semester (semester_name, academic_year) values
    ('Fall', 2019),
    ('Spring', 2020),
    ('Fall', 2020),
    ('Spring', 2021)
;

insert into course (course_name, field_id, faculty_id, semester_id) values
    ('Calculus I', 1, 1, 1),
    ('Microbiology (AP)', 2, 2, 3),
    ('English & Composition II', 3, 3, 2),
    ('Antarctic Literature', 4, 3, 4),
    ('Beat Making II: Trap', 5, 4, 3)
;

-- inserting dummy student data (50 rows); generated via https://mockaroo.com/
insert into student (fname, lname, dob, grad_year, gpa, occupation_id) values
    ('Debi', 'McGarry', '8/30/2004', 2022, 3.31, 1),
    ('Adiana', 'Deluce', '9/2/2004', 2021, 3.74, 1),
    ('Zara', 'Henstridge', '12/3/2004', 2022, 2.32, 1),
    ('Eve', 'Guiness', '4/29/2004', 2021, 3.82, 2),
    ('Maitilde', 'Hartlebury', '6/16/2004', 2022, 2.55, 2),
    ('Arleyne', 'Bonnesen', '8/12/2004', 2021, 3.03, 2),
    ('Graham', 'Goldstraw', '10/5/2004', 2022, 3.28, 3),
    ('Sheridan', 'Markham', '11/26/2004', 2021, 3.14, 3),
    ('Adair', 'Harold', '12/23/2004', 2022, 3.82, 3)
;

insert into grade (grade, student_id, course_id) values
    (92, 1, 1),
    (83, 6, 2),
    (74, 2, 3),
    (65, 7, 4),
    (96, 3, 5),
    (87, 8, 4),
    (78, 4, 3),
    (69, 9, 2),
    (90, 5, 1)
;
