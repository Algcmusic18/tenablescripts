import requests
from pandas import json_normalize
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from openpyxl import Workbook
import smtplib


#API llamada 1
url = "https://cloud.tenable.com/workbenches/vulnerabilities"

querystring = {"authenticated":"true","exploitable":"true","resolvable":"true","severity":"high"}

headers = {
    "Accept": "application/json",
    "X-ApiKeys": "accessKey=55e23ec9ef4f66275e011f28a0a7d23a3e303a5ff9fb5ae05137a4ae0d68bda4;secretKey=54469980639bd43fe46c48bca7f541c815aaaf78274546260995ec9a44c2e53c"
}

response = requests.request("GET", url, headers=headers, params=querystring)
#construcción del excel y segunda llamada a la api para traer los detalles de cada incidencia
res = response.json()
book = Workbook()
sheet = book.active
sheet ['A1'] = 'description'
sheet ['B1'] = 'synopsis'
sheet ['C1'] = 'solution'
columnas= ['A', 'B', 'C']
contador=2
for i in res['vulnerabilities']:
 url = "https://cloud.tenable.com/workbenches/vulnerabilities/"+str(i['plugin_id'])+"/info"
 response2 = requests.request("GET", url, headers=headers)
 res2 = response2.json()
 objeto = res2['info']
 titulo = objeto.keys()
 valores = objeto.values()
 elementos = objeto.items()
 for titulo, valores in elementos:
    if titulo=='description':
         sheet[f'A{contador}'] = valores
         pass

    elif titulo=='synopsis':
         sheet[f'B{contador}'] = valores
         pass

    elif titulo=='solution':
         sheet[f'C{contador}'] = valores
         pass

book.save('prueba.xlsx')

#----------------------------Correo---------------------

receptor = input('Ingrese correo electronico del receptor: ')

#Correo del emisor
emisor = 'pruebatenable2021@gmail.com'

asunto = 'Reporte de vulnerabilidades'

#Objeto mensaje
mensaje = MIMEMultipart()
 
# Establecemos los atributos del mensaje
mensaje['From'] = emisor
mensaje['To'] = receptor
mensaje['Subject'] = asunto

with open('prueba.xlsx','rb') as f:
         # Aquí adjuntoMIMEY el nombre del archivo, aquí está el tipo xlsx
    adjunto = MIMEBase('xlsx','xlsx',filename="report.xlsx")
         # Más información de encabezado necesaria
    adjunto.add_header('Content-Disposition','attachment',filename="report.xlsx")
    adjunto.add_header('Content-ID','<0>')
    adjunto.add_header('X-Attachment-Id','0')
         #Lea el contenido del archivo adjunto
    adjunto.set_payload(f.read())
         # Codificación con Base64
    encoders.encode_base64(adjunto)
    mensaje.attach(adjunto)
""" 
    adjunto = MIMEBase("application","octect-stream")
    adjunto.set_payload(open('report.xlsx',"rb").read())
    adjunto.add_header("content-Disposition",'attachment; filename="report.xlsx"')
    mensaje.attach(adjunto)
 """

#conexion server
server = smtplib.SMTP(host='smtp.gmail.com', port=587)
server.starttls()

#autenticar/Colocar correo y contraseña
server.login(user= 'pruebatenable2021@gmail.com', password= 'tenable12345')

# Convertimos el objeto mensaje a texto
#texto = mensaje.as_string().encode('utf-8')

#emisor, receptor y mensaje/declarado en variables o directo en comillas simples
server.sendmail(emisor, receptor, mensaje.as_string())

#salir del servidor
server.quit()

#Mensaje de confirmación
print("Correo enviado")