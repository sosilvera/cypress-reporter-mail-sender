
# Usuario que envia mail (Tiene que ser gmail)
USR = "sender_mail_user@gmail.com"
PASS = "djbmxmuuxkhqnroq"

# Datos de encabezado de mail
SRC = "sender_mail_user@gmail.com"
REPORTER_TEST = False
TITLE_REPORTER_ALM = f"Informe de bugs actualizados"

# Mail server
MAILSRV = "smtp.gmail.com"

# ALM
ALM_TEST = False
ALM_ENDPOINT_LOGIN = 'https://alm-server.com/qcbin/api/authentication/sign-in'
ALM_ENDPOINT_GENERAL = 'https://alm-server.com/qcbin/rest/domains/CERTIFICACION/projects/'
ALM_DEFECT_TITLE = 'TITLE PREFIX '
ALM_USER_DEFECT = 'sosilvera'
ALM_DEFECT_GROUP = 'GI_ALM_GRUP'
ALM_USER = 'sosilvera'
ALM_PASS = 'asdqwe'

if ALM_TEST:
    ALM_ENVIROMENT = 'capacitacion'
    ALM_CYCLE_ID = '1008'
    ALM_XML_ID_NODE = 13
else:
    ALM_ENVIROMENT = 'ALM-Envieroment'
    ALM_CYCLE_ID = '3589'
    ALM_XML_ID_NODE = 10

# JIRA
JIRA_TEST = False
JIRA_USER = 'sosilvera'
JIRA_PASS = 'asdqwe'
if JIRA_TEST:
    JIRA_USERS = ['SOSILVERA']
    JIRA_DST = ["mail_receiver@gmail.com"]
else:
    JIRA_USERS = ['SOSILVERA', 'USER_TO_QUERY']
    JIRA_DST = ["mail_receiver@gmail.com"]

JIRA_TIMEDELTA = 2
