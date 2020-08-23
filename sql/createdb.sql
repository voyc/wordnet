create schema wn;

create table wn.word (
	id serial,
	word varchar(50)
);

create table wn.sense (
	id serial,
	pos char(1),  /* code for part of speech */
	cat char(2),  /* code for category */
	sense varchar(100)
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
	defid1 int,
	ptr varchar(2),  /* code for relation pointer */
	defid2 int
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

create table wn.sensekey (
	id serial,
	princetonkey char(10), /* n-00045678 */
	sqlkey int
);

create table wn.wordkey (
	id serial,
	princetonkey char(13), /* v-00045678-01 */
	sqlkey int
);
