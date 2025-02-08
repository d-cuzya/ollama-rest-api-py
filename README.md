# Ollama API
This is a simple rest api service. It work in python and save requests and answers in Postgresql.
# Install & Run
> ##### Download and install Ollama

1) Visit [website](https://ollama.com/download) or their [repository](https://github.com/ollama/ollama) and download program for your os.
2) Install a suitable AI model
```
ollama pull name_model
```
Insert the name of your model instead of name_model. You can see all models in their [repository](https://github.com/ollama/ollama?tab=readme-ov-file#model-library).

3) Run ollama service
```
ollama serve
```
> ##### Create DataBase and Tables

1) Create DataBase
2) Run file `ai-api-struct.sql` (the file contains the structure of tables for postgresql)
> ##### If I want to use a GPU?

You should download the `cuda-toolkit` from the [official nvidia website](https://developer.nvidia.com/cuda-toolkit) (if you have nvidia)

> ##### Download python library

```
pip install ollama asyncpg fastapi contextlib uvicorn
```
> ##### Change settings

1) open file `settings.json`
Its structure:
```
{
    "server": {
        "host":"0.0.0.0",
        "port": 8000
    },
    "database": {
        "user_name": "postgres",
        "user_password": "password123",
        "host": "127.0.0.1:5432",
        "database_name":"ai-api"
    },
    "ollama": {
        "model": "llama3.2",
        "options": {
            "num_threads":1,
            "temperature": 0.7,
            "num_predict": 4096
        }
    }
}
```
Server:

`host` - the host/ip on which the api service will run

`port` - port on which the api service will run

Database:

`user_name` - username for database

`user_password`- password for database

`host`- database's host

`database_name`- database's name

Ollama:

`model`- the name of the model from ollama

`options`- [full list options](https://pypi.org/project/ollama-python/)

> ##### Start service

```
python api-server.py
```

# Rest api Guide
Example local addres:
```
http://127.0.0.1:8000/api/
```

> Create request for AI

```
(POST) http://127.0.0.1:8000/api/create_request
```

Request's body:
```
{ "request" : "Your request for AI" }
```

Return:
```
{ "uuid" : "unic_uuid" }
Example: { "uuid" : "9ea6ee69-6fc4-45b8-9d32-390c7539a2df" }
```

> Get request's status

```
(GET) http://127.0.0.1:8000/api/get_status/{uuid}
```
change `uuid`

Example:
```
http://127.0.0.1:8000/api/get_status/9ea6ee69-6fc4-45b8-9d32-390c7539a2df
```

Return:
```
{ "status" : "FINISHED" }
```

There are 5 statuses:
`CREATED` - Created, but processing has not started yet

`MAKING` - Processing has started

`MADE` - The response has been generated, but the response has not yet been saved to the database.

`FINISHED` - The response is ready to receive

`ERROR` - An error has occurred, and the text has been saved in response.

> Get answer
