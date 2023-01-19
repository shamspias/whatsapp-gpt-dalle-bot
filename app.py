import os
import requests
import openai
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import cross_origin
from celery import Celery

app = Flask(__name__)

load_dotenv()

VERIFY_TOKEN = os.getenv('WHATSAPP_HOOK_TOKEN')

# Configure Celery here we use radis
app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL')
app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND')

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# GPT-3 endpoint and credentials
gpt3_endpoint = "https://api.openai.com/v1/engines/text-davinci-003/completions"
gpt3_api_key = os.getenv("OPEN_AI_KEY")
openai.api_key = gpt3_api_key


# @celery.task(serializer='json', name="send_message")
@celery.task
def send_normal_message(replay, phone_number):
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": phone_number,
        "text": {
            "body": replay,
        }
    })
    API_URL = os.getenv("GRAPH_API_URL")
    API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
    NUMBER_ID = os.getenv("WHATSAPP_NUMBER_ID")
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }
    API_URL = API_URL + NUMBER_ID

    response = requests.request("POST", f"{API_URL}/messages", headers=headers, data=payload)

    assert response.status_code == 200, jsonify({"error": "Error sending message"})

    return jsonify({"status": response.status_code})


@celery.task
def generate_text(prompt):
    # Send request to GPT-3
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {gpt3_api_key}"
    }
    data = {
        "prompt": prompt,
        "temperature": 0.5,
        "max_tokens": 128
    }
    response = requests.post(gpt3_endpoint, headers=headers, json=data)

    # Return response
    return response.json()


@celery.task
def generate_image(prompt, number, image_size, image_width):
    response = openai.Image.create(
        prompt=prompt,
        n=number,
        size=str(image_size) + "x" + str(image_width)
    )
    image_url = response['data']

    return image_url


@app.route('/pocketgod', methods=["POST", "GET"])
@cross_origin()
def chat():
    if request.method == "GET":
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Authentication failed. Invalid Token."

    # Get prompt from client
    prompt = request.json.get('prompt')

    if prompt.startwith("/image"):
        # Run GPT-3 task asynchronously
        task = generate_image.apply_async(args=(prompt, 1, 1027, 1027))
        response = generate_image.AsyncResult(task.id).get()
        status = send_normal_message(response["data"][0]["url"])
    else:
        # Run GPT-3 task asynchronously
        task = generate_text.apply_async(args=(prompt,))
        response = generate_text.AsyncResult(task.id).get()
        result = response['choices'][0]['text']
        status = send_normal_message(result)

    # Return task id
    return jsonify({'status': status})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
