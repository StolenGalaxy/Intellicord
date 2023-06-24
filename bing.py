from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle


async def ask(prompt):
    bot = await Chatbot.create()

    response = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative, simplify_response=True)

    return response
