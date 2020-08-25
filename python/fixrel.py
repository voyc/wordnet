# fixrel.py
# set defid1 and defid2 in wn.rel

import json
import psycopg2

# open config settings
dircfg = '../../'
fconfig = open(f'{dircfg}/config.json', 'r')
config = json.load(fconfig)
print(config['default']['appname_long'])

# connect to database
gconn = psycopg2.connect(f"dbname={config['db']['name']} user={config['db']['user']} password={config['db']['password']} port={config['db']['port']}") 
gconn.autocommit = True

def fixpkey(pkeyin):
	#a0000174001
	if pkeyin[10:12] == '00':
		pkeyout = pkeyin[0:10]
	else:
		pkeyout = pkeyin
	return pkeyout

def lookup(pkey):
	global gconn
	cur = gconn.cursor()
	sql = 'select id from wn.def where pkey = %s'
	cur.execute(sql, (pkey,))
	defid = cur.fetchone()
	cur.close()
	return defid

def update(num,defid,pkey):
	global gconn
	if num == 1:
		sql = 'update wn.rel set defid1 = %s where pkey1 = %s'
	elif num == 2:
		sql = 'update wn.rel set defid2 = %s where pkey2 = %s'
	cur = gconn.cursor()
	cur.execute(sql, (defid,pkey))
	cur.close()

counter = 0
runaway = 400000

# pass 1
sqlin = 'select distinct pkey1 from wn.rel'
sqlin += ' where defid1 is null order by pkey1'
curin = gconn.cursor()
curin.execute(sqlin)
for row in curin:
	counter += 1
	if counter > runaway:
		break;
	pkey = row[0]
	pkey = fixpkey(pkey) 
	defid = lookup(pkey)
	update(1,defid,pkey)
	if counter%1000 == 0:
		print(f'{counter},', end='', flush=True)
curin.close()

# pass 2
counter = 0
sqlin = 'select distinct pkey2 from wn.rel'
sqlin += ' where defid2 is null order by pkey2'
curin = gconn.cursor()
curin.execute(sqlin)
for row in curin:
	counter += 1
	if counter > runaway:
		break;
	pkey = row[0]
	pkey = fixpkey(pkey) 
	defid = lookup(pkey)
	update(2,defid,pkey)
	if counter%1000 == 0:
		print(f'{counter},', end='', flush=True)
curin.close()
print('complete')
