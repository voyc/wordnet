grant connect on database wordnet to username;
grant usage on schema wn to username;
grant select,insert,update,delete on wn.word to username;
grant select,update on wn.word_id_seq to username;
grant select,insert,update,delete on wn.sense to username;
grant select,update on wn.sense_id_seq to username;
grant select,insert,update,delete on wn.def to username;
grant select,update on wn.def_id_seq to username;
grant select,insert,update,delete on wn.rel to username;
grant select,update on wn.rel_id_seq to username;
grant select,insert,update,delete on wn.pos to username;
grant select,update on wn.pos_id_seq to username;
grant select,insert,update,delete on wn.ptr to username;
grant select,update on wn.ptr_id_seq to username;
grant select,insert,update,delete on wn.cat to username;
grant select,update on wn.cat_id_seq to username;

