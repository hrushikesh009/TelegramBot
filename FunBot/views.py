import json
import os
import random

import requests
from django.db.models import Count
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from dotenv import load_dotenv

from .models import UserActivityTracker

load_dotenv()
#fetching the Telegram token form environment variable
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

button_id_dict = {
    'fat': 1,
    'stupid': 2,
    'dumb': 3
}

jokes = {
         'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                    """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
         'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                    """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
         'dumb':   ["""THis is fun""",
                    """THis isn't fun"""] 
    }

greets = ['Hello there!','Hi, how are you?',"Hey, what's up?",'Hii','Hello']
end_conversation = ['Bye','Goodbye','See you later']


def capture_click_stream(user_id,button_id,username=None):
    try:
        print(user_id,button_id,username)
        instance = UserActivityTracker(user_id=user_id,
                            username=username,
                            button_id = button_id)
        instance.save()
    except Exception as e:
        #logging the information
        print("Error Occured while capturing the data!")


def telegram_sendmessage(response_msg):
    """This Function is responsible for actually sending the message to the Telegram API"""
    post_message_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    status = requests.post(
        post_message_url, 
        headers={"Content-Type": "application/json"}, 
        data=response_msg)
    return status


def get_message_from_request(request):
    """
    Function extracts the useful information from the response conveyed by the Telegram Bot
    """
    received_message = {}
    decoded_request = json.loads(request.body.decode('utf-8'))
 
    if 'callback_query' in decoded_request:
        received_message = decoded_request['callback_query']['message']
        received_message['option_opted'] = decoded_request['callback_query']['data']
    elif 'message' in decoded_request:
        received_message = decoded_request['message']
    
    if 'username' in received_message['chat']:
        received_message['user'] = received_message['chat']['username']
    received_message['chat_id'] = received_message['chat']['id']
    
    return received_message


def send_greet_message(message):
    """
    Binds Greet Message
    """
    result_message = {}

    result_message['chat_id'] = message['chat_id']
    result_message['text'] = random.choice(greets)
    
    response_msg = json.dumps(result_message)
    telegram_sendmessage(response_msg)
    
    
def send_end_conversation(message):
    """
    Handles Conversation closure
    """
    result_message = {}

    result_message['chat_id'] = message['chat_id']
    result_message['text'] = random.choice(end_conversation)
    
    response_msg = json.dumps(result_message)
    telegram_sendmessage(response_msg)
    


def send_messages(message):
    """
    Handles random text message and the users input for the jokes requested.
    """
    result_message = {} 
    user_id = button_id = username = None
    # the response needs to contain just a chat_id and text field for  telegram to accept it
    user_id = message['chat_id']
    result_message['chat_id'] = user_id
    if 'option_opted' in message:
        result_message['text'] = random.choice(jokes[message['option_opted']])
        button_id = button_id_dict.get(message['option_opted'],None)

        if 'user' in message:
            username = message['user']
        
        capture_click_stream(user_id,button_id,username)

    else:
        result_message['text'] = "If you're interested in yo mama Jokes? Please Select any one of the below options!."
        result_message['reply_markup'] = {
            "inline_keyboard": [[
                {
                    "text": "fat",
                    "callback_data": "fat"
                },
                {
                    "text": "stupid",
                    "callback_data": "stupid"
                },{
                    "text": "dumb",
                    "callback_data": "dumb"
                }]
            ]
        }

    response_msg = json.dumps(result_message)
    telegram_sendmessage(response_msg)
    
    

class TelegramBotView(generic.View):

    # csrf_exempt is necessary because the request comes from the Telegram server.
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)


    # Post function to handle messages in whatever format they come
    def post(self, request, *args, **kwargs):
        message = get_message_from_request(request)
        if message['text'] in greets:
            send_greet_message(message)
            send_messages(message)
        elif message['text'] in end_conversation:
            send_end_conversation(message)
        else:
            send_messages(message)

        return HttpResponse()

class HomeView(ListView):
    template_name = 'index.html'
    context_object_name = 'usersactivity'
    queryset = UserActivityTracker.objects.values('user_id','username').annotate(clicks=Count('id'))

    
