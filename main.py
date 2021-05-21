import discord
import os
import requests
import ast

client = discord.Client()
token = os.environ['TOKEN']
d = {}

@client.event
async def on_ready():
  print('Bot {0.user}'.format(client) + 'is ready for use')

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello! {0.author}'.format(message) + ' this is skynet')
  
  if message.content.startswith('$quiz'):
    response = requests.get('https://opentdb.com/api.php?amount=1')
    s = response.content.decode("utf-8")
    global d
    d = ast.literal_eval(s)
    question = d['results'][0]['question']
    answers = d['results'][0]['incorrect_answers']
    answers.append(d['results'][0]['correct_answer'])
    await message.channel.send(question + ':\n')
    await message.channel.send('Type out your answer number from the following:\n')
    for i in range(len(answers)):
      await message.channel.send(str(i) + ". " + answers[i] + '\n')
    await message.channel.send('Type out your answer as $answer <num>\n') 

  if message.content.startswith('$answer'):
    if message.content[-1] == str(len(d['results'][0]['incorrect_answers']) - 1):
      await message.channel.send('Correct answer\n') 
    else:
      await message.channel.send('Incorrect answer\n')
       

client.run(token)
