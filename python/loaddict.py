import re

def composeSense(senseid, sense):
	#return f"insert into wn.sense(id,sense) values({senseid},\'{sense}\');"
	x = f'xxx'
	return x
def composeDict(wordid, dict):
	return 'xxx'
def composeDef(wordid, defnum, senseid):
	return 'xxx'

#infile = open('../princeton/dict/dbfiles/noun.Tops', 'r')
infile = open('../princeton/dict/data.noun', 'r')
fdict = open('../sql/loaddict.sql', 'w')
fsense = open('../sql/loadsense.sql', 'w')
fdef = open('../sql/loaddef.sql', 'w')

counter = 0
wordid = 1
senseid = 1
	
for line in infile:
	counter += 1
	if counter > 40:
		break

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

	if line[0:2] == '  ':
		continue

	h = line.split(' | ')
	a = h[0]
	sense = h[1].strip()

	a = line.split(' ')
	#print(a)

	ofst = a[0]
	numwords = int(a[3])
	#print(ofst, numwords)

	i = 1
	j = 4
	inc = 2
	aword = [a[j]]
	while i < numwords:
		j += inc
		aword.append(a[j])	
		i += 1
	print aword
	print sense
	print '\n'

	fsense.write(composeSense(senseid, sense))
	senseid += 1

	defnum = 1
	for word in aword:
		fdict.write( composeDict(wordid, dict))
		fdef.write( composeDef(wordid, defnum, senseid))
		wordid += 1
		defnum += 1
	
infile.close()
fdict.close()
fsense.close()
fdef.close()

