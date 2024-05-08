from openai import OpenAI
import re
from .abstractEvaluator import abstractEvaluator

api_key = ""
client = OpenAI(api_key=api_key)


class EmotionEval(abstractEvaluator): 
    """Class representing a person"""

    def callChat(self, text):

        article = open("evaluators\\TestArticle.txt","r").read()

        if text is None:
            text = article

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": ("The following texts you will recieve will be news articles that may or may not contain elements of propaganda within. "
                                                "For each text I would like you to extract and return exact sentences from the article that contain examples of "
                                                "emotionally charged language, please number each one. Emotionally charged language does not include examples of text that is only deciet "
                                                "or manipulation. If you do not find any such examples then say 'I found none'. Additionally please "
                                                "explain your reasoning for choosing each example.")},
                    {"role": "user", "content": text}], 
            stream=True, seed = 2, temperature = 0
        )
        with open("evaluators\\output.txt", "w") as file:
            for chunk in response:
                
                if chunk.choices[0].delta.content is not None:
                    #print(chunk.choices[0].delta.content, end="")
                    file.write(chunk.choices[0].delta.content)

            file.write("\n")
            
    def count_sentences(self, text):
        sentences = re.split(r'[.!?]', text)
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        return len(sentences)

    def count_examples(self):
        examples = 0
        with open("evaluators\\output.txt", 'r') as file:
            for line in file:
                if line.strip() == '':
                    examples += 1
        
        return examples


    def evaluate(self, text):

        self.callChat(text)
        totalSentences = self.count_sentences(text)
        exampleSentences = self.count_examples()
        return (exampleSentences/totalSentences)

