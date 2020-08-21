import re

infile = open('../princeton/dict/dbfiles/noun.Tops', 'r')
fdict = open('../sql/loaddict.sql', 'w')
fsense = open('../sql/loadsense.sql', 'w')

counter = 0
for line in infile:
	counter += 1
	if counter > 10:
		break
# { entity, (that which is perceived or known or inferred to have its own distinct existence (living or nonliving)) }

#00001740 03 n 01 entity 0 003 ~ 00001930 n 0000 ~ 00002137 n 0000 ~ 04431553 n 0000 | that which is perceived or known or inferred to have its own distinct existence (living or nonliving)  

#00002137 03 n 02 abstraction 0 abstract_entity 0 010 @ 00001740 n 0000 + 00694095 v 0101 ~ 00023280 n 0000 ~ 00024444 n 0000 ~ 00031563 n 0000 ~ 00032220 n 0000 ~ 00033319 n 0000 ~ 00033914 n 0000 ~ 05818169 n 0000 ~ 08016141 n 0000 | a general concept formed by extracting common features from specific examples  

	# mat = re.match('{ (.*?), ((.*?)) }', '')
	mat = re.match('{ (.*?) \((.*?)\) }', line)
	print( mat)
	
	if mat:
		print line
		fdict.write(mat.group(1))
		fdict.write('\n')
		fsense.write(mat.group(2))
		fsense.write('\n')


infile.close()
fdict.close()
fsense.close()

