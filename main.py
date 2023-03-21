import logging
import time
from random import randrange
import openai
from aiogram import Bot, Dispatcher, executor, types
import config

logging.basicConfig(level=logging.INFO)

openai.api_key = config.OPENAI_TOKEN

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def greeting(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name} {message.from_user.last_name}!\n"
                         f"Напиши мне что-то :)")


@dp.message_handler(commands='getnumber')
async def greeting(message: types.Message):
    print('Looking for the number')
    time.sleep(randrange(2))
    await message.answer(f"{randrange(0, 9)}")
    print('Number found')


thinking_msg = [
    "Дай-ка подумать...",
    "Ищу ответ...",
    "Подожди немного...",
    "Изучаю вопрос",
    "Дай мне несколько секунд"
]


@dp.message_handler()
async def gpt_answer(message: types.Message):
    prompt = message.text
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    await message.answer(thinking_msg[randrange(0, len(thinking_msg) - 1)])
    print('Searching for an answer')
    time.sleep(randrange(5, 10))
    await message.answer(completion.choices[0].text)
    print('Answer found')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
