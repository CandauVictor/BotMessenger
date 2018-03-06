# Librairies python nécessaires à l'implémentation du bot
import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAACwAiZCFtecBABJkMUHncJ2HE7FyJq8wnu0opviWnqwcZBKKBXamj7qVqOBOWeJBZAfrQ0ZBGabeVCcIzZAk5RmtEMV2VE7iDx4C6BgfGqdbb0p5NkbPZBmRZB1dYhJE4oYvGrvMB5bMIgJFg9z2SUtNYrhHWhc2mFIZBIegFo6EOQ4W7HLwUg0'
VERIFY_TOKEN = 'NndhUoefjdco83kcpdjdKFHZJCJOZD9183NC73BC082N']
bot = Bot(ACCESS_TOKEN)


# Nous recevrons les messages que Facebook envoie au bot à cet instant
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # Si la request n'est pas un "GET", c'est un POST et nous pouvons juste renvoyer un message à l'utilisateur
    else:
        # Récupère le message envoyé par l'utilisateur au bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # Facebook Messenger ID pour l'utilisateur de manière à savoir où renvoyer la réponse
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    # Si l'utilisateur envoie un GIF, une photo, vidéo ou tout message non-texte
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


# Choisit un message au hasard à envoyer à l'utilisateur
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!",
                        "We're greatful to know you :)","Hello Farah","Hello Victor"]
    # Envoie l'item choisi à l'utilisateur
    return random.choice(sample_responses)


# Utilise PyMessenger pour envoyer le message à l'utilisateur
def send_message(recipient_id, response):
    # Envoie à l'utilisateur le message texte
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    app.run()
