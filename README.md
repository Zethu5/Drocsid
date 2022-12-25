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
      
[ספר פרוייקט.docx](https://github.com/Zethu5/Drocsid/files/10299786/default.docx)


![image](https://user-images.githubusercontent.com/19743731/209463269-47dc5483-74cf-4134-b428-42d0697bfdf1.png)

  
![image](https://user-images.githubusercontent.com/19743731/209463270-b3f3b568-81fd-4197-8fdb-4bc46c291689.png)

    
![image](https://user-images.githubusercontent.com/19743731/209463289-44b20444-1ab5-44f1-8b6a-7b340cb3a9c7.png)


![image](https://user-images.githubusercontent.com/19743731/209463294-ef43a328-5bcb-4028-ab80-e6248c00b897.png)

