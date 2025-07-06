import discord
import requests
import json
import asyncio
from random import choice
from blackjack_game import blackjack  # Import the Blackjack function
from openai import OpenAI
import os

# Load the API key from environment variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Create an OpenAI client instance configured for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,

)

# List of features
list_of_features = "?game for BlackJack\n?inspire for Inspirational Quotes!\n?fun for fun inputs!"
fun_commands = "🌟 ?hello\n🌟 ?bye\n🌟 ?sleep\n🌟 ?smile\n🌟 ?games\n🌟 ?pets\n🌟 ?movies\n🌟 ?cinema"

# List of inspirational quotes
inspirational_quotes = [
    "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    "Hard times create strong people, strong people create good times, good times create weak people, and weak people create hard times. - G. Michael Hopf",
    "Do not pray for an easy life. Pray for the strength to endure a difficult one. - Bruce Lee",
    "A person is not defeated when they lose, they are defeated when they give up. - Richard Nixon",
    "With great power comes great responsibility. - Uncle Ben",
    "To be, or not to be, that is the question. - William Shakespeare"
]

# AI System Prompt for Friendly Anime Character
AI_PROMPT = """Your name is Ralsei, a friendly anime-style virtual assistant. You have blue hair, You are cheerful, kind, and helpful to everyone. You enjoy making people smile and helping with questions. You know about games, movies, and fun activities. Always stay positive and friendly in your responses.

Your favorite music artist is Miku, you like Studio Ghibli movies. You love games and cute animals. Keep your answers appropriate for all ages. Type in normal sentence case with proper spelling. Keep answers around 100 characters for simple questions, up to 2000 for more complex ones.

Always be welcoming and helpful!

User: "Hello"
You: "Hello there! How are you doing today? :)"

User: "How are you?"
You: "I'm doing great, thanks for asking! Just happy to be here helping out."


async def get_response(message, user_input: str):
    """Handles different bot responses based on user input"""
    
    lowered = user_input.lower()

    responses = {
        "fun": fun_commands,
        "help": f"🌟 Need some help? Here's what I can do: 🌟\n{list_of_features}\nLet me know how I can help! 🌟",
        "hello": "Hello there! Nice to see you! 😊",
        "bye": "Goodbye! Have a wonderful day!",
        "sleep": "Time to rest!",
        "inspire": f"📜 **Inspirational Quote:** {choice(inspirational_quotes)}"
    }

    if lowered in responses:
        return responses[lowered]

    if lowered in image_responses:
        await message.channel.send(image_responses[lowered])
        return None

    if lowered == "game":
        await blackjack(message)
        return None

    return await chat_with_ai(user_input)
