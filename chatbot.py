#!/user/programfiles/python36/python
from __future__ import \
    unicode_literals  # Default import to use any feature from a later or upcoming release of Python has been backported into this version
#from http.server import BaseHTTPRequestHandler
#from wsgiref.simple_server import WSGIServer
import MySQLdb
import os
import re
import time
import datetime
import logging
from threading import Thread
from threading import Timer
from multiprocessing import process
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from flask import Flask
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import request
from flask import render_template
from flask import flash
from flask import jsonify
import winsound
import socketserver
from socketserver import ThreadingMixIn
from werkzeug.serving import run_simple


app = Flask(__name__)


#logging of the conversation along with the date, time, and PID.
logging.basicConfig(filename='example.log', level=logging.DEBUG,
                    format='%(asctime)s | %(process)d %(name)s- %(message)s', datefmt="%Y-%m-%d %H:%M:%S", )

#Connecting to MySQL, user - CUSTOMER
db1 = MySQLdb.connect(host="localhost", user="test", passwd="testpassword")

#Create / Open a doc file to keep logs of the Bot-User conversation
chatFile = open('C:/Users/Sahana/PycharmProjects/virtualenvir/my_app/ChatLogs.doc', 'a')

#PID to assign to each conversation
pid = os.getpid()

#Date of the conversation
date = datetime.datetime.now().strftime("%d-%m-%Y")

# Start time of the conversation
start_time = datetime.datetime.now().strftime("%I:%M:%S %p")
stime = time.time()

# creating a ChatterBot bot with the name Test, declaring that storage adapter will my sql and output format will be text
bot = ChatBot("Test",
              storage_adapter="chatterbot.storage.SQLStorageAdapter",
              output_adapter="chatterbot.output.OutputAda"
                             "pter",
              output_format="text"
              )

#Setting  Corpus as the bot's trainer
bot.set_trainer(ChatterBotCorpusTrainer)
#training the bot with particular corpus files of yml format
#bot.train("chatterbot.corpus.custom.my")
#bot.train("chatterbot.corpus.custom.ques")
#bot.train("chatterbot.corpus.english")
#bot.train("chatterbot.corpus.english.botprofile")
#bot.train("chatterbot.corpus.english.greetings")
#bot.train("chatterbot.corpus.english.food")
#bot.train("chatterbot.corpus.english.movies")
#bot.train("chatterbot.corpus.english.conversations")
#bot.train("chatterbot.corpus.english.emotion")
#bot.train("chatterbot.corpus.english.humor")
#bot.train("chatterbot.corpus.english.science")


#opening a textfile in read mode
#conv = open('chat.txt', 'r').readlines()
#Setting a list as the bot's trainer
#bot.set_trainer(ListTrainer)
#Training the bot with the chat file
#bot.train(conv)


#Creating a cursor to be able to execute multiple sql queries
cursor = db1.cursor()
#Executing SQL Queries with Cursor
#Selecting a particular database
cursor.execute('USE test_db;')

# Creating a timer to check user's activity
timeout = 500
t = Timer(timeout, print,
          ['\nBot: Hello! It looks like you’ve been inactive for a while. Can we help you find anything?'])

# List of words to sort user's queries as questions and problems/issues.
list1 = ['no', 'No', 'NO', 'nah', 'nope', 'Nope', 'NOPE', 'nop','no thanks', ' no thank you', 'nope, thanks', 'nah, thanks']
list2 = ['yes', 'Yes', 'YES', 'ya', 'YA', 'Ya', 'yes', 'yep', 'Yep', 'YEP']
list3 = ['not working', 'not working for me', 'still not working', 'not working at all', 'no, not working',
         'no not working', 'no, still not working', 'its not happening', 'not happening', 'its not working', 'its stopped working', 'its not working at all', 'its not responding']
list4 = ['no','hi', 'hello', 'ya' 'nah', 'noo', 'no sorry', 'no not okay', 'no not ok', 'no, not okay', 'no, not ok', 'not giving',
         'not okay', 'not ok', 'i dont want to give', 'I do not want to give', 'I do not wish to give', 'NOT OKAY', 'NOT OK', 'Noo', 'cant provide', 'Cant provide',
         'i dont want to provide', 'cant give', 'i am not giving', 'i dont know', 'i do not know', 'no you may not',
         'you may not', 'no, you may not', 'nope sorry', 'sorry', ' cant give', ' i cant give', "i can't give", 'wont give', ' i wont give', "I won't give"]
pattern = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '=', '+', '/', '.', ',', '<', '>', '?',';', ':', '{', '}', '[', ']','~', '`']
req = 'How may I help you?'
msg = 'Sorry, I did not get that. Could you reword your query again please?'
exit_msg = 'It looks like you do not have any queries. Get back to us when you have one, we will be waiting for you! :)'
line = '_________________________________________________________________________'
var_pattern = ['']

# Setting the status of the ticket of the user generated as 'OPEN'
status = 'CLOSED'


#Drawing a line and writing date, time and pid into the log file
chatFile.write('\n' + line)
chatFile.write('\n' + str(datetime.datetime.now().strftime("%d %B, %Y")))
chatFile.write('\n' + str(start_time))
chatFile.write('\nID: ' + str(pid))

k = 0
count = 0
name = ''
emailid = ''
phonenum = ''
i = 0


def sound():
    winsound.PlaySound('Chat_Tone.wav', winsound.SND_ASYNC)


def shutdown():
    global count, chatFile, k
    count = 0

    func = request.environ.get('werkzeug.server.shutdown')
    func()
    chatFile = open('ChatLogs.doc', 'a')
    # Drawing a line and writing date, time and pid into the log file
    chatFile.write('\n' + line)
    chatFile.write('\n' + str(datetime.datetime.now().strftime("%d %B, %Y")))
    chatFile.write('\n' + str(start_time))
    chatFile.write('\nID: ' + str(pid))
    k = 1

@app.route("/")
def home1():
    return render_template("get.html")


# Starting the timer
t.start()


@app.route("/name", methods=['POST'])
def name():
    message = (request.form['messageText'])
    global count, name, emailid, phonenum, i, status, chatFile, k
    while True:
        if k == 1:
            k += 1
            sound()
            return jsonify({'status': 'OK', 'answer': 'May I know your name?'})

        #FOR NAME
        if count == 0:
            name = message
            if not name or name.isspace():
                sound()
                return jsonify({'status': 'OK',
                                'answer': 'Err! Seems like you have not entered anything. Please enter your name.'})
            elif name in list4:
                sound()
                return jsonify({'status': 'OK',
                                'answer': 'May I know please know your name?'})
            elif bool(re.search(r'\d', name)) or bool(re.search(r'\W', name)):
                sound()
                return jsonify({'status': 'OK',
                                'answer': 'Err! Seems like its not in a valid form. Could you please type in your name again?'})
            else:
                count += 1
                chatFile.write('\nName: ' + name.title())
                sound()
                return jsonify({'status': 'OK', 'answer': 'Hi ' +name.title()+ ', May I know your email ID?'})


        #FOR EMAIL ID
        elif count == 1:
            emailid = message
            if emailid in list4:
                sound()
                return jsonify({'status': 'OK',
                                'answer': 'May I please know your email ID?'})
            #elif '@' and '.' not in emailid:
            elif not bool(re.match('.+\@.+\..+', emailid)):
                sound()
                return jsonify({'status': 'OK',
                                'answer': 'Err! seems like its not in a valid email form.. Could you type it again?'})
            else:
                count += 1
                sound()
                return jsonify({'status': 'OK', 'answer': 'May I know your phone number?'})


        #FOR PHONE NUMBER
        elif count == 2:
            phonenum = message
            if not bool(re.match('[\d+]+$', phonenum)):
                sound()
                return jsonify({'status': 'OK',
                                'answer': 'Err! Seems like its not in a valid phone number form. Could you please type in your phone number again?'})
            elif len(phonenum) > 15:
                sound()
                return jsonify({'status': 'OK',
                                'answer': 'Err! Seems like you have entered more than the valid digits. Could you please type in your phone number again?'})
            else:
                count += 1
                sound()
                return jsonify({'status': 'OK', 'answer': 'Thank you ' + (name.title()) + '. How may I help you?'})



        # FOR QUERY
        elif count == 3:
            chatFile.write('\nUser: ' + message)
            bot_response = (bot.get_response(message))


            # The bot gives a response only if the confidence of the response is more than 0.5, otherwise the bot prompts the user to input more.
            if float(bot_response.confidence) > 0.6:
                chatFile.write('\nBot: ' + str(bot_response))
                sound()
                bot_response = str(bot_response).replace(". ", ".<br /><br />")
                bot_response = str(bot_response).replace(":-", ":-<br /><br />")
                return jsonify({'status': 'OK', 'answer': (bot_response)})

            elif float(bot_response.confidence) < 0.6 and (
                    message not in list1 and message not in list2 and message not in list3):
                i += 1
                if i < 8:
                    chatFile.write('\nBot: ' + msg)
                    sound()
                    return jsonify({'status': 'OK', 'answer': msg})
                else:
                    chatFile.write('\nBot: ' + exit_msg)
                    sound()
                    return jsonify({'status': 'OK', 'answer': exit_msg})

            # If the problem persists
            if message in list3:
                chatFile.write(
                    '\nBot: Okay, I will mark your issue unresolved and our customer executive will get back to you soon.')
                status = 'OPEN'
                sound()
                return jsonify({'status': 'OK',
                                'answer': 'Okay, I will mark your issue unresolved and our customer executive will get back to you soon.'})


             # When the user has more questions to ask
            if message in list2:
                sound()
                return jsonify({'status': 'OK', 'answer': 'How may I help you?'})

            #When the user is done with asking questions and has no more to ask
            elif message in list1:
                # END TIME
                end_time = datetime.datetime.now().strftime("%I:%M:%S %p")
                etime = time.time()
                duration = round(etime - stime, 2)
                # Enter the TID, STATUS< NAME and PHONE NUMBER into the database
                cursor.execute(
                    "INSERT INTO CUSTOMER(TID, STATUS, NAME, EMAILID, PHONENUM, DATE, START_TIME, END_TIME, DURATION) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (pid, status, name, emailid, phonenum, date, start_time, end_time, duration))
                # Commit the values inserted
                db1.commit()
                chatFile.write('\nSTATUS: '+status)
                chatFile.close()
                count += 1
                sound()
                return jsonify({'status': 'redirection', 'answer': 'Thank you for visiting. Have a good day!'})


        else:
            shutdown()


while True:
    #port = 5000
    if __name__ == "__main__":
        #app.run(threaded=True)#, debug=True, host="localhost", port=port)
        #app.run(processes=3)
        app.run(host='192.168.0.1', port=5050, threaded=True, debug=True)
