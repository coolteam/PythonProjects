from collections import Counter
import os
import csv
import time
import re


def read_dict(path_info, path_dict):
    with open(path_info, 'r', newline='', encoding='utf-8') as info_file:
        reader = csv.reader(info_file)
        info = list()
        for row in reader:
            info.append(row[0])
    with open(path_dict, 'r', newline='', encoding='utf-8') as dict_file:
        reader = csv.reader(dict_file)
        word_dict = {}
        for row in reader:
            values = []
            for i in range(1, 7):
                values.append(row[i])
            word_dict[row[0]] = values
    return info[1], info[2], word_dict


def read_text(path):
    pattern = r"[^\w\s\-\']"
    file = open(path, 'r', encoding='utf-8')
    text = file.read()
    file.close()
    lower_case_text = text.lower()
    prepared_text = re.sub(pattern, '', lower_case_text)
    splitted_text = prepared_text.split()
    stripped_text = [el.strip('\'') for el in splitted_text]
    non_empty_text = [el for el in stripped_text if el]
    F_counter = Counter(non_empty_text)
    return F_counter


text_path = 'D:/Research/John Ronald Reuel Tolkien/LOTR.txt'
main_corpora_data_path = 'D:/Research/PythonProjects/CorpusData'
corpora_name = 'eng_corpora_ABC'
start_time = time.perf_counter()
info_path = os.path.join(main_corpora_data_path, corpora_name + '_info.csv')
dict_path = os.path.join(main_corpora_data_path, corpora_name + '_dict.csv')
n, sum_l, words_corpora = read_dict(info_path, dict_path)
F_counter = read_text(text_path)
L = sum(F_counter.values())
print(L)
unique_words = {}
# for key in F_counter:
    # print(key, F_counter[key], 'Unique' if key not in words_corpora else '')
print('n={0}, sum L={1}'.format(n, sum_l))
print("time elapsed", time.perf_counter()-start_time, "s")
