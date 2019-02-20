#!/usr/bin/python
# coding=utf-8

__author__ = "Maxime Hutinet, Livio Nagy"
__version__ = "0.0.1"
__status__ = "Finished"

#    LaPieFestivalSearchEngine : Webapp allowing users to find concerts/festivals around them.
#    Copyright (C) 2019  Maxime Hutinet & Livio Nagy

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

from flask import Flask, render_template, request
from flask_restful import Resource, Api
from EventfulClient import EventfulClient
from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask_cors import CORS
from Artist import Artist
from Event import Event
import boto3
import DB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
api = Api(app)
CORS(app)

# Change this variable to True if you want to use the DB locally
workLocally = True

# Change this variable to True if you need to create the tables
createTable = True

# Change the port if necessary
portDB = 5002

if workLocally:
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:' + str(portDB), region_name='eu-west-1', aws_access_key_id='xxx', aws_secret_access_key='zzz')

else:
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')


if createTable:
    tableEvent = DB.createTable(dynamodb, 'Event', 'eventfulID')
    tableArtist = DB.createTable(dynamodb, 'Artist', 'artistName')
else:
    tableEvent = dynamodb.Table('Event')
    tableArtist = dynamodb.Table('Artist')

"""
@api {get} events Retrieve list of events around a given GPS position.
@apiName GetEvents
@apiGroup Event

@apiParam {Number} latitude Latitude of the position.
@apiParam {Number} longitude Longitude of the position.
@apiParam {Number} radius Radius of the position.

@apiExample {curl} Example usage:
    curl -i http://127.0.0.1:5000/events?latitude=46.4123346&longitude=6.2650554&radius=13

@apiSuccess {Object[]} events                   List of events.
@apiSuccess {String}   events.event-name        Name of the event.
@apiSuccess {String}   events.description       Description of the event.
@apiSuccess {Number}   events.latitude          Latitude of the event.
@apiSuccess {Number}   events.longitude         Longitude of the event.
@apiSuccess {String}   events.venue-name        Venue-name of the event.
@apiSuccess {String}   events.address           Address of the event.
@apiSuccess {Number}   events.zipcode           ZIP code of the event.
@apiSuccess {String}   events.city-name         City name of the event.
@apiSuccess {String}   events.country-name      Country name of the event.
@apiSuccess {String}   events.event-start-time  Start date / time of the event.
@apiSuccess {String}   events.duration          Duration of the event.
@apiSuccess {String}   events.artist            Artist(s) of the event.
@apiSuccess {String}   events.eventful-link     Link to the original Eventful event.
@apiSuccess {String}   events.image             URL of the main image of the event.
@apiSuccess {String}   events.eventfulID        ID eventful.
@apiSuccess {String}   events.eventStartTime    Starting time of the event.

@apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
       "events":[
          {
             "eventfulID":"E0-001-117564670-8",
             "event-name":"Adana Twins",
             "description":null,
             "latitude":"46.2",
             "longitude":"6.16667",
             "venue-name":"Audio Club",
             "address":null,
             "zipcode":null,
             "city-name":"Geneva",
             "country-name":"Switzerland",
             "event-start-time":"2018-12-22 00:00:00",
             "duration":"2",
             "artist":["Adana Twins"],
             "eventful-link":"http://eventful.com/events/adana-twins-/E0-001-117564670-8?utm_source=apis&utm_medium=apim&utm_campaign=apic",
             "image":"http://d1marr3m5x4iac.cloudfront.net/images/medium/I0-001/005/884/596-2.jpeg_/adana-twins-96.jpeg"
    
             
          }
       ]
    }

"""


class events(Resource):
    def get(self):
        myEventfulClient = EventfulClient()
        response = myEventfulClient.search(request.args['latitude'], request.args['longitude'], request.args['radius'])
        numberOfEvent = myEventfulClient.getNumberOfEvent(response)
        if int(myEventfulClient.getNumberOfItems(response)) == 0:
            return {'events': 0}
        else:
            eventList = []
            for x in range(0, int(numberOfEvent)):
                data = Event(response, x).createDictFromVariable()
                if data['eventfulID'] is not None:
                    try:
                        eventList.append(DB.getDataFromTable(tableEvent, 'eventfulID', data['eventfulID']))
                    except KeyError:
                        DB.insertItem(tableEvent,data)
                        eventList.append(DB.getDataFromTable(tableEvent, 'eventfulID', data['eventfulID']))

            myJson = {'events': eventList}
            return myJson



"""
@api {get} artist/:name Get detailed information about an artist.
@apiName GetArtist
@apiGroup Artist

@apiExample {curl} Example usage:
    curl -i http://127.0.0.1:5000/artist/Adana%20Twins

@apiSuccess {String}    artist-name Name of the artist.
@apiSuccess {String[]}  pictureLinks Links to pictures of the artist.
@apiSuccess {String}    artistTopTrack Link of the top track of the artist.
@apiSuccess {String}    gender Gender of the artist.
@apiSuccess {String}    country Country of the artist.
@apiSuccess {String}    type Type of music the artist is composing.
@apiSuccess {String}    birthdate Date of birth of the artist.
@apiSuccess {String}    place-of-birth Place of birth of the artist.
@musicBrainzID {String} ID MusicBrainz.
@spotifyID {String}     ID Spotify.



@apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
       "artist-name":"Adana Twins",
       "pictureLinks":[
          "https://i.scdn.co/image/492a1bf2ecf99308b549e5977423d90fef9b2e27",
          "https://i.scdn.co/image/1652ca79d0e8b9ca5976c323e01c61adffe52208",
          "https://i.scdn.co/image/defeab6e7c8650214f7d07f0a50204158e44fbad"
       ],
       "artistTopTrack":{
          "Strange":"https://p.scdn.co/mp3-preview/90814d289632fda1e608790d2c6ff8363350b63d?cid=a9a6974a611244299b897f851d128c65"
       },
       "gender":null,
       "country":"Germany",
       "type":"Group",
       "birthdate":null,
       "place-of-birth":null,
       "birthDate": None,
       "placeOfBirth": None,
       "musicBrainzID": None,
       "spotifyID": '2JnkjHtuUjz83gkEx8QMS4'
       
    }

"""


class artist(Resource):
    def get(self, artistName):
        try:
            response = DB.getDataFromTable(tableArtist, 'artistName', artistName)
            return response

        except KeyError:
            myArtist = Artist(artistName)
            DB.insertItem(tableArtist, myArtist.__dict__)
            return self.get(artistName)


api.add_resource(events, '/events')
api.add_resource(artist, '/artist/<string:artistName>')

if __name__ == '__main__':
    socketio.run(app)


@socketio.on('my event')
def handle_event(json):
    emit('my response', json, broadcast=True)
    try:
        if json['eventfulID'] and json['interestedPersonName'] != '':
            DB.addEntryToTable(tableEvent, 'eventfulID', json['eventfulID'], 'interestedPersonName', json['interestedPersonName'])

    except KeyError:
        pass


@app.route("/")
def hello(name=None):
    return render_template('index.html', name=name)

