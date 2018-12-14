import translate
import re

def main(line:str):
    words = line.split(" ")
    if "from" in words and "to" in words:
        result = limit(line)
    elif "by" in words:
        result = difference(line)
    else:
        result = other(line)
    return result


def limit(line:str):
    #print("limit")
    sections = re.match(r"(.*) from (.*) to (.*)",line)
    if sections is None:
        print(line, "Not translated")
        return ""
    else:
        pre_section = sections.group(1)
        from_section = sections.group(2)
        to_section = sections.group(3)
        trend, pre_section = check_trend(pre_section)
        pre_section_translation = translate.translate_line(pre_section)
        from_section_translation = translate.translate_line(from_section)
        to_section_translation = translate.translate_line(to_section)
        #print(pre_section_translation+"从"+from_section_translation+trend+"至"+to_section_translation)
        return pre_section_translation+"从"+from_section_translation+trend+"至"+to_section_translation
    

def difference(line:str):
    #print("difference")
    sections = re.match(r"(.*) by (.*)", line)
    if sections is None:
        print(line, "Not translated")
        return ""
    else:
        pre_section = sections.group(1)
        after_section = sections.group(2)
        trend, pre_section = check_trend(pre_section)
        pre_section_translation = translate.translate_line(pre_section)
        after_section_translation = translate.translate_line(after_section)
        #print(pre_section_translation+trend+after_section_translation)
        return pre_section_translation+trend+after_section_translation

def other(line:str):
    #result = translate.standard_translate(line)
    return "Not Translated"

def check_trend(line:str):
    dictionary = {
        "increas":"increase",
        "reduc":"decrease",
        "rescal":"balance",
        "decreas":"decrease",
        "chang":"balance",
        "improv":"increase",
        "balanc":"balance"
    }
    keyword = ""
    trend = ""
    for key,value in dictionary.items():
        if key in line:
            keyword = key
            trend = value
            break
    words = line.split(" ")
    result = ""
    for word in words:
        if keyword!= ""  and keyword in word:
            continue
        else:
            result += word+" "
    if trend == "increase":
        return "增加", result
    elif trend == "decrease":
        return "减少", result
    else:
        return "调整", result

if __name__ == "__main__":
    print(main("strength gain from 1 to 2"))
    
    with open('file_to_translate.txt', 'r', encoding='utf-8') as changelog:
        contents = changelog.readlines()
    with open('result.txt', 'w', encoding='utf-8') as result:
        for line in contents:
            if line.strip() is "":
                continue
            else:
                translation = main(line)
                if translation is not None:
                    print(line.strip())
                    print(translation)
                    result.write(line.strip()+'\n')
                    result.write(translation+'\n')
                else:
                    continue
    
