# (っ◔◡◔)っ 📅  Planner Telegram Bot

### This bot is a great helper in planning tasks for a certain date.
### Also, it will not let you forget about your plans, because it will remind you about the tasks that have not been completed yet.



## <span style="color:DarkRed">Adjust the bot</span>


### Create '.env' file based on '.env.default'
```bash
cp .env.default .env
```
#### You will need:
* create a new bot in Telegram (use BotFather);
* get a token and assign its value to the TELEBOT_TOKEN variable in the .env file


### Install deps
```bash
pipenv sync

# Activate the environment
pipenv shell
```


### Create the database
 * run the file <span style="color:green">models.py</span>


### Start the bot
 * run the file <span style="color:green">bot.py</span>


### Go to Telegram and start using your bot 
 * after finding your bot in Telegram by bot name

============================================================

## <span style="color:DarkGreen">List of available bot commands</span>

  * **/start** - welcome message
  * Create and save a task when you enter text in the message field
  * *task_id* **done** - when entering this message, the task is marked as completed
  * **/today**, **/t** - list of all tasks for today

  
  







============================================================
### Libraries: 
   - pytelegrambotapi
   - peewee
   - schedule 

============================================================
