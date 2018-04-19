import os, sys
import time 

# convert to sequence
# REQUEST_METHODS = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS', 'CONNECT']



def generate_data(infile, label, type , outfile):
	"""
		input: 
			- infile/outfile : input , output file 
			- label : label for file (1=anormal, 0=normal)
			- type :  
					+ 1 if generate from full request 
					+ 0 if generate from query only  
	"""
	fout = open(outfile, 'w')
	with open(infile, 'r') as fin:
		while True:
			full_request = ''
			first_line = fin.readline()						# read first line
			if first_line == '' :
				print "EOF"
				break
			full_request += first_line.rstrip()	
			method = first_line.split(' ')[0]
			while True:
				line = fin.readline().rstrip()				# read other line
				if len(line) == 0:							# 1st empty line
					if method == 'GET' :
						fin.readline() 						# 2nd empty line in GET
						break 
					elif method == 'POST' or method == 'PUT':
						params = fin.readline().rstrip()	# post params
						if len(params) == 0:
							print "POST/PUT no params"
							break 
						full_request += '#' + params
						fin.readline()						# 2nd empty line in POST/PUT 
						break 
					else:
						print first_line 					# just for check
						break 
				else :
					if type == 1 :
						full_request += '#' + line

				
			fout.write('|'+full_request + '|,' + str(label) + '\n')



if __name__ == '__main__':
	print '--------------------------'
	print "- Only running on Linux  -"
	print "--------------------------\n"
	in_normal_test = 'normalTrafficTest.txt'
	in_anormal = 'anomalousTrafficTest.txt'
	in_normal_train = 'normalTrafficTraining.txt'
	out_normal_test = 'csic_normal_test.txt'
	out_normal_train = 'csic_normal_train.txt'
	out_anormal		= 'csic_anormal.txt'

	start = time.time()
	# generate full 
	generate_data(in_normal_test, 0, 1, out_normal_test)
	generate_data(in_normal_train, 0, 1, out_normal_train)
	generate_data(in_anormal, 1, 1, out_anormal)
	os.system("sort -R " + out_anormal + " " + out_normal_train + " " + out_normal_test + " -o csic_full_request_data.csv")
	
	print "time1:", time.time()-start 
	start = time.time()
	# generate query only 
	generate_data(in_normal_test, 0, 0, out_normal_test)
	generate_data(in_normal_train, 0, 0, out_normal_train)
	generate_data(in_anormal, 1, 0, out_anormal)
	os.system("sort -R " + out_anormal + " " + out_normal_train + " " + out_normal_test + " -o csic_query_only_data.csv")
	print "time2:", time.time()-start 

