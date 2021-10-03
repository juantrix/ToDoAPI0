import datetime
from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine, select
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware

# para conectar la base de datos se le pasa el siguiente formato 'nombreGestor://nombreUser:@direccion/nombreDB'
engine = create_engine('postgresql://gutuuijp:iOnVnPilpeuqIOHeIrm4ImPymFpCGNqj@kesavan.db.elephantsql.com/gutuuijp')
Base = declarative_base()
app = FastAPI()

origins = [
    "http://localhost.herokuapp.com",
    "https://localhost.herokuapp.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:*",
    "http://localhost:*/*",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Task(Base):
    __tablename__ = 'Task'

    id = Column(Integer(), primary_key=True)
    title = Column(String(32), nullable=False)
    body = Column(String(128), nullable=False)
    completed = Column(Boolean, default=False)
    date = Column(DateTime(), default=datetime.datetime.now())

    def __str__(self) -> str:
        return self.title


Session = sessionmaker(bind=engine)
session = Session()

@app.post('/new')
def newTask(title: str, body: str):
    with Session() as session:
        session.add(Task(title=title,body=body))
        session.commit()

    return  'added'


@app.get('/tasks')
def task_list():
    return session.query(Task).all()


@app.delete('/delete')
def delete_task(id: int):
    task = session.query(Task).filter(Task.id==id)
    if task.first() is not None:
        task.delete()
        session.commit()
        return 'Deleted'
    else:
        return 'the task doesnt exist'


@app.put('/change')
def change_task(id, title, body, completed):
    task = session.query(Task).filter(Task.id==id)
    if task.first() is not None:
        task.first().body = body
        task.first().title = title
        task.first().completed = bool(completed)
        task.first().date = datetime.datetime.now()
        return 'Changed'
    else:
        return 'the task doesnt exist'


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)