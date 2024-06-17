from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.data.decode('utf-8')  # Decode the raw data as UTF-8
    # Process the data or perform actions
    response = {"message": "Received text:", "data": data}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)













#
# import sys
# import os
# from flask import Flask, request, jsonify
#
# # Ensure the parent directory of 'evaluators' is in the Python path
# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
#
# from evaluators.riskWords.riskWords import RiskWordsEvaluator
# from evaluators.emotionEval import EmotionalEvaluator
# from evaluators.Positive_Generalities_and_stereotypes.pos_gen import PositiveGeneralitiesEvaluator
# from evaluators.Positive_Generalities_and_stereotypes.stereotypes import StereotypesEvaluator
#
# app = Flask(__name__)
#
# # Instantiate the evaluators
# risk_word_evaluator = RiskWordsEvaluator()
# emotional_evaluator = EmotionalEvaluator()
# positive_generalities_evaluator = PositiveGeneralitiesEvaluator()
# stereotypes_evaluator = StereotypesEvaluator()
#
# @app.route('/api/data', methods=['POST'])
# def receive_data():
#     # Receive text data from the POST request
#     data = request.data.decode('utf-8')
#
#     # Call each evaluator with the text data
#     risk_word_result = risk_word_evaluator.evaluate(data)
#     emotional_result = emotional_evaluator.evaluate(data)
#     positive_generalities_result = positive_generalities_evaluator.evaluate(data)
#     stereotypes_result = stereotypes_evaluator.evaluate(data)
#
#     # Construct the response JSON
#     response = {
#         "risk_word_result": risk_word_result,
#         "emotional_result": emotional_result,
#         "positive_generalities_result": positive_generalities_result,
#         "stereotypes_result": stereotypes_result
#     }
#
#     return jsonify(response)
#
# if __name__ == '__main__':
#     app.run(debug=True)