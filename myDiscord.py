import requests
from datetime import datetime
from random import choice
import aiohttp


class myDiscord:
    def __init__(self, authToken, channelID):
        self.channelID = channelID
        self.rSession = aiohttp.ClientSession()
        self.rSession.headers = {"Authorization": authToken}

    async def readMessages(self, limit):
        json = await self.rSession.get(f"https://discord.com/api/v9/channels/{self.channelID}/messages?limit={limit}").json()

        messages = []
        i = 0
        recentAuthor = ""

        for message in json:
            if (not message["content"]):
                continue
            time = (datetime.fromisoformat(message["timestamp"])).strftime("%d %m %Y %X")

            item = message["author"]["username"] + " : " + message["author"]["id"] + " : " + message["content"] + " : " + message["id"] + " : " + time
            messages.append(item)

            # So the author of the most recent message can be stored
            if not i:
                recentAuthor = message["author"]["username"]
                i += 1

        messages.reverse()
        # print(f"Response of retrieving message: {messages}")
        print("Retrieved recent messages successfully.")

        return [messages, recentAuthor]

    async def sendMessage(self, text):
        data = {"content": text}
        json = self.rSession.post(f"https://discord.com/api/v9/channels/{self.channelID}/messages", data=data)
        print(f"Response of sending message: {json.content}")

    async def uploadImage(self, imagePath, message):
        file = open(imagePath, "rb")
        data = {"content": message}

        json = await self.rSession.post(f"https://discord.com/api/v9/channels/{self.channelID}/messages", files={"file": file}, data=data)

        print(f"Response of uploading image: {json.content}")

    async def replyMessage(self, messageID, text):
        data = {"content": text, "message_reference": {
            "message_id": messageID
        }}
        json = await self.rSession.post(f"https://discord.com/api/v9/channels/{self.channelID}/messages", json=data)
        print(f"Response of replying to message: {json.content}")

    async def findGif(self, search):
        # Search for gif
        json = self.rSession.get(f"https://discord.com/api/v9/gifs/search?q={search}&media_format=mp4&provider=tenor").json()

        gifs = []
        for gif in json:
            gifs.append(gif["url"])

        return choice(gifs)

    async def reactToMessage(self, messageID, emojiURLEncode):
        await self.rSession.put(f"https://discord.com/api/v9/channels/{self.channelID}/messages/{messageID}/reactions/{emojiURLEncode}/@me")

    async def showTyping(self):
        await self.rSession.post(f"https://discord.com/api/v9/channels/{self.channelID}/typing")

    async def getOwnInfo(self):
        json = await self.rSession.get("https://discord.com/api/v9/users/@me").json()
        return json

    async def getChatInfo(self):
        json = await self.rSession.get(f"https://discord.com/api/v9/channels/{self.channelID}").json()
        return json
