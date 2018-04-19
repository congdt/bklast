import os 
import sys
import operator 
import time

HOME_PATH = '/media/gekko/FA8A195BBBBEC20C/bk10-2017.2/'
#HOME_PATH = 'D:\\bk10-2017.2\\'
FILE_OUT = 'data_no_label.txt'
dirs = ['log', 'log2']

count = 0 
def preprocess_logs():
	global count 

	pname_dict = dict()
	spec_set = set()
	for d in dirs:

		path = HOME_PATH + d + '/'

		files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

		for filename in files :
			if filename == '.gitignore':
				continue
			log_set = set()
			with open( path + filename, 'r') as f:
				for l in f :
					if len(l.split('"')) < 3:
						print l 
						exit()
					request = l.split('"')[1]
					#ip = l.split(' ')[0]
					#response_code = l.split('"')[2]
					
					if '|' in request :				# '|' -> ko parse csv 
						count += 1
						spec_set.add(request + '\n')
						continue 
					#log_set.add(ip + ' ##' + response_code + '##' + request + '|,1\n')
					
					log_set.add(request + '\n')

				print d, ':', filename + ' ====> done. Size set: ', len(log_set) 
				

			f_out = open('preprocess_logs/' + d + '_' + filename, 'w')
			for item in log_set:
				f_out.write(item)

			f_out.close()
	
	# store all request has '|' in URL
	with open(HOME_PATH + "spec_req.txt", "w") as f_out:
		for item in spec_set:
			f_out.write(item)




def generate_data():

	path = HOME_PATH + 'preprocess_logs/'
	files = [ f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

	log_set = set()
	for filename in files:

		with open(path + filename, 'r') as f:
			log_set.update(f.readlines())

	with open(HOME_PATH + FILE_OUT, 'w') as f_out:
		for item in log_set:
			f_out.write(item)


#REQUEST_METHODS = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS', 'CONNECT']


if __name__ == '__main__' :
	if len(sys.argv) == 1:
		start = time.time()
		print '----------------- Preprocesss ----------------------\n'
		preprocess_logs()
		print "Number of line has '|': ", count 

		print '----------------- Generate data ------------------------\n'
		generate_data()

		print '--------------------- Statistic -----------------------------\n'
		#data_statistic()
		
		#seperate_into_params(FILE_OUT)
		print "time", time.time() - start
	elif len(sys.argv) == 2 :
		if sys.argv[1] == '-h' or sys.argv[1] == '--help' or sys.argv[1] == '-help': 
			print "Usage: "
			print "python " + sys.argv[0] + "              : do all process on files in log & log2"
			print "python " + sys.argv[0] + " file_name    : do statistic on file file_name"
		else:
			print "only do statistic on file " + sys.argv[1]
			FILE_OUT = sys.argv[1]
			data_statistic()

