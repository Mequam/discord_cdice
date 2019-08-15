#!/usr/bin/python3.7
import discord
import cdice
import validate
from math import floor
from math import ceil
#print(discord.__version__)  # check to make sure at least once you're on the right version!

#this function parses a single rolling sequence of [-expr[D] [-expr[D]...]] <expr>
def strip(string):
    while string[-1] == '0' or string[-1] == '.':
        string = string[0:-1]
        if string[-1] == '.':
            string = string[0:-1]
            break
    return string
def parse_seq(seq,buff):
    #buff is a refrence to a string that we use to store the output of the function
    #the user wants to run a cdice program
    if seq[0][0] == 'x':
        #defualt our delimiter to spaces
        delimiter = ' '
        end = len(seq[0])
        if 'B' in seq[0]:
            #they want to change the default delimiter
            #so parse out the delimiter
            if seq[0][-1] == 'B':
                #they gave us the D symbol without a delimiter so we use \n
                delimiter = '\n'
            else:
                delimiter = seq[0][seq[0].find('B')+1:len(seq[0])]
            end = seq[0].find('B')
        for i in range(0,int(cdice.parse(seq[0][1:end]))):
            parse_seq(seq[1:len(seq)],buff)
            buff[0] += delimiter
    else:
        buff[0] += strip(str(cdice.parse(seq[0])))
#this function uses the above function with a list of arguments to and runs it foreach expression in the argument
def eval_roll(args):
    buff = ['']
    last = 0
    for i in range(0,len(args)):
        if args[i][0] != 'x':
            print('[*] parsing sequence:' + str(args[last:i+1]))
            parse_seq(args[last:i+1],buff)
            last = i+1
    return buff[0]

#initilise all of the variables found inside of text files
f = open('token.txt','r')
token = f.readline()[0:-1]
f.close()
f = open('help/help1.txt','r')
data = f.readline()
help1 = data
while data:
    data = f.readline()
    help1+=data
f.close()
f = open('help/help2.txt')
data = ''
data = f.readline()
help2 = data
while data:
    data = f.readline()
    help2 += data
f.close()
#this is the code that we use to interface with discord
client = discord.Client()  # starts the discord client.
stop = False #global variable
@client.event  
# event decorator/wrapper. More on decorators here: https://pythonprogramming.net/decorators-intermediate-python-tutorial/
async def on_ready():  # method expected by client. This runs once when connected
    print(f'[*] connected to Discord as {client.user}')  # notification of login.

@client.event
async def on_message(message):  # event that happens per any message
    #store the split message content into args becuse im lazy and prefer to type args
    args = message.content.split(' ')
    #if the first argument is cdice they want to run the cdice program
    if args[0] == 'cdice':
        if len(args) > 1:
            #we have arguments
            if args[1] == 'help':
                page = 1
                if len(args) > 2:
                    page = validate.safe_int(args[2])
                    if page == None:
                        page = 1
                if page == 1:
                    await message.channel.send(help1)
                elif page == 2:
                    await message.channel.send(help2)
            else:
                #they gave the program none help arguments to parse, feed them into our parser
                result = eval_roll(args[1:len(args)])
                if len(result) > 2000:
                    await message.channel.send('sorry, output larger than 2000 :(')
                else:
                    await message.channel.send(result)
        else:
            #they did not give us arguments assume they are rolling a d20
            result = cdice.parse('1d20')
            if result == 20.0 or result == 1.0:
                msg = 'good gravy a ' + strip(str(result))
            else:
                msg = strip(str(result))
            await message.channel.send(msg)
    elif args[0] == 'statmod':
        resp = ''
        for i in range(1,len(args)):
            num = validate.safe_int(args[i])
            if num != None:
                resp += str(floor((num-10)/2)) + ' '
        await message.channel.send(resp)

client.run(token)
