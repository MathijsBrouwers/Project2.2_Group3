

from pathlib import Path
import os
import numpy as np
import glob
from sklearn.model_selection import train_test_split

from evaluators.emotionEval import EmotionEval
from evaluators.Positive_Generalities_and_stereotypes.stereotypes import Stereotypes
from evaluators.Positive_Generalities_and_stereotypes.pos_gen import PosGen
from evaluators.riskWords.riskWords import RiskWords

from evaluators.riskWords.constants import EMOTIONAL_LANGUAGE
from evaluators.riskWords.constants import LOADED_LANGUAGE
from evaluators.riskWords.constants import BANDWAGON_LANGUAGE

from evaluators.riskWords.riskWordsLists import emotional_language
from evaluators.riskWords.riskWordsLists import loaded_language
from evaluators.riskWords.riskWordsLists import bandwagon_language




# Initialize evaluators
emotionEvaluator = EmotionEval()
stereotypeEvaluator = Stereotypes()
posgenEvaluator = PosGen()
riskWords = RiskWords()

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def compile_evaluations(file_path, evaluators):
    print("begin compilation")
    content = read_text_file(file_path)
    results = []
    for evaluator in evaluators:
        result = evaluator.evaluate(file_path)
        results.append(result)

    print("all except risk")

    results.append(riskWords.evaluate(file_path, emotional_language, EMOTIONAL_LANGUAGE))
    results.append(riskWords.evaluate(file_path, loaded_language, LOADED_LANGUAGE))
    results.append(riskWords.evaluate(file_path, bandwagon_language, BANDWAGON_LANGUAGE))

    return np.array(results)

def process_folder(folder_path, evaluators, label, max_files=1000):
    all_results = []
    labels = []
    folder_path = Path(folder_path)
    
    file_num = 0
    for filepath in glob.glob(os.path.join(folder_path, '*.txt')):
        if file_num>=max_files:
            break

        file_num+=1
        results_vector = compile_evaluations(filepath, evaluators)
        all_results.append(results_vector)
        labels.append(label)

    return all_results, labels

def retrieve_data():
    evaluators = [emotionEvaluator, stereotypeEvaluator, posgenEvaluator]

    print("retrieving data")

    fake_tweets_folder = 'DATA/Fake_tweets txt files'
    true_tweets_folder = 'DATA/True_tweets txt files'

    fake_results, fake_labels = process_folder(fake_tweets_folder, evaluators, 1)
    true_results, true_labels = process_folder(true_tweets_folder, evaluators, 0)

    all_results_array = np.array(fake_results + true_results)
    y = np.array(fake_labels + true_labels)

    #print("All Results Array:")
    #print(all_results_array)
    #print("Y Labels:")
    #print(y)
    
    return all_results_array, y

def get_data_shuffled():
    X, y = retrieve_data()
    data = list(zip(X, y))
    np.random.shuffle(data)
    X_shuffled, y_shuffled = zip(*data)
    return np.array(X_shuffled), np.array(y_shuffled)

def get_data_sets():
    X, y = get_data_shuffled()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=5)
    return X_train, X_test, y_train, y_test

def save_data(X_train, X_test, y_train, y_test, folder_path='DATASETS'):
    os.makedirs(folder_path, exist_ok=True)
    np.save(os.path.join(folder_path, 'X_train.npy'), X_train)
    np.save(os.path.join(folder_path, 'X_test.npy'), X_test)
    np.save(os.path.join(folder_path, 'y_train.npy'), y_train)
    np.save(os.path.join(folder_path, 'y_test.npy'), y_test)
    print(f"Data saved to {folder_path}")

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = get_data_sets()
    save_data(X_train, X_test, y_train, y_test)
    # Now `X_train`, `X_test`, `y_train`, `y_test` contain the data to use later for an ANN
