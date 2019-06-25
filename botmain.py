import aiml
import os
import requests
import json
import time
import socket
CACHE_FNAME = 'cache.json'

k = aiml.Kernel()
k.verbose(False)
k.learn("startup.xml")
k.respond("load aiml")

print("########################################################\n")
print(k.respond("bot start"))

# Loop forever, reading user input from the command
# line and printing responses.


apiKeyMap = "AIzaSyDu6_IvvOAWebssopk0c5HovtSGyi5E_rw"
baseUrlMap = "https://maps.googleapis.com/maps/api/distancematrix/json?"

try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

# CACHE FUNCTION FOR GOOGLE GEOCODING API
def apiMapCache(baseUrlMap, orig, dest):
	params = {
		'units': 'imperial',
		'origins': orig,
		'destinations': dest,
		'key': apiKeyMap
	}
	req = requests.Request(method='GET', url=baseUrlMap, 
		params=sorted(params.items()))
	prepped = req.prepare()
	fullURL = prepped.url

	# Check to see if request exists in cache
	if fullURL not in CACHE_DICTION:
	# make the request and store the response
		response = requests.Session().send(prepped)
		CACHE_DICTION[fullURL] = response.text

	# Update cache file
	cache_file = open(CACHE_FNAME, 'w')
	cache_file.write(json.dumps(CACHE_DICTION))
	cache_file.close()

	# Return cache file
	return CACHE_DICTION[fullURL]


# RESPONSE UNWRAPPER FOR GOOGLE GEOCODING API
def unwrapMapApi(json):
	res = {}
	res['duration'] = json['rows'][0]['elements'][0]['duration']['text']
	res['distance'] = json['rows'][0]['elements'][0]['distance']['text']
	res['origin'] = json['origin_addresses'][0]
	res['destination'] = json['destination_addresses'][0]
	return res


def learnMap(orig, dest):
	try:
		#print(json.loads(apiMapCache(baseUrlMap, orig, dest)))
		res = unwrapMapApi(json.loads(apiMapCache(baseUrlMap, orig, dest)))
		return 'It takes about {duration} to drive {distance} from {origin} to {destination}.'.format(duration= res['duration'], distance=res['distance'], origin=res['origin'], destination=res['destination'])
	except Exception as e:
		return e
k.addPattern("HOW LONG DOES IT TAKE TO DRIVE FROM {orig} TO {dest}?", learnMap)

# CHECK INTERNET CONNECTION
def checkInternet():
	try:
		# connected
		socket.create_connection(("www.google.com", 80))
		return True
	except:
		# no internet
		pass
	return False


ternet = False
while(True):
	user_input = input("> ")
	if (checkInternet() != True):
		if ternet == False:
			ternet = True
			print ("RaiseAI Lost Connection to Internet. \n All following prompts are cache-dependent until noted otherwise.")
	else:
		if ternet == True:
			ternet = False
			print ("RaiseAI Regained Connection to Internet.")

	if user_input == "exit":
		print ("RaiseAI Shutting Down. Good Bye.")
		break
	else:
		print(k.respond(user_input))
