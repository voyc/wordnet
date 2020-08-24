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

create table wn.pos (
	pos char(1) primary key,
	num int,
	name varchar(10),
	alt varchar(10),
	st varchar(10)
);

create table wn.ptr (
	ptr char(2) primary key,
	name varchar(30) unique,
	reltype varchar(8),
	pos varchar(4)
);

create table wn.cat (
	cat char(2) primary key,
	name varchar(20),
	pos varchar(4)
);
