create database p
use p
create table login(userid varchar(20) primary key,pass varchar(50),name varchar(100),bd date,city varchar(100))
SELECT * from login
insert into login VALUES('agrima','we123','Agrima','03-06-2002','mumbai')
insert into login VALUES('','','','','')
delete from login where userid='agrima'