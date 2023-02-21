from keep_alive import keep_alive
import discord
import os
import requests
import json
import random
import openai
import discord

import nest_asyncio
nest_asyncio.apply()


#load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_KEY = os.getenv('OPENAI_KEY')

# Set up the OpenAI API client
openai.api_key = OPENAI_KEY

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person!"
]
prompt= "cheer me up"
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
    
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))
    
  # Mention the client user
  if prompt in message.content: #client.user in message.mentions:  
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,  #f"{message.content}",
    max_tokens=150,
    temperature=0.8,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.3,
    stop=["\n"]
    )
    # Send the response as a message
    await message.channel.send(response.choices[0].text)
    
keep_alive()
client.run(os.getenv('DISCORD_TOKEN'))  # #'MTA3NzE0NTk1NTczODA3MTA2MA.GD2rpA.5S_yKWGf5fDNxtM9LlVJxttpNeN71dPZkl5UMs'