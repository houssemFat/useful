"""
	Code that convert a txt file
	line by line file to json format
	example of text file 
	
	`Reading# Mote-ID Humidity Tepmrature Label

	1	1	45.93	27.97	0
	1	1	45.93	27.97	0
	...`

"""
import json

data = {
	'head' : [],
	'data' : []
}
# split line 
def push_line (line) :
	line_data = line.split ()
	#print line_data
	line_data[0] = int(line_data[0])
	line_data[1] = int(line_data[1])
	line_data[2] = float(line_data[2])
	line_data[3] = float(line_data[3])
	line_data[4] = float(line_data[4])
	data['data'].append(line_data)
	
i = 0
# note that header = 2 
with open('singlehop-indoor-moteid1-data.txt') as data_file:
	for line in data_file:
		# data start at line 4 (5 in file)
		if (i > 4) :
			push_line (line)
		# header start at line 2 (3 in file)
		elif i == 2 :
			data['head'] = line.split()
		i = i+1

target = open('singlehop-indoor-moteid1-data.json', 'w')
target.write(json.dumps(data))
print "And finally, we close it."
target.close()
