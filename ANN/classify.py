# ----------------------------------------------------------------------
# This file when run will ask to be provided with a text. Upon recieving it the text will be classified by the ann
# as propaganda or non-propaganda. To run this file on must put "python -m ANN.classify" into the terminal, then 
# enter the text you wish to classify when prompted.
# ----------------------------------------------------------------------

import numpy as np
from evaluators.emotionEval import EmotionEval
from evaluators.Positive_Generalities_and_stereotypes.stereotypes import Stereotypes
from evaluators.Positive_Generalities_and_stereotypes.pos_gen import PosGen
from evaluators.riskWords.riskWords import RiskWords
from evaluators.riskWords.constants import EMOTIONAL_LANGUAGE, LOADED_LANGUAGE, BANDWAGON_LANGUAGE
from evaluators.riskWords.riskWordsLists import emotional_language, loaded_language, bandwagon_language

from .predict import classify

# Create instances of evaluators
emotionEvaluator = EmotionEval()
stereotypeEvaluator = Stereotypes()
posgenEvaluator = PosGen()
riskWords = RiskWords()

def compile_evaluations(file_path, evaluators):
    results = []
    for evaluator in evaluators:
        result = evaluator.evaluate(file_path)
        results.append(result)

    results.append(riskWords.evaluate(file_path, emotional_language, EMOTIONAL_LANGUAGE))
    results.append(riskWords.evaluate(file_path, loaded_language, LOADED_LANGUAGE))
    results.append(riskWords.evaluate(file_path, bandwagon_language, BANDWAGON_LANGUAGE))

    print(results)

    return np.array(results)

def process_text(text, evaluators):
    temp_file_path = "temp_text.txt"
    with open(temp_file_path, "w") as file:
        file.write(text)

    feature_vector = compile_evaluations(temp_file_path, evaluators)

    print(feature_vector.shape)

    np.save("feature_vector.npy", feature_vector)
    
def classifyText(text):
    
    evaluators = [emotionEvaluator, stereotypeEvaluator, posgenEvaluator]
    
    process_text(text, evaluators)
    classify()


if __name__ == "__main__":

    text = input("Please enter the text to be evaluated: ")
    
    evaluators = [emotionEvaluator, stereotypeEvaluator, posgenEvaluator]
    
    process_text(text, evaluators)
    classify()
    #y_pred = predict(feature_vector)
    #print("Doc prediction", y_pred)
