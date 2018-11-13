"""
* Created by PyCharm.
* User: tuhoangbk
* Date: 05/10/2018
* Time: 23:27
*Have a nice day　:*)　:*)
"""
from os import listdir, makedirs
from os.path import isfile, isdir, join, exists
import csv

def get_file_from_folder(path_to_folder):
    onlyfiles = [f for f in listdir(path_to_folder) if isfile(join(path_to_folder, f))]

    return onlyfiles

def file_is_exist(path_to_file):

    return isfile(path_to_file)

def folder_is_exist(folder_name):

    return isdir(folder_name)

def get_sub_path_from_folder():
    pass

def create_new_folder(path):
    if not exists(path):
        makedirs(path)

def read_lines(path_to_file):
    if(not file_is_exist(path_to_file)):
        print("File not exist: read_lines")

        return 0
    file_open_to_read = open(path_to_file, 'r')

    return file_open_to_read.readlines()

def write_str_to_file(path_to_file, str):
    if (not file_is_exist(path_to_file)):
        print("File not exist: write_str_to_file")

        return 0
    file_open_to_write = open(path_to_file, 'a')
    file_open_to_write.writelines(str)

    return 1

def write_arr_to_file(arr_string, dest_path):
    file_open_to_write = open(dest_path, 'w')
    for string in arr_string:
        string = str(string)
        file_open_to_write.write(string + '\n')

    return True

def read_file_csv(path_to_file_csv):
    if (not file_is_exist(path_to_file_csv)):
        print("File not exist: read_file_csv")

        return 0
    open_file_to_read = open(path_to_file_csv, 'r')
    csv_reader = csv.reader(open_file_to_read, delimiter=',')

    return csv_reader