'''
Author: @Teemu
Date: 19.11.2020
'''


import os
import spotipy
import datetime
from datetime import datetime, timedelta
from threading import Timer

from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv()

x = datetime.today()
y = x.replace(day=x.day, hour=6, minute=0, second=0, microsecond=0) + timedelta(days=1)
delta_t = y - x

secs = delta_t.total_seconds()

def main():
	spotify_user = os.environ.get("SPOTIPY_CLIENT_USERNAME")
	spotify_scope = "playlist-modify-private playlist-modify-public"
	oauth = SpotifyOAuth(username=spotify_user, scope=spotify_scope)
	user_token = oauth.get_access_token(as_dict=False)

	spotify = spotipy.Spotify(auth=user_token)
	id = "20TwbfnWDzKClpUOiCWQZs"

	playlist = spotify.playlist_items(playlist_id=id)

	ShowList = [
		"https://open.spotify.com/show/1410RabA4XOqO6IV8p0gYF", #FT News Briefing
		"https://open.spotify.com/show/3dB6pl9tTWQiVlk96F4QOb", #Numbers by Barron's
		"https://open.spotify.com/show/5cOfqdkomvzyhPTR7n6KFa",	#Thoughts on the Market
		"https://open.spotify.com/show/05uLjJxkVgQsRk8LWLCLpx",	#Wall Street Breakfast 		klo 15
		"https://open.spotify.com/show/5D0lxDwv8xqBWgG2G95ysR",	#Mad Money w/ Jim Cramer
		"https://open.spotify.com/show/1WOja8nmm4IuS9QK6rEyJI",	#Marketplace Morning Report	3x päivässä
		"https://open.spotify.com/show/4ysyyH8E37tOoes4jhLVAc",	#Rahapodi
		"https://open.spotify.com/show/6A9Ckx3Mn521m1fAQXbYFD",	#InderesPodi
		"https://open.spotify.com/show/7akL7A9jeT1QCJXtLnfk47",	#Leadcast
		"https://open.spotify.com/show/08c8y61kd8eW68bNVzdb6H"	#Stock Club
		]

	oldlist=[]
	response = spotify.playlist_items(id,fields='items.track.uri')

	for x in range(len(response['items'])):
		try:
			asd = (response['items'][x]['track']['uri'])
			oldlist.append(asd)
		except TypeError:
			pass


	spotify.playlist_remove_all_occurrences_of_items(id,oldlist)

	for i in range(len(ShowList)):
		print(str(i)+" "+spotify.show_episodes(ShowList[i])['items'][0]['name'])
		spotify.playlist_add_items(id, [spotify.show_episodes(ShowList[i])['items'][0]['uri']])

	'''
	for j in range(len(playlist['items'])):
		old_episode = playlist['items'][j]['track']
		new_episode = spotify.show_episodes(ShowList[j])['items'][0]
	
	
		if new_episode['name'] != old_episode['name']:
			spotify.playlist_remove_all_occurrences_of_items(id, [old_episode['uri']])
			spotify.playlist_add_items(id, [new_episode['uri']],position=0)
			print("Removed episode: " + old_episode["name"])
			print("Added episode: " + new_episode["name"])
	'''


	#print(pprint.pformat(playlist['items'][0]['track']))

	message = "Updated on: "+str(datetime.datetime.today())
	spotify.playlist_change_details(playlist_id=id,description=message)
	print(message)



t = Timer(secs, main)
t.start()