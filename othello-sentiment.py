import re
from textblob import TextBlob
import csv
from matplotlib import pyplot as plt
import numpy as np

# uncomment if running first time on a PC
# import nltk
# nltk.download('punkt')


othello_character_list = ['othello','desdemona','iago','michael cassio','emilia',
                        'roderigo','bianca','brabanzio','montano','lodvico','graziano','clown','duke of venice']

othello_scene_breakdown = {1: [1, 2, 3], 2:[1, 2, 3], 3:[1, 2, 3, 4], 4:[1, 2, 3], 5:[1, 2]}

def readFileDict(filename):
    fullList = []
    characterList = []
    char_list = []
    speech_list = []

    append = fullList.append

    with open(filename, 'r') as file:
        seq = ''
        for line in file:
            line = line.rstrip('\n').replace(' ', '#').replace('\t', '@').replace('\r', '@')
            if line.startswith('>'):
                line += ' '
                line = line.replace('>', ' >')
            append(line)
            seq = ''.join(fullList).lower()
            characterList = seq.split()

        for element in characterList:
            if '>' in element:
                element = element.replace('@', "")
                element = element.strip('>')
            char_list.append(element)
            
        speech_list = [x for x in characterList if '>' not in x]
        speech_list = list(map(str.lower, speech_list))

        for i in range(len(speech_list)):
            if '@' in speech_list[i]:
                speech_list[i] = speech_list[i].replace('@', ' ') 
            
            if ';' in speech_list[i]:
                speech_list[i] = speech_list[i].replace(';', '. ')

            if "'d" in speech_list[i]:
                speech_list[i] = speech_list[i].replace("'d", "ed") # corrrct 'old-english' to current for anaylsis
                 
            if '--' in speech_list[i]:
                speech_list[i] = speech_list[i].replace("--", " ")
                
            if '.' in speech_list[i]:
                speech_list[i] = speech_list[i].replace(".", ". ") # increase spacing for sentences
                
            if ',' in speech_list[i]:
                speech_list[i] = speech_list[i].replace(",", ", ") # increase spacing for commas
                
            if '?' in speech_list[i]:
                speech_list[i] = speech_list[i].replace("?", "? ") # increase spacing for ?'s

        # print(speech_list)
		# check that no duplicates in keys occur
        # print("duplicates: {0}".format([x for n, x in enumerate(char_list) if x in char_list[:n]]))
        char_speech_dict = dict(zip(char_list, speech_list)) # tuples of a pair's list and a dictionary {seq:gen}
        final_with_spaces_dict = addSpacestoSpeech(char_speech_dict)
    return final_with_spaces_dict, char_list

def addSpacestoSpeech(char_speech_dict):
    for key, value in char_speech_dict.items():
        if '#' in value:
            char_speech_dict[key] = value.replace('#', ' ')
    return char_speech_dict

def sortedSpeakingInOrder(given_list, deli_num):
    split_keys = [order.split('_') for order in given_list]
    sorted_lines = sorted(split_keys, key = lambda x: int(x[deli_num]))
    sorted_keys = ['_'.join(order) for order in sorted_lines]
    return sorted_keys

def determineSentiment(sent_dict):
    final_sent_dict = {}
    for speech in sent_dict:
        text_sent = TextBlob(sent_dict[speech])
        counter = 1
        for sentence in text_sent.sentences:
            final_sent_dict[speech + '_' + str(counter)] = (sentence.sentiment, sentence)
            counter += 1
    final_sent_dict['_average'] = text_sent.sentiment
    return final_sent_dict


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='flag format given as: -F <filename>')
    parser.add_argument('-F', '-filename', help='name of the .fasta file')
    parser.add_argument('-A', '-act', help='act to analyze')
    parser.add_argument('-S', '-scene', help='specific scene from act')
    parser.add_argument('-C', '-character', help='name of character to analyze')

    args = parser.parse_args()
    filename = args.F
    act_value = args.A
    scene_value = args.S
    character_value = args.C

    arguments = [filename]
    if None in arguments:
        if filename is None:
            print('File name not given')
            exit()

    if scene_value is not None and act_value is None:
        print('Scene needs to be given in association with specific act')
        exit()
    
    if act_value is not None:
        if type(act_value) is str:
            if act_value.lower() == 'one' or act_value == '1' or act_value.lower() == 'i':
                act_value = 1
            if act_value.lower() == 'two' or act_value == '2' or act_value.lower() == 'ii':
                act_value = 2
            if act_value.lower() == 'three' or act_value == '3' or act_value.lower() == 'iii':
                act_value = 3
            if act_value.lower() == 'four' or act_value == '4' or act_value.lower() == 'iv':
                act_value = 4
            if act_value.lower() == 'five' or act_value == '5' or act_value.lower() == 'v':
                act_value = 5
        else:
            print(act_value, 'is not a valid act, enter act value between 1 & 5')
            exit()

    if scene_value is not None:
        if type(scene_value) is str:
            if scene_value.lower() == 'one' or scene_value == '1' or scene_value.lower() == 'i':
                scene_value = 1
            elif scene_value.lower() == 'two' or scene_value == '2'  or scene_value.lower() == 'ii':
                scene_value = 2
            elif scene_value.lower() == 'three' or scene_value == '3' or scene_value.lower() == 'iii':
                scene_value = 3
            elif scene_value.lower() == 'four' or scene_value == '4' or scene_value.lower() == 'iv':
                scene_value = 4
            else:
                print('Scene must be between 1-4. {} is not a valid scene'.format(scene_value))
        else:
            print('scene must be between 1-4, {} is not a valid scene'.format(scene_value))

    if scene_value is not None and scene_value not in othello_scene_breakdown[act_value]:
        print('Act {} has {} scences, {} is not a valid scene'.format(act_value, max(othello_scene_breakdown[act_value]), scene_value))
    
    if character_value is not None:
        character_value = character_value.lower()
        if character_value not in othello_character_list:
            print(character_value, 'is not a valid character, try "other" for characters not listed')
            print('character list: ')
            for char in othello_character_list:
                print(char)
            exit()

    fileFastaRead = readFileDict(filename)
    char_speech_dict = fileFastaRead[0]
    ordered_headers_list = fileFastaRead[1]
    regex_total = ''
    if character_value is not None:
        if act_value is not None:
            if scene_value is not None:
                regex_total = re.compile(r'{0}{1}{2}_\d'.format(character_value, act_value, scene_value))            
            else:
                regex_total = re.compile(r'{0}{1}\d_\d'.format(character_value, act_value))
        else:
            regex_total = re.compile(r'{0}\d\d_\d'.format(character_value))
    else:
        if act_value is not None:
            if scene_value is not None:
                regex_total = re.compile(r'[a-z]+{0}{1}_\d'.format(act_value, scene_value))
            else:
                regex_total = re.compile(r'[a-z]+{0}\d_\d'.format(act_value))
        else:
            regex_total = re.compile(r'[a-z]+\d_\d')
    if character_value is not None and scene_value is not None and act_value is None:
        focus_dict = char_speech_dict
    else:
        focus_dict = {k:v for k, v in char_speech_dict.items() if bool(re.search(regex_total, k))}

    if len(focus_dict) == 0:
        print('character {} does not exist in this range'.format(character_value))
    
    if character_value is not None:
        sorted_speaking = sortedSpeakingInOrder(focus_dict.keys(), 1)

        sentiment_focus_dict = determineSentiment(focus_dict)

        sent_sentences_dict = {}

        lst_speaking = []
        total = []

        for speaking_num in sorted_speaking:
            for key, value in sentiment_focus_dict.items():
                regex_header = re.compile(r'{0}_\d+'.format(speaking_num))
                total.append(key)
                if bool(re.search(regex_header, key)):
                    lst_speaking.append(key)
                
            sent_sentences_dict[speaking_num] = lst_speaking
            lst_speaking = []
        
        for key, value in sent_sentences_dict.items():
            sorted_speaking_sentences = sortedSpeakingInOrder(value, 2)
            sent_sentences_dict[key] = sorted_speaking_sentences

    else:
        sorted_speaking = []
        for order_head in ordered_headers_list:
            if order_head in focus_dict:
                sorted_speaking.append(order_head)
        
        sentiment_focus_dict = determineSentiment(focus_dict)
        
        sent_sentences_dict = {}
        total = []
        lst_speaking = []
        for speaking_num in sorted_speaking:
            for key, value in sentiment_focus_dict.items():
                regex_header = re.compile(r'{}_\d+'.format(speaking_num))
                total.append(key)
                if bool(re.search(regex_header, key)):
                    lst_speaking.append(key)
            sent_sentences_dict[speaking_num] = lst_speaking
            lst_speaking = []

        for key, value in sent_sentences_dict.items():
            sorted_speaking_sentences = sortedSpeakingInOrder(value, 2)
            sent_sentences_dict[key] = sorted_speaking_sentences

    output_filename = 'OTHELLO_'
    if character_value is None:
        if act_value is None:
            output_filename += 'FULL.csv'
        else:
            if scene_value is None:
                output_filename += 'A{}.csv'.format(act_value)
            else:
                output_filename += 'A{}_S{}.csv'.format(act_value, scene_value)
    
    else:
        if act_value is None:
            output_filename += 'FULL_{}.csv'.format(character_value)
        else:
            if scene_value is None:
                output_filename += '{}_A{}.csv'.format(character_value, act_value)
            else:
                output_filename += '{}_A{}_S{}.csv'.format(character_value, act_value, scene_value)
    
    print(output_filename, end='\n\n')
    
    with open(output_filename, 'w+') as given_sent:
        fieldNames = ['id', 'speaker_header', 'polarity', 'subjectivity']
        writer = csv.DictWriter(given_sent, fieldnames = fieldNames)
        writer.writeheader()
        id_value = 1
        
        for overall_speech in sorted_speaking:
            for sentence in sent_sentences_dict[overall_speech]:
                polarity = sentiment_focus_dict[sentence][0].polarity
                subjectivity = sentiment_focus_dict[sentence][0].subjectivity
                # if polarity != 0.0 and subjectivity != 0.0:
                writer.writerow({'id': '{}'.format(id_value), 'speaker_header': sentence, 'polarity': '{}'.format(polarity), 'subjectivity': '{}'.format(subjectivity)})
                id_value += 1

                # if polarity == 0.0:
                #     updated_polarity = updateSentimentifNeutral(sentence, sentiment_focus_dict, sentiment_focus_dict[sentence][0])

    chart_title = ''
    if character_value is None:
        if act_value is None:
            chart_title = 'FULL Play'
        else:
            if scene_value is None:
                chart_title = 'Act {}'.format(act_value)
            else:
                chart_title = 'Act {} Scene {}'.format(act_value, scene_value)
    else:
        if act_value is None:
            chart_title = 'Full Play for {}'.format(character_value.title())
        else:
            if scene_value is None:
                chart_title = 'Act {} for {}'.format(act_value, character_value.title())
            else:
                chart_title = 'Act {} Scene {} for {}'.format(act_value, scene_value, character_value.title())
    
    line_stamp = []
    sent_polarity = []
    with open(output_filename) as results:
        reader = csv.DictReader(results, delimiter = ',')
        for row in reader:
            line_stamp.append(row['id'])
            sent_polarity.append(row['polarity'])
    
    overall_avg = [float(n) for n in sent_polarity if n != 0]
    overall_avg = sum(overall_avg)/len(overall_avg)
    print(overall_avg)

    plt.figure('Polarity over Time')
    plt.title(chart_title)
    plt.ylabel('Polarity [-1.0, 1.0]')
    # plt.yticks([-1.0, -0.75, -0.50, -0.25, 0.0, 0.25, 0.50, 0.75, 1.0])
    plt.xlabel('Lines')

    avg_line = [(float(a) + float(b))/2 for a, b in zip(sent_polarity[:],sent_polarity[1:])]
    avg_line.append((float(sent_polarity[-2]) + float(sent_polarity[-1]))/2)

    pos_pol = []
    neg_pol = []
    zer_pol = []
    print(sent_polarity, end = '\n\n')
    sent_polarity = list(map(float, sent_polarity))
    for value in sent_polarity:
        neg_pol.append(value if float(value) < 0 else np.nan)
        pos_pol.append(value if float(value) > 0 else np.nan)
        zer_pol.append(value if float(value) == 0 else np.nan)

    print(pos_pol)
    print()
    print(neg_pol)
    print()
    print(zer_pol)
    # for value in sent_polarity:
    #     if float(value) < 0:
    #         neg_pol.append(value)
    #         pos_pol.append(np.nan)
    #         zer_pol.append(np.nan)
    #     elif float(value) > 0:
    #         pos_pol.append(value)
    #         neg_pol.append(np.nan)
    #         zer_pol.append(np.nan)
    #     else:
    #         zer_pol.append(value)
    #         neg_pol.append(np.nan)
    #         pos_pol.append(np.nan)


    plt.plot(line_stamp, avg_line, color='k', linestyle=':')
    plt.scatter(line_stamp, pos_pol, color = 'r')
    plt.scatter(line_stamp, neg_pol, color = 'b')
    plt.scatter(line_stamp, zer_pol, color = '0.75')
    plt.savefig(chart_title+'.png')
    plt.show()

    
    # Image.open(chart_title).save(chart_title, 'JPEG')
