import os, sys 
import optparse
import time 
import socket 
def regen_from_mods(filename):
	return 
def regen_from_csis(filename):
	with open(filename, 'r') as fin:
		print "--------------------------"
		while True:
			full_request = ''
			first_line = fin.readline()						# read first line
			if first_line == '' :
				print "EOF"
				break
			full_request += first_line
			method = first_line.split(' ')[0]
			while True:
				line = fin.readline()				# read other line
				#full_request += line
				if len(line.rstrip()) == 0:							# 1st empty line
					if method == 'GET' :
						full_request += fin.readline() 						# 2nd empty line in GET
						break 
					elif method == 'POST' or method == 'PUT':
						params = fin.readline()	# post params
						if len(params.rstrip()) == 0:
							print "POST/PUT no params"
							break 
						full_request += params
						full_request += fin.readline()		# 2nd empty line in POST/PUT 
						
						break 
					else:
						print first_line 					# just for check
						break 
				else :
					full_request += line
			print full_request
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect(("localhost", 80))
			s.sendall(full_request)
			data = s.recv(1024)
			print data 

if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option('-f', action="store", dest="file", help="input file")
	parser.add_option('-t', "--type", action="store", dest="type", help="file type = 'mods' if ModSec File else 'csis'")
	options, args = parser.parse_args()
	if options.file is not None:
		in_file = options.file
	else :
		print "No Input File "
		exit()
	if options.type is not None :
		file_type = options.type 
	else :
		print "No Type File" 
		exit() 

	if file_type == 'mods':
		regen_from_mods(in_file)
	elif file_type == 'csis':
		regen_from_csis(in_file)
	else :
		print "Error: unknow file type"
