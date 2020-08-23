replace pkey with defid
loop thru the rel table
for each rel record
	get the def record matching pkey1
	get the id from that record
	set it in wn.rel.defid1

	get the def record matching pkey2
	get the id from that record
	set it in wn.rel.defid2

	update the rel record

