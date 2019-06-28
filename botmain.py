import aiml
import botcore.map as map
import botcore.util as util


k = aiml.Kernel()
k.verbose(False)
k.learn("startup.xml")
k.respond("load aiml")

print("########################################################\n")
print(k.respond("bot start"))

k.addPattern("HOW LONG DOES IT TAKE TO DRIVE FROM {orig} TO {dest}?", map.learnMap)

ternet = False
while(True):
	user_input = input("> ")
	if (util.checkInternet() != True):
		if ternet == False:
			ternet = True
			print ("Kivis Lost Connection to Internet. \n All following prompts are cache-dependent until noted otherwise.")
	else:
		if ternet == True:
			ternet = False
			print ("Kivis Regained Connection to Internet.")

	if user_input == "exit":
		print ("Kivis Shutting Down. Good Bye.")
		break
	else:
		print(k.respond(user_input))
