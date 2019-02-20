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

from EventfulClient import EventfulClient

myEventfulClient = EventfulClient()


class Event:
    def __init__(self, response, eventNumber):
        self.name = myEventfulClient.getName(response, eventNumber)
        self.description = myEventfulClient.getDescription(response, eventNumber)
        self.latitude = myEventfulClient.getLatitude(response, eventNumber)
        self.longitude = myEventfulClient.getLongitude(response, eventNumber)
        self.address = myEventfulClient.getAddress(response, eventNumber)
        self.zipCode = myEventfulClient.getZipCode(response, eventNumber)
        self.eventfulLink = myEventfulClient.getEventfulLink(response, eventNumber)
        self.eventfulID = myEventfulClient.getEventfulID(response, eventNumber)
        self.cityName = myEventfulClient.getCityName(response, eventNumber)
        self.countryName = myEventfulClient.getCountryName(response, eventNumber)
        self.eventStartTime = myEventfulClient.getEventStartTime(response, eventNumber)
        self.duration = myEventfulClient.getDuration(response, eventNumber)
        self.venueName = myEventfulClient.getVenueName(response, eventNumber)
        self.artist = myEventfulClient.getArtist(response, eventNumber)
        self.details = None
        self.image = None

    def createDictFromVariable(self):
        return {'eventfulID':self.eventfulID,
                'event-name': self.name,
                'description': self.description,
                'latitude': self.latitude,
                'longitude': self.longitude,
                'venue-name': self.venueName,
                'address': self.address,
                'zipcode': self.zipCode,
                'city-name': self.cityName,
                'country-name': self.countryName,
                'event-start-time': self.eventStartTime,
                'duration': self.duration,
                'artist': self.artist,
                'eventful-link': self.eventfulLink,
                }

    def fillDetails(self,id):
        self.details = myEventfulClient.getEventDetails(id)
        self.image = myEventfulClient.getEventImage(id)




