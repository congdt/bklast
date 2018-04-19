import os 
import sys, optparse

def data_statistic():

	method_dict = {'GET' : 0, 'POST': 0, 'HEAD' :0 , 'PUT': 0, 
						'DELETE': 0, 'OPTIONS' : 0, 'CONNECT' : 0}
	methods = method_dict.keys()
	wrong_method = 0 
	
	with open(FILE_DATA, 'r') as f :
		
		max_line_length = 0
		num_of_max_length = 0 
		lines_length_statistic = {'512':0, '1024':0, '2048': 0, '4096': 0, 'upper': 0}
		lines = f.readlines() 

		for i in range(len(lines)): 
			
			line_length = len(lines[i]) 
			if line_length > max_line_length :
				max_line_length = line_length
				num_of_max_length = i

			if line_length < 512: 
				lines_length_statistic['512'] += 1
			elif line_length < 1024:
				lines_length_statistic['1024'] += 1
			elif line_length < 2048 :
				lines_length_statistic['2048'] += 1
			elif line_length < 4096:
				lines_length_statistic['4096'] += 1
			else :
				lines_length_statistic['upper'] += 1

			
			method = lines[i].split(' ')[0]			 
			if method in methods :
				method_dict[method] += 1
			elif method[1:] in methods:
				method_dict[method[1:]] += 1
			else :
				print i, method 
				wrong_method += 1
		print "\n===================== Statistics =================================\n"
		print "   Number of Lines:                  ", len(lines) 
		print "\n   Max line's length: ", max_line_length, " - ", num_of_max_length
		print "\n   Line's length Statistics: "
		print lines_length_statistic
		print "\n   Number of undefined method:       ", wrong_method 
		print "\n\n   ", method_dict
		
		print "\n=========================  TERMINATE  ============================\n"

if __name__ == "__main__" :
	if len(sys.argv) == 2:
		FILE_DATA = sys.argv[1]
		data_statistic()
	else :
		print "\n Usage: python " + sys.argv[0] + " filename\n"
		