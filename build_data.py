import os, sys
import optparse

HOME_PATH = '/media/gekko/FA8A195BBBBEC20C/bk10-2017.2/'
#HOME_PATH = 'D:\\bk10-2017.2\\'

INPUT_DIR = "pre_classify/"
FILE_OUT = 'data_set.csv'
MALICIOUS_FILE = 'malicious.txt'
NORMAL_FILE = 'remain.txt'


MAX_LINE = 1000000
REQUEST_METHODS = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS', 'CONNECT']

def label_data(numberNormal, numberMalicious, n_start, m_start):

	fout = open(HOME_PATH + "dataset.csv", "w")
	with open(HOME_PATH + INPUT_DIR + MALICIOUS_FILE, "r") as malicious_file:
		count = 0 
		count2 = 0
		for line in malicious_file:
			count += 1
			if count < m_start :
				continue
			if count2 > numberMalicious :
				break
			count2 += 1
			if len(line) == 0 :
				continue 
			line = "|" + line.rstrip() + "|,1\n"
			fout.write(line)

	with open(HOME_PATH + INPUT_DIR + NORMAL_FILE, "r") as normal_file :
		count = 0
		count2 = 0
		for line in normal_file :
			count2 += 1
			if count2 < n_start:
				continue 
			if count > numberNormal:
				break 
			count += 1 
			if len(line) == 0 :
				continue 
			method = line.split(' ')[0]
			if method not in REQUEST_METHODS : 
				continue 
			line = "|" + line.rstrip() + "|,0\n"
			fout.write(line)

	fout.close()
	

def count_line():
	with open(HOME_PATH + INPUT_DIR + MALICIOUS_FILE, "r") as f:
		print "Number of Line in Malicous File:", len(f.readlines())
	with open(HOME_PATH + INPUT_DIR + NORMAL_FILE, "r") as f :
		print "Number of Line in Normal File  :", len(f.readlines())

if __name__ == "__main__" :
	count_line()
	parser = optparse.OptionParser()
	parser.add_option('-m', '--malicious', action="store", dest="numMalLine", help="Number of Malicious Line")
	parser.add_option('-n', '--normal',action="store", dest="numNorLine", help="Number of Normal Line")
	parser.add_option('--mStart', action="store", dest="m_start", help="Start Mal Line")
#	parser.add_option('-m_end', action="store", dest="m_end", help="End Mal Line")
	parser.add_option('--nStart', action="store", dest="n_start", help="Start Nor Line")
#	parser.add_option('-n_end', action="store", dest="n_end", help="End Nor Line")
	
	options, args = parser.parse_args()

	numberMalicious = int(options.numMalLine) if options.numMalLine is not None else MAX_LINE
	m_start = int(options.m_start) if options.m_start is not None else 0
	numberNormal = int(options.numNorLine) if options.numNorLine is not None else MAX_LINE
	n_start = int(options.n_start) if options.n_start is not None else 0

	print numberMalicious, m_start, numberNormal, n_start
	label_data(numberNormal, numberMalicious, n_start, m_start)
	"""
	if len(sys.argv) == 1 :
		print "build all data"
		label_data(MAX_LINE, MAX_LINE)
	elif len(sys.argv) == 3 : 
		numberNormal = int(sys.argv[1]) if int(sys.argv[1]) >= 0 else MAX_LINE
		numberMalicious = int(sys.argv[2]) if int(sys.argv[2]) >= 0 else MAX_LINE

		label_data(numberNormal, numberMalicious)
	else : 
		print "\n===================== Usage =============================="
		print "\n+ python " + sys.argv[0] + " :==>  build all data\n"
		print "+ python " + sys.argv[0] + "  numNormalLine numMaliciousLine:==> build data with these amount line \n"
		print "NOTE: if numberLine <= 0 : \n     ==> build all this datatype\n"
		count_line()
		print "\n===================== Usage ==============================\n"

	"""
