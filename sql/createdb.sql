create schema wn;

create table wn.word (
	id serial,
	word varchar(50)
);

create table wn.sense (
	id serial,
	pos char(1),  /* code for part of speech */
	cat char(2),  /* code for category */
	sense varchar(600)
);

create table wn.def (
	id serial,
	wordid int,
	defnum int,
	senseid int,
	pkey char(13)
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
	id serial,
	num int,
	pos varchar(10),
	name varchar(10),
	cd char(1),
	st varchar(10)
);

create table wn.ptr (
);

create table wn.cat (
);
