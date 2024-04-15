import os
import re
import random
import pandas as pd
from tqdm import tqdm

def aug(size, filename):
        tempFile1 = open('./classifiers/modifiers/data/temp1.csv', 'w', encoding='UTF-8', newline='')
        tempFile2 = open('./classifiers/modifiers/data/temp2.csv', 'w', encoding='UTF-8', newline='')
        data = open('./classifiers/modifiers/data/data.csv', 'r', encoding='UTF-8', newline='')
        linesData = [l for l in data]

        for line in linesData:
                tempFile1.write(line)
        tempFile1.close()
        
        with open(filename, 'r', encoding='UTF-8', newline='') as rawInfile:
                linesRaw = [l for l in rawInfile]
                pex = []     # personal expressions
                n = []       # singular nouns
                # npl = []     # plural nouns
                # shnpl = []   # shortened plural nouns
                # mwn = []     # multiword nouns
                # mwexn = []   # multiword nominal expressions
                # en = []      # exaggerated nouns
                eex = []     # (exaggerated) expressions
                adj = []     # adjectives
                # eadj = []    # exaggerated adjectives
                # sha = []     # shortened adjectives
                shmex = []   # shortened (multiword) expressions
                # v = []       # infinitive verb
                
                for sent in linesRaw:
                        words = sent.split(' ')
                        for w in words:
                                slang = re.findall(r'\[.*<*>\]', w)
                                for s in slang:
                                        if '<pex>' in w:
                                                pex.append(s)
                                        if '<n>' in w:
                                                n.append(s)
                                        if '<eex>' in w:
                                                eex.append(s)
                                        if '<adj>' in w:
                                                adj.append(s)
                                        if '<shmex>' in w:
                                                shmex.append(s)

                # removing duplicates and empty objects
                pex = list(set(filter(None, pex)))
                n = list(set(filter(None, n)))
                eex = list(set(filter(None, eex))) 
                adj = list(set(filter(None, adj)))
                shmex = list(set(filter(None, shmex)))    
                
                newLines = [] 
                                
                with open('./classifiers/modifiers/data/data.csv', 'r', encoding='UTF-8', newline='') as rawInfile2:
                        next(rawInfile2) # skips initial line with headers
                        with open('./classifiers/modifiers/data/temp1.csv', 'a', encoding='UTF-8', newline='') as augOutfile:
                                lines = [l for l in rawInfile2]
                                print('\nAugmenting...')
                                message = 'Augmenting...'
                                progressbar = tqdm(total=size-1)
                                for x in range(size-1):
                                        for line in lines:
                                                words = line.split(' ')
                                                for word in words:
                                                        if '<pex>' in word:
                                                                R_pex = random.choice(pex)
                                                                if word.endswith('\n'):
                                                                        word = R_pex + ',slang\n'
                                                                else:
                                                                        word = R_pex
                                                        if '<n>' in word:
                                                                R_n = random.choice(n)
                                                                if word.endswith('\n'):
                                                                        word = R_n + ',slang\n'
                                                                else:
                                                                        word = R_n
                                                        if '<eex>' in word:
                                                                R_eex = random.choice(eex)
                                                                if word.endswith('\n'):
                                                                        word = R_eex + ',slang\n'
                                                                else:
                                                                        word = R_eex
                                                        if '<adj>' in word:
                                                                R_adj = random.choice(adj)
                                                                if word.endswith('\n'):
                                                                        word = R_adj + ',slang\n'
                                                                else:
                                                                        word = R_adj
                                                        if '<shmex>' in word:
                                                                R_shmex = random.choice(shmex)
                                                                if word.endswith('\n'):
                                                                        word = R_shmex + ',slang\n'
                                                                else:
                                                                        word = R_shmex
                                                        newLines.append(word)        
                                                                
                                        for newWord in newLines:
                                                spacedWord = newWord + ' '
                                                augOutfile.write(spacedWord)   
                                        progressbar.update()
                                progressbar.close()
                # removing initial whitespaces
                with open('./classifiers/modifiers/data/temp1.csv', 'r', encoding='UTF-8', newline='') as augInfile:
                        for x in augInfile:
                                tempFile2.write(x.lstrip(' '))
                
                df = pd.read_csv('./classifiers/modifiers/data/temp2.csv', sep=',')
                df.drop_duplicates(subset=None, inplace=True)
                df.to_csv('./classifiers/modifiers/data/augmented_data.csv', index=False)
                tempFile2.close()
        progressbar_str = str(progressbar)
        end = "\n"      
        os.remove('./classifiers/modifiers/data/temp1.csv')      
        os.remove('./classifiers/modifiers/data/temp2.csv')
        return message, progressbar_str, end
# aug(2, 'data.csv')

