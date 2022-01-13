from fastapi import FastAPI
import database
import Account.account_model as account_model
import User.user_model as user_model
from Account import account_controller
from User import user_controller


app = FastAPI()

account_model.Base.metadata.create_all(database.engine)
user_model.Base.metadata.create_all(database.engine)

app.include_router(account_controller.router)
app.include_router(user_controller.router)