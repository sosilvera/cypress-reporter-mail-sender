import json
from jira import jira
from alm import alm
import env
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--sendMail", help="Envia mail con los bugs actualizados")

almSession = alm(env.ALM_USER, env.ALM_PASS)
jiraSession = jira(env.JIRA_USER, env.JIRA_PASS)

args = parser.parse_args()

print("Comienzo sincronizacion")

# Reporto por mails los bugs actualizados
if args.sendMail:
    print("Envio mail")
    jiraSession.sendMailActualizados()

# Obtengo los bugs creados en las ultimas 24hs
dicCreados = jiraSession.obtenerCreadosEn24hs()

# Abro el archivo de bugs-defectos
file = open('jira-alm.json', 'rb')
defectosActuales = json.load(file)
file.close()

defectosNuevos = False

print("Reviso nuevos defectos")
# Recorro el diccionario de bugs creados y me fijo si tienen un defecto asociado
for i in dicCreados:
    if i not in defectosActuales:
        # Si no tienen, lo creo
        print("No existe ", i)
        titulo = i + " || " + dicCreados[i]['titulo']
        idALM = almSession.newDefect(titulo,dicCreados[i]['descripcion'], "0", env.ALM_CYCLE_ID)
        print("Se crea el defecto ", idALM)
        if idALM == -1:
            break;
        # Agrego el numero de defecto al diccionario de bugs-defectos
        defectosActuales[i] = idALM
        defectosNuevos = True

if not defectosNuevos:
    print("No se creo ningun defecto")

# Escribo el diccionario a archivo
defectos = json.dumps(defectosActuales)
file = open('jira-alm.json', 'wb')
file.write(defectos.encode())
file.close()

















# getIssues = 'https://devops.movistar.com.ar/jira/rest/api/2/search?jql=reporter=ssilvera'
# user = 'ssilvera'
# passw = '41262305Jul22'
# response = requests.get(getIssues, auth=(user, passw))
#print(response.json())

# issuesArray = response.json()['issues']

# for i in issuesArray:
#     fechaCreacion = i['fields']['created']
#     fechaActualizacion = i['fields']['updated']
#     fechaBug = datetime.datetime.strptime(fechaCreacion[0:10], "%Y-%m-%d")
#     fechaHoy = datetime.datetime.today()
#     if fechaBug > fechaHoy - datetime.timedelta(4):
#         print(i['key'])
#         print(i['fields']['summary'])
#         #print(i['fields']['description'])
#         print(fechaCreacion)
#         print(fechaActualizacion)
#         print(i['fields']['status']['name'])
#         print('\n')
    


# Me gustaria que si un issue esta en To Do o In Progress desde hace
# mas de 24hs, me cree un Defecto en ALM

# reporter.name == ssilvera
# status.name == Done
# labels[0] == 'Tested'

# issues[]
    # issues[].key -> DWC-517
    # issues[].created -> fecha Creacion
    # issues[].status.name -> status
    # issues[].description -> titulo
    # issues[].summary -> descripcion
    # issues[].reporter.name -> user
    # issues[].updated -> fecha actualizacion