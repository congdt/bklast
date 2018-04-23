import sys
import os
import time
import json
import pandas
import numpy
import optparse
from keras.callbacks import TensorBoard
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from collections import OrderedDict

def train(csv_file):

    #
    dataframe = pandas.read_csv(csv_file, engine='python', quotechar='|', header=None)
    dataset = dataframe.sample(frac=1).values
    
    #print dataset
    
    # Preprocess dataset
    '''
        type(dataset) = ndarray, size 2*x
            dataset[a:b,c] : return a ndarray that include elements c'th from row a'th to row b'th 
    '''
    X = dataset[:,0]
    Y = dataset[:,1]
    
	
    # tao tokenizer object, filter loai bo cac ki tu '\n\t'
	#                       char_level=True -> moi ki tu dc coi la 1 token 

    tokenizer = Tokenizer(filters='\t\n', char_level=True)
    
    # giong nhu load X vao Tokenizer, X ko thay doi 
    # Store everything in word-index
    # https://github.com/keras-team/keras/issues/7551
    tokenizer.fit_on_texts(X)

    # Extract and save word dictionary
    word_dict_file = 'build/word-dictionary.json'

    if not os.path.exists(os.path.dirname(word_dict_file)):
        os.makedirs(os.path.dirname(word_dict_file))

    with open(word_dict_file, 'w') as outfile:
        json.dump(tokenizer.word_index, outfile, ensure_ascii=False)


    num_words = len(tokenizer.word_index)+1

    # convert cac string trong X theo cac index cua tokenizer.word_index 
    # thanh 1 mang cac index, thay vi mang ky tu 
    # vd: x[1] = 'abc', idex(a) = 2, idex(b) = 10, idex(c) = 8
    #   => x[1] = [2, 10, 8]
    X = tokenizer.texts_to_sequences(X)
    print len(X)
    #print '---------------------__X 3 ---------------------'
    #print X

    max_log_length = 1024
    train_size = int(len(dataset) * .70)
    eval_size = int(len(dataset) * .05)

    # padding cac gia tri 0 (truoc or sau) 
    # de tat ca cac ptu trong X deu co do dai max_log_length 
    X_processed = sequence.pad_sequences(X, maxlen=max_log_length)
    
    X_train = X_processed[0:train_size]
    X_eval  = X_processed[train_size:train_size+eval_size]
    X_test  = X_processed[train_size+eval_size:]

    Y_train = Y[0:train_size]
    Y_eval  = Y[train_size:train_size+eval_size]
    Y_test  = Y[train_size+eval_size:]
    
    #print ("-------------------- X_train ------------------"	)
    #print Y_train
    
    tb_callback = TensorBoard(log_dir='./logs', embeddings_freq=1)

    model = Sequential()
    model.add(Embedding(num_words, 32, input_length=max_log_length))
    model.add(Dropout(0.5))
    # change from 64 > 128 / 22-4
    model.add(LSTM(128, recurrent_dropout=0.5))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(model.summary())

    model.fit(X_train, Y_train, validation_split=0, epochs=3, batch_size=128, callbacks=[tb_callback])

    # Evaluate model
    score, acc = model.evaluate(X_eval, Y_eval, verbose=1, batch_size=128)

    print("Model Accuracy: {:0.2f}%".format(acc * 100))

    # Save model
    model.save_weights('securitai-lstm-weights.h5')
    model.save('securitai-lstm-model.h5')
    with open('securitai-lstm-model.json', 'w') as outfile:
        outfile.write(model.to_json())
    
    # Test model 
    print "-----------------------------------------------"
    print "Testing ....."
    prediction = model.predict(X_test)
    print "Prediction finish. "
    print prediction
    print Y_test 
    count = 0
    for i in range(len(prediction)):
        pred = 1 if prediction[i][0] >= 0.5 else 0 
        if Y_test[i] == pred:
            count += 1 
    print "Test Accuracy:", count*1.0/len(prediction), "%"


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', action="store", dest="file", help="data file")
    options, args = parser.parse_args()

    if options.file is not None:
        csv_file = options.file
    else:
        csv_file = 'csic_query_only_data.csv'
    start_time = time.time()
    model = train(csv_file)

    print("time: ", time.time()-start_time)
