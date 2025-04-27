from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}


import databases, sqlalchemy

DB_URL = "sqlite:///./tasks.sqlite3"
db = databases.Database(DB_URL)
metadata = sqlalchemy.MetaData()
tasks_table = sqlalchemy.Table(
    "tasks", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
)
engine = sqlalchemy.create_engine(DB_URL)
metadata.create_all(engine)

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

@app.post("/tasks")
async def create_task(task: dict):
    query = tasks_table.insert().values(title=task["title"])
    last_id = await db.execute(query)
    return {"id": last_id, **task}

@app.get("/tasks")
async def list_tasks():
    return await db.fetch_all(tasks_table.select())

print("In Branch")
