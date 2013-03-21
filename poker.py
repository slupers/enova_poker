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

# LOGIC
def pokerLogic(hand):
   string = strongestHand(hand)
   return string


def strongestHand(hand):
   # check for cards of same rank
   sequence = determineSequences(hand)
   length = sequence[0]


   pairs = determineDuplicates(hand)
   suit = determineSameSuit(hand)
   numFirst = pairs[0][1]
   numSecond = pairs[1][1]

   if suit[1] == 5:
       return "Flush"

   elif numFirst == 4:
       return "Four of a Kind"
   elif numFirst == 3:
       if numSecond == 2:
           return "Full House"
       elif suit[1] == 5:
           return "Flush"

       elif length == 5:
           return "Straight"
       else:
           return "Three of A Kind"
   elif numFirst == 2:
       if numSecond == 2:
           return "Two Pair"
       else:
           return "One Pair"
   else:
       return "Nothing"

   # check for cards of same suit








# will need to handle Aces
def determineSequences(hand):
   # determine length of longest sequence
   numbers = getJustNumbers(hand)
   numbers = sequencize(numbers)
   numbers.sort()

   currSeq = []
   maxSeq = []

   max_length = 0
   curr_length = 0
   prev = numbers[0]-1
   for num in numbers:
       if num==(prev+1):
           currSeq.append(num)
           prev = num
           curr_length+=1
       else:
           if curr_length > max_length:
               maxSeq = currSeq
               max_length = curr_length
               curr_length = 1
               currSeq = [num]
               prev = num

   # determine which cards are in longest sequence
   # currently doesn't pick smart if there are duplicates
   cards = []
   for num in list(set(maxSeq)):
       cards.append(toCard(num))

   # return card positions in longest sequence    
   positions = getPositions(hand, cards)

   return (max_length, positions)

# find positions of cards in hand
def getPositionsGivenRank(hand, cards):
   positions = []
   for char in cards:
       position = 1
       for card in hand:
           if char == card[0]:
               positions.append(position)
               position+=1
           else:
               position+=1

   return positions

def getPositionsGivenSuit(hand, cards):
   positions = []
   for char in cards:
       position = 1
       for card in hand:
           if char == card[1]:
               positions.append(position)
               position+=1
           else:
               position+=1

   return positions

# returns two most common card ranks as a list [(tuple1, (tuple2)]
def determineDuplicates(hand):
   numbers = getJustNumbers(hand)
   counter = collections.Counter(numbers)
   mostcommoncard = counter.most_common(2)
   return mostcommoncard

# returns most common suit occurrence as a tuple (suit, #occurrences)
def determineSameSuit(hand):
   suits = getJustSuits(hand)
   counter = collections.Counter(suits)    
   mostcommonsuit = counter.most_common(1)

   return mostcommonsuit[0]

def sequencize(numbers):
   sequenced=[]
   for card in numbers:
       sequenced.extend(toNum(card))
   return sequenced

def toNum(card):
   if card=="T":
       return [10]
   elif card=="J":
       return [11]
   elif card=="Q":
       return [12]
   elif card=="K":
       return [13]
   elif card=="A":
       return [1,14]
   else:
       return [ord(card)-48]

def toCard(num):
   if num==10:
       return "T"
   elif num==11:
       return "J"
   elif num==12:
       return "Q"
   elif num==13:
       return "K"
   elif num==14 or num==1:
       return "A"
   else:
       return chr(num+48)


def getJustSuits(hand):
   suits=[]
   for element in hand:
       suits.append(element[1])
   return suits

def getJustNumbers(hand):
   numbers=[]
   for element in hand:
       numbers.append(element[0])
   return numbers

def switchCards():
   pass

def bet(amount):
   pass

def POST(action=None, param=None,debug=0):
	"""Makes a POST request to API with provided data and returns the decoded JSON response"""
	data = {}
	data["name"] =  "TESTSERLO"#"Serlo"
	data["game_id"] = "664493182"#"653347285"5a4c74b9acaceab5e023fbf5e6f06b36
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
	data["game_id"] = "664493182"#653347285"5a4c74b9acaceab5e023fbf5e6f06b36
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
	
luck = pokerLogic(["Ac","Kc","Qc","Jc","9c"])
raise	
while (1):
	get_response = GET(debug=0)
	luck = ""
	replacement = False
	action = ""
	param = ""
	try:
		replacement = get_response["replacement"]
		#print "GET response:", get_response
	except:
		print "---------------------REPLACEMENT FALSE"
		replacement = False
	#print "CURRENT PLAYER:",get_response["current_player"]
	stack = get_response["stack"]
	if get_response["play"]:
		print "OUR HAND:",get_response["hand"]
		try:
			hand = get_response["hand"]
			luck = pokerLogic(hand)
		except:
			print "MESSED UP HAND CHECK"
		print "WE ARE IN PLAY----------------------"
		if get_response["bet"] == get_response["min_bet"]:
			print "bet = min_bet"
			action = "bet"
			bet_amount = int(get_response["min_bet"]) + 1
			#if luck != "Nothing" and "Pair" not in luck:
			#	bet_amount = (bet_amount*2)-2
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
		try:
			hand = get_response["hand"]
			luck = pokerLogic(hand)
		except:
			print "MESSED UP HAND CHECK"
		print "WE ARE REPLACING-----------------"
		action = "replacement"
		to_replace = "0"
		if luck == "Nothing":
			to_replace = "123"
		param = to_replace
		print "--ACTION:",action,"PARAM:",param,"--"
		post_response = POST(action=action,param=param, debug=0)
		#print "POST response:", post_response
	
	sleep(2.5)