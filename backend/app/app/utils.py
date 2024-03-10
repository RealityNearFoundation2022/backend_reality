from email.message import EmailMessage
import logging
from datetime import datetime, timedelta
from pathlib import Path
import smtplib
import ssl
from typing import Any, Dict, List, Optional
from fastapi import UploadFile, HTTPException

import pandas as pd
import io
import cgi

import os

import emails
from emails.template import JinjaTemplate
from jose import jwt
from uuid import uuid4

from app.core.config import settings


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    print("******* SEND EMAIL *******")
    print("Emails_from_name: ", settings.EMAILS_FROM_NAME)
    print("Emails_from_email: ", settings.EMAILS_FROM_EMAIL)
    print("SMTP_HOST: ", settings.SMTP_HOST)
    print("SMTP_PORT: ", settings.SMTP_PORT)
    print("SMTP_TLS: ", settings.SMTP_TLS)
    print("SMTP_USER: ", settings.SMTP_USER)
    print("SMTP_PASSWORD: ", settings.SMTP_PASSWORD)
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    print("******* RESULT *******")
    print(response)
    logging.info(f"send email result: {response}")
    # assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    # message = emails.Message(
    #     subject=JinjaTemplate(subject_template),
    #     html=JinjaTemplate(html_template),
    #     mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    # )
    # smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    # if settings.SMTP_TLS:
    #     smtp_options["tls"] = True
    # if settings.SMTP_USER:
    #     smtp_options["user"] = settings.SMTP_USER
    # if settings.SMTP_PASSWORD:
    #     smtp_options["password"] = settings.SMTP_PASSWORD
    # response = message.send(to=email_to, render=environment, smtp=smtp_options)
    # logging.info(f"send email result: {response}")


def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    
    email_sender = "realityneardev@gmail.com"
    email_password = "ecgu ekco ocjj onvi"
    
    environment_html = {
        "project_name": settings.PROJECT_NAME,
        "username": email,
        "email": email_to,
        "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
        "link": link,
    }

    template_str_copy = template_str

    for key, value in environment_html.items():
        template_str_copy = template_str_copy.replace("{{my_{}}}".format(key), str(value))

    # Replace Jinja variables with actual values
    # template_str = template_str.format(**environment_html)

    print("******* SEND RESET PASSWORD EMAIL *******")
    print(link)
    print(email_to)
    print(subject)
    print(settings.PROJECT_NAME)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_to
    em['Subject'] = subject
    em.set_content(template_str_copy, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_sender, email_password)
        server.send_message(em)
    # send_email(
    #     email_to=email_to,
    #     subject_template=subject,
    #     html_template=template_str,
    #     environment={
    #         "project_name": settings.PROJECT_NAME,
    #         "username": email,
    #         "email": email_to,
    #         "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
    #         "link": link,
    #     },
    # )



def send_new_account_email(email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None


def save_image(formats, path: str, file: UploadFile):
    contents = file.file.read()

    extension = os.path.splitext(file.filename)[1]

    if extension not in formats:
        raise HTTPException(
            status_code=400,
            detail="The extension must be " + ", ".join(formats)
        )

    compress_file = '{}{}'.format(uuid4(), extension)  

    with open('./static/'+path+'/' + compress_file, 'wb') as image:
        image.write(contents)
        image.close()

    path = '/api/v1/static/'+path+'/' + compress_file

    return path


def create_excel(report_data):
    """
    Crea un archivo Excel con los datos proporcionados por la función get_report.

    Parameters:
    - report_data (dict): Diccionario con las columnas y datos obtenidos de get_report.

    Returns:
    - BytesIO: Objeto BytesIO que contiene el archivo Excel.
    """
    try:
        # Crear un DataFrame con las columnas y datos
        df = pd.DataFrame(report_data['data'], columns=report_data['columns'])

        # Guardar el DataFrame en un objeto BytesIO (en lugar de un archivo físico)
        excel_file = io.BytesIO()
        df.to_excel(excel_file, index=False)

        return excel_file

    except Exception as e:
        print(f"Error al crear el archivo Excel: {str(e)}")
        return None