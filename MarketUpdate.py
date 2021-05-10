'''
Author: @Teemu
Date: 19.11.2020
'''


import os
import time

import spotipy
import datetime
import schedule
from datetime import datetime

from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv()


def main():
	spotify_user = os.environ.get("SPOTIPY_CLIENT_USERNAME")
	spotify_scope = "playlist-modify-private playlist-modify-public"
	oauth = SpotifyOAuth(username=spotify_user, scope=spotify_scope)
	user_token = oauth.get_access_token(as_dict=False)

	spotify = spotipy.Spotify(auth=user_token)
	id = "20TwbfnWDzKClpUOiCWQZs"

	playlist = spotify.playlist_items(playlist_id=id)


	ShowList = [
		"https://open.spotify.com/show/1410RabA4XOqO6IV8p0gYF",  # FT News Briefing
		"https://open.spotify.com/show/3dB6pl9tTWQiVlk96F4QOb",  # Numbers by Barron's
		"https://open.spotify.com/show/5cOfqdkomvzyhPTR7n6KFa",  # Thoughts on the Market
		"https://open.spotify.com/show/05uLjJxkVgQsRk8LWLCLpx",  # Wall Street Breakfast 		klo 15
		"https://open.spotify.com/show/1WOja8nmm4IuS9QK6rEyJI",  # Marketplace Morning Report	3x päivässä
		"https://open.spotify.com/show/5D0lxDwv8xqBWgG2G95ysR",  # Mad Money w/ Jim Cramer
		"https://open.spotify.com/show/4ysyyH8E37tOoes4jhLVAc",  # Rahapodi
		"https://open.spotify.com/show/6A9Ckx3Mn521m1fAQXbYFD",  # InderesPodi
		"https://open.spotify.com/show/7akL7A9jeT1QCJXtLnfk47",  # Leadcast
		"https://open.spotify.com/show/08c8y61kd8eW68bNVzdb6H"  # Stock Club
		]

	oldlist = []
	response = spotify.playlist_items(id, fields='items.track.uri')

	for x in range(len(response['items'])):
		try:
			asd = (response['items'][x]['track']['uri'])
			oldlist.append(asd)
		except TypeError:
			pass

	spotify.playlist_remove_all_occurrences_of_items(id, oldlist)
	print("MarketUpdate.py succesfully cleared old playlist tracks @ " + str(datetime.utcnow()))

	for i in range(len(ShowList)):
		print("Added playlist item: " + str(i) + " " + spotify.show_episodes(ShowList[i])['items'][0][
			'name'] + " at " + str(datetime.utcnow()))
		spotify.playlist_add_items(id, [spotify.show_episodes(ShowList[i])['items'][0]['uri']])


	message = "Updated on: " + str(str(datetime.utcnow()))
	spotify.playlist_change_details(playlist_id=id, description=message)
	print(message)
	print("--------------------------------------------------------------------------------")

print("MarketUpdate.py started succesfully at " + str(datetime.utcnow()))
print("--------------------------------------------------------------------------------")
schedule.every(6).hours.at(":01").do(main)
while 1:
	schedule.run_pending()
	time.sleep(1)