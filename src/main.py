"""
* Created by PyCharm.
* User: tuhoangbk
* Date: 05/10/2018
* Time: 23:31
*Have a nice day　:*)　:*)
"""
from File_Processing import File_Processing
from Image_Processing import Image_Processing
from Sentence_Processing import Sentence_Processing
from Dictionary_Processing import Dictionary_Processing
from Data_Processing import Data_Processing
from Google_Vision_API import Google_Vision_API
from Model_MLP import Model_MLP
from os.path import join
from keras.models import load_model
from keras.utils import plot_model
import numpy as geek
import numpy as np
import random
import pickle
from keras.callbacks import ModelCheckpoint

IS_RAW_TO_CSV = False
IS_SHOW_IMAGE = False
IS_SAVE_DICTIONARY = False
IS_WRITE_DATA_TO_FILE = True

INPUT_DIM = 50
BATCH_SIZE = 8
NUM_EPOCHES = 10
TRAIN_PER_ALL = 0.8

path_to_file_csv = '/home/tuhoangbk/20181/demo-datn/file_csv/out.csv'
path_to_raw_data = '../folder_raw'
path_to_test_image = '../image/test_image.png'
path_to_dict = '/home/tuhoangbk/20181/demo-datn/dict_pickle'
path_to_input = '/home/tuhoangbk/20181/demo-datn/train_test_data/train.txt'
path_to_target = '/home/tuhoangbk/20181/demo-datn/train_test_data/test.txt'
path_to_folder_training = '/home/tuhoangbk/20181/demo-datn/file_training'

if __name__ == '__main__':
    # Create file csv
    if IS_RAW_TO_CSV:
        Dictionary_Processing.create_csv_from_raw(path_to_raw_data, path_to_file_csv)

    # Text Detection & Text Recognition
    arr_blocks, boxes = Google_Vision_API.detect_document(path_to_test_image)
    print(arr_blocks)
    print(boxes)

    #Show Image
    if IS_SHOW_IMAGE:
        Image_Processing.draw_rectangle_on_image(path_to_test_image, boxes)

    # Search sentence in file csv (matching)
    id = Sentence_Processing.is_sentence_exist_in_knowlege(arr_blocks)

    # Create Dictionary chinese and vietnamese:
    vn_dict = Dictionary_Processing.create_dict_vietnamese(path_to_file_csv)
    chn_dict = Dictionary_Processing.create_dict_chinese(path_to_file_csv)
    print(len(vn_dict))
    print(len(chn_dict))

    print(vn_dict)
    print(chn_dict)
    if IS_SAVE_DICTIONARY:
        f_vn = open(join(path_to_dict, "vn_dict"), 'wb')
        pickle.dump(vn_dict, f_vn)
        f_chn = open(join(path_to_dict, 'chn_dict'), 'wb')
        pickle.dump(chn_dict, f_chn)
    # word to vec
    xx = Sentence_Processing.convert_sentence_vietnamese_to_vector("Diễn xuất là nam thánh tổ", vn_dict)
    print(xx)

    #Create input & target:
    arr_chn, arr_vn = Sentence_Processing.get_arr_of_sentence(path_to_file_csv)
    if IS_WRITE_DATA_TO_FILE:
        File_Processing.write_arr_to_file(arr_chn, path_to_input)
        File_Processing.write_arr_to_file(arr_vn, path_to_target)

    input, input_decode, target_decode = Data_Processing.create_data_train(arr_chn, arr_vn, chn_dict, vn_dict, INPUT_DIM, path_to_folder_training)

    # Build model
    vocab_size_china = len(chn_dict) + 1
    vocab_size_vietnam = len(vn_dict) + 1
    hidden_size = 200
    print('vocab_size_china: ', vocab_size_china)
    print('vocab_size_vietnam: ', vocab_size_vietnam)

    # rnn_lstm = Model_MLP.model_rnn_lstm(vocab_dim=vocab_size_china, hidden_size=hidden_size, input_dim=input_dim, output_dim=input_dim)
    # rnn_lstm.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])
    # rnn_gru = Model_MLP.model_rnn_lstm(vocab_dim=vocab_size_china, hidden_size=hidden_size, input_dim=input_dim, output_dim=input_dim)
    # rnn_gru.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])

    new_model = Model_MLP.build_model(vocab_size_china=vocab_size_china, vocab_size_vietnam=vocab_size_vietnam, hidden_size=hidden_size)

    #Fit model
    len_train_data = (int)(len(input) * TRAIN_PER_ALL)
    len_test_data = len(input) - len_train_data

    checkpointer_lstm = ModelCheckpoint(filepath='/home/tuhoangbk/20181/demo-datn/model_checkpoint_lstm' + '/model-{epoch:02d}.hdf5', verbose=1)
    checkpointer_gru = ModelCheckpoint(filepath='/home/tuhoangbk/20181/demo-datn/model_checkpoint_gru' + '/model-{epoch:02d}.hdf5', verbose=1)
    checkpointer_nmt = ModelCheckpoint(filepath='/home/tuhoangbk/20181/demo-datn/model_checkpoint_nmt' + '/model-{epoch:02d}.hdf5', verbose=1)

    # train_data_generator = Data_Processing.KerasBatchGenerator(input[:len_train_data], input_decode[:len_train_data], input_dim, batch_size, vocabulary=vocab_size_china)
    # test_data_generator = Data_Processing.KerasBatchGenerator(input[len_train_data:], input_decode[len_train_data:], input_dim, batch_size, vocabulary=vocab_size_china)

    # a = np.random.randint(5, size=(2, 4))
    from keras.utils import to_categorical

    # rnn_lstm.fit_generator(train_data_generator.generate(), len_train_data // (batch_size * input_dim), num_epochs,
    #                     validation_data=test_data_generator.generate(),
    #                     validation_steps=len_test_data // (batch_size * input_dim), callbacks=[checkpointer])
    # rnn_lstm.fit_generator((a, b), 1, num_epochs,
    #                     validation_data=(a, b),
    #                     validation_steps=1, callbacks=[checkpointer])
    # rnn_lstm.fit(input, target_one_hot, batch_size=batch_size, epochs=num_epochs, callbacks=[checkpointer_lstm])

    target_one_hot = Data_Processing.target_to_onehot(target_decode, INPUT_DIM, vocab_size_vietnam)
    new_model.fit([input, input_decode], target_one_hot,
              batch_size=BATCH_SIZE,
              epochs=NUM_EPOCHES,
              validation_split=0.20, callbacks=[checkpointer_nmt])
    assert False

    #predict model

    model_preetrain = load_model('/home/tuhoangbk/20181/demo-datn/model_checkpoint_gru/model-10.hdf5')
    y_new = model_preetrain.predict(input[:2])
    soft_max_y = geek.argmax(y_new[1], axis=1)
    print(input[1])
    print(soft_max_y)

    #show model

    plot_model(rnn_lstm, to_file='model.png')
