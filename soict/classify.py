import sys , os
import time 
import re

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

GROUP_ALPHA = ['smtemp', 'smite', 'view', 'searchphrase', 'ver', 'option', 'task', 'lang']
GROUP_PATH = ['path', 'img', 'fileName', 'fileName', 'name', 'file', 'url', 'page'] 
GROUP_NUM = ['smid', 'limit', 'limitstart', 'id', 'p', 'start', 'src']

# wp-config.php /etc/passwd magmi.ini
def classify_v2():
	alpha_re = re.compile('^[0-9A-Za-z\-._]*$')
	num_re = re.compile('^[0-9]*$')

	fout_malicious 		= open(HOME_PATH + OUT_DIR + "malicious_v2.txt", "w")
	fout_remain 		= open(HOME_PATH + OUT_DIR + "remain_v2.txt", "w")

	with open("data_no_label.txt", 'r') as fin :
		for line in fin:
			line = line.split(' ')
			if len(line) < 2:		# not in form GET path/?name=value HTTP/1.1
				# abnormal
				continue

			l = line[1].split('?')
			if len(l) < 2 : 		
				# normal (no param)
				
				continue


			#params = l[1].split('&')
			params = line[1][len(l[0])+1:].split('&')
			for p in params:		# 
				tmp = p.split('=')
				if len(tmp) < 2:
					# abnormal
					continue
				if len(tmp[0]) == 0 :
					# abnormal
					continue
				param_name = tmp[0]
				param_value = '' if len(tmp[1])== 0 else p[len(param_name)+1:]	
				if param_name in GROUP_ALPHA:
					if alpha_re.match(param_value) :
						# normal
					else :
						# abnormal

				elif param_name in GROUP_NUM:
					if num_re.match(param_value) :
						# normal 
					else:
						# abnormal
				# wp-config.php /etc/passwd magmi.ini ../../
				elif param_name in GROUP_PATH:
					if "wp-config.php" in param_value or \
						"/etc/passwd" in param_value or \
						"magi.ini"  in param_value or \
						"../../"  in param_value :
						# abnormal 

				else :
					# normal 
				


#pre_classify()

classify()