from flask import Flask, request, jsonify

app = Flask(__name__) # creates a Flask application instance

@app.route('/api/data', methods=['POST']) # decorator defines a route (/api/data) that listens for POST requests.
# when a POST request is made to this URL, the receive_data function is called
def receive_data():
    data = request.json #access incoming request data
    # Process the data or perform actions
    response = {"message": "Data received", "data": data} # creates a response dictionary containing a message and the received data
    return jsonify(response) # Convert Python dictionaries to JSON format for responses

if __name__ == '__main__': # ensures the Flask app runs only if the script is executed directly, not when imported as a module
    app.run(debug=True)
