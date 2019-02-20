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

import xmltodict
import requests
import urllib.parse

class MusicBrainzClient:
    def __init__(self, artist):
        self.artist = artist
        self.response = self.search(self.artist)

    def search(self, artist):
        # Create an URL with the right format
        urlToSend = "http://musicbrainz.org/ws/2/artist/?query=artist:" + self.urlEncode(artist)
        response = requests.get(urlToSend)
        response = xmltodict.parse(response.content)
        if type(response['metadata']['artist-list']['artist']) != list:
           response['metadata']['artist-list']['artist'] = dict(response['metadata']['artist-list']['artist'])

    def urlEncode(self, data):
        myUrl = urllib.parse.quote(data)
        return myUrl

    def getArtistID(self):
        try:
            artistID = self.response['metadata']['artist-list']['artist'][0]['@id']
        except KeyError:
            artistID = None
        except TypeError:
            artistID = None
        return artistID

    def getArtistGender(self):
        try:
            gender = self.response['metadata']['artist-list']['artist'][0]['gender']
        except KeyError:
            gender = None
        except TypeError:
            gender = None
        return gender

    def getArtistCountry(self):
        try:
            artistCountry = self.response['metadata']['artist-list']['artist'][0]['area']['name']
        except KeyError:
            artistCountry = None
        except TypeError:
            artistCountry = None
        return artistCountry

    def getArtistType(self):
        try:
            artistType = self.response['metadata']['artist-list']['artist'][0]['@type']
        except KeyError:
            artistType = None
        except TypeError:
            artistType = None
        return artistType


    def getArtistBirthDate(self):
        try:
            artistBirthDate = self.response['metadata']['artist-list']['artist'][0]['life-span']['begin']
        except KeyError:
            artistBirthDate = None
        except TypeError:
            artistBirthDate = None
        return artistBirthDate

    def getArtistPlaceOfBirth(self):
        try:
            artistPlaceOfBirth = self.response['metadata']['artist-list']['artist'][0]['begin-area']['name']
        except KeyError:
            artistPlaceOfBirth = None
        except TypeError:
            artistPlaceOfBirth = None
        return artistPlaceOfBirth
