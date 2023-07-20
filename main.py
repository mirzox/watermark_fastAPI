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
    photos: List[str] | None = None


@app.get('/')
async def get_r():
    return {}


@app.post('/')
async def get(data: Item):
    bot = Bot(conf.TOKEN)
    if data.photos is not None:
        collection = []
        if len(data.photos) > 10:
            photos = data.photos[:10]
        else:
            photos = data.photos
        imgs = await download_images(photos)
        msg = text.format(**data.model_dump(exclude={'photo', }))
        for index, img in enumerate(imgs):
            collection.append(InputMediaPhoto(watermark(BytesIO(img)), caption=msg if not index else '', parse_mode='html'))

        async with bot:
            await bot.send_media_group(
                chat_id=conf.CHANNEL_ID,
                media=collection,
                write_timeout=100,
                read_timeout=30
            )
    else:
        msg = text.format(**data.model_dump(exclude={'photo', }))
        async with bot:
            await bot.send_message(
                chat_id=conf.CHANNEL_ID,
                text=msg,
                write_timeout=100,
                read_timeout=30,
                parse_mode="html"
            )
    return {}
