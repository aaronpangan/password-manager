from fastapi import FastAPI
import database
import models
from Account import accountController


app = FastAPI()

models.Base.metadata.create_all(database.engine)

app.include_router(accountController.router)