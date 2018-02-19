from flask import Flask
from flask import render_template,jsonify,request
import requests
from models import *
import random

@app.route('/')
def hello_world():
    """
    Sample hello world
    """
    return render_template('home.html')

get_random_response = lambda intent:random.choice(response[intent])


@app.route('/chat',methods=["POST"])
def chat():
    """
    chat end point that performs NLU using rasa.ai
    and constructs response from response.py
    """
    try:
        response = requests.get("http://localhost:5000/parse",params={"q":request.form["text"]})
        response = response.json()
        intent = response["intent"]
        print intent
        entities = response["entities"]
        print entities
        if entities:
            entity_value = entities[0]["value"]
            print entity_value
        if intent["name"] == "ORDER_NUMBER":
            response_text = "Getting details of order number  " + entity_value
        elif intent["name"]== "greeting":
            response_text = "Hello,do you have a query or a problem?" #
        else:
            response_text = get_random_response(intent)
        return jsonify({"status":"success","response":response_text})
    except Exception as e:
        print e
        return jsonify({"status":"success","response":"Sorry I am not trained to do that yet..."})


app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8000)
