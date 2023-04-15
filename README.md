# Optical-monke-pon

Решение от команды "Оптические бибизяны пон" для DS буткемпа в Райффайзенбанке 2023.

## Deploy

Решение состоит из двух частей, телеграм-бота и `fastapi` сервиса с моделями + `prometheus` + `graphana` для
мониторинга.

### Телеграм бот:

Написан на библиотеке `aiogram`, запускаем:

```BOT_TOKEN="YOUR_TOKEN" PYTHONPATH='$PYTHONPATH:./' python3.10 bot/main.py```

Бот умеет принять фото картины и ответить ее примерную цену, для оценки цены стучится в `fastapi` сервис.
Бот умеет сгенерировать вариации картины, для генерации вариаций стучится в тот же `fastapi` сервис.
Бот умеет прислать стикер с бибизяной и написать пон.

### `FastAPI` сервис с модельками + мониторинг (актуальный вариант деплоя)

Написан с помощью библиотеки `fastapi`, запускаем:

```docker-compose build```
```docker-compose up```

Это поднимет три контейнера, один с `fastapi` сервисом, на порте 5000, второй с `prometheus` на 9090 и третий
с `graphana` на 3000.
Прометеус собирает метрики с нашего сервиса, потом рисуем их в Графане.

#### Ручки сервиса
 - /
 - /predict
 - /docs
 - /metrics
 - /variate

### `COG` сервис с моделькой

Первый вариант деплоя, упакован и задеплоен с помощью библиотеки `cog`, запускаем:

```cog build -t monke-model:latest```
```docker run -p 5000:5000 --gpus all monke-model:latest```

Это поднимет `fastapi` сервис на порту 5000 и можно будет стучаться в ручку `/predict` чтобы делать предсказания моделью.

## Модель
Пишем модели на библиотеке `pytorch`.
В качестве модели используем `resnet18` с последним слоем модифицированным в млп.
Дообучаем только голову.

```
self.model = resnet18()
self.model.fc = nn.Sequential(
    nn.Linear(512, 256),
    nn.LeakyReLU(),
    nn.Linear(256, 1)
)
```

В качестве обучающих данных используем оригинальный датасет + наскрапили картин с сайта `www.artsy.net`.
