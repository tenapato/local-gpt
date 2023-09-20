# Local GPT

A personal project to use openai api in a local environment as an assitant for developers

## How to run

```shell
docker build -t assistant-api . 
```

```shell
docker run -p 5001:5001 -e OPEN_AI_KEY=<your-key> assistant-api
```

## How to use

```shell
curl -X POST -H "Content-Type: application/json" -d '{"prompt": "write a typescript code that creates a basic encryption function that uses sha256"}' "http://localhost:5001/api/answer?gpt4=false"
```

> You can also define here if you want to use gpt-4 model instead

