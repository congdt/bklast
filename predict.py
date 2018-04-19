import sys
import os, time 
import json
import pandas
import numpy
import optparse
from keras.models import Sequential, load_model
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from collections import OrderedDict

def predict(csv_file, log_entry):
    # Loading processed word dictionary into keras Tokenizer would be better
    dataframe = pandas.read_csv(csv_file, engine='python', quotechar='|', header=None)
    dataset = dataframe.values

    # Preprocess dataset
    X = dataset[:,0]
    '''
    for index, item in enumerate(X):
        reqJson = json.loads(item, object_pairs_hook=OrderedDict)
        del reqJson['timestamp']
        del reqJson['headers']
        del reqJson['source']
        del reqJson['route']
        del reqJson['responsePayload']
        X[index] = json.dumps(reqJson, separators=(',', ':'))
	'''
    tokenizer = Tokenizer(filters='\t\n', char_level=True)
    tokenizer.fit_on_texts(X)
    seq = tokenizer.texts_to_sequences([log_entry])
    max_log_length = 1024
    log_entry_processed = sequence.pad_sequences(seq, maxlen=max_log_length)

    model = load_model('securitai-lstm-model.h5')
    model.load_weights('securitai-lstm-weights.h5')
    model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
    prediction = model.predict(log_entry_processed)
    print prediction[0]

def test(csv_file, data_test_file):
	# Process test data
	dataframe = pandas.read_csv(data_test_file, engine='python', quotechar='|', header=None)
	dataset = dataframe.values 
	X_test = dataset[:,0]
	Y_test = dataset[:,1]
	# Loading processed word dictionary into keras Tokenizer would be better
	dataframe = pandas.read_csv(csv_file, engine='python', quotechar='|', header=None)
	dataset = dataframe.values

	# Preprocess dataset
	X = dataset[:,0]

	tokenizer = Tokenizer(filters='\t\n', char_level=True)
	tokenizer.fit_on_texts(X)
	max_log_length = 1024
	
	model = load_model('securitai-lstm-model.h5')
	model.load_weights('securitai-lstm-weights.h5')
	model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
	#prediction = model.predict(log_entry_processed)
	count = 0 
	start_time = time.time()
	print start_time
	for i in range(len(Y_test)):
		seq = tokenizer.texts_to_sequences([X_test[i]])
		log_entry_processed = sequence.pad_sequences(seq, maxlen=max_log_length)
		prediction = model.predict(log_entry_processed)
		prediction = 1 if prediction[0][0] >= 0.5 else 0 
		if Y_test[i] == prediction :
			count += 1
		if (count %1000) == 0 :
			print time.time() - start_time
			start_time = time.time()
	#print prediction[0]
	print "Test:", count*1.0/len(X_test)
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', action="store", dest="file", help="data file")
    options, args = parser.parse_args()


    if options.file is not None:
        csv_file = options.file
    else:
        csv_file = 'dataset.csv'
	
	#request = "GET /?q='%20and%201=1; HTTP/1.1"
	#print request
	#predict(csv_file, request)
	 
	#if args[0] is not None:			
	#	predict(csv_file, args[0])
	if args[0] is not None:
		test(csv_file, args[0])