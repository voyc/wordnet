grant connect on database wordnet to voyccom_webuser64;
grant usage on schema wn to voyccom_webuser64;

grant select,insert,update,delete on wn.word to voyccom_webuser64;
grant select,update on wn.word_id_seq to voyccom_webuser64;

grant select,insert,update,delete on wn.sense to voyccom_webuser64;
grant select,update on wn.sense_id_seq to voyccom_webuser64;

grant select,insert,update,delete on wn.def to voyccom_webuser64;
grant select,update on wn.def_id_seq to voyccom_webuser64;

grant select,insert,update,delete on wn.rel to voyccom_webuser64;
grant select,update on wn.rel_id_seq to voyccom_webuser64;

grant select,insert,update,delete on wn.cat to voyccom_webuser64;
grant select,insert,update,delete on wn.pos to voyccom_webuser64;
grant select,insert,update,delete on wn.ptr to voyccom_webuser64;
