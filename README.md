# Sincro-ALM-Jira

Script que permite tomar los bugs en Jira y crearlos como defectos en ALM. Y en caso de querer, enviar por mail los ultimos bugs que fueron actualizados

## Como empezar

Clona el repositorio ejecutando este comando:

```
git clone https://gitlab-ee.agil.movistar.com.ar/automatizaciones-certificacion/cloudersGroup/reportes/sincro-alm-jira.git

cd reportes

```

Ahora configura el archivo de entorno env.py
## Configuracion de ENV

Se detalla el proposito de las variables mas importantes a ser configuradas. Las otras tienen su comentario en el mismo archivo

Para el envio de mails, se tiene una lista de los destinatarios
```
JIRA_DST = ["sebastian.silvera.ext@telefonica.com", "rodrigo.sosa.ext@telefonica.com"]
```

El titulo del mail
```
TITLE_REPORTER_ALM = f"Informe de casos ejecutados"
```

Usuario responsable del defecto subido
```
ALM_USER_DEFECT = 'ssilvera'
```

Grupo responsable de la resolucion del defecto
```
ALM_DEFECT_GROUP = 'GI_WEB_CLOUDERS'
```

Si la variable ALM_TEST = True, entonces los defectos se subiran al ambiente de Capacitacion, de lo contrario iran a Telefonica_Argentina
```
ALM_ENVIROMENT = 'capacitacion'
```

Ciclo al cual se cargara el defecto. Esta informacion se obtiene en 'Management' -> <Release a asignar> -> <Ciclo del Release> -> 'ID Ciclo'
```
ALM_CYCLE_ID = '3589'
```
Lista de usuarios sobre la que se van a consultar los bugs creados
```
JIRA_USERS = ['SSILVERA']
```

Rango de dias para los cuales se quiere consultar los bugs creados/modificados
```
JIRA_TIMEDELTA = 10
```

## Funcionamiento
Para correr el script, en una consola escribir:

```
py jira-reporter.py

```
En caso de querer que llegue el mail con los ultimos bugs modificados, ejecutar:

```
py jira-reporter.py -m true

# O

py jira-reporter.py --sendMail true
```
Al ejecutar, se hara uno (o varios) request a Jira, trayendo los bugs modificados en los ultimos TIMEDELTA dias, estos se guardaran en un diccionario, usando como clave el nombre del bug (Ej. DWC-510), y el titulo, la descripcion y el status como valor.
En el archivo jira-alm.json se guarda el id de defecto de ALM para cada bug creado. Para decidir si se crea un defecto o no, el script verifica para cada bug, si esta en el archivo jira-alm.
Si no esta, crea uno, llamando al servicio createDefect de ALM. Aqui se arma el json del request y se lo guarda en el archivo 'body.json', el cual puede servir para revisarlo en caso de algun error. El response tambien es guardado en el archivo 'error_response.xml'.

## Importante
Para hacer pruebas, verificar que todas las variables de ENV que contengan 'TEST' en su nombre esten en True.
Tener en cuenta que los defectos que son creados en el ambiente de Telefonica_Argentina son defectos verdaderos y que pueden afectar a las metricas.
Por otra parte, se recomienda fuertemente no modificar manualmente el archivo 'jira-alm.json', ya que ahi se decide si se crea o no un defecto.

Ante cualquier duda sobre el funcionamiento, o por algun error, comunicarse conmigo (sebastian.silvera.ext@telefonica.com)