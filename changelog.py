from bs4 import BeautifulSoup
import requests
import json
import time

import configurations.configurations as configurations

def changelog_crawler(configs = None):
    if configs is None:
        configs = configurations.load_configs()
    versions = configs['versions']
    for version in versions:
        url = configs["wiki_url"]+version
        print(url)
        page_source = requests.get(url).text
        soup = BeautifulSoup(page_source,'html.parser')
        with open('changelogs/resource/'+version+'.html', 'w', encoding='utf-16') as page_file:
            page_file.writelines(soup.prettify())
            time.sleep(5)
            page_file.close()

def changelog_parser(configs = None):
    if configs is None:
        configs = configurations.load_configs()
    versions = configs['versions']
    print("Start to parser changelogs")
    for version in versions:
        print("Start to parser version " + version + " changelogs.")
        with open('changelogs/resource/'+version+'.html', 'r', encoding='utf-16') as page_file:
            page_content = page_file.read()
            soup = BeautifulSoup(page_content, 'html.parser')
            page_file.close()
        with open('changelogs/text/'+version+'.txt', 'w', encoding='utf-16') as version_file:
            flag = True
            previous  = ""
            for line in soup.find_all(['h2', 'h3', 'li', 'a', 'dd', 'b', 'span']):

                if line.string is not None:
                    if line.string.strip() == 'Patches':
                        break
                    if line.string.strip() in ["[","edit","]"]:
                        continue
                    if flag == True and line.string.strip()!=previous:
                        version_file.writelines(line.string.strip().lower()+'\n')
                        previous = line.string.strip()
                else:
                    if len(line.contents) > 1:
                        string = ''
                        for content in line.contents:
                            if content.string is not None:
                                string += content.string.strip()
                        string = string.strip()
                        if string.strip() in ['[edit]']:
                            continue
                        else:
                            if string is not None and string != previous:
                                version_file.writelines(string.strip().lower()+'\n')
                                previous = string.strip()
            version_file.close()
        
def summary():
    configs = configurations.load_configs()
    versions = configs['versions']
    print("Combining changelogs.")
    with open('changelogs/text/summary.txt', 'w', encoding='utf-16') as summary_file:
        for version in versions:
            with open('changelogs/text/'+version+'.txt', 'r', encoding='utf-16') as version_file:
                contents = version_file.readlines()
                for line in contents:
                    if line != '\n':
                        summary_file.write(line)
                version_file.close()
        summary_file.close()


if __name__ == "__main__":
    #changelog_crawler()
    print("Crawling process has been omitted to reduce Dota2 Wiki website load.")
    changelog_parser()
    summary()