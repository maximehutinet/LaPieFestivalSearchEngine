# !/usr/bin/python
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

from SpotifyClient import SpotifyClient
from MusicBrainzClient import MusicBrainzClient
import json


class Artist:
    def __init__(self, artist):
        mySpotifyClient = SpotifyClient(artist)
        myMusicBrainz = MusicBrainzClient(artist)
        self.artistName = artist
        self.spotifyID = mySpotifyClient.getArtistID()
        self.musicBrainzID = myMusicBrainz.getArtistID()
        self.pictureLinks = mySpotifyClient.getArtistPictures()
        self.artistTopTrack = mySpotifyClient.getArtistTopTrack()
        self.country = myMusicBrainz.getArtistCountry()
        self.type = myMusicBrainz.getArtistType()
        self.gender = myMusicBrainz.getArtistGender()
        self.birthDate = myMusicBrainz.getArtistBirthDate()
        self.placeOfBirth = myMusicBrainz.getArtistPlaceOfBirth()
