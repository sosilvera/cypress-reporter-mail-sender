import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import env

def buildMail(date, passed, fail, bodyMailF):
    html = f"""
        <head>
        <meta charset="utf-8" />
        <title>Reporte de automatizaciones</title>
        </head>

        <p>Buen día<br/>
        Se envía el reporte de casos corridos del día de ayer para la web Tuenti.</p>
        <ul>

        <li><span style="color: #00ff00;"><strong>Test pasados</strong></span>: {passed}</li>
        <li><span style="color: #ff0000;"><strong>Test fallidos</strong></span>: {fail}</li>

        </ul>
        <p><strong><span style="color: #ff0000;">######################### FALLIDOS #########################</span></strong></p>
        {bodyMailF}

        <br><br>
        <p>Para el informe completo visitar: <a href="http://file-server/project/project/{date}_200000/project_{date}.html" target="_blank" rel="noopener noreferrer" data-auth="NotApplicable" data-linkindex="0">Informe Tuenti</a><br aria-hidden="true" />
        <br aria-hidden="true"/>Cualquier duda, avisenme
        <br aria-hidden="true"/>Saludos
        <br aria-hidden="true"/>Seba Silvera</p>
        </html>
        """

    return html

def buildMailTableuReporter(passed, fail, norun, bodyMailF):
    html = f"""
        <head>
        <meta charset="utf-8" />
        <title>Reporte de Casos corridos en el sprint actual</title>
        </head>

        <p>Buen día<br/>
        Se envía el reporte de casos ejecutados en el sprint actual</p>
        <ul>

        <li><span style="color: #00ff00;"><strong>Casos pasados</strong></span>: {passed}</li>
        <li><span style="color: #ff0000;"><strong>Casos fallidos</strong></span>: {fail}</li>
        <li><span style="color: #0000ff;"><strong>Casos no corridos</strong></span>: {norun}</li>

        </ul>
        <p><strong><span style="color: #ff0000;">######################### FALLIDOS #########################</span></strong></p>
        {bodyMailF}

        <br><br>
        <br aria-hidden="true"/>Cualquier duda, avisenme
        <br aria-hidden="true"/>Saludos
        <br aria-hidden="true"/>Seba Silvera</p>
        </html>
        """

    return html

def buildMsjHeader(title):
    msj = MIMEMultipart("alternative")

    # Titulo
    msj["Subject"] = title
    # Quien envia
    msj["From"] = env.SRC
    # Hacia quien
    msj["To"] = env.SRC

    return msj

def send(msj, html, MAILSRV, USR, PASS, SRC, DST):
    # Parseo a html y agrego al msj
    parte_html = MIMEText(html, "html")
    msj.attach(parte_html)

    # Defino server origen y puerto
    server = smtplib.SMTP(MAILSRV, 587)
    # Indico uso de protocolo TLS
    server.starttls()

    server.login(USR, PASS)

    origen= SRC
    destino = DST

    # Envio mail: origen, destino, mensaje
    server.sendmail(origen, destino,msj.as_string())

    server.quit()
    print("Correo enviado")