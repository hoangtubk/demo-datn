"""
* Created by PyCharm.
* User: tuhoangbk
* Date: 05/10/2018
* Time: 23:29
*Have a nice day　:*)　:*)
"""
import csv
from Dictionary_Processing import Dictionary_Processing
def search_in_dictionary(self, full_sentence):
    pass

def search_sentence_by_id(self):
    pass

def is_sentence_exist_in_knowlege(arr_blocks):
    path_to_file_csv = '/home/tuhoangbk/20181/demo-datn/file_csv/out.csv'
    open_file_to_read = open(path_to_file_csv, 'r')
    csv_reader = csv.reader(open_file_to_read, delimiter=',')
    sentence_exist = False
    list_id = []
    for sentence in arr_blocks:
        id = 0
        for row in csv_reader:
            id = id + 1
            if sentence in row[1]:
                sentence_exist = True
                print("Câu " + sentence + " đã tồn tại trong CSDL với id: " + id)
                list_id.append(id)
                break
        print("Câu: " + sentence + " chưa có trong CSDL")

    return sentence_exist, list_id

def convert_sentence_chinese_to_vector(sentence, chn_dictionary, input_dim = 21):
    vec_sentence = []
    # sentence = 'B' + sentence + 'E'
    for symbol in sentence:
        for i in range(0, len(chn_dictionary)):
            if symbol == chn_dictionary[i]:
                vec_sentence.append(i)
                break
    if len(vec_sentence) < input_dim:
        for j in range(len(vec_sentence), input_dim):
            vec_sentence.append(0)

    return vec_sentence

def convert_sentence_vietnamese_to_vector(sentence, vn_dictionary, input_dim = 21):
    vec_sentence = []
    sentence = 'bos ' + sentence + ' eos'
    sentence = sentence.lower()
    sentence = sentence.split(' ')
    for word in sentence:
        for i in range (0, len(vn_dictionary)):
            if word == vn_dictionary[i]:
                vec_sentence.append(i)
                break
    if len(vec_sentence) < input_dim:
        for j in range(len(vec_sentence), input_dim):
            vec_sentence.append(0)

    return vec_sentence

def get_arr_of_sentence(path_to_file_csv):
    arr_of_chinese_sentence = []
    arr_of_vietnamese_sentence = []
    open_file_to_read = open(path_to_file_csv, 'r')
    csv_reader = csv.reader(open_file_to_read, delimiter=',')
    for row in csv_reader:
        # Add chinese sentence to array
        chn_sentence = row[1]
        chn_sentence = chn_sentence.split('|')
        number_of_sentence_in_one_line = len(chn_sentence)
        for line in chn_sentence:
            line = Dictionary_Processing.clean_string(line)
            line = line.replace(' ', '')
            arr_of_chinese_sentence.append(line)
        # Add vietnamese sentence to array
        vn_sentence = row[2]
        vn_sentence = vn_sentence.split('|')
        for i in range(0, number_of_sentence_in_one_line):
            vn_sentence[i] = Dictionary_Processing.clean_string(vn_sentence[i])
            arr_of_vietnamese_sentence.append(vn_sentence[i])

    return arr_of_chinese_sentence, arr_of_vietnamese_sentence
if __name__ == '__main__':
    chn, vn = get_arr_of_sentence('/home/tuhoangbk/20181/demo-datn/file_csv/out.csv')
    print(len(chn))
    print(len(vn))
    print((chn))
    print((vn))