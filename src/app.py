from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from faker import Faker
import json
import requests
import random

fake = Faker()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:secret@127.0.0.1:3306/enviame'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#CREAR MODELO
class Empresa(db.Model):
    idEmpresa = db.Column(db.Integer, primary_key=True)
    nombreEmpresa = db.Column(db.String(70), unique=True)
    rutEmpresa = db.Column(db.String(70), unique=True)
    direccionEmpresa = db.Column(db.String(70))
    razonsocialEmpresa = db.Column(db.String(70))
    gerentegeneralEmpresa = db.Column(db.String(70))
    telefonoEmpresa = db.Column(db.String(70))

    def __init__(self, nombreEmpresa, rutEmpresa, direccionEmpresa,  razonsocialEmpresa, gerentegeneralEmpresa, telefonoEmpresa):
        self.nombreEmpresa = nombreEmpresa
        self.rutEmpresa = rutEmpresa
        self.direccionEmpresa = direccionEmpresa
        self.razonsocialEmpresa = razonsocialEmpresa
        self.gerentegeneralEmpresa = gerentegeneralEmpresa
        self.telefonoEmpresa = telefonoEmpresa

db.create_all()

class AccionSchema(ma.Schema):
    class Meta:
        fields = ('nombreEmpresa', 'rutEmpresa', 'direccionEmpresa', 'razonsocialEmpresa', 'gerentegeneralEmpresa', 'telefonoEmpresa')

accion_schema = AccionSchema()
accions_schema = AccionSchema(many=True)

##################################################################################
################################ INICIO RUTAS ####################################
@app.route('/', methods=['GET'])
def inicio():

    rutas = [{  "rutas":[
                    {"ejercicio2":[
                            {"crearEmpresa(POST)":"http://10.42.0.203:4000/acciones"},
                            {"consultarTodasLasEmpresas(GET)":"http://10.42.0.203:4000/acciones"},
                            {"consultarUnaEmpresa(GET)":"http://10.42.0.203:4000/acciones/<idEmpresa>"},
                            {"actualizarEmpresa(PUT)":"http://10.42.0.203:4000/acciones/<idEmpresa>"},
                            {"quitarEmpresa(DELETE)":"http://10.42.0.203:4000/acciones/<idEmpresa>"},
                            {"generarEmpresas(POST)":"http://10.42.0.203:4000/generar/<n>"},
                        ]
                    },
                    {"ejercicio3":[
                            {"RespuestaEjercicio3":"http://10.42.0.203:4000/ejercicio5/1/n"},
                            {"palindromoOtrasPalabras":"http://10.42.0.203:4000/ejercicio5/2/<palindromo>"},
                            {"palindromo":"el segundo link, es para ser probado con cualquier posible polindromo ej: Yo hago yoga hoy"},
                        ]
                    },
                    {"ejercicio4":[
                            {"consumirApi(POST)":"http://10.42.0.203:4000/ejercicio4/1"},
                            {"Observarcion1":"faltaron modificaciones para generar con faker n cantidad de envios"},
                            {"NOTA":"La respuesta de este ejercicio se aloja en respuesta.html en la raiz de la aplicación"},
                        ]
                    },
                    {"ejercicio5":[
                            {"RespuestaEjercicio5":"http://10.42.0.203:4000/ejercicio5/1/1000"},
                            {"fibonnacciRespuesta":"http://10.42.0.203:4000/ejercicio5/1/<fibonnaci>"},
                            {"fibonnacciSecuencia":"http://10.42.0.203:4000/ejercicio5/2/<fibonnaci>"},
                            {"NOTA":"El primer link es la respuesta del ejercicio, el segundo es para visualizar un solo resultado segun el parametro, y el tercero muestra todos los posibles numero divisibles del parametro que se envie"},
                        ]
                    },
                    {"ejercicio6":[
                            {"RespuestaEjercicio6":"http://10.42.0.203:4000/ejercicio6/<n>"},
                        ]
                    },
                    {"ejercicio7":[
                            {"RespuestaEjercicio7":"http://10.42.0.203:4000/ejercicio7/1"},
                        ]
                    },
                    {"ejercicio8":[
                            {"RespuestaEjercicio6":"http://10.42.0.203:4000/ejercicio8/1/<especifico>"},
                            {"fibonnacciRespuesta":"http://10.42.0.203:4000/ejercicio8/2/0"},
                            {"NOTA":"Este es el ejercicio 6, crei haberlo resuelto, luego de repasar comprendi que aunque si di solucion al objetivo del ejercicio, no desarrolle la logica siguiendo los principios del mismo, decidi rehacerlo y dejar este como practica adicional"},
                            {"NOTA":"El segundo link permite generar respuesta aleatoria, sin importar el valor de N"},
                        ]
                    },
                ]
            }]
    return jsonify(rutas)

##################################################################################
################################  EJERCICIO 2 ####################################
#CREAR EMPRESA
@app.route('/acciones', methods=['POST'])
def crear_empresa():
    nombreEmpresa = request.json['nombreEmpresa']
    rutEmpresa = request.json['rutEmpresa']
    direccionEmpresa = request.json['direccionEmpresa']
    razonsocialEmpresa = request.json['razonsocialEmpresa']
    gerentegeneralEmpresa = request.json['gerentegeneralEmpresa']
    telefonoEmpresa = request.json['telefonoEmpresa']

    nueva_empresa = Empresa(nombreEmpresa, rutEmpresa, direccionEmpresa, razonsocialEmpresa, gerentegeneralEmpresa, telefonoEmpresa)
    db.session.add(nueva_empresa)
    db.session.commit()

    return accion_schema.jsonify(nueva_empresa)

#CONSULTAR TODAS LAS EMPRESAS
@app.route('/acciones', methods=['GET'])
def consultar_empresas():
    all_empresa = Empresa.query.all()
    result = accions_schema.dump(all_empresa)
    return jsonify(result)

#CONSULTAR UNA EMPRESA
@app.route('/acciones/<idEmpresa>', methods=['GET'])
def consultar_empresa(idEmpresa):
    accion = Empresa.query.get(idEmpresa)
    return accion_schema.jsonify(accion)

#ACTUALIZAR DATOS DE UNA EMPRESA
@app.route('/acciones/<idEmpresa>', methods=['PUT'])
def actualizar_empresa(idEmpresa):
    accion = Empresa.query.get(idEmpresa)

    nombreEmpresa = request.json['nombreEmpresa']
    rutEmpresa = request.json['rutEmpresa']
    direccionEmpresa = request.json['direccionEmpresa']
    razonsocialEmpresa = request.json['razonsocialEmpresa']
    gerentegeneralEmpresa = request.json['gerentegeneralEmpresa']
    telefonoEmpresa = request.json['telefonoEmpresa']

    accion.nombreEmpresa = nombreEmpresa
    accion.rutEmpresa = rutEmpresa
    accion.direccionEmpresa = direccionEmpresa
    accion.razonsocialEmpresa = razonsocialEmpresa
    accion.gerentegeneralEmpresa = gerentegeneralEmpresa
    accion.telefonoEmpresa = telefonoEmpresa

    db.session.commit()
    return accion_schema.jsonify(accion)

#QUITAR UNA EMPRESA
@app.route('/acciones/<idEmpresa>', methods=['DELETE'])
def quitar_empresa(idEmpresa):
    accion = Empresa.query.get(idEmpresa)
    db.session.delete(accion)
    db.session.commit()
    return accion_schema.jsonify(accion)

#GENERAR EMPRESAS CON FAKER
@app.route('/generar/<n>', methods=['POST'])
def generar_empresas(n):
    empresasDatos = []
    empresa = []
    for i in range(int(n)):
        nombreEmpresa = fake.company()
        rutEmpresa = fake.phone_number()
        direccionEmpresa = fake.address()
        razonsocialEmpresa = fake.job()
        gerentegeneralEmpresa = fake.name()
        telefonoEmpresa = fake.phone_number()
        
        empresasDatos.append(nombreEmpresa)
        empresasDatos.append(rutEmpresa)
        empresasDatos.append(direccionEmpresa)
        empresasDatos.append(razonsocialEmpresa)
        empresasDatos.append(gerentegeneralEmpresa)
        empresasDatos.append(telefonoEmpresa)

        empresa.append(empresasDatos)

    empresanum = [empresa[0][k:k + 6] for k in range(0, len(empresa[0]), 6)] #DIVIDE EL ARRAY 
    cantidadempresas = range(len(empresanum))
    resultados = []
    for j in cantidadempresas:
        nombreEmpresa = str(empresanum[j][0])
        rutEmpresa = str(empresanum[j][1])
        direccionEmpresa = str(empresanum[j][2])
        razonsocialEmpresa = str(empresanum[j][3])
        gerentegeneralEmpresa = str(empresanum[j][4])
        telefonoEmpresa = str(empresanum[j][5])

        genera_empresa = Empresa(nombreEmpresa, rutEmpresa, direccionEmpresa, razonsocialEmpresa, gerentegeneralEmpresa, telefonoEmpresa)
        db.session.add(genera_empresa)
        db.session.commit()

        respuesta = [
            {"nombreEmpresa":nombreEmpresa},
            {"rutEmpresa":rutEmpresa},
            {"direccionEmpresa":direccionEmpresa},
            {"razonsocialEmpresa":razonsocialEmpresa},
            {"gerentegeneralEmpresa":gerentegeneralEmpresa},
            {"telefonoEmpresa":telefonoEmpresa},
        ]

        resultados.append(respuesta)

    return json.dumps(resultados)

##################################################################################
################################  EJERCICIO 3 ####################################
@app.route('/ejercicio3/<opt>/<palindromo>', methods=['GET'])
def palindromo(opt,palindromo):
    if int(opt) == 1:
        cadenaNormal = "afoolishconsistencyisthehobgoblinoflittlemindsadoredbylittlestatesmenandphilosophersanddivineswithconsistencyagreatsoulhassimplynothingtodohemayaswellconcernhimselfwithhisshadowonthewallspeakwhatyouthinknowinhardwordsandtomorrowspeakwhattomorrowthinksinhardwordsagainthoughitcontradicteverythingyousaidtodayahsoyoushallbesuretobemisunderstoodisitsobadthentobemisunderstoodpythagoraswasmisunderstoodandsocratesandjesusandlutherandcopernicusandgalileoandnewtonandeverypureandwisespiritthatevertookfleshtobegreatistobemisunderstood"
    else:
        cadenaNormal = str(palindromo)

    #cadenaPrueba = "Yo hago yoga hoy"

    cadenaSinEspacios = cadenaNormal.replace(" ","")
    tamaño = range(len(cadenaSinEspacios))
    cadena_invertida = ""
    cadena_normal = ""
    coincidenciasArray1 = []
    coincidenciasArray2 = []
    coincidenciasTotales = []

    for letra in cadenaSinEspacios:
        cadena_invertida = letra + cadena_invertida
        coincidenciasArray1.append(letra)
    
    for letra2 in cadena_invertida:
        cadena_normal = letra2 + cadena_normal
        coincidenciasArray2.append(letra2)
        
    for k in tamaño:
        if coincidenciasArray1[k].lower() == coincidenciasArray2[k].lower():
            coincidenciasTotales.append(coincidenciasArray1[k])
            resultado = "".join(coincidenciasTotales)
        else:
            if int(opt) == 2:
                resultado = "NO ES UN PALINDROMO"
    
    resultadoPalindromo = {"Palindromo":resultado}
    return jsonify(resultadoPalindromo)

##################################################################################
################################  EJERCICIO 4 ####################################
@app.route('/ejercicio4/<n>', methods=['POST'])
def crear_envio(n):
    envioDatos = []
    envio = []
    for i in range(int(n)):
        #shipping_order
        n_packages = "1"
        content_description = fake.phone_number()
        imported_id = fake.address()
        order_price = fake.job()
        weight = fake.name()
        volume = fake.phone_number()
        type = fake.phone_number()
        #shipping_origin
        warehouse_code = "401"
        #shipping_destination -> customer
        name = fake.name()
        email = fake.name()
        phone = fake.phone_number()
        #delivery_address -> home_address
        place = fake.address()
        full_address = fake.address()
        #carrier
        carrier_code = "blx"
        tracking_number = fake.currency()

        envioDatos.append(n_packages)
        envioDatos.append(content_description)
        envioDatos.append(imported_id)
        envioDatos.append(order_price)
        envioDatos.append(weight)
        envioDatos.append(volume)
        envioDatos.append(type)
        envioDatos.append(warehouse_code)
        envioDatos.append(name)
        envioDatos.append(email)
        envioDatos.append(phone)
        envioDatos.append(place)
        envioDatos.append(full_address)
        envioDatos.append(carrier_code)
        envioDatos.append(tracking_number)

        envio.append(envioDatos)

    envionum = [envio[0][k:k + 15] for k in range(0, len(envio[0]), 15)] #DIVIDE EL ARRAY 
    cantidadenvios = range(len(envionum))
    resultados = []

    for j in cantidadenvios:
        
        n_packages = str(envionum[j][0])
        content_description = str(envionum[j][1])
        imported_id = str(envionum[j][2])
        order_price = str(envionum[j][3])
        weight = str(envionum[j][4])
        volume = str(envionum[j][5])
        type = str(envionum[j][6])
        warehouse_code = str(envionum[j][7])
        name = str(envionum[j][8])
        email = str(envionum[j][9])
        phone = str(envionum[j][10])
        place = str(envionum[j][11])
        full_address = str(envionum[j][12])
        carrier_code = str(envionum[j][13])
        tracking_number = str(envionum[j][14])

        url = 'https://stage.api.enviame.io/api/s2/v2/companies/401/deliveries'
            
        headers = {
                    "Accept": "application/json",
                    "api-key": "ea670047974b650bbcba5dd759baf1ed",
                    "Content-Type": "application/json",
                }

        envios = {
            "shipping_order":{
                "n_packages": n_packages,
                "content_description":content_description,
                "imported_id": imported_id,
                "order_price": order_price,        
                "weight": weight,        
                "volume": volume,        
                "type": type    
            }, 
            "shipping_origin":{     
                "warehouse_code": warehouse_code  
            },    
            "shipping_destination":{        
                "customer": {            
                    "name": name,            
                    "email": email,            
                    "phone": phone       
                },        
                "delivery_address":{            
                    "home_address":{                
                        "place": place,                
                        "full_address": full_address            
                    }        
                }    
            },    
            "carrier":{        
                "carrier_code": carrier_code,        
                "tracking_number": tracking_number    
            }
        }
    
        resultados.append(envios)

    res = json.dumps(resultados)
    remplazar = res.replace("[","")
    remplazar = remplazar.replace("]","")
    
    payload = remplazar

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        response_json = json.loads(response.text)
        content=response.content

        file = open("respuesta.html", "a")
        file.write(str(content)+"\n")
        file.close()

        return json.dumps(response_json)
    else:
        response_json = json.loads(response.text)
        content=response.content

        file = open("respuesta.html", "a")
        file.write(str(content)+"\n")
        file.close()

        return json.dumps(response_json)

##################################################################################
################################  EJERCICIO 5 ####################################
@app.route('/ejercicio5/<opt>/<n>', methods=['GET'])
def fibonacci(opt, n):
    Fn1 = 1
    Fn2 = 1
    FnTotal = 1
    divisores = []

    for i in range(int(n)):

        if FnTotal != 1:
            Fn1 = Fn2
            Fn2 = FnTotal

        FnTotal = Fn1 + Fn2
        
        if Fn2 == 1:
            divisores.append(Fn1)
        else:
            divisores.append(FnTotal)

        tamaño = len(divisores)

    if int(opt) == 1:
        RespuestaFibonacci = {"Fibonacci":FnTotal}
    elif int(opt) == 2:
        RespuestaFibonacci = {"Fibonacci":divisores}
    else:
        RespuestaFibonacci = {"Error":"Opcion incorrecta solo puede elegir 1 o 2"}
    return jsonify(RespuestaFibonacci)

##################################################################################
################################  EJERCICIO 6 ####################################
@app.route('/ejercicio6/<n>', methods=['GET'])
def comrpa_onlines(n):
    rangot = 1
    rango1 = 0
    rango2 = 0
    origenKM = 0
    origenPibote = 0
    distanciaKM = 0
    destinoKM = 100
    diaPasado = 0
    diaAntepasado= 0
    diaEntrega = 0
    contador = 1
    arrayDias=[]
    for i in range(int(n)):
        if contador == 1:
            distanciaKM = random.randint(origenKM, destinoKM)
            origenKM = origenKM + destinoKM
            destinoKM = origenKM + destinoKM

            rango1 = rangot

            arrayDias.append("vacio")
            arrayDias.append(diaEntrega)

        elif contador == 2:
            distanciaKM = random.randint(origenKM, destinoKM)
            origenPibote = destinoKM
            destinoKM = origenKM + destinoKM

            rangot = rangot + rango1
            rango2 = rangot

            diaPasado = rangot-1
            diaEntrega = (rangot-2)+diaPasado
            diaPasado = diaEntrega
            diaAntepasado = diaPasado

            arrayDias.append(diaEntrega)

        elif contador > 2:
            distanciaKM = random.randint(origenPibote, destinoKM)
            origenPibote = destinoKM
            destinoKM = origenKM + destinoKM

            rangot = rangot + rango1
            posicion1 = rangot-1
            posicion2 = rangot-2
            diaAntepasado = arrayDias[posicion1]
            diaPasado = arrayDias[posicion2]
            diaEntrega = diaPasado + diaAntepasado

            diaPasado = diaEntrega
            diaAntepasado = diaPasado

            arrayDias.append(diaEntrega)

        contador = 1 + contador

    resultado = "Rango "+str(rangot)+". distancia "+str(distanciaKM)+" km, se entregan al dia "+str(diaEntrega)
    
    respuesta = [{"resultado": resultado}] 

    return jsonify(respuesta)

##################################################################################
################################  EJERCICIO 7 ####################################
@app.route('/ejercicio7', methods=['GET'])
def query_ejercicio7():
    querys = """'SELECT * FROM ejercicio7.employees where salary < 5001 LIMIT 0, 1000 ||| UPDATE ejercicio7.employees SET salary=(4/100+1)*2000 WHERE id = 1 ||| UPDATE ejercicio7.employees SET salary=(4/100+1)*2100 WHERE id = 2 ||| UPDATE ejercicio7.employees SET salary=(4/100+1)*3050 WHERE id = 3 ||| UPDATE ejercicio7.employees SET salary=(4/100+1)*2150 WHERE id = 4 ||| UPDATE ejercicio7.employees SET salary=(3/100+1)*2000 WHERE id = 9 ||| UPDATE ejercicio7.employees SET salary=(3/100+1)*5000 WHERE id = 10'"""
    respuesta = [{"querys":querys}]
    return jsonify(respuesta)

##################################################################################
################################  EJERCICIO 8 ####################################
@app.route('/ejercicio8/<opt>/<rango>', methods=['GET'])
def comrpa_online(opt, rango):
    rang = int(rango)
    
    if int(opt) == 1:
        rang = int(rango)
    elif int(opt) == 2:
        rang = random.randint(0, 20)
    
    distanciaMax = rang * 100
    distanciaMin = distanciaMax-100
    
    distaciaALeatoria = random.randint(distanciaMin, distanciaMax)

    contadordias1 = 0
    contadordias2 = 1
    contadordiast = 0
    array = []

    for i in range(int(rang)):
        if i == 0:
            contadordiast = contadordias1
            contadordias1 = contadordias2 + contadordiast
        if i == 1:
            contadordiast = 1
        if i == 2:
            contadordiast = 1
        if i == 3:
            contadordiast = contadordias1 + contadordias2
            contadordias1 = contadordias2
            contadordias2 = contadordiast
        if i > 3:
            contadordiast = contadordias1 + contadordias2
            contadordias1 = contadordias2
            contadordias2 = contadordiast
        
        array.append(contadordiast)
    
    resultado = "Rango "+str(rang)+". Menos de "+str(distanciaMax)+" km, se entregan al dia "+str(contadordiast)

    respuesta = [
                    {"rango": rang},
                    {"distancia": distaciaALeatoria},
                    {"dias": contadordiast},
                    {"resultado": resultado}
                ] 

    if int(opt) > 2 or int(opt) < 1:
        resultado = "option incorrect"
        respuesta = [{"resultado": resultado}] 

    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)    