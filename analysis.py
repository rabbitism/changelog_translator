from os import path
import json
import re
import configurations.configurations as configurations
import string

current_path = path.dirname(__file__) 
def apriori(configs = None):
    if configs is None:
        configs = configurations.load_configs()
    dictionary = {}
    with open('changelogs/text/summary.txt', 'r', encoding='utf-16') as summary_file:
        contents = summary_file.readlines()
        for line in contents:
            words = line.split(" ")
            for word in words:
                key = word.strip().strip(string.punctuation)
                if key == "":
                    continue
                if any(char.isdigit() for char in key):
                    continue
                if key in dictionary.keys():
                    dictionary[key] += 1
                else:
                    dictionary[key] = 1
    sorted_list = sorted(dictionary.items(),key = lambda x:x[1],reverse = True)
    with open("results/frequency.json", "w", encoding='utf-8') as fp:
        json.dump(sorted_list , fp, ensure_ascii=False) 
    return sorted_list

def level_2_apriori(configs = None):
    if configs is None:
        configs = configurations.load_configs()
    sorted_list = apriori(configs)
    frequent_words = []
    for tup in sorted_list:
        if tup[1]>configs['level_1_threshold']:
            frequent_words.append(tup[0])
    print(frequent_words)
    level_2_dictionary = {}
    with open('changelogs/text/summary.txt', 'r', encoding='utf-16') as summary_file:
        contents = summary_file.readlines()
    level_2_candidates = []
    for word in frequent_words:
        for another_word in frequent_words[frequent_words.index(word)+1:]:
            level_2_candidates.append((word, another_word))
    for line in contents:
        words  = line.split(" ")
        for tup in level_2_candidates:
            if tup[0] in words and tup[1] in words:
                if tup in level_2_dictionary.keys():
                    level_2_dictionary[tup] += 1
                else:
                    level_2_dictionary[tup] = 1

    sorted_list = sorted(level_2_dictionary.items(),key = lambda x:x[1],reverse = True)
    with open("results/level_2_frequency.json", "w", encoding='utf-8') as fp:
        json.dump(sorted_list , fp, ensure_ascii = False)
    return sorted_list
                
def level_3_apriori(configs = None):
    if configs is None:
        configs = configurations.load_configs()
    level_2_sorted_list = level_2_apriori(configs)
    level_1_sorted_list = apriori(configs)
    level_1_frequent_words = []
    level_2_frequent_words = []
    for item in level_1_sorted_list:
        if item[1]>configs['level_1_threshold']:
            level_1_frequent_words.append(item[0])
    for item in level_2_sorted_list:
        if item[1]>configs['level_2_threshold']:
            level_2_frequent_words.append(item[0])
    print(level_1_frequent_words)
    print(level_2_frequent_words)
    level_3_candidates = []
    for tup in level_2_frequent_words:
        for word in level_1_frequent_words:
            if word in tup:
                continue
            else:
                key_list = [tup[0], tup[1], word]
                key_list.sort()
                key = tuple(key_list)
                if key not in level_3_candidates:
                    level_3_candidates.append(key)
    
    with open('changelogs/text/summary.txt', 'r', encoding='utf-16') as summary_file:
        contents = summary_file.readlines()

    level_3_dictionary = {}

    for line in contents:
        words = line.split(" ")
        for tup in level_3_candidates:
            if tup[0] in words and tup[1] in words and tup[2] in words:
                if tup in level_3_dictionary.keys():
                    level_3_dictionary[tup] += 1
                else:
                    level_3_dictionary[tup] = 1

    print(level_3_dictionary)

    sorted_list = sorted(level_3_dictionary.items(),key = lambda x:x[1],reverse = True)
    with open("results/level_3_frequency.json", "w", encoding='utf-8') as fp:
        json.dump(sorted_list , fp, ensure_ascii = False)
    return sorted_list

def level_4_apriori(configs = None):
    if configs is None:
        configs = configurations.load_configs()
    level_3_sorted_list = level_3_apriori(configs)
    level_1_sorted_list = apriori(configs)
    level_1_frequent_words = []
    level_3_frequent_words = []
    for item in level_1_sorted_list:
        if item[1]>configs['level_1_threshold']:
            level_1_frequent_words.append(item[0])
    for item in level_3_sorted_list:
        if item[1]>configs['level_3_threshold']:
            level_3_frequent_words.append(item[0])
    print(level_1_frequent_words)
    print(level_3_frequent_words)
    level_4_candidates = []
    for tup in level_3_frequent_words:
        for word in level_1_frequent_words:
            if word in tup:
                continue
            else:
                key_list = [tup[0], tup[1], tup[2], word]
                key_list.sort()
                key = tuple(key_list)
                if key not in level_4_candidates:
                    level_4_candidates.append(key)
    
    with open('changelogs/text/summary.txt', 'r', encoding='utf-16') as summary_file:
        contents = summary_file.readlines()

    level_4_dictionary = {}

    for line in contents:
        words = line.split(" ")
        for tup in level_4_candidates:
            if tup[0] in words and tup[1] in words and tup[2] in words and tup[3] in words:
                if tup in level_4_dictionary.keys():
                    level_4_dictionary[tup] += 1
                else:
                    level_4_dictionary[tup] = 1

    print(level_4_dictionary)

    sorted_list = sorted(level_4_dictionary.items(),key = lambda x:x[1],reverse = True)
    with open("results/level_4_frequency.json", "w", encoding='utf-8') as fp:
        json.dump(sorted_list , fp, ensure_ascii = False)
    return sorted_list


def check_trend():
    with open('changelogs/text/summary.txt', 'r', encoding='utf-16') as summary_file:
        contents = summary_file.readlines()
    dictionary = {}
    for line in contents:
        words = line.split(" ")
        if "from" in words:
            word = words[words.index("from")-1]
            if word in dictionary.keys():
                dictionary[word]+=1
            else:
                dictionary[word]=1
    sorted_list = sorted(dictionary.items(),key = lambda x:x[1],reverse = True)
    print(sorted_list)

if __name__ == "__main__":
    configs = configurations.load_configs()
    #level_4_apriori(configs)
    check_trend()
