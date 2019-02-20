#!/usr/bin/python
# coding=utf-8
import json

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


class EventfulClient:
    def __init__(self):
        self.appKey = "crQ4GmtSRMvm9bMV"

    def search(self, latitude, longitude, radius):
        response = requests.get("http://api.eventful.com/json/events/search"
                                "?app_key=" + self.appKey +
                                "&where=" + latitude + "," + longitude +
                                "&within=" + radius +
                                "&units=km"
                                "&category=festivals_parades,music"
                                "&sort_order=popularity"
                                "&page_size=50"
                                )

        events = json.loads(response.text)
        return events

    def getEventDetails(self, eventID):
        responseDetails = requests.get("http://api.eventful.com/json/events/get"
                                "?app_key=" + self.appKey +
                                "&id=" + eventID
                                )
        details = json.loads(responseDetails.text)
        return details

    def getEventImage(self, eventDetails):
        try:
            if type(eventDetails['images']['image']) == list:
                return eventDetails['images']['image'][0]['medium']['url']
            else:
                return eventDetails['images']['image']['medium']['url']
        except TypeError:
            return None

    def getNumberOfEvent(self, response):
        return response['page_size']

    def getNumberOfItems(self, response):
        return response['total_items']

    def getName(self, response, eventNumber):
        try:
            name = response['events']['event'][eventNumber - 1]['title']
        except (TypeError,IndexError):
            name = None
        return name

    def getDescription(self, response, eventNumber):
        try:
            description = response['events']['event'][eventNumber - 1]['description']
        except (TypeError,IndexError):
            description = None
        return description

    def getLatitude(self, response, eventNumber):
        try:
            latitude = response['events']['event'][eventNumber - 1]['latitude']
        except IndexError:
            latitude = None
        return latitude

    def getLongitude(self, response, eventNumber):
        try:
            longitude = response['events']['event'][eventNumber - 1]['longitude']
        except IndexError:
            longitude = None
        return longitude

    def getAddress(self, response, eventNumber):
        try:
            address = response['events']['event'][eventNumber - 1]['venue_address']
        except IndexError:
            address = None
        return address

    def getZipCode(self, response, eventNumber):
        try:
            zipCode = response['events']['event'][eventNumber - 1]['postal_code']
        except IndexError:
            zipCode = None
        return zipCode

    def getEventfulLink(self, response, eventNumber):
        try:
            url = response['events']['event'][eventNumber - 1]['url']
        except IndexError:
            url = None
        return url

    def getCityName(self, response, eventNumber):
        try:
            city = response['events']['event'][eventNumber - 1]['city_name']
        except IndexError:
            city = None
        return city

    def getCountryName(self, response, eventNumber):
        try:
            country = response['events']['event'][eventNumber - 1]['country_name']
        except IndexError:
            country = None
        return country

    def getEventStartTime(self, response, eventNumber):
        try:
            startTime = response['events']['event'][eventNumber - 1]['start_time']
        except IndexError:
            startTime = None
        return startTime

    def getDuration(self, response, eventNumber):
        try:
            duration = response['events']['event'][eventNumber - 1]['all_day']
        except IndexError:
            duration = None
        return duration

    def getVenueName(self, response, eventNumber):
        try:
            venueName = response['events']['event'][eventNumber - 1]['venue_name']
        except IndexError:
            venueName = None
        return venueName

    def getEventfulID(self, response, eventNumber):
        try:
            eventfulId = response['events']['event'][eventNumber - 1]['id']
        except IndexError:
            eventfulId = None
        return eventfulId

    def getArtist(self, response, eventNumber):
        myList = []
        try:
            if response['events']['event'][eventNumber - 1]['performers']:
                for element in (response['events']['event'][eventNumber - 1]['performers']).values():
                    if type(element) == list:
                        for artist in element:
                            myList.append(artist['name'])
                    else:
                        myList.append(element['name'])
        finally:
            return myList
