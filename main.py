from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message
from responses import get_response  # Import response handler

# Load environment variables
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Set multiple allowed channel IDs in order: humans, testing server, balls...
ALLOWED_CHANNEL_IDS = [1349758355610144880, 1349826852696359012, 1350138786532560969] 

# Bot setup with proper intents
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Function to send responses
async def send_message(message: Message, user_message: str) -> None:
    """Handles message sending while ensuring responses are only for valid commands"""

    if not user_message.startswith("?"):
        return  # Ignore messages that don't start with '?'

    command = user_message[1:]  # Remove '?' to process the actual command

    try:
        response = await get_response(message, command)  # Pass message & command to response function

        if response:
            await message.channel.send(response)  # Send response in the allowed channel
    except Exception as e:
        print(f"Error sending message: {e}")

# Event: Brainrot-chan terminal message
@client.event
async def on_ready() -> None:
    print(f'✅ {client.user} is now running! Only responding in channels: {ALLOWED_CHANNEL_IDS}')

# Event: Message handling (Restrict bot to multiple allowed channels & only respond to '?commands')
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return  # Ignore brainchans own messages

    if message.channel.id not in ALLOWED_CHANNEL_IDS:  # Check if message is in allowed channels
        return  # Ignore messages from other channels

    user_message: str = message.content

    await send_message(message, user_message)  # Process message only if it starts with '?'

# Main function to run the brainrot-chan
def main() -> None:
    if not TOKEN:
        print("DISCORD_TOKEN is missing in your .env file!")
        return

    client.run(TOKEN)

if __name__ == '__main__':
    main()
