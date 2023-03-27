# This is a sample Python script.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# Press the green button in the gutter to run the script.
# if __name__ == '__main__':

from fastapi import FastAPI
from pydantic import BaseModel
import hashlib
from datetime import datetime
from tinydb import TinyDB, Query


class ApplicationData():
    configuration: {}
    memory = {}


class User(BaseModel):
    id: str
    name: str
    lastname: str
    username: str
    mail: str


def generateId():
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    return hashlib.sha256(formatted_date.encode()).hexdigest()


# Create file database if not exists
def createFile():
    try:
        open('myLocalDatabase.json', 'x')
    except:
        print("File already exists")


# read with tinydb the database looking for users if not exists create a new one with the next code and save it,
# "user = User(**{"id": generateId(),"name": "Mia","lastname": "Ruiz","username": "Minicoru","mail": "miarg49@gmail.com"})"
def validateUsers():
    if 'users' not in appData.memory:
        users = db.table('users')
        if len(users) == 0:
            user = User(**{
                "id": generateId(),
                "name": "Mia",
                "lastname": "Ruiz",
                "username": "Minicoru",
                "mail": "miarg49@gmail.com"
            })
            users.insert(user.dict())


createFile()
db = TinyDB('myLocalDatabase.json')
appData = ApplicationData()
validateUsers()
print(appData)
app = FastAPI()


@app.get("/")
async def root():
    # get root service status
    return {"message": "Root service active"}


@app.get("/user")
async def users():
    users = db.table('users')
    # get all users in database
    return users.all()


@app.get("/user/count")
async def userCount():
    users = db.table('users')
    # get count of users in database
    return {"count": len(users)}


@app.get("/user/{id}")
async def user(id: str):
    users = db.table('users')
    # find user in database
    return users.search(Query().id == id).pop()


@app.post("/user")
async def user(user: User):
    user.id = generateId()
    users = db.table('users')
    # add user to database
    return users.insert(user.dict())


@app.put("/user/{id}")
async def user(id: str, user: User):
    found = {"message": "Record not found."}
    position = 0
    users = db.table('users')
    if len(id) == 0 and len(user.id) > 0:
        id = user.id

    # find user to update in database
    return users.update({'name': user.name, 'lastname': user.lastname}, Query().id == id)


@app.delete("/user/{id}")
async def user(id: str):
    if len(id) == 0:
        return {"message": "ID value cannot be empty."}
    users = db.table('users')
    # find user to remove in database
    return users.remove(Query().id == id)
