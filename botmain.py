import aiml

k = aiml.Kernel()
k.learn("startup.xml")
k.respond("load aiml")

print("########################################################\n")
print(k.respond("bot start"))

# Loop forever, reading user input from the command
# line and printing responses.
while True: print(k.respond(input("> ")))
