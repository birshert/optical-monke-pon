FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

RUN apt-get update  \
    && apt-get upgrade -y  \
    && apt-get install tmux git --no-install-recommends -y  \
    && apt-get clean -y  \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y python3.10 python3-pip

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
