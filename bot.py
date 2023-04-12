import os
import json
import time

from tkinter import *
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from extract import class_prediction, get_response
from keras.models import load_model

# loading variables from .env file
load_dotenv()

# defining global variables
DIALOG_START: bool = False
USER_NAME: str = None 
USER_EMAIL:str = None

def chatbot_response(message_user: str) -> str:
    """
        Function to get formatted chatbot response

        Args:
            message_user (str): message received by user
    """
    global DIALOG_START, USER_NAME, USER_EMAIL

    if DIALOG_START and USER_NAME is None:
        USER_NAME = message_user
        time.sleep(1)
        return f'Bem vindo {USER_NAME}, poderia me informa seu e-mail?'
    elif DIALOG_START and USER_EMAIL is None:
        USER_EMAIL = message_user
        DIALOG_START = False
        time.sleep(1)
        return f'Obrigado pelas informações {USER_NAME}, como posso ajudar?'
    else:
        intent = class_prediction(message_user, model)
        response, DIALOG_START = get_response(intent, intents)
        return response

def message_send() -> None:
    """
        Function to get the text and send it to the model
    """
    # get text from input box
    input_message = inbox.get('1.0', 'end-1c').strip()
    inbox.delete('0.0', END)

    # validates if to some content
    if input_message != '':
        # inserts the user's message on the text area
        text_area.config(state=NORMAL)
        text_area.insert(END, f'Você: {input_message}\n\n')
        text_area.config(foreground='#000000', font=('Arial', 12))
        window.update()

        # call the model
        response = chatbot_response(input_message)
        text_area.insert(END, f'Luna Bot: {response}\n\n')

        # disable text area state
        text_area.config(state=DISABLED)
        text_area.yview(END)

def on_closing():
    global USER_EMAIL
    try:
        content = text_area.get('1.0', 'end-1c').strip()

        if USER_EMAIL is None:
            print('[ERROR] e-mail is none')
        elif content is not None and len(content) > 0:
            print('[INFO] envio e-mail')
            message = Mail(
                from_email=os.getenv('NOTIFICATION_EMAIL'),
                to_emails=USER_EMAIL,
                subject='Luna Chat: Cópia de conversa',
                html_content=content
            )
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            sg.send(message)
    except Exception as ex:
        print('[ERROR]', ex)
    finally:
        window.destroy()

if __name__ == '__main__':
    # loading the model to memory
    model = load_model('models/model.h5')

    # we carry our intentions
    intents = json.loads(open('data/intents.json').read())

    # creating the base of the canvas
    window = Tk()
    window.title('Chatbot')
    window.geometry('400x500') 
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.resizable(width=FALSE, height=FALSE)

    # create the chat text area
    text_area = Text(window, bd=0, bg='white', height='8', width='50', font='Arial')
    text_area.config(state=DISABLED)

    # binds the scroll bar to the chat text area
    scrollbar = Scrollbar(window, command=text_area.yview)
    text_area['yscrollcommand'] = scrollbar.set

    # creates the send message button, where the command sends to the send function
    message_send_button = Button(
        window, 
        font=('Verdana', 10, 'bold'), 
        text='Enviar', 
        width='12', 
        height=2, 
        bd=0, 
        bg='#666', 
        activebackground='#333', 
        fg='black', 
        command=message_send
    )

    # Cria o box de texto
    inbox = Text(window, bd=0, bg='white', width='29', height='2', font='Arial')

    # Coloca todos os componentes na tela
    scrollbar.place(x=376, y=6, height=386)
    text_area.place(x=6, y=6, height=386, width=370)
    inbox.place(x=128, y=401, height=50, width=260)
    message_send_button.place(x=6, y=401, height=50)

    # initializing window
    window.mainloop()
