"""
* Created by PyCharm.
* User: tuhoangbk
* Date: 05/10/2018
* Time: 23:31
*Have a nice day　:*)　:*)
"""

import random
from File_Processing import File_Processing
from os.path import join

def split_word_from_sentence(self, full_sentence):
    pass

def load_dictionary_from_file(self, file_dictionary):
    pass

def save_dictionary_to_file(self, file_dictionary):
    pass

def add_word_to_dictionary(self, new_word):
    pass

def get_id_from_dictionary_by_word(self, word):
    pass

def get_word_from_dictionary_by_id(self, id):
    pass

def get_len_of_dictionary(self):
    return len(self.dictionary)

def create_dictionary(self):
    pass

def clean_string(string):
    string = string.lower()
    return ''.join(e for e in string if (e.isalnum() or e == ' '))

def sentence_is_vietnamese(sentence):
    list_character_vietnames = 'àáảãạăắằẵặẳâầấậẫẩđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵqwertyuiopasdfghjklzxcvbnm'
    is_vietnamese = False
    for c in sentence:
        if c in list_character_vietnames:
            is_vietnamese = True
            break
    return is_vietnamese

def create_csv_from_raw(path_to_folder_raw, csv_output):
    list_file = File_Processing.get_file_from_folder(path_to_folder_raw)
    arr_chi_vi = []
    for file in list_file:
        lines = File_Processing.read_lines(join(path_to_folder_raw, file))
        # print(lines)
        vietnamese_string = ''
        chinese_string = ''
        comment_string = ''
        chi_vi_string = ''
        for line in lines:
            line = line.strip()
            if not sentence_is_vietnamese(line):
                if (chinese_string != '') and (vietnamese_string != ''):
                    chi_vi_string = file + ',,' + chinese_string + ',,' + vietnamese_string + ',,' + comment_string
                    arr_chi_vi.append(
                        chi_vi_string.replace(',,', '~').replace(',', '').replace('~', ',').replace(';', ''))
                    chinese_string = ''
                    vietnamese_string = ''
                    comment_string = ''
                    chi_vi_string = ''
                if chinese_string == '':
                    chinese_string = line
                else:
                    chinese_string = chinese_string + '|' + line
            else:
                if vietnamese_string == '':
                    vietnamese_string = line
                else:
                    if ('(' in line) or (')' in line) or ('-' in line):
                        # vietnamese_string = vietnamese_string + ',,' + line
                        comment_string = comment_string + line
                    else:
                        vietnamese_string = vietnamese_string + '|' + line
        if (chinese_string != '') and (vietnamese_string != ''):
            chi_vi_string = file + ',,' + chinese_string + ',,' + vietnamese_string + ',,' + comment_string
            arr_chi_vi.append(chi_vi_string.replace(',,', '~').replace(',', '').replace('~', ',').replace(';', ''))
    print('Read: ' + str(len(list_file)) + ' file OK')
    File_Processing.write_arr_to_file(arr_chi_vi, csv_output)

def create_dict_chinese(path_to_file_csv):
    dictionary_chinese = []
    data_from_csv_file = File_Processing.read_file_csv(path_to_file_csv)
    for row in data_from_csv_file:
        for symbol in row[1]:
            symbol = symbol.strip().replace(' ', '')
            if symbol in dictionary_chinese or symbol == ' ' or symbol == '|':
                continue
            dictionary_chinese.append(symbol)
    # print(dictionary_chinese)
    # print(len(dictionary_chinese))

    # dictionary_chinese.append('B')
    # dictionary_chinese.append('E')
    dictionary_chinese.sort()
    dictionary_chinese.append(dictionary_chinese[0])
    dictionary_chinese[0] = 'none'

    return dictionary_chinese

def create_dict_vietnamese(path_to_file_csv):
    dictionary_vietnamese = []
    data_from_csv_file = File_Processing.read_file_csv(path_to_file_csv)
    for row in data_from_csv_file:
        viet_string = row[2].replace('|', ' ')
        viet_string = clean_string(viet_string)
        arr_word = viet_string.split(' ')
        for word in arr_word:
            if (word == '') or (word in dictionary_vietnamese):
                continue
            dictionary_vietnamese.append(word)
    # print(dictionary_vietnamese)
    # print(len(dictionary_vietnamese))
    dictionary_vietnamese.append('eos')
    dictionary_vietnamese.append('bos')

    dictionary_vietnamese.sort()
    dictionary_vietnamese.append(dictionary_vietnamese[0])
    dictionary_vietnamese[0] = 'none'

    return dictionary_vietnamese

if __name__ == '__main__':
    # create_dict_chinese('/home/tuhoangbk/20181/demo-datn/file_csv/out.csv')
    create_dict_vietnamese('/home/tuhoangbk/20181/demo-datn/file_csv/out.csv')