
import discord
import os
import openai

# Get tokens from environment variables
token = os.environ["SECRET_KEY"]
openai.api_key = os.environ["OPENAI_API_KEY"]

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')

    async def on_message(self, message):
        # Don't respond to ourselves
        if message.author == self.user:
            return

        # Check if the bot is mentioned in the message
        if self.user in message.mentions:
            # Remove the bot mention from the message content
            prompt = message.content.replace(f"<@{self.user.id}>", "").strip()

            try:
                # Generate response using OpenAI GPT-4
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=1,
                    max_tokens=286,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                # Extract and send the response
                message_to_send = response['choices'][0]['message']['content'].strip()
                await message.channel.send(message_to_send)
            except Exception as e:
                await message.channel.send("Sorry, I couldn't process that.")
                print(f"Error: {e}")

# Set intents to include message content
intents = discord.Intents.default()
intents.message_content = True

# Initialize client and run the bot
client = MyClient(intents=intents)
client.run(token)
