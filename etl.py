from os import path
import os
import re
import json

def etl():
    current_path = path.dirname(__file__) 
    resource_path = current_path + "/resource"

    filenames = []
    for file in os.listdir(resource_path):
        filenames.append('resource/' + file)

    chinese_dictionary = {}
    english_dictionary = {}

    for filename in filenames:
        with open(filename, 'r', encoding='utf-16') as file_to_open:
            text = file_to_open.readlines()
            for line in text:
                m = re.match(r".*\"(\w+)\".*\"(.+)\".*", line)
                if m is not None:
                    #print(m.group(1), m.group(2))
                    if 'chinese' in filename:
                        chinese_dictionary[m.group(1)] = m.group(2)
                    if 'english' in filename:
                        english_dictionary[m.group(1)] = m.group(2)

    with open("results/chinese.json", "w", encoding='utf-8') as fp:
        json.dump(chinese_dictionary , fp, indent=2, ensure_ascii=False) 
    with open("results/english.json", "w") as fp:
        json.dump(english_dictionary , fp, indent=2) 

if __name__ == "__main__":
    etl()