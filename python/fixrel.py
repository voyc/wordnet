#replace pkey with defid
#loop thru the rel table
#for each rel record
#	get the def record matching pkey1
#	get the id from that record
#	set it in wn.rel.defid1
#
#	get the def record matching pkey2
#	get the id from that record
#	set it in wn.rel.defid2
#
#	update the rel record
#
# =+  | Derivationally related form  | lexical | nv
# ^   | Also see                     | lexical | vj
# \   | Pertainym (pertains to noun) | lexical | j
# -\  | Pertainym (derived from adj) | lexical | a
# <   | Participle of verb           | lexical | j

lexptrs = ['=+','^','\\','-\\','<']
ptr = 'h'
print(ptr in lexptrs)
ptr = '^'
print(ptr in lexptrs)

