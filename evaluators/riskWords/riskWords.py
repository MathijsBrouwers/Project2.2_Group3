import riskWordsLists
import string


##Takes as input .txt file and gives as output only the cleaned words in an array.
def tokenize(file_path):
    try:
        with open(file_path, 'r',encoding="utf-8") as file:
            contents = file.read()
            words = contents.split()
            translation_table = str.maketrans('','', string.punctuation)
            return [word.translate(translation_table).lower() for word in words]
    except FileNotFoundError:
        print('File not found error')
        return None
    

def get_ratio_of_risk_words(file_path, amount_of_risk_words):
    try:
        with open(file_path, 'r',encoding="utf-8") as file:
            contents = file.read()
            words = contents.split()
            translation_table = str.maketrans('','', string.punctuation)
            return amount_of_risk_words/len([word.translate(translation_table).lower() for word in words])
    except FileNotFoundError:
        print('File not found error')
        return None
    


def count_risk_words(cleaned_list, words):
    count = 0
    for word in cleaned_list:
        if word in words:
            count +=1
    return count      


##print(tokenize('evaluators\\riskWords\\testFile.txt'))

##print(tokenize('evaluators\\riskWords\\testFile.txt'))



amount_of_loaded_words =  count_risk_words(tokenize('evaluators\\riskWords\\testFile.txt'), riskWordsLists.loaded_language)
print('Amount of loaded words: ', amount_of_loaded_words)
print('This gives ratio: ', get_ratio_of_risk_words('evaluators\\riskWords\\testFile.txt', amount_of_loaded_words ))

print('Amount of emotional words: ', count_risk_words(tokenize('evaluators\\riskWords\\testFile.txt'), riskWordsLists.emotional_language))





