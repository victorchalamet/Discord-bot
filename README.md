# Discord music bot
This is an example of a discord music bot that support multiple commands:
```
!help - Display all the available commands.
!play <url> - Play the Youtube audio. Connect to the voice channel if already not.
!pause - Pause the current audio.
!resume - Resume the current audio.
!skip - Skip the current audio.
!stop - Stop the current audio.
!leave - Leave the voice channel and clear the queue.
!queue - Display the elements in the queue.
!clear - Clear the queue.
```
## How to run your own bot with this code ?
You'll need to create a .env file with this command in the terminal
```bash
touch .env
```
Then create a variable inside this file
```
bot_token = your_bot_token
```
### Where do I get the bot token
I advise you to follow this [video](https://www.youtube.com/watch?v=xdg39s4HSJQ&list=PLzMcBGfZo4-kdivglL5Dt-gY7bmdNQUJu), it'll explain you well how to create a bot on the [Discord Developer Portal](https://discord.com/developers/applications) and then get its token.
