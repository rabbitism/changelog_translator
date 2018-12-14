from os import path
import math
import json
import re
import configurations.configurations as configurations
import string

def extract():
    with open('changelogs/text/summary.txt', 'r', encoding='utf-16') as summary_file:
        contents = summary_file.readlines()
    
    with open('results/changes.txt', 'w', encoding='utf-16') as change_file:
        for line in contents:
            if 'from' in line and 'to' in line:
                change_file.write(line)

def standard_translate(word:str):
    with open('resource/proper_names.json', 'r', encoding='utf-8') as proper_names:
        contents = json.loads(proper_names.read())
    with open('results/english.json', 'r', encoding='utf-8') as english_dict:
        english_dictionary = json.loads(english_dict.read())
    with open('results/chinese.json', 'r', encoding='utf-8') as chinese_dict:
        chinese_dictionary = json.loads(chinese_dict.read())
    words = []
    words_lower = []
    for key in contents.keys():
        words.extend(contents[key])
    for word in words:
        words_lower.append(word.lower())
    print(words_lower)
    if word in words_lower:
        for key,value in english_dictionary.items():
            if value.lower() == word:
                if key in chinese_dictionary.keys():
                #current_key = key
                    return chinese_dictionary[key]
                else: return ""
    else:
        return ""

def translate(word:str):
    if word == "":
        return "",0
    with open('results/english.json', 'r', encoding='utf-8') as english_dict:
        english_dictionary = json.loads(english_dict.read())
    with open('results/chinese.json', 'r', encoding='utf-8') as chinese_dict:
        chinese_dictionary = json.loads(chinese_dict.read())
    candidate_keys = []
    for key, value in english_dictionary.items():
        if word.strip().lower() in value.lower():
            candidate_keys.append(key)
    candidate_translations= []
    for key in candidate_keys:
        try:
            candidate_translations.append(chinese_dictionary[key])
        except:
            continue
    #print(candidate_translations)
    translation, max = find(candidate_translations)
    return translation, max

def find(translations:list):
    frequency = configurations.load_configs()['frequency']
    dictionary = {}
    for line in translations:
        sub_dict = {}
        for character in line:
            if (not character.isalnum()) or (character.lower() in "abcdefghijklmnopqrstuvwxyz"):
                continue
            else:
                if character in sub_dict.keys():
                    sub_dict[character]+=1
                else:
                    sub_dict[character]=1
        for word in sub_dict.keys():
            if word in dictionary.keys():
                dictionary[word]+=sub_dict[word]/len(line)
            else:
                dictionary[word]=sub_dict[word]/len(line)
    sorted_list = sorted(dictionary.items(),key = lambda x:x[1],reverse = True)
    frequent_words = {}
    frequent_characters = []
    for i in range(0,min(frequency,len(sorted_list))):
        frequent_words[sorted_list[i][0]]=sorted_list[i][1]
        frequent_characters.append(sorted_list[i][0])
    #print(frequent_characters)
    flag = frequency
    candidates = frequent_characters
    while flag > 0:
        candidates = create_candidates(candidates, frequent_characters)
        candidate_counter = {}
        for candidate in candidates:
            candidate_counter[candidate]=0
            for line in translations:
                if candidate in line:
                    candidate_counter[candidate]+=1/len(line)
        candidates = []
        sorted_list = sorted(candidate_counter.items(),key = lambda x:x[1],reverse = True)
        for i in range(0,min(frequency,len(sorted_list))):
            if sorted_list[i][1]>0:
                frequent_words[sorted_list[i][0]]=sorted_list[i][1]
                candidates.append(sorted_list[i][0])
        flag-=1
    #print(frequent_words)
    max = 0
    max_word = ""
    for key,value in frequent_words.items():
        if key in '的1234567890':
            continue
        else:
            if value*len(key)> max:
                max_word = key
                max = value*len(key)
    #print("result: ", max_word, max)
    return max_word, max

def create_candidates(strings:list, characters:list):
    result = []
    for string in strings:
        for character in characters:
            result.append(string+character)
    return result
        
def translate_line(line:string):
    words = line.split(" ")
    current_string = ""
    result = ""
    for word in words:
        number_flag = False
        for character in word:
            if character in "1234567890":
                number_flag = True
        #if word.strip(string.punctuation).strip('/').isnumeric():
        if number_flag==True:
            result += translate(current_string)[0]
            current_string = ""
            result += word
        else:
            #print("NO")
            if translate(current_string)[1]>0 and translate(current_string+ " " + word)[1]==0:
                result += translate(current_string)[0]
                current_string = word
            else:
                current_string = current_string + " " + word
    result += translate(current_string)[0]
    return result

if __name__ == "__main__":
    #extract()
    #standard_translate("Axe")
    #print(translate_line("spell shield magic reduction"))
    print(translate("strength gain"))
    print(translate_line("strength gain"))