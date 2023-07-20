from io import BytesIO
import asyncio

import requests
from PIL import Image
import aiohttp


async def fetch_image(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            image_data = await response.read()
            return image_data
        else:
            print(f"Failed to fetch image from {url}, status code: {response.status}")
            return None


async def download_images(image_urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_image(session, url) for url in image_urls]
        image_data_list = await asyncio.gather(*tasks)
        return image_data_list


# def get_images(urls):
#     photos = []
#     for url in urls:
#         get_response = requests.get(url)
#         if get_response.status_code == 200:
#             photos.append(get_response.content)
#     return photos


def watermark(photo: BytesIO):
    coefficient = 0.451
    with Image.open(photo) as img:
        w, h = img.size
        image = img.resize((int(w//1.5), int(h//1.5)), Image.NEAREST)
    w, h = image.size
    img = image
    logo_size = int(w * coefficient if w < h else h * coefficient)
    logo = Image.open('logo_764x763.png' if logo_size <= 760 else 'logo_2000x1999.png' if 760 < logo_size <= 2000 else 'logo_3000x2999.png')

    logo.thumbnail((logo_size, logo_size))
    l_w, l_h = w // 2 - logo_size // 2, h // 2 - logo_size // 2
    img.paste(logo, (l_w, l_h), logo)
    image_bytes_io = BytesIO()
    try:
        img.save(image_bytes_io, format='JPEG')
    except OSError:
        img.save(image_bytes_io, format='PNG')
    image_bytes_io.seek(0)
    image_bytes = image_bytes_io.getvalue()
    logo.close()
    return image_bytes
