# THIS BY ITSELF IS NOT A GOOD PROPAGANDA DETECTOR, it tries to detect stereotypes by checking through commonly used steretype wordss and sentiment analysis of words
#then checks if the words are close to entities if they are it would increase the score. the score is from 0 to 1, 0 meaning no stereotypes and 1 a lot



# anyway you can run this by using the run method, which needs an input of a txt file and returns a score of 0-1 for that txt file 0 meaning no postive generalites 1 alot. 


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import spacy

nlp = spacy.load('en_core_web_sm')
def function(x):# tries to change the representation of the ratio a bit to a bit more significant, might want to change this into smth better
    return x * (2 - x)

def tokenize(file_path): # takes txt files and tokenizes the tweet, using some basic preporcessing techniques and spacy lemmatizes the text
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            contents = file.read()
            
           
            contents = contents.lower()
            contents = re.sub(r'http\S+|www\S+|https\S+', '', contents, flags=re.MULTILINE)
            contents = re.sub(r'#\w+', '', contents)
    
            
            doc = nlp(contents)
            
    
            cleaned_words = [
                token.lemma_ for token in doc 
                if not token.is_stop and not token.is_punct and not token.like_num and token.is_alpha
            ]
            return cleaned_words

    except FileNotFoundError:
        print('File not found error')
        return None
    
def detect_stereotypes(tokens):
    stereotypes = ["lazy", "violent", "aggressive", "dumb", "criminal", "thug", "terrorist", "greedy", "untrustworthy", "ignorant", "savage", "uncivilized", "backward", "inferior", "exotic", "submissive", "promiscuous", "oppressed", "primitive", "barbaric", "dangerous", "unclean", "fanatical", "militant", "radical", "illegal", "alien", "parasite", "menace", "welfare queen", "trailer trash", "gang member", "thief", "druggie", "jihadist"]
    detected_stereotypes = []

    sentiment_analyzer = SentimentIntensityAnalyzer()  # Initialize sentiment analyzer

    for i, token in enumerate(tokens):
        if token in stereotypes:
            # Check if the stereotype word is close to entities, the idea being that if the word is found clsoe to an entity the chance of if being a steretype is higher. 
            #need to experiment with the range I look through 
            for entity in nlp(" ".join(tokens[max(0, i - 4): min(i + 5, len(tokens))])).ents:
                if entity.label_ in ["PERSON", "NORP", "ORG"]:
                    detected_stereotypes.append((token, entity.text, "Entity"))
                    break  

        else:
         
            token_sentiment = sentiment_analyzer.polarity_scores(token)
            if token_sentiment['compound'] < -0.6: #might have to adjust this value 
                entity_found = False
                for entity in nlp(" ".join(tokens[max(0, i - 4): min(i + 5, len(tokens))])).ents:
                    if entity.label_ in ["PERSON", "NORP", "ORG"]:
                        detected_stereotypes.append((token, entity.text, "Entity"))
                        entity_found = True
                        break  
               
                if not entity_found:
                    detected_stereotypes.append((token, "Negative sentiment", "Sentiment"))

    return detected_stereotypes

def calculate_stereotype_score(detected_stereotypes, tokens):
    #I give more value to the steretypes describing an entity as the likelihood the word is used in the contetx of being a steretype is higher.  
    entity_stereotype_weight = 1  # Weight for stereotypes found describing an entity
    non_entity_stereotype_weight = 0.5  # Weight for stereotypes found without entity

    total_entity_stereotypes = sum(1 for stereotype, context, context_type in detected_stereotypes if context_type == "Entity")
    total_non_entity_stereotypes = len(detected_stereotypes) - total_entity_stereotypes

    
    total_words = len(tokens)
    if total_words > 0:
        score = (total_entity_stereotypes * entity_stereotype_weight + total_non_entity_stereotypes * non_entity_stereotype_weight) / total_words
    else:
        score = 0  
    return function(score)

def run(file_path):
    tokens = tokenize(file_path)
    stereotypes= detect_stereotypes(tokens)
    score = calculate_stereotype_score(stereotypes,tokens)
    return score


