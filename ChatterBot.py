#!/user/programfiles/python36/python
from __future__ import unicode_literals                         #Default import to use any feature from a later or upcoming release of Python has been backported into this version
import logging                                                  #for logging of conversation is system's format
import MySQLdb                                                  #for database
import os                                                       #for generating process ID or PID
import re                                                       #Regular Expression, to validate names with only letters and no numbers, and validate phone numbers for only digits and a plus sign or a hyphen
import time                                                     #to print logs of conversation with time formats
import datetime
from chatterbot import ChatBot                                  #importing the chatterbot module
from chatterbot.trainers import ChatterBotCorpusTrainer         #Corpus trainer for the chatbot - has inbuilt files for chats like greetings, movies, etc.
from chatterbot.trainers import ListTrainer                     #List Trainer for chatbot - to train the chatbot with custom chat files
from threading import Timer                                     #Thread module to start a thread to start a thread to check inactivity of the user
import winsound

class Chatbot:

    #For the conversation tones
    def bot_sound(self):
        winsound.PlaySound('Chat_Tone.wav', winsound.SND_ASYNC) #SND_ASYNC so that the windows play the sound and returns


    def chatbot(self):

        #logging of the conversation along with the date, time, and PID.
        logging.basicConfig(filename='example.log',level=logging.DEBUG,
        format='%(asctime)s | %(process)d %(name)s- %(message)s', datefmt="%Y-%m-%d %H:%M:%S", )

        #Connecting to MySQL, user - CUSTOMER
        db1 = MySQLdb.connect(host="localhost",user="test",passwd="testpassword")

        #Create / Open a doc file to keep logs of the Bot-User conversation
        chatFile = open('ChatLogsTry1.doc','a')

        #PID to assign to each conversation
        pid = os.getpid()
        #Date of the conversation
        date = datetime.datetime.now().strftime("%d-%m-%Y")
        #Start time of the conversation
        start_time= datetime.datetime.now().strftime("%I:%M:%S %p")
        stime=time.time()

        #creating a ChatterBot bot with the name Test, declaring that storage adapter will my sql and output format will be text
        bot=ChatBot("Test",
                    storage_adapter="chatterbot.storage.SQLStorageAdapter",
                    output_adapter="chatterbot.output.OutputAda"
                                   "pter",
                    output_format="text"
                    )

        #Setting  Corpus as the bot's trainer
        bot.set_trainer(ChatterBotCorpusTrainer)
        #training the bot with particular corpus files of yml format
        bot.train("chatterbot.corpus.custom.my")
        bot.train("chatterbot.corpus.custom.ques")
        bot.train("chatterbot.corpus.english")
        #bot.train("chatterbot.corpus.english.greetings")
        #bot.train("chatterbot.corpus.english.food")
        #bot.train("chatterbot.corpus.english.conversations")
        #bot.train("chatterbot.corpus.english.humor")
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

        #Creating a timer to check user's activity
        timeout = 200
        t = Timer(timeout, print, ['\nBot: Hello! It looks like you’ve been inactive for a while. Can we help you find anything?'])

        #List of words to sort user's queries as questions and problems/issues.
        list1=['no', 'No', 'NO', 'nah']
        list2=['yes', 'Yes', 'YES', 'ya', 'YA', 'Ya']
        list3=['not working', 'not working for me', 'still not working', 'not working at all','no, not working', 'no not working', 'no, still not working']
        list4=['no','nah', 'noo','no sorry', 'no not okay', 'no not ok', 'no, not okay', 'no, not ok', 'not giving', 'not okay', 'not ok', 'i dont want to give', 'NOT OKAY','NOT OK', 'Noo', 'cant provide', 'Cant provide', 'i dont want to provide', 'cant give', 'i am not giving','i dont know', 'i do not know', 'no you may not', 'you may not', 'no, you may not']
        req='How may I help you?'
        msg='Bot: Sorry, I did not get that. Could you reword your query again please?'
        exit_msg='Bot: It looks like you do not have any queries. Get back to us when you have one, we will be waiting for you! :)'
        line='_________________________________________________________________________'

        self.bot_sound()
        print('Bot: Hello')
        request = input('You: ')

        #bool variable
        val=True
        #variable to keep a count of the number of times user enters random junk as input
        i=0
        #setting the status of the ticket of the user generated as 'OPEN'
        status='CLOSED'

        #Drawing a line and writing date, time and pid into the log file
        chatFile.write('\n'+(line))
        chatFile.write('\n'+str(datetime.datetime.now().strftime("%d %B, %Y")))
        chatFile.write('\n'+str(start_time))
        chatFile.write('\nID: '+str(pid))

        #Taking details of the user to keep it in the database and using the details for generation of the ticket.
        self.bot_sound()
        print('Bot: If it’s okay with you, we’ll need to collect a little bit of additional information before we proceed')
        print('Bot: May I know your name?')
        name = input('You: ')
        #To check if the name is empty or has a set of spaces only
        while not name or name.isspace():
            self.bot_sound()
            print('Bot: Err! Seems like you have not entered anything. Please enter your name.')
            name = input('You: ')
        # To check if the user refuses to enter name with a negation
        while name in list4:
            self.bot_sound()
            print('Bot: May I please know your name? We need the details to answer your queries.')
            name = input('You:')
        #To check if the user enters numbers for the name field
        while bool(re.search(r'\d', name))== True:
            self.bot_sound()
            print('Bot: Err! Seems like its not in a valid form. Could you please type in your name again?')
            name = input('You: ')

        self.bot_sound()
        print('Bot: Your emailID? ')
        email = input('You: ')
        # To check if the user refuses to enter EMAILID with a negation
        while email in list4:
            self.bot_sound()
            print('Bot: May I please know your EmailID? We need the details to answer your queries.')
            email = input('You:')
        #To check if the email ID is in the right format with '@' and '.' symbol
        while not bool(re.match('.+\@.+\..+', email)):
            self.bot_sound()
            print("Bot: Err! seems like its not in a valid email form.. Could you type it again?")
            email = input('You: ')

        self.bot_sound()
        print('Bot: Your Phone number?')
        phno = input('You: ')
        #To check if phone number is only digits or contains a plus sign also
        while bool(re.match('[\d+]+$', phno)) == False:
            self.bot_sound()
            print('Bot: Err! Seems like its not in a valid form. Could you please type in your phone number again?')
            phno = input('You: ')
        #To check if the user has entered more than 15 digits
        while len(phno)>15:
            self.bot_sound()
            print('Bot: Err! Seems like you have entered more than 10 digits. Could you please type in your phone number again?')
            phno = input('You: ')

        chatFile.write('\nName: '+(name.title()))

        #Starting the timer
        t.start()

        #chatFile.write('\nUser:'+response)
        #Val - for making sure that once the inner while is exited, this while does not repeat
        #i value for making sure that if the user enters junk input more than 4 times, then the chatbot exits.
        while val == True:

            #If the user says questions
            #if True:
            self.bot_sound()
            print(('Bot: Hey, '+name+'. ').title() +req)    #To capitalize the first letter of the user's name
            chatFile.write('\nBot: '+req)

            while True :
                request = input('You: ')
                chatFile.write('\nUser: '+str(request))

                #Getting response to the user's input request
                response = bot.get_response(request)


                #The bot gives a response only if the confidence of the response is more than 0.5, otherwise the bot prompts the user to input more.
                if float(response.confidence)>0.5:
                   # time.sleep(0.2)
                    self.bot_sound()
                    print('Bot: ', response)
                    chatFile.write('\nBot: '+str(response))

                elif float(response.confidence)<0.5 and (request not in list1 and request not in list2 and request not in list3):
                    #time.sleep(0.3)
                    self.bot_sound()
                    val=True
                    i+=1
                    #When the user enters random input multiple times
                    if i<8:
                        print(msg)
                        chatFile.write('\nBot: '+msg)

                    else:
                        self.bot_sound()
                        print(exit_msg)
                        chatFile.write('\nBot: '+exit_msg)
                        time.sleep(0.3)
                        break
                #If the problem of the user persists
                if request in list3:
                    self.bot_sound()
                    print('Bot: Okay, I will mark your issue unresolved and our customer executive will get back to you soon.')
                    chatFile.write('\nBot: Okay, I will mark your issue unresolved and our customer executive will get back to you soon.')
                    status='OPEN'
                #When the user is done with asking questions and has no more to ask
                if request in list1:
                    self.bot_sound()
                    print('Bot: Thank you for visiting. Have a good day! ')
                    db1.commit()
                    time.sleep(1)
                    break
                #When the user says she/he has more questions to ask
                elif request in list2:
                    self.bot_sound()
                    print('Bot: '+req)
                    continue

            #Setting value FALSE so that the outer while loop does not repeat
            val=False


            #END TIME
            end_time= datetime.datetime.now().strftime("%I:%M:%S %p")
            etime = time.time()
            duration = round(etime - stime, 2)

            #Enter the TID, STATUS< NAME and PHONE NUMBER into the database
            cursor.execute("INSERT INTO CUSTOMER(TID, STATUS, NAME, EMAILID, PHONENUM, DATE, START_TIME, END_TIME, DURATION) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(pid, status, name, email, phno, date, start_time, end_time, duration))
            #Commit the values inserted
            db1.commit()

        chatFile.write('\nSTATUS: '+status)
        #Stopping the timer
        t.cancel()

#Calling the chatbot function of the chatbot class from main
Chatbot().chatbot()
