import socket

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