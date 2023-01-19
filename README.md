# Whatsapp-GPT-Dalle-Bot
A WhatsApp bot built using Flask, Celery and WhatsApp Business API, powered by GPT-3 and DALL-E. This bot allows for natural language conversational interaction and can assist with tasks such as answering questions, providing information, and completing tasks.

## Installation
1. Clone this repository by running git clone https://github.com/yourusername/whatsapp-gpt-dalle-bot.git
2. Install the required dependencies by running pip install -r requirements.txt
3. Set up a Meta Business account and obtain a WhatsApp Business API account
4. Fill in the .env.example file with your Twilio account SID, auth token, WhatsApp Business API account credentials, and rename it to .env
5. Run celery -A app.celery worker --loglevel=info to start celery worker and flask run to start the server

## Usage
Once the server and worker are running, you can interact with the bot by sending messages to the WhatsApp Business API number. The bot will respond to your messages and complete tasks as specified.

## Customization
You can customize the bots functionality by editing the app.py file. For example, you can add new commands or change the way the bot responds to certain inputs.

## Disclaimer
This bot is for educational and demonstration purposes only and should not be used for any production purposes. The developers of this bot are not responsible for any damages or losses caused by its use.

## Support
If you have any issues or questions, please open an issue on this repository or contact the developers at [email].

## Contributing
If you would like to contribute to this project, please fork this repository and make your changes. Once you are ready, please submit a pull request for review.