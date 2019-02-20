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


import requests
import urllib.parse
import pybase64
import json

class SpotifyClient:
    def __init__(self, artist):
        self.artist = artist
        self.client_id = "" # To change in order to make it work
        self.client_secret = "" # To change in order to make it work
        self.base64id = self.createBase64ID()
        self.token = self.getToken()
        self.headers = {"Authorization": "Bearer " + self.token}
        self.response = self.search(self.artist)

    # Create an URL with the right format
    def urlEncode(self, data):
        myUrl = urllib.parse.quote(data)
        return myUrl

    def request(self, urlToSend):
        response = requests.get(urlToSend,headers=self.headers)
        return response.json()

    def post(self, urlToSend, payload, headers):
        response = requests.request("POST", urlToSend, data=payload, headers=headers)
        return response.json()

    def search(self, name):
        type = "artist"
        market = "FR"
        urlToSend = "https://api.spotify.com/v1/search" + '?' \
                         + "q=" + self.urlEncode(name) + "&"\
                         + "type=" + type + "&"\
                         + "market=" + market

        return self.request(urlToSend)

    def getArtistID(self):
        try:
            artistId = self.response['artists']['items'][0]['id']
        except IndexError:
            artistId = None
        return artistId

    def getArtistPictures(self):
        pictureLinks = []
        try:
            for element in self.response['artists']['items'][0]['images']:
                pictureLinks.append(element['url'])
        except IndexError:
            pictureLinks = []
        return pictureLinks

    def getArtistTopTrack(self):
        artistTopTrack = {}
        if self.getArtistID():
            # Prepare the URL to perform the GET to the API
            urlToSend = "https://api.spotify.com/v1/artists/" + self.getArtistID() + "/top-tracks" + "?country=FR"
            # Send the request
            response = self.request(urlToSend)
            # Get the most populare song
            artistTopTrack[response['tracks'][0]['name']] = response['tracks'][0]['preview_url']
        return artistTopTrack

    def createBase64ID(self):
        encodedID = pybase64.standard_b64encode((self.client_id + ":" + self.client_secret).encode('ascii'))
        return encodedID.decode()

    def getToken(self):
        urlToSend = "https://accounts.spotify.com/api/token"
        payload = "grant_type=client_credentials&undefined="
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization': "Basic " + self.base64id,
        }
        response = self.post(urlToSend, payload, headers)
        return response['access_token']

#







