from typing import List
from io import BytesIO


from fastapi import FastAPI
from pydantic import BaseModel
from telegram import Bot, InputMediaPhoto

from utils import download_images, watermark
from message import text
from config import Config


conf = Config()
app = FastAPI()


class Item(BaseModel):
    number_of_rooms: int
    floor: int
    number_of_floors: int
    sub_district: str
    repair: str
    area: int
    landmark: str
    price: int
    description: str
    photos: List[str]


@app.get('/')
async def get_r():
    return {}


@app.post('/')
async def get(data: Item):
    collection = []
    imgs = await download_images(data.photos)
    msg = text.format(**data.model_dump(exclude={'photo', }))
    for index, img in enumerate(imgs):
        collection.append(InputMediaPhoto(watermark(BytesIO(img)), caption=msg if not index else '', parse_mode='html'))
    bot = Bot(conf.TOKEN)

    async with bot:
        await bot.send_media_group(
            chat_id=conf.CHANNEL_ID,
            media=collection,
            write_timeout=100
        )
    return {}
