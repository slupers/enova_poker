#!/usr/bin/python

from urllib import urlencode, urlopen
from urllib2 import HTTPError
#from HTTPException import HTTPException
#import ClientCookie
#import ClientForm
import json
from time import sleep
#import httplib, urllib

def _my_urlencode(data):
	"""Convert provided dictionary to URL-encoded format that the API understands"""
	encoded_data = ""
	for k,v in data.iteritems():
		#value is just an actual value (or something crazy unexpected)
		encoded_data = "".join([encoded_data, quote(unicode(k)), "=", quote(unicode(v)), "&" ])
		return encoded_data


def POST(action=None, param=None,debug=0):
	"""Makes a POST request to API with provided data and returns the decoded JSON response"""
	data = {}
	data["name"] =  "TESTSERLO"#"Serlo"
	data["game_id"] = "664493182"#"653347285"
	data["player_key"] = "5a4c74b9acaceab5e023fbf5e6f06b36"#2bebfe74747b8f34436ba82a4e74b969"
	data["player_action"] = action
	data["parameters"] = param
	
	encoded_data = urlencode(data)

	# construct request URL
	#reqURL = "".join(["http://no-limit-code-em.com/player"])
	reqURL = "http://treydev-poker.herokuapp.com/player"
	
	if debug:
		print "".join(["- Request URL:\n", reqURL])
		print "-"*20
		print "".join(["- Encoded data:\n", encoded_data])
	
	try:
		# load response into a dictionary
		response = urlopen(reqURL,encoded_data)
	except HTTPError as exc:
		print "!!!!",str(exc),"!!!!"
		
	#return response

def GET(debug=0):
	"""Makes a GET request to API with provided data and returns the decoded JSON response"""
	data = {}
	data["name"] =  "TESTSERLO"#"Serlo"
	data["game_id"] = "664493182"#653347285"
	data["player_key"] = "5a4c74b9acaceab5e023fbf5e6f06b36"#2bebfe74747b8f34436ba82a4e74b969"
	
	encoded_data = urlencode(data)

	# construct request URL
	#reqURL = "".join(["http://no-limit-code-em.com/player"])
	reqURL = "http://treydev-poker.herokuapp.com/"
	
	reqURL = "".join([reqURL,"game_state?",encoded_data])
	if debug:
		print "".join(["- Request URL:\n", reqURL])
		print "-"*20
		print "".join(["- Encoded data:\n", encoded_data])
	
	try:
		# load response into a dictionary
		response = json.load(urlopen(reqURL))
	except HTTPError as exc:
		print "!!!!",str(exc),"!!!!"
		
	return response
	
while (1):
	get_response = GET(debug=0)
	replacement = False
	action = ""
	param = ""
	try:
		replacement = get_response["replacement"]
		#print "GET response:", get_response
	except:
		print "---------------------REPLACEMENT FALSE"
		replacement = False
	print "CURRENT PLAYER:",get_response["current_player"]
	stack = get_response["stack"]
	if get_response["play"]:
		print "OUR HAND:",get_response["hand"]
		print "WE ARE IN PLAY----------------------"
		if get_response["bet"] == get_response["min_bet"]:
			print "bet = min_bet"
			action = "bet"
			bet_amount = int(get_response["min_bet"]) + 1
			if bet_amount > stack:
				print "----BET AMOUNT > STACK~~~~~~~~~~"
				bet_amount = stack
			param = bet_amount
		elif get_response["bet"] < get_response["min_bet"]:
			print "bet < min_bet"
			action = "raise"
			bet_amount = int(get_response["min_bet"]) - int(get_response["bet"]) + 1
			if bet_amount > stack:
				print "----BET AMOUNT > STACK~~~~~~~~~~"
				bet_amount = stack
			param = bet_amount
		else:
			print "~~~~~~~~~~~~~~~~~~~~~in else"
		print "--ACTION:",action,"PARAM:",param,"--"
		post_response = POST(action=action,param=param, debug=0)
	elif replacement:
		#hand = get_respone
		print "WE ARE REPLACING-----------------"
		action = "replacement"
		to_replace = "0"
		param = to_replace
		print "--ACTION:",action,"PARAM:",param,"--"
		post_response = POST(action=action,param=param, debug=0)
		#print "POST response:", post_response
	
	sleep(2.5)