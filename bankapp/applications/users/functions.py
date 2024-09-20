#Paquete que se debe instarlar para enviar mensajes con gmail
#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
#
import random
#
import string

#genero codigo de registro
def create_cod(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#
import string
#
import random
#
import os.path
from email.mime.text import MIMEText

from google.oauth2 import service_account

import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


#Envio de correo de registro
def send_mail_register(nombre, correo, codigo, url):

    creds = None
    # El archivo token.json almacena los tokens de acceso y actualización del usuario, y se crea automáticamente 
    # cuando se completa el flujo de autorización por primera vez
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        service = build('gmail', 'v1', credentials=creds)
            
        new_mail_register(creds, nombre, correo, codigo, url)

        
    # Si no hay credenciales válidas disponibles, permite que el usuario inicie sesión
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:

            flow = InstalledAppFlow.from_client_secrets_file('credenciales.json', SCOPES)
            
            creds = flow.run_local_server(
                access_type='offline',
                prompt=None,
                login_hint='javiercaicedotobon@gmail.com'
            )

            with open('token.json', 'w') as token:
                token.write(creds.to_json())
            
            new_mail_register(creds, nombre, correo, codigo, url)



def new_mail_register(creds, nombre, correo, codigo, url):
    service = build('gmail', 'v1', credentials=creds)
            
    message = MIMEText(f"""Correo de confirmacion,
        \nRegistro exitoso en el Banco Cisneros.
        \nUsuario: {correo}
        \nNombre usuario: {nombre}
        \nCodigo para activar su cuenta: {codigo}.
        \nurl para validar codigo y activar la cuenta : {url}.
        \nSaludos.""")
    message['to'] = correo
    message['subject'] = 'Confirmacion de registro'
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message')
    except HttpError as error:
        print(F'******** ocurrio un error****: {error}')
        message = None



def send_mail_verify(usuario, codigo, correo):

    creds = None
    # El archivo token.json almacena los tokens de acceso y actualización del usuario, y se crea automáticamente 
    # cuando se completa el flujo de autorización por primera vez
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        service = build('gmail', 'v1', credentials=creds)
            
        new_mail_verify(creds, usuario, codigo, correo)

        
    # Si no hay credenciales válidas disponibles, permite que el usuario inicie sesión
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:

            flow = InstalledAppFlow.from_client_secrets_file('credenciales.json', SCOPES)
            
            creds = flow.run_local_server(
                access_type='offline',
                prompt=None,
                login_hint='javiercaicedotobon@gmail.com'
            )

            with open('token.json', 'w') as token:
                token.write(creds.to_json())
            
            new_mail_verify(creds, usuario, codigo, correo)



def new_mail_verify(creds, usuario, codigo, correo):
    service = build('gmail', 'v1', credentials=creds)
            
    message = MIMEText(f"""Correo de seguridad,
        \nSe acaba de iniciar sesion con sus credenciales en TiendaOnline.
        \nUsuario: {correo}
        \nCodigo de seguridad para ingresar a su cuenta: {codigo}
        \nurl para iniciar sesion : http://127.0.0.1:8000/users/verify-user/{usuario}/
        \nSi no es usted quien a iniciado sesion, se recomienda cambiar la contraseña de acceso.
        \nSaludos.""")
    message['to'] = correo
    message['subject'] = 'Confirmacion de acceso'
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message')
    except HttpError as error:
        print(F'******** ocurrio un error****: {error}')
        message = None