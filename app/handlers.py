from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from asyncio import TimeoutError
import asyncio


from neironka import ask_ai

router = Router()

active_requests = {}

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply('Hello\nEnter your response')


@router.message()
async def ai_answer(message: Message):
    user_id = message.from_user.id
    if active_requests.get(user_id, False):
        await message.reply("Your last response is on working, wait")
        return

    active_requests[user_id] = True
    edited_message = await message.answer('AI is working on your response, wait')
    
    try:
        ai_answer = await asyncio.wait_for(ask_ai(message.text), timeout=60.0)
        await edited_message.edit_text(ai_answer, parse_mode="Markdown")
        print(message.text)
        print(ai_answer)
    except TimeoutError:
        await edited_message.edit_text('Error\nExceeded time limit for response from AI')
    except Exception as e:
        await edited_message.edit_text(f'Error: {str(e)}')
    finally:
        active_requests[user_id] = False
