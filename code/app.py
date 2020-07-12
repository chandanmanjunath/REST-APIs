from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import Store,StoreList

from db import db

app=Flask(__name__)

#The below configuration allows sqlalchemy to find the database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.secret_key='chan'

api=Api(app)

'''The jwt works as below:
   1.Create an endpoint /auth by default and receives user_name and password from this endpoint(POST)
   2.Pass username and password to authenticate
   3.If user is authenticated return a 'JWT token'
   4.From Next time onwards,send JWT token from UI, gets verified through identity method and user will be authenticated 
'''
jwt=JWT(app,authenticate,identity)

api.add_resource(Store,'/store/<string:name>')
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(StoreList,'/stores')

#The below flask decorator is used to automatically create the tables before the first request
@app.before_first_request
def create_tables():
    db.create_all()

#app.run is ran only when explicitely python app.py is run,not when its imported
if __name__ == '__main__' :
 db.init_app(app)
 app.run(port=5000,debug=True)