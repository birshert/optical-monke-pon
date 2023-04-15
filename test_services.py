import asyncio
from io import BytesIO

import aiohttp
import pandas as pd


async def get_prediction(session, url, img):
    data = aiohttp.FormData()
    data.add_field('file', img)

    async with session.post(
            url,
            data=data,
            timeout=5
    ) as request:
        response = await request.json()

        if request.status == 200 and "price" in response:
            return response["price"]


async def async_requests(services, imgs):
    async with aiohttp.ClientSession() as session:
        tasks = []

        for img, service in zip(imgs, services):
            task = asyncio.ensure_future(get_prediction(session, service, img))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

        return responses


async def main():
    services = ["http://91.77.160.33:5000/predict", "http://91.77.160.33:5000/predict",
                "http://91.77.160.33:5000/predict"]

    test = pd.read_csv("artDataset.csv")
    test.price = test.price.map(lambda x: int(x[:-4].replace(".", "")))

    teams_y_pred = []
    y_true = []

    for i, row in test.iterrows():
        y_true.append(row.price)

        with open(f"artDataset/image_{i + 1}.png", "rb") as f:
            img_data = f.read()
            imgs = [BytesIO(img_data) for _ in services]

        res = await async_requests(services, imgs)
        teams_y_pred.append(res)


if __name__ == "__main__":
    asyncio.run(main())
