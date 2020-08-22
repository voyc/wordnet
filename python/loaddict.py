import re

def composeSense(senseid, pos, sense):
	return f"insert into wn.sense(id,pos,sense) values({senseid},'{pos}','{sense}');\n"
def composeDict(wordid, word):
	return f"insert into wn.dict(id,word) values({wordid},'{word}');\n"
def composeDef(wordid, defnum, senseid):
	return f"insert into wn.def(wordid,defnum,senseid) values({wordid},{defnum},{senseid});\n"

dirin = '../princeton/dict/'
dirout = '../sql/gen/'

fdict = open(f'{dirout}/loaddict.sql', 'w')
fsense = open(f'{dirout}/loadsense.sql', 'w')
fdef = open(f'{dirout}/loaddef.sql', 'w')

counter = 0
runaway = 83000 
wordid = 1
senseid = 1

def processFile(fname, pos):
	global fdict,fsense,fdef,counter,runaway,wordid,senseid
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
		numwords = int(a[3],16)
		i = 1
		j = 4
		inc = 2
		aword = [a[j]]
		while i < numwords:
			j += inc
			aword.append(a[j])	
			i += 1
	
		# write the outputs
		fsense.write(composeSense(senseid, pos, sense))
		defnum = 1
		for word in aword:
			fdict.write( composeDict(wordid, word))
			fdef.write( composeDef(wordid, defnum, senseid))
			wordid += 1
			defnum += 1
	
		senseid += 1
		if counter%1000 == 0:
			print(f'{counter},', end='', flush=True)
		#print(f'.', end='')
	infile.close()
	print( f'\n{fname} completed.\n')

processFile(f'{dirin}/data.adv', 'r')
processFile(f'{dirin}/data.verb','v')
processFile(f'{dirin}/data.adj', 'a')
#processFile('f{dirin}/data.noun', 'n')

print(f'\ncomplete. {counter} rows. {senseid} sense records. {wordid} dict records.\n')
	
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

