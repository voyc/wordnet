
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
	senseid int
);

create table wn.rel (
	id serial,
	defid1 int,
	ptr varchar(2),  /* code for relation pointer */
	defid2 int
);

create table wn.code (
	id serial,
	type char(3),  /* pos, cat, ptr */
	code varchar(2),
	value varchar(50)
);

# list synsets
select senseid, count(senseid) from wn.def 
group by senseid
having count(senseid) > 1;

# list synonyms for a word
select w.word, d.defnum
from wn.word w, wn.def d
where d.wordid = w.id
and d.senseid in (
	select s.id 
	from wn.word w, wn.sense.s, wn.def d
	where d.wordid = w.id and d.senseid = s.id
	and w.word = 'speak' and d.defnum = 1
);

# list adjectives
select w.word, d.defnum, s.sense
from wn.word w, wn.sense.s, wn.def d
where d.wordid = w.id and d.senseid = s.id
and s.pos = 'j';

