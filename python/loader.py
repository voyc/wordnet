# loader.py
# load the princeton lexicographer files into the SQL database
# princeton input files described here:
# https://wordnet.princeton.edu/documentation/wndb5wn
# example input records included at the end of this file

import json
import psycopg2

# folders
dirin = '../princeton/dict/'
dirout = '../sql/gen/'
dircfg = '../../'

# open config settings
fconfig = open(f'{dircfg}/config.json', 'r')
config = json.load(fconfig)
print(config['default']['appname_long'])
print('princeton data file loader')

# connect to database
gconn = psycopg2.connect(f"dbname={config['db']['name']} user={config['db']['user']} password={config['db']['password']} port={config['db']['port']}") 
gconn.autocommit = True

def  insertSense(pos, cat, sense):
	# insert one sense record
	global gconn, gcsense
	sql = 'insert into wn.sense(pos,cat,sense)'
	sql += ' values(%s,%s,%s) returning id'
	cur = gconn.cursor()
	cur.execute(sql,(pos,cat,sense,))
	senseid = cur.fetchone()
	cur.close()
	gcsense += 1
	return senseid

def insertWord(word):
	# find a matching word record, or insert a new one
	global gconn, gcword
	wordid = 0
	defnum = 1
	scur = gconn.cursor()
	sql = 'SELECT min(w.id), max(d.defnum) from wn.word w, wn.def d'
	sql += ' where w.word = %s and w.id = d.wordid group by d.wordid'
	scur.execute(sql, (word,))
	if scur.rowcount == 1:
		row = scur.fetchone()
		wordid = row[0]
		defnum = int(row[1]) + 1
	elif scur.rowcount == 0:		
		icur = gconn.cursor()
		sql = 'insert into wn.word(word) values(%s) returning id'
		icur.execute(sql, (word,))
		row = icur.fetchone()
		wordid = row[0]
		icur.close()
		gcword += 1
	elif scur.rowcount > 1:
		raise Exception('duplicate words in word table')
	scur.close()
	return (wordid,defnum)

def insertDef(wordid,defnum,senseid,pkey):
	# insert one def record
	global gconn,gcdef
	sql = 'insert into wn.def(wordid,defnum,senseid,pkey)'
	sql += ' values(%s,%s,%s,%s) returning id'
	cur = gconn.cursor()
	cur.execute(sql,(wordid,defnum,senseid,pkey,))
	defid = cur.fetchone()
	cur.close()
	gcdef += 1
	return defid

def insertRel(relptr,pkey1,pkey2):
	# insert one rel record
	global gconn,gcrel
	sql = 'insert into wn.rel(ptr,pkey1,pkey2)'
	sql += ' values(%s,%s,%s) returning id'
	cur = gconn.cursor()
	sql = cur.execute(sql,(relptr,pkey1,pkey2))
	relid = cur.fetchone()
	cur.close()
	gcrel += 1
	return relid

def insertFrame(defid,framenum,pkey):
	# insert one frame record
	global gconn,gcframe
	sql = 'insert into wn.frame(defid,framenum,pkey)'
	sql += ' values(%s,%s,%s) returning id'
	cur = gconn.cursor()
	sql = cur.execute(sql,(defid,framenum,pkey))
	frameid = cur.fetchone()
	cur.close()
	gcframe += 1
	return frameid

def insertSatellite():
	return satid

# global counters
counter = 0
runaway = 130000 #117941
gcword = 0
gcdef = 0
gcsense = 0
gcrel = 0
gcframe = 0

# input files
inputfiles = [
	'data.test', 
#	'data.adv',  #r 
#	'data.verb', #v 
#	'data.adj',  #a,s
#	'data.noun', #n
]

for fname in inputfiles:
	infile = open(dirin+fname, 'r')
	for line in infile:
		counter += 1
	
		# stop after too many lines
		if counter > runaway:
			break
	
		# skip copyright lines at head of file
		if line[0:2] == '  ':
			continue
	
		# parse sense, ofst, cat, pos
		h = line.split(' | ')
		a = h[0]
		sense = h[1].strip().replace("'","''");
		a = line.split(' ')
		ofst = a[0]
		cat = a[1]
		pos = a[2]

		# parse words
		numwords = int(a[3],16)
		i = 1
		j = 4
		words = []
		while i <= numwords:
			words.append(a[j])	
			j += 2
			i += 1

		# insert sense, word, def 
		senseid = insertSense(pos,cat,sense)
		symnum = 0
		for word in words:
			(wordid,defnum) = insertWord(word)
			symnum += 1
			pkey = pos+ofst+str(symnum).zfill(2) 
			defid = insertDef(wordid,defnum,senseid,pkey)
	
		# parse and insert rel
		numrel = int(a[j])
		j += 1
		i = 1
		while i <= numrel:
			relptr = a[j+0]
			relofst = a[j+1]
			relpos = a[j+2]
			relnumnum = a[j+3]
			num1 = relnumnum[0:2]
			num2 = relnumnum[2:4]
			pkey1 = pos+ofst+num1
			pkey2 = relpos+relofst+num2
			insertRel(relptr,pkey1,pkey2)
			j += 4
			i += 1
	
		# parse and insert frame
		if pos == 'v':
			numframes = int(a[j])
			j += 1
			i = 1
			while i <= numframes:
				#plussign = a[j+0] # constant
				framenum = a[j+1]	
				synnum = a[j+2]	
				pkey = pos+ofst+synnum
				insertFrame(defid,framenum,pkey)
				j += 3
				i += 1 

		# adjective clusters, satellites

		if counter%1000 == 0:
			print(f'{counter},', end='', flush=True)
	infile.close()
	print( f'\n{fname} completed.', flush=True)

print(f'complete. rows:{counter} sense:{gcsense} word:{gcword} def:{gcdef} rel:{gcrel} frame:{gcframe}')


#00001740 03 n 01 entity 0 003 ~ 00001930 n 0000 ~ 00002137 n 0000 ~ 04431553 n 0000 | that which is perceived or known or inferred to have its own distinct existence (living or nonliving)  

#00002137 03 n 02 abstraction 0 abstract_entity 0 010 @ 00001740 n 0000 + 00694095 v 0101 ~ 00023280 n 0000 ~ 00024444 n 0000 ~ 00031563 n 0000 ~ 00032220 n 0000 ~ 00033319 n 0000 ~ 00033914 n 0000 ~ 05818169 n 0000 ~ 08016141 n 0000 | a general concept formed by extracting common features from specific examples  

#00001740 29 v 
#04 
#breathe 0 take_a_breath 0 respire 0 suspire 3 
#021 
#* 00005041 v 0000 
#* 00004227 v 0000 
#+ 03121972 a 0301 
#+ 00832852 n 0303 
#+ 04087945 n 0301 
#+ 04257960 n 0105 
#+ 00832852 n 0101 
#^ 00004227 v 0103 
#^ 00005041 v 0103 
#$ 00002325 v 0000 
#$ 00002573 v 0000 
#~ 00002573 v 0000 
#~ 00002724 v 0000 
#~ 00002942 v 0000 
#~ 00003826 v 0000 
#~ 00004032 v 0000 
#~ 00004227 v 0000 
#~ 00005041 v 0000 
#~ 00006697 v 0000 
#~ 00007328 v 0000 
#~ 00017024 v 0000 
#02 
#+ 02 00 
#+ 08 00 
#| draw air into, and expel out of, the lungs; "I can breathe better when the air is clean"; "The patient is respiring"  


