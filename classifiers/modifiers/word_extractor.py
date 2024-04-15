
tokenData = open('./data/token_data.csv', 'w', encoding='UTF-8', newline='')
tokenData.close()
with open('./data/data.csv', 'r', encoding='UTF-8', newline='') as infile:
    with open('./data/token_data.csv', 'a', encoding='UTF-8', newline='') as outfile:
        next(infile) # skips initial line with headers
        lines = [l for l in infile]
        clean = []
        words = []
        
        for i in lines:
            words = i.split(' ')
            for w in words:
                clean.append(w.replace(',slang', '').replace(',formal', '').replace('\r\n', '').replace('\n', ''))
        clean = list(filter(None, clean))
        # print(clean)
        outfile.write('phrase,type\n')
        for w in list(clean):
            if w.startswith('['):
                w = w + ',slang\n'    
            if w.startswith('[') == False:    
                w  = w + ',formal\n'
            outfile.write(w)
        
        