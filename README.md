Modify:
	Step 2: Classify: 
		- ..%2f vs ../ can xem lai 
		- sua lai SELECT%20 (ko dc co comment)
	New Classify : 
		- filter by values of parameters (no care about parameter's name)


Logs:
	apache: access_log

Step 1: process_logs.py 

	"""

	"""
	- preprocess_logs() : 
		+ read each file log (in log & log2 directory) 
			=> get only request (ex: "GET / HTTP/1.1")
			=> filter, get only unique requests (remove all same requests) 
			=> write to file respectly (in preprocess_logs directory)

	- generate_data() : 
		+ from preprocessed file, put them all together
		+ output: data_no_label.txt

Step 1.5: params_stat.py

	"""
		print all statistic info of params in request
	"""

Step 2: classify.py 

	"""
		classify data.
			input : all file in folder: preprocess_logs/
			output: all file in folder: pre_classify/

	"""
	- classcify(): divide into 3 groups
		+ malicious:
			- has '%2f**%2f'
			- has '/etc' or '..%2f' or '../'
			- has '%20AND%20' follow '=' '>' '<' 
			- has '%20UNION%20SELECT%20CHAR'
			- has "SELECT%20" 
		+ suspicious:
			- has '%20AND%20' and 'comment='   
			- len(line) > 300 and no "comment="

		+ normal:
			- remain

	- detail_classify(): divide into all of these signals 
		+ malicious:
			- malicious1: "%2f**%2f"
			- malicious2: "/etc"

		+ suspicious:
			- suspicious1: "%20AND%20" following "=" "<" ">"
			- suspicious2: "%20UNION%20SELECT%20CHAR" 
			- suspicious3: "SELECT%20"
			- suspicious: len(line) > 300 and no "comment="

		+ normal :
			- remain 

Step 3: Build data 

	"""
		label data from file malicious & normal, 
		convert to csv type, put them all together

		can specify number of (line) malicious request, normal request, and which line to start copy data

		input: 	pre_classify/malicious.txt
				pre_classify/normal.txt
		output: dataset.csv 
	"""
		


Step 4: Training 

	"""
		training with input file: dataset.csv 

	"""

Step 5: Testing: predict.py 

	"""
		Test all request in given file 
		Test one request per time  
	"""
