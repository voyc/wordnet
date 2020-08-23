import re
import json

dirin = '../princeton/dict/'
dirout = '../sql/gen/'
dircfg = '../../'

fconfig = open(f'{dircfg}/config.json', 'r')
config = json.load(fconfig)
print(config['default']['appname_long'])

def composeSense(senseid, pos, sense):
	return f"insert into wn.sense(id,pos,sense) values({senseid},'{pos}','{sense}');\n"

def composeDict(wordid, word):
	return f"insert into wn.dict(id,word) values({wordid},'{word}');\n"

def composeDef(wordid, defnum, senseid, ofst, pos):
	pkey = f'{pos}{ofst}{str(defnum).zfill(2)}'
	return f"insert into wn.def(wordid,defnum,senseid,pkey) values({wordid},{defnum},{senseid},'{pkey}');\n"

def composeRel(relptr,relofst,relpos,relnumnum):
	#num1 = int(relnumnum[0,2])
	#num2 = int(relnumnum[2,4])
	#if num1 <= 0:
	#	princetonkey = f'{relpos}-{relofst}'
	#	s = f'insert into wn.wordkey(princetonkey,sqlkey) values({princetonkey},{senseid});
	#else:	
	#	princetonkey = f'{relpos}-{relofst}-{num1}'
	#	s = f'insert into wn.wordkey(princetonkey,sqlkey) values({princetonkey},{senseid});
	#return s
	return f"insert into wn.rel(relptr,relofst,relpos,relnumnum) values('{relptr}','{relofst}','{relpos}','{relnumnum}');\n"

fdict = open(f'{dirout}/loaddict.sql', 'w')
fsense = open(f'{dirout}/loadsense.sql', 'w')
fdef = open(f'{dirout}/loaddef.sql', 'w')
frel = open(f'{dirout}/loadrel.sql', 'w')

counter = 0
runaway = 83000 
wordid = 1
senseid = 1
defctr = 0
relctr = 0
totrel = 0

def processFile(fname, pos):
	global fdict,fsense,fdef,counter,runaway,wordid,senseid,defctr,relctr,totrel
	infile = open(fname, 'r')
	for line in infile:
		counter += 1
	
		# stop after maximum number of lines
		if counter > runaway:
			break
	
		# skip copyright lines at head of file
		if line[0:2] == '  ':
			continue
	
		# parse words and sense from the line
		h = line.split(' | ')
		a = h[0]
		sense = h[1].strip().replace("'","''");
		a = line.split(' ')
		ofst = a[0]
		cat = a[1]
		poscd = a[2]
		numwords = int(a[3],16)
		i = 1
		j = 4
		inc = 2
		aword = [a[j]]
		while i < numwords:
			j += inc
			aword.append(a[j])	
			i += 1

		# parse relationships
		j += inc
		numrel = int(a[j])
		totrel += numrel
		j += 1
		i = 1
		while i <= numrel:
			relptr = a[j+0]
			relofst = a[j+1]
			relpos = a[j+2]
			relnumnum = a[j+3]
			frel.write(composeRel(relptr,relofst,relpos,relnumnum))
			relctr += 1
			j += 4
			i += 1
	
		# write the outputs
		fsense.write(composeSense(senseid, pos, sense))
		defnum = 1
		for word in aword:
			fdict.write( composeDict(wordid, word))
			fdef.write( composeDef(wordid, defnum, senseid, ofst, pos))
			defctr += 1
			wordid += 1
			defnum += 1
	
		senseid += 1
		if counter%1000 == 0:
			print(f'{counter},', end='', flush=True)
	infile.close()
	print( f'\n{fname} completed.', flush=True)

processFile(f'{dirin}/data.adv', 'r')
#processFile(f'{dirin}/data.verb','v')
#processFile(f'{dirin}/data.adj', 'a')
#processFile('f{dirin}/data.noun', 'n')

print(f'complete. rows:{counter} sense:{senseid-1} dict:{wordid-1} def:{defctr} rel:{relctr} totrel:{totrel}')

fdict.close()
fsense.close()
fdef.close()


#infile = open('{dirin}dbfiles/noun.Tops', 'r')
# mat = re.match('{ (.*?), ((.*?)) }', '')
#mat = re.match('{ (.*?) \((.*?)\) }', line)
#print( mat)
#if mat:
#	print line
#	fdict.write(mat.group(1))
#	fdict.write('\n')
#	fsense.write(mat.group(2))
#	fsense.write('\n')

# { entity, (that which is perceived or known or inferred to have its own distinct existence (living or nonliving)) }

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
#02 + 02 00 + 08 00 
#| draw air into, and expel out of, the lungs; "I can breathe better when the air is clean"; "The patient is respiring"  
