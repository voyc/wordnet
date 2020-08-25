create schema wn;

create table wn.word (
	id serial,
	word varchar(100) unique  /* maxlen 71 */
)

create table wn.sense (
	id serial,
	pos char(1),  /* code for part of speech */
	cat char(2),  /* code for category */
	sense varchar(600) /* maxlen 505 */
);

create table wn.def (
	id serial,
	wordid int,
	defnum int,
	senseid int,
	pkey char(13),
	unique (wordid, defnum)
);

create table wn.rel (
	id serial,
	ptr varchar(2),
	defid1 int,
	defid2 int,
	pkey1 char(13),
	pkey2 char(13)
);

drop table wn.pos;
create table wn.pos (
	pos char(1) primary key,
	num int,
	name varchar(4),
	lname varchar(10),
	alt varchar(4),
	st varchar(4)
);

drop table wn.ptr;
create table wn.ptr (
	ptr char(2) primary key,
	name varchar(30) unique,
	field varchar(8), /* semantic, lexical */
	pos varchar(4)
);

drop table wn.cat;
create table wn.cat (
	cat char(2) primary key,
	pos char(1),
	name varchar(20),
	lname varchar(70)
);
