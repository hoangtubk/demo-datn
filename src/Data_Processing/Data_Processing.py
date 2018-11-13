"""
* Created by PyCharm.
* User: tuhoangbk
* Date: 13/10/2018
* Time: 09:09
*Have a nice day　:*)　:*)
"""
import numpy as np
from keras.utils import to_categorical
from File_Processing import File_Processing
from os.path import join
from Sentence_Processing import Sentence_Processing
class KerasBatchGenerator(object):

    def __init__(self, data_input, data_target, input_dim, batch_size, vocabulary, skip_step=5):
        self.data_input = data_input
        self.data_target = data_target
        self.input_dim = input_dim
        self.batch_size = batch_size
        self.vocabulary = vocabulary
        # this will track the progress of the batches sequentially through the
        # data set - once the data reaches the end of the data set it will reset
        # back to zero
        self.current_idx = 0
        # skip_step is the number of words which will be skipped before the next
        # batch is skimmed from the data set
        self.skip_step = skip_step

    def generate(self):
        x = np.zeros((self.batch_size, self.input_dim))
        y = np.zeros((self.batch_size, self.input_dim, self.vocabulary))
        print(x.shape)
        print(y.shape)

        while True:
            print(self.batch_size)
            for i in range(self.batch_size):
                if self.current_idx + self.input_dim >= len(self.data_input):
                    # reset the index back to the start of the data set
                    self.current_idx = 0
                x[i, :] = self.data_input[self.current_idx + i]
                temp_y = self.data_target[self.current_idx + i]

                # convert all of temp_y into a one hot representation
                y[i, :, :] = to_categorical(temp_y, num_classes=self.vocabulary)
                self.current_idx += self.skip_step
            print(x)
            print(y)
            yield x, y
def create_data_train(arr_chn, arr_vn, chn_dict, vn_dict, input_dim, path_to_folder_training):
    input = []
    input_decode = []
    target_decode = []
    for i in range(0, len(arr_chn)):
        vector_chn = Sentence_Processing.convert_sentence_chinese_to_vector(arr_chn[i], chn_dict,
                                                                            input_dim=input_dim)
        vector_vn = Sentence_Processing.convert_sentence_vietnamese_to_vector(arr_vn[i], vn_dict,
                                                                              input_dim=input_dim)
        # if len(vector_chn) != len(vector_vn):
        #     continue
        input.append(vector_chn)
        input_decode.append(vector_vn)
        target_decode.append(vector_vn[1:])
        target_decode[-1].append(0)

    input = np.asarray(input)
    input_decode = np.asarray(input_decode)
    target_decode = np.asarray(target_decode)
    print(input.shape)
    print(input_decode.shape)
    print(target_decode.shape)

    File_Processing.write_arr_to_file(input, join(path_to_folder_training, 'input.txt'))
    File_Processing.write_arr_to_file(input_decode, join(path_to_folder_training, 'input_decode.txt'))
    File_Processing.write_arr_to_file(target_decode, join(path_to_folder_training, 'target_decode'))

    return input, input_decode, target_decode

def target_to_onehot(target_decode, INPUT_DIM, vocab_size_vietnam):
    target_one_hot = np.zeros((len(target_decode), INPUT_DIM, vocab_size_vietnam))
    print(target_one_hot.shape)
    print(target_one_hot.shape[0])

    for i in range(target_one_hot.shape[0]):
        target_one_hot[i, :, :] = to_categorical(target_decode[i], vocab_size_vietnam)

    return target_one_hot


if __name__ == '__main__':
    data_input = [[1020, 886, 253, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [675, 609, 227, 1546, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1837, 1233, 1345, 815, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [294, 691, 1813, 815, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [897, 1157, 227, 1569, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [897, 1894, 959, 1569, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1508, 166, 1550, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1754, 732, 1167, 374, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [959, 479, 166, 739, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [494, 353, 1177, 761, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    data_target = [[1558, 1822, 817, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [948, 1242, 3, 646, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1751, 785, 1724, 1254, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [734, 1169, 29, 1254, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [131, 1060, 3, 927, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [131, 1277, 997, 927, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1087, 1301, 1339, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1912, 1173, 130, 639, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1275, 598, 1301, 602, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [20, 1545, 735, 1552, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    print(len(data_input))
    abc = KerasBatchGenerator(data_input, data_target, 25, 4, 2000, 5)
    abc.generate()
