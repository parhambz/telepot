import telepot
import time
from pprint import pprint
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup , InlineKeyboardButton
import requests
import json
userList={}
serverUrl="http://87.236.214.182:8000"
class userClass:
    def __init__(self):
        self.chatId=0
        self.email = ""
        self.state = 0
        self.name=""
        self.lastName=""
        self.ticketTitle=""
        self.ticketBodey=""
        self.loginEmailTry=""
        self.loginPassTry=""

    def setEmail(self,email):
        self.email=email
    def getEmail(self):
        return self.email
        
    def setState(self,state):
        self.state=state
    def getState(self):
        return self.state
        
    def setName(self,name):
        self.name=name
    def getName(self):
        return self.name
        
    def setLastName(self,lastName):
        self.lastName=lastName
    def getLastName(self):
        return self.lastName
        
    def setChatId(self,chatId):
        self.chatId=chatId
    def getChatId(self):
        return self.chatId

    def setTicketTitle(self,ticketTitle):
        self.ticketTitle=ticketTitle
    def getTicketTitle(self):
        return self.ticketTitle

    def setTicketBodey(self,ticketBodey):
        self.ticketBodey=ticketBodey
    def getTicketBodey(self):
        return self.ticketBodey 

    def setLoginEmailTry(self,loginEmailTry):
        self.loginEmailTry=loginEmailTry
    def getLoginEmailTry(self):
        return self.loginEmailTry 
    
    def setLoginPassTry(self,loginPassTry):
        self.loginPassTry=loginPassTry
    def getLoginPassTry(self):
        return self.loginPassTry 
    
def isLogin(chatId):
    global userList
    if chatId in userList:
        return userList[chatId]
    return False


def login(user):
    email=user.getLoginEmailTry()
    password=user.getLoginPassTry()
    request=requests.post(serverUrl+"/book/",data={'action':'login','email':email,'password':password})
    if (request.text=="False"):
        userList.pop(user.getChatId())
        return False
    response=request.json()
    dict1 = response[0]
    dict2 = dict1['fields']
    user.setName(dict2['name'])
    user.setEmail(dict2['email'])
    user.setLastName(dict2['lastName'])
    return True
    
def showMenu(chatId,user):
    if user!=False:
        button2=InlineKeyboardButton(text="send ticket",callback_data=2)
        button1=InlineKeyboardButton(text="logout",callback_data=3)
        text="salam "+user.getName()+" "+user.getLastName()+" yeki az gozine haye zir ra vared konid"
        menu=InlineKeyboardMarkup(inline_keyboard=[[button1],[button2]])
    else:
        button1=InlineKeyboardButton(text="login",callback_data=1)
        text="salam yeki az gozine haye zir ra vared konid"
        menu=InlineKeyboardMarkup(inline_keyboard=[[button1]])
    bot.sendMessage(chatId,text,reply_markup=menu)

def textHandle(msg):
    msgType,chatType,chatId=telepot.glance(msg)
    msgText=msg['text']
    user=isLogin(chatId)
    if msgText=="/start" or msgText=="/menu":
        showMenu(chatId,user)
    if user!=False:
        if user.getState()==1:
            user.setTicketTitle(msgText)
            bot.sendMessage(chatId,"matne ticket ra vared konid")
            user.setState(2)
        elif user.getState()==2:
            user.setTicketBodey(msgText)
            button2=InlineKeyboardButton(text="yes",callback_data=20)
            button1=InlineKeyboardButton(text="no",callback_data=21)
            text="( "+user.getTicketTitle()+"\n"+user.getTicketBodey()+" ) \n aya motmaen hastid?"
            menu=InlineKeyboardMarkup(inline_keyboard=[[button1],[button2]])

        elif user.getState()==10:
            user.setLoginEmailTry(msgText+"")
            bot.sendMessage(chatId,"password ra vared konid")
            user.setState(11)
        elif user.getState()==11:
            user.setLoginPassTry(msgText)
            res=login(user)
            if res==True:
                bot.sendMessage(chatId,user.getLastName()+" vared shodid")
                user.setState(100)
                showMenu(chatId,user)
            else:
                if user.getState()!=100:
                    bot.sendMessage(chatId,"vared nashod")
        
            
def callbackHandle(msg):
    queryId,fromId,queryData=telepot.glance(msg,flavor="callback_query")
    user=isLogin(fromId)
    queryData=int(queryData)
    if queryData==1 and user==False:
        #login
        user=userClass()
        userList[fromId]=user
        user.setChatId(fromId)
        bot.sendMessage(fromId,"email ra vared konid")
        user.setState(10)
    if queryData==2 and user!=False:
        #send ticket
        bot.sendMessage(chatId,"mozooe ticket ra vared konid")
        user.setState(1)
    if queryData==3 and user!=False:
        #logout
        userList.pop(fromId)
        bot.answerCallbackQuery(queryId,"kharej shodid")
        showMenu(fromId,False)
    if queryData==20 and user!=False:
        user.setState(50)
        bot.answerCallbackQuery(queryId,"ticket sabt shod")
    if queryData==21 :
        user.setState(51)
        bot.answerCallbackQuery(queryId,"ticket sabt nashod")

    #bot.answerCallbackQuery(queryId,"zadi roosh")
    #bot.sendMessage(fromId,queryData)
bot=telepot.Bot("485564318:AAE8mXpO-yA8Y0Oi0wN9p4mEvu1Hpv8CPoY")

MessageLoop(bot,{'chat':textHandle,'callback_query':callbackHandle}).run_as_thread()
while(1):
    time.sleep(10)
    