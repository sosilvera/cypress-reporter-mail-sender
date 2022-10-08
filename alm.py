from urllib import response
import requests
import env
import json
from xml.dom import minidom

class alm:
    def __init__(self, usr, passw):
        self.session = requests.session()
        self.session.auth = (usr, passw)
        response = self.session.post(env.ALM_ENDPOINT_LOGIN)
        #print(response.status_code)

    def newDefect(self, titulo, descripcion, cycle_id, rel_cycle_id):
        print('Creo defecto')
        url = env.ALM_ENDPOINT_GENERAL + env.ALM_ENVIROMENT + '/defects/'

        # Construyo el payload del request con los datos del defecto
        payload = self.buildBody(titulo, descripcion,cycle_id,rel_cycle_id)
        
        # Hago un post, asignando que el tipo de datos a enviar es JSON, y guardo el response
        response = self.session.post(url,  headers={'Content-Type': 'application/json;charset=utf-8'}, data=payload)
        print(response.status_code)
       
        file = open('error_response.xml','wb')
        file.write(response.content)
        file.close()

        # Parseo el XML de respuesta
        id = minidom.parseString(response.content).getElementsByTagName("Fields")

        # Devuelvo el valor del id del defecto
        return id[0].childNodes[env.ALM_XML_ID_NODE].childNodes[0].firstChild.data
        

    def buildBody(self, titulo, descripcion, cycle_id, rel_cycle_id):
        payload2 = {"Fields":[{"Name":"detected-by","values":[{"value":env.ALM_USER_DEFECT }]},                   
            {"Name":"severity","values":[{"value":"4-Media"}]},
            {"Name":"status","values":[{"value":"New"}]},
            {"Name":"user-07","values":[{"value": env.ALM_DEFECT_GROUP}]},
            {"Name":"user-12","values":[{"value":"02_Ambiente"}]},
            #{"Name":"user-29","values":[{"value":"02_Funcional - Problema de desarrollo (Functional - Development issue )"}]}, 
            {"Name":"detected-in-rcyc","values":[{"value":rel_cycle_id}]},
            {"Name":"cycle-id","values":[{"value": cycle_id }]},
            {"Name":"user-30","values":[{"value":"Otros"}]},
            {"Name":"user-44","values":[{"value":"N"}]},
            {"Name":"name","values":[{"value": env.ALM_DEFECT_TITLE + titulo }]},
            {"Name":"description","values":[{"value": descripcion }]}
            ]}

        objPay = json.dumps(payload2)
        file = open('body.json', 'wb')
        file.write(objPay.encode())
        file.close()
        return objPay.encode()