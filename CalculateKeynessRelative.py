from collections import Counter
import os
import csv
import time
import re
import math


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
            values = [int(row[1]), float(row[2]), float(row[3]), int(row[4]), float(row[5]), float(row[6]),
                      float(row[7]), float(row[8])]
            word_dict[row[0]] = values
    return int(info[1]), int(info[2]), word_dict


def read_text(path):
    pattern = r"[^\w\s\-\']"
    file = open(path, 'r', encoding='utf-8')
    text = file.read()
    file.close()
    lower_case_text = text.lower()
    prepared_text = re.sub(pattern, '', lower_case_text)
    splitted_text = prepared_text.split()
    stripped_text = [el.strip('\'-') for el in splitted_text]
    non_empty_text = [el for el in stripped_text if el]
    F_counter = Counter(non_empty_text)
    return F_counter


def save_rang_result(path, counter):
    with open(path, 'w', newline='', encoding='utf-8') as rang_file:
        writer = csv.writer(rang_file)
        i = 1
        sumV = sum(counter.values())
        for key, value in counter.most_common():
            writer.writerow([i, key, value, value / sumV])
            i += 1


text_path = 'D:/Research/John Ronald Reuel Tolkien/LOTR_withoutContractions.txt'
main_corpora_data_path = 'D:/Research/PythonProjects/CorpusData'
corpora_name = 'eng_corpora'
useMinF = True
minF = 10
useMinf = False
minf = 2.0e-5
sumOfUsedOptions = int(1 if useMinF else 0) + int(1 if useMinf else 0)
if sumOfUsedOptions > 1:
    useMinF, useMinf = False, False
    print('You can use only one option. Program will use no option')
start_time = time.perf_counter()
info_path = os.path.join(main_corpora_data_path, corpora_name + '_info.csv')
dict_path = os.path.join(main_corpora_data_path, corpora_name + '_dict.csv')
print('loading dictionary...')
n, sum_L, words_corpora = read_dict(info_path, dict_path)
print('dictionary loaded')
print('loading text...')
F_counter = read_text(text_path)
print('text loaded')
F_filtered_counter = F_counter
Lt = sum(F_counter.values())
if useMinF:
    F_filtered_counter = Counter({k: v for k, v in F_counter.items() if v >= minF})
if useMinf:
    F_filtered_counter = Counter({k: v for k, v in F_counter.items() if v / Lt >= minf})
Lt = sum(F_filtered_counter.values())
f_counter = Counter({k: v / Lt for k, v in F_filtered_counter.most_common()})
unique_words = {word for word in f_counter if word not in words_corpora}
Lu = len(unique_words)
nc = n + 1
Lc = sum_L + Lu
words_corpora_corrected = {}
for key in f_counter:
    if key in unique_words:
        Fc = 1
        f = 0
        fc = 1 / (nc * Lu)
        fw = 0
        fwc = 1 / Lc
        ntc = 1
        sigmac = math.sqrt((1 - (1 / nc)) / nc) / Lc
        sigmawc = math.sqrt(((1 / Lu) - (1 / Lc)) / Lc)
    else:
        Fc = words_corpora[key][0]
        fc = (words_corpora[key][1] * n) / nc  # words_corpora[key][1]
        fwc = words_corpora[key][0] / Lc  # words_corpora[key][2]
        ntc = words_corpora[key][3]
        sigmac = math.sqrt((words_corpora[key][7] / nc) - (fc ** 2))
        sigmawc = math.sqrt((words_corpora[key][6] - (Fc ** 2) / Lc) / Lc)
    words_corpora_corrected[key] = [Fc, fc, fwc, ntc, sigmac, sigmawc]
rm1_counter = Counter({k: f * math.log10(nc/words_corpora_corrected[k][3]) for k, f in f_counter.items()})
rm2_counter = Counter({k: f / words_corpora_corrected[k][1] for k, f in f_counter.items()})
rm2w_counter = Counter({k: f / words_corpora_corrected[k][2] for k, f in f_counter.items()})
rm3_counter = Counter({k: (f - words_corpora_corrected[k][1]) / words_corpora_corrected[k][4]
                       for k, f in f_counter.items()})
rm3w_counter = Counter({k: (f - words_corpora_corrected[k][2]) / words_corpora_corrected[k][5]
                       for k, f in f_counter.items()})
rm4_counter = Counter({k: (f / words_corpora_corrected[k][1]) * math.log10(nc/words_corpora_corrected[k][3])
                       for k, f in f_counter.items()})
rm4w_counter = Counter({k: (f / words_corpora_corrected[k][2]) * math.log10(nc/words_corpora_corrected[k][3])
                       for k, f in f_counter.items()})
rm5_counter = Counter({k: ((f - words_corpora_corrected[k][1]) / words_corpora_corrected[k][4]) *
                          math.log10(nc/words_corpora_corrected[k][3]) for k, f in f_counter.items()})
rm5w_counter = Counter({k: ((f - words_corpora_corrected[k][2]) / words_corpora_corrected[k][5]) *
                          math.log10(nc/words_corpora_corrected[k][3]) for k, f in f_counter.items()})
current_path = os.path.dirname(os.path.abspath(__file__))
new_path = os.path.join(current_path, 'ResultRelativeMethod')
if not os.path.exists(new_path):
    os.makedirs(new_path)
save_rang_result(os.path.join(new_path, 'rm1.csv'), rm1_counter)
save_rang_result(os.path.join(new_path, 'rm2.csv'), rm2_counter)
save_rang_result(os.path.join(new_path, 'rm3.csv'), rm2w_counter)
save_rang_result(os.path.join(new_path, 'rm4.csv'), rm3_counter)
save_rang_result(os.path.join(new_path, 'rm5.csv'), rm3w_counter)
save_rang_result(os.path.join(new_path, 'rm6.csv'), rm4_counter)
save_rang_result(os.path.join(new_path, 'rm7.csv'), rm4w_counter)
save_rang_result(os.path.join(new_path, 'rm8.csv'), rm5_counter)
save_rang_result(os.path.join(new_path, 'rm9.csv'), rm5w_counter)
print('n={0}, sum L={1}'.format(nc, Lc))
print("time elapsed", time.perf_counter()-start_time, "s")
