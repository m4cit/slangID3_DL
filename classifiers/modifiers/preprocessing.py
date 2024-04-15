from tqdm import tqdm
import os

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   

# removes unwanted type indicators
def pp(file):
    filename = os.path.basename(file)
    # filename = str(file).replace('./data/', '')
    filepath = './classifiers/modifiers/data/'
    
    if filename.startswith("token_data"):
        filename = "token_data.csv"
    if filename.startswith("augmented_"):
        filename = "data.csv"
        
    with open(file, 'r', encoding='UTF-8', newline='') as rawInfile:
        with open(filepath+"processed_"+filename, 'w', encoding='UTF-8', newline='') as tempOutfile:
            linesRaw = [l for l in rawInfile]
            
            print('\nProcessing...')
            message = 'Processing...'
            progressbar = tqdm(total=len(linesRaw)) 
            for line in linesRaw:
                tempOutfile.write(line.lower()
                                  .replace('<eex>', '')
                                  .replace('<en>', '')
                                  .replace('<eadj>', '')
                                  .replace('<mwexn>', '')
                                  .replace('<shmex>', '')
                                  .replace('<shnpl>', '')
                                  .replace('<sha>', '')
                                  .replace('<adj>', '')
                                  .replace('<v>', '')
                                  .replace('<mwn>', '')
                                  .replace('<n>', '')
                                  .replace('<npl>', '')
                                  .replace('<pex>', '')
                                  .replace('[', '')
                                  .replace(']', '')
                                  .replace('-', ' ')
                                  )
                progressbar.update()
            progressbar.close()
            progressbar_str = str(progressbar)
            end = "\n"
            print(color.BLUE,"\nprocessed_" + filename + " created successfully!",color.END)
            success = "\nprocessed_" + filename + " created successfully!"
    return message, progressbar_str, success, end 
# pp("./data/data.csv")

