from flask_restful import Resource,reqparse
from models.store import StoreModel


class Store(Resource):

    def get(self,name):
        store=StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message':'store not found'},404



    def post(self,name):
        if StoreModel.find_by_name(name):
           return {'message':'Store with the name {} already exitss'.format(name)},400

        store= StoreModel(name)

        try:
            store.save_to_db()

        except:

            return {'message':'Error occured in creating the store'},500


        return store.json(),201

    def delete(self,name):
        store=StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Store with the name {} deleted successfully'.format(name)}

        else:
            return {'message': 'Store with the name {} does not exists'.format(name)}

class StoreList(Resource):
      def get(self):
          return {'stores':[store.json() for store in StoreModel.query.all()]}


