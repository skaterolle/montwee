# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 20:26:36 2020

@author: Jacinto
"""

from tweepy import Stream
import json
import time
import random
from pymongo import MongoClient
from datetime import datetime

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# Conexión a una instancia en localhost
cliente = MongoClient('127.0.0.1', 27017)

# Conexión a un clúster (replica set) en localhost
# stringConexion='mongodb://localhost:27000/?replicaSet=miReplicaSet&readPreference=primary&appname=MongoDB%20Compass&ssl=false'
#cliente = MongoClient(stringConexion)

bd = cliente.Twitter
tweets = bd.tweets


class MiClaseTwitter(Stream):

    # Podemos forzar el streaming para que termine
    # cuando se alcance un determinado número de tweets
    contador = 0
    limite = 5000
    Hora_inicial = ""

    def on_connection_error(self):
        self.disconnect()

    def on_connect(self):
        print("¡¡¡¡Conexión correcta!!!!")
        now = datetime.now()
        self.Hora_inicial = now.strftime("%H:%M:%S")

    def on_data(self, data):

        if self.contador < self.limite:
            random_number = 0
            #random_number = random.randint(0, 5)
            # Para que no todos sean seguidos, sino que se recojan a lo largo de cierto tiempo
            time.sleep(random_number)

            now = datetime.now()
            Hora_actual = now.strftime("%H:%M:%S")

            # Decode the JSON data from Twitter
            tweet = json.loads(data)

            # Mostramos algunos campos por pantalla para
            # comprobar que el proceso se está realizando correctamente
            # print(tweet['created_at'])
            print(tweet['user']['screen_name'])
            print("Tweets Encontrados: ", self.contador +
                  1, "  - ", random_number, "sec")
            # print("Tweets Encontrados: ",self.contador + 1, "  - ", self.Hora_inicial, "-", Hora_actual, "  - ", random_number, " sec")

            tweets.insert_one(tweet)

            self.contador += 1

        else:
            now = datetime.now()
            Hora_actual = now.strftime("%H:%M:%S")
            print('Límite de tweets alcanzado')
            print('Tiempo: ', self.Hora_inicial, " - ", Hora_actual)
            self.disconnect()
            input("Pulse ENTER para terminar.")

    def on_error(self, status_code):
        print("Error", status_code)


MiStream = MiClaseTwitter(consumer_key, consumer_secret,
                          access_token, access_token_secret)

# Busca todos los tweets que contengan algo de real madrid
#MiStream.filter(track = ['real madrid'])

# Busca todos los tweets que estén en español
# MiStream.sample(languages=['es'])
# Buscar todos los tweets que estén en español y en ingles
# MiStream.sample(languages=['es','en'])


MiStream.filter(track=['Pokemon'])
