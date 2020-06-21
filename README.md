# ChatBot
This bot is fed with some predefined questions and answers, also it builds some answers over the time as the user responses increase.
ChatterBot module desing is language independent. The chatterbot has a mchine learning nature. 

Chatterbot is a machine learning library in Python which is used to create software that can engage in conversation. An untrained instance of ChatterBot starts off with no knowledge of how to communicate. Each time a user enters a statement, the library saves the text that they entered and the text that the statement was in response to. As ChatterBot receives more input the number of responses that it can reply and the accuracy of each response in relation to the input statement increase. The program selects the closest matching response by searching for the closest matching known statement that matches the input, it then chooses a response from the selection of known responses to that statement.

What all does chatterbot need?
It needs a name, a few adapters from the built in adapter class, and a conversation to get it started. 
ChatterBot uses adapter modules to control the behavior of specific types of tasks. There are four distinct types of adapters that ChatterBot uses, these are storage adapters, input adapters, output adapters and logic adapters.

Adapters types
1. Storage adapters - Provide an interface for ChatterBot to connect to various storage systems such as MongoDB, MySQL, etc. or local file storage.
2. Input adapters - Provide methods that allow ChatterBot to get input from a defined data source.
3. Output adapters - Provide methods that allow ChatterBot to return a response to a defined data source.
4. Logic adapters - Define the logic that ChatterBot uses to respond to input it receives.
ADAPTERS: 
Storage adapter: Allows to connect to different types of databases. By default is SQLite. 
Input and Output adapters: The input adapter reads the user's input from Terminal and the output terminal adapter prints the response. 
Logic Adapter: Is a class that takes an input statement and returns a response to that statement. Example of adapters: MathematicalEvaluation adapter(solves basic math problems), TimeLogicAdapter( returns current time)
The Chatterbot module has a class named Chatbot which has framework of function for getting response, generating response, training the Chatbot, learning response etc. 
Getting a response: Write into the abstract function of get_response to parse the input statement and send it to the generate_response function to generate an appropriate response to it. 
Training: Training a chatbot can be done in multiple ways. 
You can give examples of questions and answers in the bot.train parameters where it understands that the first statement is the  question and the second one is the response to it.
Can create a text file with questions and answers in series , create a YML file with questions and answers or give it access to an online database with knowledge base like twitter posts of people. 


The Chatbot learns responses when it is returned. It remembers the response it gave to questions and improves over time. This learning feature can be disabled by putting the bot in a read only mode. 
So how does the learning happen? 
There is a function called learn_respone where when the response is given by the bot, the response and the question in response to are saved and sent to another function called add_response. 
Add_response Adds the response to the list of statements that this statement is in response to.        If the response is already in the list, increment the occurrence count of that response. Another  function get_response_count keeps a count of the number of times the statement has been used as a response to the current statement. 
Preprocessors: 
ChatterBot’s preprocessors are simple functions that modify the input statement that a chat bot receives before the statement gets processed by the logic adaper. 
The preprocessors can be used to clean whitespace, convert to asci, etc. 
Preprocessor has been created to convert escaped html characters into unescaped. Like “&lt”, “<b>”

The MultiLogicAdapter is used to select a single response from the responses returned by all of the logic adapters that the chat bot has been configured to use. Each response returned by the logic adapters includes a confidence score that indicates the likeliness that the returned statement is a valid response to the input.
Response selection
The MultiLogicAdapter will return the response statement that has the greatest confidence score. The only exception to this is a case where multiple logic adapters return the same statement and therefore agree on that response.

The more the Chatbot is run the more the confidence of a specific  answer to a question increases and the it returns the greatest confidence value for a statement that occurs multiple times in the set of options. 
A typical logic adapter designed to return a response to an input statement will use two main steps to do this. The first step involves searching the database for a known statement that matches or closely matches the input statement. Once a match is selected, the second step involves selecting a known response to the selected match. Frequently, there will be a number of existing statements that are responses to the known match.

Selection of response or response selection methods determine which response should be used in the event where multiple responses are generated within a logic adapter. 
It can be set to get the first response, get most frequent response, get random response, etc. 
Our chatbot is set to get_most_frequent_response, the default is get_first_response.
 
