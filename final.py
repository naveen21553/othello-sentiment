
import random
import re
import csv
import string
import operator

from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import matplotlib.pyplot as plt
import numpy as np
import pickle
import re
import pandas as pd




othello_character_list = ['othello','desdemona','iago','michael cassio','emilia',
                        'roderigo','bianca','brabanzio','montano','lodvico','graziano','clown','duke of venice']

othello_scene_breakdown = {1: [1, 2, 3], 2:[1, 2, 3], 3:[1, 2, 3, 4], 4:[1, 2, 3], 5:[1, 2]}




def readingFileDict(filename):
    fullList = []
    characterList = []
    char_list = []
    speech_list = []

    append = fullList.append
    with open(filename, "r") as given_file:
        seq = ''
        for line in given_file:
            line = line.rstrip('\n').replace(" ", "#").replace("\t", "@").replace("\r", "@") # replace spaces with known character and replace tabs
            if line.startswith('>'):
                line = line + ' '
                line = line.replace('>', ' >')
            append(line)
        seq = ''.join(fullList).lower()
        characterList = seq.split()

        append = char_list.append 
        for element in characterList:
            if ">" in element:
                element = element.replace("@", "")
                element = element.strip(">") 
                append(element) 
        
        speech_list =  [x for x in characterList if '>' not in x]
        #speech_list = map(str.lower, speech_list) 
        
        for i in range(len(speech_list)):
            if '@' in speech_list[i]:
                new_value = speech_list[i].replace("@", " ") 
                speech_list[i] = new_value
            if ';' in speech_list[i]:
                new_value = speech_list[i].replace(";", ". ") 
                speech_list[i] = new_value
            if "'d" in speech_list[i]:
                new_value = speech_list[i].replace("'d", "ed")
                speech_list[i] = new_value
            if '--' in speech_list[i]:
                new_value = speech_list[i].replace("--", " ")
                speech_list[i] = new_value
            if '.' in speech_list[i]:
                new_value = speech_list[i].replace(".", ". ") 
                speech_list[i] = new_value
            if ',' in speech_list[i]:
                new_value = speech_list[i].replace(",", ", ") 
                speech_list[i] = new_value
            if '?' in speech_list[i]:
                new_value = speech_list[i].replace("?", "? ") 
                speech_list[i] = new_value


        char_speech_dict = seqDictPairs(char_list, speech_list) 
        final_with_spaces_dict = addSpacestoSpeech(char_speech_dict)
        #print(char_list)
        #print(final_with_spaces_dict)
        temp=[]
        for i in final_with_spaces_dict.keys():
                if "othello" in i:
                        #print final_with_spaces_dict[i]
                    temp.append(final_with_spaces_dict[i])
        file1 = open("my.txt","w")
        for i in temp:
                file1.writelines(i+"\n")
        #file1.writelines(temp)
        file1.close()
    return (final_with_spaces_dict, char_list)




def addSpacestoSpeech(char_speech_dict):
    for key in char_speech_dict:
        if "#" in char_speech_dict[key]:
            with_spaces = char_speech_dict[key].replace("#", " ")
            char_speech_dict[key] = with_spaces
    return char_speech_dict




def seqDictPairs(header_list, sequence_list):

    seq_gen_dict = {}
    seq_gen_dict = zip(header_list, sequence_list) 
    seq_gen_dict = dict(seq_gen_dict)
    return seq_gen_dict




def findMissingName(list_character, char_dict):
        # find headers that are not being included (debugging)
    missing_ch = []
    for key in char_dict:
        found = False
        for character_type in list_character:
            if character_type in key:
                found = True
                #print("found: {0} in {1}".format(key, character_type))
        if not found:
            missing_ch.append(key)
    if len(missing_ch) > 0:
        print("\nmissing")
        for ch in missing_ch:
            print("not found: {0}".format(ch))




def sortedSpeakingInOrder(given_list, deli_num):
    # return the list of speaking roles in order

    # order the keys in the order they appear in the play
    split_keys = [order.split('_') for order in given_list]
    # breaks hamlet51_1 => ['hamlet51', '1']
    sorted_lines = sorted(split_keys, key=lambda x:int(x[deli_num])) 
    # returns the list of character lines in order [['hamlet52', '1'], ['hamlet51, '2']]
    sorted_keys = ['_'.join(order) for order in sorted_lines]
    
    # returns to a single list: ['hamlet52_1', 'hamlet52_2'] in order
    return sorted_keys



def main():
	import argparse
	parser = argparse.ArgumentParser(description="flag format given as: -F <filename>")
	parser.add_argument('-F', '-filename', help="filename, given as .fasta")
	parser.add_argument('-A', '-act', help="act to analysis") # optional argument
	parser.add_argument('-S', '-scene', help="specific scene from act") # optional argument
	parser.add_argument('-C', '-character', help="character to analysis") # optional argument

	args = parser.parse_args()
	filename = args.F
	act_value = args.A 
	scene_value = args.S
	character_value = args.C 

	arguments = [filename]
	if None in arguments:
	    if filename is None:
	        print("filename not given")
	        exit()

	fileFastaRead = readingFileDict(filename)
	keys = list(fileFastaRead[0].keys())
	values = list(fileFastaRead[0].values())
	keys[0] = 'roderigo11_1'

	fileFastaRead[0]['roderigo11_1'] = fileFastaRead[0].pop('ï»¿>roderigo11_1tush,#never#tell#me;#i#take#it#much#unkindlythat#thou,#iago,#who#hast#had#my#purseas#if#the#strings#were#thine,#shouldst#know#of#this,--')

	temp = [re.findall(r'[\d]+', element) for element in keys]
	name = [re.findall(r'[^\d_]+', element) for element in keys]
	df = pd.DataFrame(temp, columns = ['scene+act', 'dialogue'])

	df['name'] = name
	df['name'] = df['name'].apply(np.squeeze)

	df['text'] = values
    
	to_drop = df[df['scene+act'].isnull()].index.values
	df = df.drop(labels = to_drop, axis = 0).reset_index(drop = True)

	to_drop = df[df['dialogue'].isnull()].index.values
	df = df.drop(labels = to_drop, axis = 0).reset_index(drop = True)

	df['scene+act'] = df['scene+act'].apply(int)
	df['dialogue'] = df['dialogue'].apply(int)
	df['sentiment'] = df['text'].apply(lambda x : TextBlob(x).sentiment.polarity)
	df.to_csv('final.csv', header = True, index = False)    

	mapper = {i:df.loc[i-1, :] for i in np.array(range(len(df)))[1:]}
	'''char_speech_dict = fileFastaRead[0] 
	ordered_headers_list = fileFastaRead[1]'''
	othello_index = df[df.name.str.match('othello', na = False)].index.values

	a = []
	for i in othello_index:
		a.append(df.loc[i-1, :])
		a.append(df.loc[i+1, :])

	final = pd.DataFrame(a)

	othello_char = {}
	for element in list(final.name.value_counts().keys()):
		othello_char[element] = sum(final[final.name == element]['sentiment'])
	print(othello_char)

main()