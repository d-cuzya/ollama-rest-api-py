import json
# settings = {}
with open('settings.json', 'r') as file:
    settings = json.load(file)
settings["server"]
# AI
import ollama
client = ollama.AsyncClient()
async def ai_gen(request: str):
    return (await client.generate(  
        model=settings["ollama"]["model"],
        prompt=f"{request}",
        # https://pypi.org/project/ollama-python/
        options=settings["ollama"]["options"],
        stream=False
    ))["response"]
# POSTGRES
import asyncpg
class database:
    conn = None
    async def db_connect(self):
        self.conn = await asyncpg.create_pool(dsn=f"postgresql://{settings["database"]["user_name"]}:{settings["database"]["user_password"]}@{settings["database"]["host"]}/{settings["database"]["database_name"]}")
    async def create_request(self, text_request):
        return await self.conn.fetchrow('INSERT INTO requests (request) VALUES ($1) RETURNING uuid;', text_request)
    async def get_request(self, uuid_request):
        return await self.conn.fetchrow('SELECT request FROM REQUESTS WHERE uuid = $1;', uuid_request)
    async def make_status(self, uuid_request, new_status):
        return await self.conn.fetchrow(f'INSERT INTO status (uuid, status) VALUES (\'{uuid_request}\', \'{new_status}\');')
    async def get_status(self, uuid_request):
        return await self.conn.fetchrow(f'SELECT status FROM status WHERE uuid = \'{uuid_request}\'')
    async def set_status(self, uuid_request, new_status):
        return await self.conn.fetchrow(f'UPDATE status SET status = \'{new_status}\' WHERE uuid = \'{uuid_request}\'')
    async def create_answer(self, uuid_request, text_answer):
        return await self.conn.fetchrow('INSERT INTO answers (uuid, answer) VALUES ($1, $2)', uuid_request, text_answer)
    async def get_answer(self, uuid_request):
        return await self.conn.fetchrow('SELECT answer FROM answers WHERE uuid = $1', uuid_request)
# MAIN TASK
async def start_gen(uuid):
    await db.set_status(uuid, "MAKING")
    try:
        answer = await ai_gen(await db.get_request(uuid))
        await db.set_status( uuid, "MADE")
        await db.create_answer(uuid, answer)
        await db.set_status(uuid, "FINISHED")
    except Exception as er:
        await db.set_status( uuid, "ERROR")
        await db.create_answer(uuid, er)
# REST_API
from fastapi import FastAPI, BackgroundTasks, Request
db = database()
from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.db_connect()
    yield
    await db.conn.close()
app = FastAPI(lifespan=lifespan)
@app.post("/api/create_request")
async def api_create_requests(request: Request, background_tasks: BackgroundTasks):
    uuid = (await db.create_request((await request.json()).get("request")))['uuid']
    await db.make_status(uuid, "CREATED")
    background_tasks.add_task(start_gen, uuid)
    return {"uuid": uuid}
@app.get("/api/get_request/{uuid}")
async def api_get_requests(uuid: str):
    return await db.get_request(uuid)
@app.get("/api/get_status/{uuid}")
async def api_get_requests(uuid: str):
    return await db.get_status(uuid)
@app.get("/api/get_answer/{uuid}")
async def api_get_requests(uuid: str):
    return await db.get_answer(uuid)
import uvicorn
uvicorn.run(app, host=settings["server"]["host"], port=settings["server"]["port"])