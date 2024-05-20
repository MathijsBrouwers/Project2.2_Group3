import numpy as np
from evaluators.emotionEval import EmotionEval


emotionEvaluator = EmotionEval()


def read_text_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def compile_evaluations(text, evaluators):
    results = []
    for evaluator in evaluators:
        result = evaluator(text)
        results.append(result)
    return np.array(results)

def main(file_paths):
    evaluators = [emotionEvaluator, evaluator2, evaluator3]
    all_results = []

    for file_path in file_paths:
        text = read_text_file(file_path)
        results_vector = compile_evaluations(text, evaluators)
        all_results.append(results_vector)
    
    all_results_array = np.array(all_results)
    
    print("All Results Array:")
    print(all_results_array)
    
    return all_results_array

if __name__ == "__main__":
    file_paths = ['input1.txt', 'input2.txt', 'input3.txt']  # List your text file paths here
    all_results_array = main(file_paths)
    # Now `all_results_array` contains the data to use later for an ANN
