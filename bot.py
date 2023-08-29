import discord
import keyring

intents = discord.Intents.default()  
intents.message_content = True  

class MyClient(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)

    async def on_ready(self):
        print('Logged on as {0}'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.content == '?regras':
            await message.channel.send('Olá!')
            return

client = MyClient(intents)
client.run('MTE0NTAxODA0ODEyNjkyMjc1NA.G_ysne.9GzVYtLK_pzSG0J9DYZWgDeJfHg3Loi9D7PzzA')



