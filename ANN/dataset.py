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
    results = []
    for evaluator in evaluators:
        result = evaluator.evaluate(file_path)
        results.append(result)

    print("all except risk")

    results.append(riskWords.evaluate(file_path, emotional_language, EMOTIONAL_LANGUAGE))
    results.append(riskWords.evaluate(file_path, loaded_language, LOADED_LANGUAGE))
    results.append(riskWords.evaluate(file_path, bandwagon_language, BANDWAGON_LANGUAGE))

    return np.array(results)

def process_folder(folder_path, evaluators, label, start_index=0, batch_size=5):
    all_results = []
    labels = []
    folder_path = Path(folder_path)
    
    file_num = 0
    files_processed = 0
    for filepath in glob.glob(os.path.join(folder_path, '*.txt')):
        if files_processed >= batch_size:
            break
        if file_num >= start_index:
            results_vector = compile_evaluations(filepath, evaluators)
            all_results.append(results_vector)
            labels.append(label)
            files_processed += 1
        print(file_num)
        file_num += 1

    print(file_num)

    return all_results, labels, file_num

def load_existing_data(data_file, labels_file):
    if os.path.exists(data_file) and os.path.exists(labels_file):
        X = np.load(data_file, allow_pickle=True)
        y = np.load(labels_file, allow_pickle=True)
        return list(X), list(y)
    return [], []

def save_combined_data(X, y, data_file, labels_file):
    np.save(data_file, np.array(X))
    np.save(labels_file, np.array(y))

def retrieve_data():
    evaluators = [emotionEvaluator, stereotypeEvaluator, posgenEvaluator]

    print("retrieving data")

    fake_tweets_folder = 'DATA/Fake_tweets txt files'
    true_tweets_folder = 'DATA/True_tweets txt files'

    # Load the last processed index from the checkpoint file
    fake_checkpoint_file = 'fake_checkpoint.txt'
    true_checkpoint_file = 'true_checkpoint.txt'

    fake_start_index = 0
    true_start_index = 0

    if os.path.exists(fake_checkpoint_file):
        with open(fake_checkpoint_file, 'r') as f:
            fake_start_index = int(f.read())
    if os.path.exists(true_checkpoint_file):
        with open(true_checkpoint_file, 'r') as f:
            true_start_index = int(f.read())

    # Load existing data
    fake_data_file = 'DATA/fake_results.npy'
    fake_labels_file = 'DATA/fake_labels.npy'
    true_data_file = 'DATA/true_results.npy'
    true_labels_file = 'DATA/true_labels.npy'

    fake_results, fake_labels = load_existing_data(fake_data_file, fake_labels_file)
    true_results, true_labels = load_existing_data(true_data_file, true_labels_file)

    # Process fake tweets folder
    new_fake_results, new_fake_labels, fake_last_index = process_folder(fake_tweets_folder, evaluators, 1, fake_start_index)
    # Process true tweets folder
    new_true_results, new_true_labels, true_last_index = process_folder(true_tweets_folder, evaluators, 0, true_start_index)

    # Append new data to existing data
    fake_results.extend(new_fake_results)
    fake_labels.extend(new_fake_labels)
    true_results.extend(new_true_results)
    true_labels.extend(new_true_labels)

    # Save the current index to the checkpoint file for each folder
    with open(fake_checkpoint_file, 'w') as f:
        f.write(str(fake_last_index))
    with open(true_checkpoint_file, 'w') as f:
        f.write(str(true_last_index))

    # Save combined data
    save_combined_data(fake_results, fake_labels, fake_data_file, fake_labels_file)
    save_combined_data(true_results, true_labels, true_data_file, true_labels_file)

    all_results_array = np.array(fake_results + true_results)
    y = np.array(fake_labels + true_labels)

    return all_results_array, y

def get_data_shuffled():
    X, y = retrieve_data()
    data = list(zip(X, y))
    np.random.shuffle(data)
    X_shuffled, y_shuffled = zip(*data)
    return np.array(X_shuffled), np.array(y_shuffled)

def get_data_sets():
    X, y = get_data_shuffled()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)
    return X_train, X_test, y_train, y_test

def save_data(X_train, X_test, y_train, y_test, folder_path='DATASETS'):
    os.makedirs(folder_path, exist_ok=True)

    print(f"X_train dimensions: {X_train.shape}")

    np.save(os.path.join(folder_path, 'X_train.npy'), X_train)
    np.save(os.path.join(folder_path, 'X_test.npy'), X_test)
    np.save(os.path.join(folder_path, 'y_train.npy'), y_train)
    np.save(os.path.join(folder_path, 'y_test.npy'), y_test)
    print(f"Data saved to {folder_path}")

def reset_start_index():
    fake_checkpoint_file = 'fake_checkpoint.txt'
    true_checkpoint_file = 'true_checkpoint.txt'
    
    if os.path.exists(fake_checkpoint_file):
        os.remove(fake_checkpoint_file)
        print(f"{fake_checkpoint_file} deleted.")
    if os.path.exists(true_checkpoint_file):
        os.remove(true_checkpoint_file)
        print(f"{true_checkpoint_file} deleted.")

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = get_data_sets()
    save_data(X_train, X_test, y_train, y_test)
    # Now `X_train`, `X_test`, `y_train`, `y_test` contain the data to use later for an ANN
