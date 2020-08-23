psql -d voyccom_wn -u voyccom_jhagstrand


/* list synsets */
select senseid, count(senseid) from wn.def 
group by senseid
having count(senseid) > 1;

/* list synonyms for a word */
select w.word, d.defnum
from wn.word w, wn.def d
where d.wordid = w.id
and d.senseid in (
	select s.id 
	from wn.word w, wn.sense.s, wn.def d
	where d.wordid = w.id and d.senseid = s.id
	and w.word = 'speak' and d.defnum = 1
);

/* list adjectives */
select w.word, d.defnum, s.sense
from wn.word w, wn.sense.s, wn.def d
where d.wordid = w.id and d.senseid = s.id
and s.pos = 'j';

/* display lex rels */
select r.ptr, w2.word
from wn.rel r, wn.def d1, wn.word w1, wn.def d2, wn.word w2 
where r.ptr = '\;' and w1.word = 'speak' 
and w1.id = d1.wordid and d1.id = r.defid1
and r.defid2 = d2.id and d2.wordid = w2.id;

