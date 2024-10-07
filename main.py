from typing import List
from io import BytesIO


from fastapi import FastAPI
from pydantic import BaseModel
from telegram import Bot, InputMediaPhoto
from fastapi.middleware.cors import CORSMiddleware

from utils import download_images, watermark
from message import text
from config import Config


conf = Config()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    number_of_rooms: int
    floor: int
    number_of_floors: int
    sub_district: str | None
    repair: str
    area: int
    landmark: str | None
    price: int
    description: str
    photos: List[str] | None = None


@app.get('/')
async def get_r():
    return {}


@app.post('/')
async def get(data: Item):
    bot = Bot(conf.TOKEN)
    price = f"{data.price:,}".replace(',', '.')
    if data.photos is not None and len(data.photos):
        collection = []
        if len(data.photos) > 10:
            photos = data.photos[:10]
        else:
            photos = data.photos
        imgs = await download_images(photos)
        msg = text.format(price=price, **data.model_dump(exclude={'photo', 'price'}))
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
        msg = text.format(price=price, **data.model_dump(exclude={'photo', 'price', ''}))
        async with bot:
            await bot.send_message(
                chat_id=conf.CHANNEL_ID,
                text=msg,
                write_timeout=100,
                read_timeout=30,
                parse_mode="html"
            )
    return {}
