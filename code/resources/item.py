from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT,jwt_required,current_identity
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id")

    @jwt_required()
    def get(self,name):
        #print(list(current_identity))
        item=ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {"message": "Item with the given name does not exists"},404

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message':"The item with the name '{}' already exists ".format(name)},400

        data = Item.parser.parse_args()
        new_item=ItemModel(name,data['price'],data['store_id'])

        try:
           #self.insert(new_item)
           #ItemModel.insert(new_item)
           new_item.save_to_db()

        except:
            return {"message":"An Exception occured while inserting an item"},500 #internal server error



        return new_item.json(),201



    #deleting an item
    def delete(self,name):
        if not ItemModel.find_by_name(name):
            return {'message':"The item with the name '{}' does not exists ".format(name)},400
        item=ItemModel.find_by_name(name)

        item.delete_from_db()


        return {"message":"Item deleted successfully"},200

    #update an item
    def put(self,name):

        data = Item.parser.parse_args()
        item=ItemModel.find_by_name(name)

        if not item:
            try:
                item=ItemModel(name, data['price'],data['store_id'])
                item.save_to_db()

            except:
                return {"message": "An Exception occured while inserting an item"}

            return {'message':"The item with the name '{}' is succesfully inserted ".format(name)},400

        else:
            try:
                item.price = data['price']
                item.save_to_db()

            except:
                return {"message": "An exception occured while data update"}, 500




        return item.json(),200




class ItemList(Resource):
    def get(self):
        return {'items':[ x.json() for x in ItemModel.query.all()]}