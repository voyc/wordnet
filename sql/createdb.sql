create schema wn;

drop table wn.word cascade;
create table wn.word (
	id serial,
	word varchar(100) unique  /* maxlen 71 */
);

drop table wn.sense cascade;
create table wn.sense (
	id serial,
	pos char(1),  /* code for part of speech */
	cat char(2),  /* code for category */
	sense varchar(600) /* maxlen 505 */
);

drop table wn.def cascade;
create table wn.def (
	id serial,
	wordid int,
	defnum int,
	senseid int,
	pkey char(11),
	satellite char(1),
	unique (wordid, defnum)
);
create index def_pkey_ndx on wn.def(pkey); 

drop table wn.rel cascade;
create table wn.rel (
	id serial,
	ptr varchar(2),
	defid1 int,
	defid2 int,
	pkey1 char(11),
	pkey2 char(11)
);
create index rel_pkey1_ndx on wn.rel(pkey1); 
create index rel_pkey2_ndx on wn.rel(pkey2); 

drop table wn.frame cascade;
create table wn.frame (
	id serial,
	defid int,
	framenum int,
	pkey char(11)
);
create index frame_pkey_ndx on wn.frame(pkey); 

/* static code tables */

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
	reflex char(2),
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

/* views */

drop view wordsense;
create view wordsense (word,defnum,worddef,sense) as
select w.word, d.defnum, w.word || d.defnum, s.sense
from wn.word w, wn.sense s, wn.def d
where w.id = d.wordid and s.id = d.senseid;

drop view synset;
create view synset (senseid, syncount, pos, cat, words, sense) as
select d.senseid, count(d.senseid), min(s.pos), min(s.cat), array_agg(w.word), min(s.sense) 
from wn.def d, wn.word w, wn.sense s
where w.id = d.wordid
and s.id = d.senseid
group by d.senseid;

drop view relsimple;
create view lexrel (name1,ptr,name2) as
select substring(w1.word,1,20), r.ptr, substring(w2.word,1,20)
from wn.rel r, wn.def d1, wn.def d2, wn.word w1, wn.word w2
where d1.wordid = w1.id and r.defid1 = d1.id
and d2.wordid = w2.id and r.defid2 = d2.id;

drop view relcomplete;
create view relcomplete (id,ptr,defid1,defid2,pkey1,pkey2,field1,field2) as
select r.id, r.ptr, r.defid1, r.defid2, r.pkey1, r.pkey2, 
case when substring(r.pkey1,10,12) = '00' then 'semantic' else 'lexical' end,
case when substring(r.pkey2,10,12) = '00' then 'semantic' else 'lexical' end
from wn.rel r;

