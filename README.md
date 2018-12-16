# DOTA2 Changelog translator

## Abstract

This is a tiny project for CS410 Text Information Systems @University of Illinois MCSDS

Author: DONG Bin

email: bindong2@illinois.edu

## Scope of Project

This project aims at translating DOTA2 version update changelogs from english into simplified Chinese. All translation mapping comes directly from in-game data. No external machine translation engine used.

## Development process

### 0. Environment

Environment: python 3.6.5

### 1. In-game data extraction and ETL

I am DOTA2 traditional Chinese group member and I have authority to download these files. You can also use [GCFScape](http://nemesis.thewavelength.net/index.php?p=25) and browser in DOTA2 game source file. You can download DOTA2 from [Steam](https://store.steampowered.com)

### 2. Dota2 Changelog extraction

There is no stable DOTA2 changelog from official websites, so I download from DOTA2 wiki, you can find all DOTA2 version in [DOTA2 Wiki](https://dota2.gamepedia.com/Game_Versions)

file changelog.py is used to download and extract changelogs. Notice that I have already downloaded these webpages in /changelogs/resource folder (which makes my project looks like a pure HTML project in github, but it's actually a python project). Please don't try to run commented changelog_crawler() function in changelog.py, it will add uncessary load to poor website. extracted pure text changelogs are in /changelogs/text .

### 3. Analysis

Third step is to identify what should be carefully treated. I used Apriori to identify frequenty combinations in changelogs. You can find implementation in analysis.py .

After analysis, I choose lines with "from" "to" "by" as sentences to translate.

### 4. Translate

There are two major problems to identify. What phrases to translate as a group, and what they should be translated.

The implementation is in file translation.py

## How to Use

This project is mostly done from scratch except for BeatutifulSoup4 for webpage parser. No other external packages or libraries are used.

copy paste the changelog you want to translate in file [file_to_translate.txt](file_to_translate.txt)
and run

```python
python main.py
```

please note encoding might be different on you computer and there are some messy encoding issue between unicode and utf-8. You might need to adjust while running the scripts.

## Strategy

Such small number of corpus is not enough to support the sentence structure mining in changelog, not saying that I don't have available translated changelog. So my project mainly focus on how to find the phrases frequently used in game and find their corresponding translations.

You can find the strategy in the introduction video at [YouTube](https://youtu.be/QuOVUQmn95A) or [Bilibili](https://www.bilibili.com/video/av38346676/).