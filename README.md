# Ollama API
This is a simple rest api service. It work in python and save requests and answers in Postgresql.
#### Install & Run
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
> ##### if I want to use a GPU?

You should download the `cuda-toolkit` from the [official nvidia website](https://developer.nvidia.com/cuda-toolkit) (if you have nvidia)