build: cog.yaml
	cog build -t monke-model:latest

run: build
	docker run -p 5000:5000 --gpus all monke-model:latest
