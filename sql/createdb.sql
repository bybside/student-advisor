-- if database exists drop it
drop database if exists student_advisor_db;
-- recreate database
create database student_advisor_db owner <db_user>;
-- connect to db
\connect student_advisor_db
-- if table exists drop it
drop table if exists occupation;
-- create occupation table
create table occupation (
    id serial primary key,
    occupation_name text,
    median_sal integer
);
-- if table exists drop it
drop table if exists student;
-- create student table
create table student (
    id serial primary key,
    fname text,
    lname text,
    dob date,
    grad_year integer,
    gpa real,
    occupation_id integer references occupation (id)
);
-- if table exists drop it
drop table if exists field;
-- create field (subject) table
create table field (
    id serial primary key,
    field_name text,
    area text
);
-- if table exists drop it
drop table if exists faculty;
-- create faculty table
create table faculty (
    id serial primary key,
    fname text,
    lname text
);
-- if table exists drop it
drop table if exists semester;
-- create semester table
create table semester (
    id serial primary key,
    semester_name text,
    academic_year integer
);
-- if table exists drop it
drop table if exists course;
-- create course table
create table course (
    id serial primary key,
    course_name text,
    semester_id integer references semester (id),
    field_id integer references field (id),
    faculty_id integer references faculty (id)
);
-- if table exists drop it
drop table if exists grade;
-- create grade table
create table grade (
    grade integer,
    student_id integer references student (id),
    course_id integer references course (id),
    primary key(student_id, course_id)
);
-- if table exists drop it
drop table if exists student_snapshot;
-- create student_snapshot table
create table student_snapshot (
    class_rank integer,
    hist_rank integer,
    strongest_sub_id integer references field (id),
    strongest_sub_avg real,
    weakest_sub_id integer references field (id),
    weakest_sub_avg real,
    student_id integer references student (id),
    primary key (student_id)
);
-- update table owner to your user
alter table occupation owner to <db_user>;
alter table student owner to <db_user>;
alter table field owner to <db_user>;
alter table faculty owner to <db_user>;
alter table semester owner to <db_user>;
alter table course owner to <db_user>;
alter table grade owner to <db_user>;
alter table student_snapshot owner to <db_user>;
