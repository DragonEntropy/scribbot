import discord
import os
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()

activeList = []

def compileList(method):
    firstWord = True
    outputList = ""
    for word in activeList:
        if firstWord == True:
            outputList = word
            firstWord = False
        else:
            if method == "comma":
                outputList += ", " + word
            elif method == "line":
                outputList += "\n" + word
    return outputList

multiAdd = []

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):

    #Defining the bot output function
    async def addWord(word):
        print(activeList)
        if word in activeList:
            await message.channel.send("*" + word + "* is already in this list")
        else:
            activeList.append(word)
            await message.channel.send("*" + word + "* was added to the list")
        return activeList

    if message.author == client.user:
        return

    #Help
    if message.content.startswith("$help"):
        await message.channel.send("""
Below is the current list of available commands:
    **$help**: Displays a list of available commands
    **$add** *<entry>*: Enters a new word into the active list
    **$clear**: Clears the active list
    **$list**: Displays the words in the active list
    **$load**: Loads a saved list
    **$multi**: Toggles the ability to add words to the active list without using $add
    **$save** *<name>*: Saves the active list
    **$remove** *<entry>*: Removes a word from the active list
            """)

    #Adds words to the scribble list
    if message.content.startswith("$add"):
        string = message.content[5:]
        await addWord(string)

    #Outputs the list into chat
    if message.content.startswith("$list"):
        outputList = compileList("comma")
        print(outputList)
        await message.channel.send(outputList)

    #Allows the user to toggle multi add
    if message.content.startswith("$multi"):
        if message.author in multiAdd:
            multiAdd.remove(message.author)
            await message.channel.send("You can no longer multi add")
        else:
            multiAdd.append(message.author)
            await message.channel.send("You can now multi add")    
    #Multi add functionality
    if message.author in multiAdd:
        if message.content.startswith("$") == False:
            await addWord(message.content)

    #Remove function
    if message.content.startswith("$remove"):
        string = message.content[8:]
        global activeList
        if string in activeList:
            activeList.remove(string)
            await message.channel.send("*" + string + "* was removed from the list")
        else:
            await message.channel.send("*" + string + "* could not be found in the list")
    #Clear list function
    if message.content.startswith("$clear"):
        firstWord = False
        activeList = []
        await message.channel.send("The list was cleared!")

    #Saves the list
    if message.content.startswith("$save"):
        fileName = message.content[6:]
        file = open(fileName + ".text", "w")
        outputList = compileList("line")
        file.write(outputList)
        file.close()
        await message.channel.send("The list was saved as **" + fileName + "**")
    #Loads a saved list
    if message.content.startswith("$load"):
        fileName = message.content[6:]
        try:
            file = open(fileName + ".text", "r")
            rawList = file.readlines()
            print(rawList)
            activeList = []
            for line in rawList:
                print(line.strip())
                activeList.append(line.strip())
            await message.channel.send("The list **" + fileName + "** has been loaded successfully!")
            return activeList
        except IOError:
            await message.channel.send("The list **" + fileName + "** was not found!")

    #Bad bot
    if message.content.lower() == "bad bot":
        await message.channel.send("Sorry ;_;")

client.run(os.getenv('TOKEN'))   
    
