# Drocsid
Discord malware

### Steps to run the bot :

after cloning the repo create a '.env' file under /src and fill in the required secrets in the following format (ignoring the {}) :

  {NAME} = {VALUE}
  
Current Secrets required : 

  DISCORD_TOKEN - The token of the bot, ask somone to provide it.
  
  DISCORD_CHANNEL_ID - The id of the channel (or guild) that the bot will run on
  by default we are using the Zehus's server but u can change it to you channel id (dont forget to add the bot to the channel first)

  DISCORD_GUILD_ID - used in creating text channels per client

### Adding new feature!

  add you new feature to /features/myfeature.py

  at /main.py import ur new feature as such : from features.myfeature import *

  add you feature to the bot code as such :
    @bot.command()
    async def myfeature(ctx):
        myfeaturefunctions()
        .
        .
  update the !get_help command, for example :
      .
      .
      "!myfeature-> my features does something\n "
                       "Usage: !myfeatureusage\n\n"
      .
      .
      

  
  
    

