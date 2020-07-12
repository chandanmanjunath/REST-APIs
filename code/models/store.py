import sqlite3
from db import db
from models.item import ItemModel

class StoreModel(db.Model):
      __tablename__ = 'stores'

      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(80))

      items = db.relationship('ItemModel',lazy='dynamic')


      def __init__(self,name):
          self.name=name



      def json(self):
          return {'name':self.name,'items':[item.json() for item in ItemModel.query.all()]}

      @classmethod
      def find_by_name(cls, name):
          return cls.query.filter_by(name=name).first()  # select * from items where name=name limit 1


      def save_to_db(self):
          #The below lines will upsert data to the data base
          db.session.add(self)
          db.session.commit()


      def delete_from_db(self):
          #the below lines will delete the data from database
          db.session.delete(self)
          db.session.commit()
