import requests
import datetime
import env
import sendMail
class jira:
    def __init__(self, usr, passw):
        self.issuesArray = []
        self.bugCreados={}
        self.bugModificados={}
        
        print("Buscando bugs")

        for i in env.JIRA_USERS:
            url = f'https://jira-server.com.ar/jira/rest/api/2/search?jql=reporter={i}'
            response = requests.get(url, auth=(usr, passw))
            self.issuesArray = self.issuesArray + response.json()['issues'] # List
        
    # Devuelvo un diccionario donde la key sea i[key]
    # y valores sea un json de 'Titulo' (summay o name) y 'Descripcion'
    def obtenerCreadosEn24hs(self):
        for i in self.issuesArray:
            fechaCreacion = i['fields']['created']
            fechaBug = datetime.datetime.strptime(fechaCreacion[0:10], "%Y-%m-%d")
            fechaHoy = datetime.datetime.today()
            if fechaBug > fechaHoy - datetime.timedelta(env.JIRA_TIMEDELTA):
                self.bugCreados[i['key']] = {
                        "titulo": i['fields']['summary'],
                        "descripcion": i['fields']['description'],
                        "status": i['fields']['status']['name']
                    }
        # print(self.bug)
        return self.bugCreados

    # Devuelvo un diccionario donde la key sea i[key]
    # y valores sea un json de 'Titulo' (summay o name) y 'Descripcion'
    def obtenerModificadosEn24hs(self):
        for i in self.issuesArray:
            fechaActualizacion = i['fields']['updated']
            fechaBug = datetime.datetime.strptime(fechaActualizacion[0:10], "%Y-%m-%d")
            fechaHoy = datetime.datetime.today()
            if fechaBug > fechaHoy - datetime.timedelta(env.JIRA_TIMEDELTA):
                self.bugModificados[i['key']] = {
                        "titulo": i['fields']['summary'],
                        "descripcion": i['fields']['description'],
                        "status": i['fields']['status']['name']
                    }
        return self.bugModificados

    def getCreados(self):
        return self.bugCreados
    
    def getModificados(self):
        return self.bugModificados

    def buildMailJira(self, bodyMailF):
        html = f"""
            <head>
            <meta charset="utf-8" />
            <title>Bugs actualizados</title>
            </head>

            <p>Buen día<br/>
            Se envía el reporte de los ultimos bugs actualizados</p>
            <ul>

            {bodyMailF}

            </ul>
           

            <br><br>
            <br aria-hidden="true"/>Cualquier duda, avisenme
            <br aria-hidden="true"/>Saludos
            <br aria-hidden="true"/>Seba Silvera</p>
            </html>
        """

        return html

    def sendMailActualizados(self):
        self.obtenerModificadosEn24hs()
        bodyMailF = ""

        for i in self.bugModificados:
            if self.bugModificados[i]['status'] == 'Done':
                bodyMailF = bodyMailF + "<br><strong>" + f"""<a href="https://jira-server.com.ar/jira/browse/{i}" target="_blank" rel="noopener noreferrer" data-auth="NotApplicable" data-linkindex="0">{i}</a>""" + """ - <span style="color: #00ff00;"> """+ self.bugModificados[i]['status'] + "</span> - " + self.bugModificados[i]['titulo'] + "</strong>\n"

        html = self.buildMailJira(bodyMailF)
        sendMail.send(sendMail.buildMsjHeader(env.TITLE_REPORTER_ALM), html, env.MAILSRV, env.USR, env.PASS, env.SRC, env.JIRA_DST)
        print("Correo enviado")


    def printAll(self):
        for i in self.issuesArray:
            print(i['key'])

    def printCreados(self):
        for i in self.bugCreados:
            print(i)
            print(self.bugCreados[i]['titulo'])
            print('\n')