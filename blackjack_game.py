import discord
import random

player_money = {}

def get_card_deck():
    return {
        "Ace": 11,
        "King": 10,
        "Queen": 10,
        "Jack": 10,
        "Ten": 10,
        "Nine": 9,
        "Eight": 8,
        "Seven": 7,
        "Six": 6,
        "Five": 5,
        "Four": 4,
        "Three": 3,
        "Two": 2
    }

async def blackjack(message):
    global player_money
    channel = message.channel
    user = message.author

    if user.id not in player_money:
        player_money[user.id] = 50  

    if player_money[user.id] < 10:
        await channel.send(f"{user.mention}, Uh-oh! You're out of money! 💸")
        await channel.send(f"But don’t worry — here’s a friendly $50 boost to get you back in the game! 🎁")
        player_money[user.id] = 50
        return await blackjack(message)  # Restart after refill

    player_money[user.id] -= 10  # Game entry cost

    deck = get_card_deck()
    card_keys = list(deck.keys())

    player_cards = [random.choice(card_keys), random.choice(card_keys)]
    dealer_cards = [random.choice(card_keys)]

    player_total = sum(deck[card] for card in player_cards)
    dealer_total = deck[dealer_cards[0]]

    embed = discord.Embed(title="🎲 Blackjack Bonanza! 🎲", color=discord.Color.green())
    embed.add_field(name="Dealer's Hand", value=f"🃏 {dealer_cards[0]}", inline=False)
    embed.add_field(name="Your Hand", value=f"{', '.join(player_cards)} (Total: {player_total})", inline=False)
    embed.set_footer(text=f"Your Money: ${player_money[user.id]}")

    game_message = await channel.send(embed=embed)

    class BlackjackButtons(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.timeout = 60  

        @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
        async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
            nonlocal player_total, player_cards
            new_card = random.choice(card_keys)
            player_cards.append(new_card)
            player_total += deck[new_card]

            embed.clear_fields()
            embed.add_field(name="Dealer's Hand", value=f"🂠 {dealer_cards[0]}", inline=False)
            embed.add_field(name="Your Hand", value=f"{', '.join(player_cards)} (Total: {player_total})", inline=False)

            if player_total > 21:
                embed.add_field(name="Game Result", value="Oops! You went over 21. Dealer wins! ❌", inline=False)
                embed.set_footer(text=f"Your Money: ${player_money[user.id]}")
                self.stop()
                await game_message.edit(embed=embed, view=PlayAgainButtons())
            elif player_total == 21:
                embed.add_field(name="Game Result", value="🎉 You hit 21! Blackjack winner!", inline=False)
                player_money[user.id] += 20  
                embed.set_footer(text=f"Your Money: ${player_money[user.id]}")
                self.stop()
                await game_message.edit(embed=embed, view=PlayAgainButtons())

            await interaction.response.edit_message(embed=embed)

        @discord.ui.button(label="Stand", style=discord.ButtonStyle.red)
        async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
            nonlocal dealer_total, dealer_cards
            self.stop()

            while dealer_total < 17:
                new_card = random.choice(card_keys)
                dealer_cards.append(new_card)
                dealer_total += deck[new_card]

            if dealer_total > 21:
                result = "Dealer went over 21! 🎉 You win!"
                player_money[user.id] += 20
            elif dealer_total > player_total:
                result = "Dealer wins this round. Better luck next time! ❌"
            elif dealer_total == player_total:
                result = "It's a draw! 🤝"
                player_money[user.id] += 10  
            else:
                result = "🎉 Great job! You win this round!"
                player_money[user.id] += 20

            embed.clear_fields()
            embed.add_field(name="Dealer's Hand", value=f"{', '.join(dealer_cards)} (Total: {dealer_total})", inline=False)
            embed.add_field(name="Your Hand", value=f"{', '.join(player_cards)} (Total: {player_total})", inline=False)
            embed.add_field(name="Game Result", value=result, inline=False)
            embed.set_footer(text=f"Your Money: ${player_money[user.id]}")
            
            await interaction.response.edit_message(embed=embed, view=PlayAgainButtons())

    view = BlackjackButtons()
    await game_message.edit(embed=embed, view=view)
    await view.wait()

# Play Again button
class PlayAgainButtons(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Play Again", style=discord.ButtonStyle.blurple)
    async def play_again(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🎲 Starting another round of Blackjack! Good luck! 🍀", ephemeral=True)

        await blackjack(interaction.message)  # Restart the game