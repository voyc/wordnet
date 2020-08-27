psql -d voyccom_wn -u voyccom_jhagstrand

/* list synsets by size */
select syncount, words from synset
where syncount > 1
order by syncount desc;

/* list synonyms for a word */
select w.word, d.defnum
from wn.word w, wn.def d
where d.wordid = w.id
and d.senseid in (
        select s.id
        from wn.word w, wn.sense s, wn.def d
        where d.wordid = w.id and d.senseid = s.id
        and w.word = 'speak' and d.defnum = 1
);

/* list adjectives */
select w.word, d.defnum, s.sense
from wn.word w, wn.sense.s, wn.def d
where d.wordid = w.id and d.senseid = s.id
and s.pos = 'j';

/* list indexes */
select * from pg_indexes where schemaname = 'wn';

/* list senses for each word */
select word, defnum, sense from wordsense;

/* list relations */
select name1, ptr, name2 from lexrel;

/* show counts by ptr and field */
select r.ptr, min(p.name), r.field1, count(*) 
from relcomplete r, wn.ptr p
where p.ptr = r.ptr
group by r.ptr, r.field1;
