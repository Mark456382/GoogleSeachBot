import aiogram
import wikipedia as wk
import aiogram.utils.markdown as md
from aiogram.dispatcher import FSMContext
from config import TOKEN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class Search(StatesGroup):
    search = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Добро пожаловать.\nДля запроса введите /search')

@dp.message_handler(commands=['seach'])
async def seach(message: types.Message, state: Search):
    await Search.search.set()
    await message.answer('Введите запрос')

@dp.message_handler(state=Search.search)
async def responce_seach(message: types.Message, state: FSMContext):
    async with state.proxy() as f:
        f['search'] = message.text

    await state.finish()

    wk.set_lang("ru")
    
    await message.answer(wk.summary(md.bold(f['search'])[1:-1], sentences=None))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)