import os, sys, operator
import time 
import re 

def is_common(str):
	r = re.compile("^[0-9A-Za-z_.\-=]+$")
	if r.match(str):
		return True
	return False 


def params_stat_v2(filename):

	big_dict = dict()

	with open(filename, "r") as fin :
		for line in fin:
			line = line.split(' ')
			if len(line) < 2:
				continue

			l = line[1].split('?')
			if len(l) < 2: 
				#print l 
				continue
			params = l[1].split('&')
			for p in params:		# 
				if len(p.split('=')) < 2:
					continue
				param_name = p.split('=')[0]
				param_value = p[len(param_name):]

				if not is_common(param_name):
					continue
				if param_name not in big_dict.keys():
					big_dict[param_name] = set()
					big_dict[param_name].add(param_value)
					big_dict[param_name + '_cnt'] = 0
					big_dict[param_name + '_sum'] = 1
				else :
					big_dict[param_name + '_sum'] += 1
					if len(param_value) > 30:  # bo qua 'token'
						big_dict[param_name + '_cnt'] += 1
						continue
					big_dict[param_name].add(param_value)

		with open('params_stat_v2.txt', 'w') as fout:
			for k, v in big_dict.iteritems():
				if '_' in k :
					continue
				fout.write('-'*20 + k + ' : ' + str(big_dict[k+'_cnt']) + " : " + str(big_dict[k + '_sum']) + '-'*20 + '\n')
				l = []
				for item in v :
					if is_common(item):
						l.append(item)
					else :
						fout.write(item + '\n')
				for i in l:
					fout.write(i+'\n')




if __name__ == "__main__":
	#inp = raw_input('input:')
	#print inp
	#print is_common(inp)
	#exit()
	start = time.time()
	params_stat_v2("data_no_label.txt")
	print "time:", time.time()-start