from asyncio.windows_events import NULL
from datetime import datetime
import json
import certifi
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import yaml

app = Flask(__name__)
config = yaml.safe_load(open('database.yaml'))
client = MongoClient(config['uri'])
# client = MongoClient(config['uri'], tlsCAFile=certifi.where()) # Solo para la universidad

# db = client.lin_flask
db = client['Twitter']
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/')
def index():
    return render_template('home.html')


def All_JSON(data):
    _id = data['_id']
    created_at = data['created_at']
    id = data['id']
    id_str = data['id_str']
    text = data['text']
    source = data['source']
    user = data['user']
    geo = data['geo']
    entities = data['entities']
    lang = data['lang']
    try:
        retweeted_status = data['retweeted_status']
        dataDict = {
            '_id': str(_id),
            'created_at': created_at,
            'id': id,
            'id_str': id_str,
            'text': text,
            'source': source,
            'user': user,
            'geo': geo,
            'entities': entities,
            'retweeted_status': retweeted_status,
            'lang': lang
        }

    except KeyError:
        dataDict = {
            '_id': str(_id),
            'created_at': created_at,
            'id': id,
            'id_str': id_str,
            'text': text,
            'source': source,
            'user': user,
            'geo': geo,
            'entities': entities,
            'lang': lang
        }

    return dataDict


@app.route('/tweets', methods=['POST', 'GET'])  # methods=['POST', 'GET']
def data():

    # POST a data to database
    # if request.method == 'POST':
    # body = request.json
    # firstName = body['firstName']
    # lastName = body['lastName']
    # emailId = body['emailId']
    # # db.users.insert_one({
    # db['users'].insert_one({
    # "firstName": firstName,
    # "lastName": lastName,
    # "emailId":emailId
    # })
    # return jsonify({
    # 'status': 'Data is posted to MongoDB!',
    # 'firstName': firstName,
    # 'lastName': lastName,
    # 'emailId':emailId
    # })

    # GET all data from database
    if request.method == 'GET' or request.method == 'POST':
        min = 0
        max = 20
        colleccion = ""
        receiv = request.json
        if receiv:
            min = receiv['min']
            max = receiv['max']
            colleccion = receiv['colleccion']
        allData = db[colleccion].find()
        dataJson = []
        # for data in allData: # Devuelve todos los tweets
        # id = data['_id']
        # name = data['user']['screen_name']
        # followers = data['user']['followers_count']
        # tweet = data['text']
        # dataDict = {
        # 'id': str(id),
        # 'Name': name,
        # 'Followers': followers,
        # 'Tweet': tweet
        # }
        # dataJson.append(dataDict)
        data = allData
        # Devuelve todos los tweets pero podemos definir un rango, tarda menos que el anterior
        for x in range(min, max):
            dataDict = All_JSON(data[x])
            # id = data[x]['_id']
            # name = data[x]['user']['screen_name']
            # followers = data[x]['user']['followers_count']
            # tweet = data[x]['text']
            # dataDict = {
            #     'id': str(id),
            #     'Name': name,
            #     'Followers': followers,
            #     'Tweet': tweet,
            # }
            dataJson.append(dataDict)

        # print(dataJson)
        print("Devuelvo todos los tweets.")
        print("min: ", min, " max: ", max)
        return jsonify(dataJson)
        # return dataJson


@app.route('/find', methods=['POST', 'GET'])  # methods=['POST']
def find_text():
    if request.method == 'GET' or request.method == 'POST':
        # print("Entro")
        receiv = request.json
        parametro = False
        dataJson = []
        query = {}
        text = ""
        descart_rt = False
        order = 1
        dateTimeObj = datetime.now()
        desde = dateTimeObj.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        hasta = dateTimeObj.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        usuario = ""
        hashtag = ""
        busca_hashtag = False
        menciones = 0
        geo = False
        verificado = False
        collecion = ""
        if receiv:
            text = receiv['text']
            order = receiv['order']
            descart_rt = receiv['descart_rt']
            desde = receiv['desde']
            hasta = receiv['hasta']
            usuario = receiv['usuario']
            hashtag = receiv['hashtag']
            busca_hashtag = receiv['busca_hashtag']
            menciones = receiv['menciones']
            geo = receiv['geo'],
            verificado = receiv['verificado'],
            colleccion = receiv['colleccion']

        # QUERY - TEXTO
        if text != "":
            query = {"$text": {"$search": text}}
            parametro = True

        #print("TEXT: ", parametro)
        # QUERY - Descarta RT
        if descart_rt == True:
            query.update({"retweeted_status": None})

        #print("DESCARTA RT: ", parametro)
        # QUERY - User
        if usuario != "":
            query.update({"$or": [{"user.name": {"$regex": usuario}}, {
                         "user.screen_name": {"$regex": usuario}}]})
            parametro = True

        #print("USER: ", parametro)
        # QUERY - Hashtag
        if hashtag != "":
            lista = [str(x) for x in hashtag.replace(
                " ", "").replace(",", "#").split("#")]
            parametro = True
            # print(len(lista))
            # print(lista)
            for x in range(len(lista)-1):
                print(x)
                if(lista[x] == ""):
                    lista.pop(x)
            # print(busca_hashtag)
            # print(lista)
            # query.update({"entities.hashtags.text": {"$in": [str(x) for x in hashtag.replace(
            #     " ", "").replace(",", "#").split("#")]}})
            if(busca_hashtag == True):
                query.update({"entities.hashtags.text": {"$all": lista}})
            else:
                query.update({"entities.hashtags.text": {"$in": lista}})

        # print("HASHTAG: ", parametro)
        # QUERY - GEO
        if geo == True:
            query.update({"geo": {"$ne": None}})

        if verificado == True:
            query.update({"user.verified": True})
        # print(query)

        # print("GEO: ", parametro)
        # key = frozenset(query.items())
        # print(query)
        # print(key)
        if(parametro == True):
            allData = db[colleccion].find(query).sort(
                "user.followers_count", order)
        else:
            allData = db[colleccion].find(query).sort(
                "user.followers_count", order).limit(20)

        # if descart_rt == False:
        #     allData = db['tweets'].find(
        #         {"$text": {"$search": text}}).sort("user.followers_count", order)
        # elif descart_rt == True:
        #     allData = db['tweets'].find(
        #         {"$text": {"$search": text}, "retweeted_status": {"$exists": False}}).sort("user.followers_count", order)
        # print(desde)
        # print(hasta)
        # print(parametro)
        # QUERY - DATES
        if(desde != "False"):
            desde_time = datetime.strptime(desde, '%Y-%m-%dT%H:%M:%S.000Z')
        if(hasta != "False"):
            hasta_time = datetime.strptime(hasta, '%Y-%m-%dT%H:%M:%S.000Z')
        # print(desde_time)
        for data in allData:
            date_time = datetime.strptime(
                data['created_at'], '%a %b %d %H:%M:%S +%f %Y')
            if(desde != "False"):
                if(date_time >= desde_time):
                    if(hasta != "False"):
                        if(date_time <= hasta_time):
                            dataDict = All_JSON(data)
                            dataJson.append(dataDict)
                    else:
                        dataDict = All_JSON(data)
                        dataJson.append(dataDict)
            else:
                if(hasta != "False"):
                    if(date_time <= hasta_time):
                        dataDict = All_JSON(data)
                        dataJson.append(dataDict)
                else:
                    dataDict = All_JSON(data)
                    dataJson.append(dataDict)

    return jsonify(dataJson)


@app.route('/counts', methods=['POST', 'GET'])  # methods=['POST', 'GET']
def count_documents():
    nombre = "tweets"
    receiv = request.json
    if receiv:
        nombre = receiv['nombre']
    count = db[nombre].estimated_document_count()
    print("Retur Documents Counts: ", count)
    return str(count)


@app.route('/mostrt', methods=['POST'])  # methods=['POST', 'GET']
def mostrt():
    nombre = "tweets"
    receiv = request.json
    if receiv:
        nombre = receiv['nombre']
    print(nombre)
    data = list(db[nombre].aggregate([
        {
            '$match': {
                'retweeted_status': {
                    '$exists': True,
                    '$ne': None
                }
            }
        }, {
            '$group': {
                '_id': '$retweeted_status.id',
                'suma': {
                    '$sum': 1
                },
                'User_name': {
                    '$first': '$retweeted_status.user.screen_name'
                },
                'user_img_url': {
                    '$first': '$retweeted_status.user.profile_image_url'
                },
                'texto': {
                    '$first': '$retweeted_status.text'
                }
            }
        }, {
            '$sort': {
                'suma': -1
            }
        }, {
            '$limit': 1
        }
    ]))
    #print("Retur Documents Counts: ", count)
    return jsonify(data)


@app.route('/hashtags', methods=['POST'])  # methods=['POST', 'GET']
def hashtags():
    nombre = "tweets"
    receiv = request.json
    if receiv:
        nombre = receiv['nombre']
    print(nombre)
    data = list(db[nombre].aggregate([
        {
            '$match': {
                'entities.hashtags.text': {
                    '$exists': True,
                    '$ne': None
                }
            }
        }, {
            '$unwind': {
                'path': '$entities.hashtags',
                'includeArrayIndex': 'string',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$group': {
                '_id': '$entities.hashtags.text',
                'suma': {
                    '$sum': 1
                }
            }
        }, {
            '$sort': {
                'suma': -1
            }
        }, {
            '$limit': 5
        }
    ]))
    #print("Retur Documents Counts: ", count)
    return jsonify(data)


@app.route('/5morert', methods=['POST'])  # methods=['POST', 'GET']
def morert():
    nombre = "tweets"
    receiv = request.json
    if receiv:
        nombre = receiv['nombre']
    print(nombre)
    data = list(db[nombre].aggregate([
        {
            '$group': {
                '_id': '$user.id',
                'suma': {
                    '$sum': 1
                },
                'user_name': {
                    '$first': '$user.screen_name'
                }
            }
        }, {
            '$sort': {
                'suma': -1
            }
        }, {
            '$limit': 5
        }
    ]))
    #print("Retur Documents Counts: ", count)
    return jsonify(data)


@app.route('/5moremecionados', methods=['POST'])  # methods=['POST', 'GET']
def moremencionados():
    nombre = "tweets"
    receiv = request.json
    if receiv:
        nombre = receiv['nombre']
    print(nombre)
    data = list(db[nombre].aggregate([
        {
            '$match': {
                'entities': {
                    '$exists': True,
                    '$ne': None
                }
            }
        }, {
            '$unwind': {
                'path': '$entities.user_mentions',
                'includeArrayIndex': 'string',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$match': {
                'entities.user_mentions': {
                    '$exists': True,
                    '$ne': None
                }
            }
        }, {
            '$group': {
                '_id': '$entities.user_mentions.id',
                'suma': {
                    '$sum': 1
                },
                'nombre': {
                    '$first': '$entities.user_mentions.screen_name'
                }
            }
        }, {
            '$sort': {
                'suma': -1
            }
        }, {
            '$limit': 5
        }
    ]))
    #print("Retur Documents Counts: ", count)
    return jsonify(data)


@app.route('/5urls', methods=['POST'])  # methods=['POST', 'GET']
def url():
    nombre = "tweets"
    receiv = request.json
    if receiv:
        nombre = receiv['nombre']
    print(nombre)
    data = list(db[nombre].aggregate([
        {
            '$match': {
                'entities': {
                    '$exists': True,
                    '$ne': None
                }
            }
        }, {
            '$unwind': {
                'path': '$entities.urls',
                'includeArrayIndex': 'string',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$match': {
                'entities.urls': {
                    '$exists': True,
                    '$ne': None
                }
            }
        }, {
            '$group': {
                '_id': '$entities.urls.url',
                'suma': {
                    '$sum': 1
                },
                'url': {
                    '$first': '$entities.urls.expanded_url'
                }
            }
        }, {
            '$sort': {
                'suma': -1
            }
        }, {
            '$limit': 5
        }
    ]))
    #print("Retur Documents Counts: ", count)
    return jsonify(data)


@app.route('/5idiomas', methods=['POST'])  # methods=['POST', 'GET']
def idiomas():
    nombre = "tweets"
    receiv = request.json
    if receiv:
        nombre = receiv['nombre']
    print(nombre)
    data = list(db[nombre].aggregate([
        {
            '$group': {
                '_id': '$lang',
                'suma': {
                    '$sum': 1
                }
            }
        }, {
            '$sort': {
                'suma': -1
            }
        }, {
            '$limit': 5
        }
    ]))
    #print("Retur Documents Counts: ", count)
    return jsonify(data)


@app.route('/verificados', methods=['POST'])  # methods=['POST', 'GET']
def verificados():
    nombre = "tweets"
    receiv = request.json
    if receiv:
        nombre = receiv['nombre']
    print(nombre)
    data = list(db[nombre].aggregate([
        {
            '$group': {
                '_id': '$user.verified',
                'suma': {
                    '$sum': 1
                }
            }
        }, {
            '$match': {
                '_id': True
            }
        }
    ]))
    #print("Retur Documents Counts: ", count)
    return jsonify(data)


@app.route('/firstlast', methods=['POST', 'GET'])  # methods=['POST', 'GET']
def firs_last():
    data = list(db['tweets'].aggregate([
        {
            "$group": {
                "_id": None,
                "first_date": {
                    '$first': "$$ROOT.created_at"
                },
                "last_date": {
                    "$last": "$$ROOT.created_at"
                }
            }
        }]))
    return jsonify(data)


@app.route('/collections', methods=['POST', 'GET'])  # methods=['POST', 'GET']
def collections():
    data = db.list_collection_names()
    return jsonify(data)


@app.route('/guarda', methods=['POST', 'GET'])
def guarda():
    receiv = request.json
    if receiv:
        tweets = receiv['colleccion']
        nombre = receiv['nombre']
    allData = db[nombre].insert_many(tweets)
    data = db.list_collection_names()
    print(data)
    return jsonify(data)


@app.route('/tweets/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    # GET a specific data by id
    if request.method == 'GET':
        data = db['users'].find_one({'_id': ObjectId(id)})
        id = data['_id']
        firstName = data['firstName']
        lastName = data['lastName']
        emailId = data['emailId']
        dataDict = {
            'id': str(id),
            'firstName': firstName,
            'lastName': lastName,
            'emailId': emailId
        }
        print(dataDict)
        return jsonify(dataDict)

    # DELETE a data
    if request.method == 'DELETE':
        db['users'].delete_many({'_id': ObjectId(id)})
        print('\n # Deletion successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is deleted!'})

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        firstName = body['firstName']
        lastName = body['lastName']
        emailId = body['emailId']

        db['users'].update_one(
            {'_id': ObjectId(id)},
            {
                "$set": {
                    "firstName": firstName,
                    "lastName": lastName,
                    "emailId": emailId
                }
            }
        )

        print('\n # Update successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is updated!'})

# methods=['POST', 'GET']


if __name__ == '__main__':
    app.debug = True
    # Casa - Localhost
    app.run(host='TU DIRECCIÓN LOCAL, NO VALE LOCALHOST O 127.0.0.1')
    # app.run(host='0.0.0.0') # Servidor
