import sys , os
import time 

HOME_PATH = '/media/gekko/FA8A195BBBBEC20C/bk10-2017.2/'
#HOME_PATH = 'D:\\bk10-2017.2\\'
OUT_DIR = 'pre_classify/'
FILE_INPUT = 'data_no_label.txt'

REQUEST_METHODS = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS', 'CONNECT']

def classify():
	fout_malicious 		= open(HOME_PATH + OUT_DIR + "malicious.txt", "w")
	fout_suspicious 	= open(HOME_PATH + OUT_DIR + "suspicious.txt", "w")
	fout_suspiciousx 	= open(HOME_PATH + OUT_DIR + "suspiciousx.txt", "w")
	fout_remain 		= open(HOME_PATH + OUT_DIR + "remain.txt", "w")

	with open(HOME_PATH + 'data_no_label.txt', 'r') as f:

		for line in f :
			line_upper = line.upper()
			method = line_upper.split(' ')[0]
			#if method not in REQUEST_METHODS:
			#	fout_malicious.write(line) 
			if "%2f**%2f" in line:
				fout_malicious.write(line)
			
			elif "/etc" in line or "..%2F" in line_upper or "../" in line :
				fout_malicious.write(line)

			elif "%20AND%20" in line_upper :					# Sqli: and x = x 
				if "comment=" in line :							# sqli: and x > y 
					fout_suspiciousx.write(line)
					continue 
				index = line_upper.find("%20AND%20")
				if line_upper.find("%3D", index) != -1 or line_upper.find("=", index) != -1 or \
					line_upper.find("%3E", index) != -1 or line_upper.find(">", index) != -1 or \
					line_upper.find("%3C", index) != -1 or line_upper.find("<", index) != -1 :

					fout_malicious.write(line)
				else :
					fout_suspiciousx.write(line) 

			elif "%20UNION%20SELECT%20CHAR" in line_upper:		# sqli 
				fout_malicious.write(line)
			
			elif "SELECT%20" in line_upper:						# sqli 
				fout_malicious.write(line)

			elif len(line) > 300  and "comment=" not in line :
				fout_suspicious.write(line)
			else:
				fout_remain.write(line)

	fout_suspiciousx.close()
	fout_suspicious.close()
	fout_malicious.close()
	
	fout_remain.close()		


def detail_classify():
	fout_malicious1 	= open(HOME_PATH + OUT_DIR + "malicious1.txt", "w")
	fout_malicious2		= open(HOME_PATH + OUT_DIR + "malicious2.txt", "w")
	#fout_malicious3 	= open(HOME_PATH + OUT_DIR + "malicious3.txt", "w")
	fout_suspicious1 	= open(HOME_PATH + OUT_DIR + "suspicious1.txt", "w")
	fout_suspicious2 	= open(HOME_PATH + OUT_DIR + "suspicious2.txt", "w") 
	fout_suspicious3 	= open(HOME_PATH + OUT_DIR + "suspicious3.txt", "w") 
	fout_suspicious 	= open(HOME_PATH + OUT_DIR + "suspicious.txt", "w")
	fout_remain 		= open(HOME_PATH + OUT_DIR + "detail_remain.txt", "w")

	with open(HOME_PATH + 'data_no_label.txt', 'r') as f:

		for line in f :
			line_upper = line.upper()
			if "%2f**%2f" in line:
				fout_malicious1.write(line)
			elif "/etc" in line :
				fout_malicious2.write(line)

			elif "%20AND%20" in line_upper and "comment=" not in line:	
				if line_upper.find("%3D", index) != -1 or line_upper.find("=", index) != -1 or \
					line_upper.find("%3E", index) != -1 or line_upper.find(">", index) != -1 or \
					line_upper.find("%3C", index) != -1 or line_upper.find("<", index) != -1 :

					fout_suspicious1.write(line)

			elif "%20UNION%20SELECT%20CHAR" in line_upper:
				fout_suspicious2.write(line)
			elif "SELECT%20" in line_upper and "comment=" not in line: 
				fout_suspicious3.write(line)

			elif len(line) > 300 and "comment=" not in line :
				fout_suspicious.write(line)
			else:
				fout_remain.write(line)

	fout_suspicious3.close()
	fout_suspicious2.close()
	fout_suspicious1.close()
	fout_suspicious.close()

	fout_malicious1.close()
	fout_malicious2.close()
	#fout_malicious3.close()

	fout_remain.close()		


#pre_classify()

classify()