build:
	docker build \
  --cache-from nvidia/cuda:11.8.0-devel-ubuntu22.04 \
  -t "monke-model:latest" \
  -f Dockerfile \
  .

run:
	docker run -p 5000:5000 --gpus all monke-model:latest

run-bash:
	docker run -it --rm -p 5000:5000 --gpus all monke-model:latest bash