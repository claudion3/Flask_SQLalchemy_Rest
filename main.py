from flask import Flask,request
from flask_restful import Api, Resource,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy 
import os


app=Flask(__name__)
api=Api(app)
basedir=os.path.abspath(os.path.dirname(__file__))
#database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#init DB
db=SQLAlchemy(app)
 

class ConcertModel(db.Model):
    id=db.Column(db.Integer, primary_key=True)     
    singer=db.Column(db.String(100),nullable=False)
    venue=db.Column(db.String(100),nullable=False)
    price=db.Column(db.Float,nullable=False)
    

    def __repr__(self):
        return f"concert(singer={singer},venue={venue},price={price})"       
        

concert_put_args=reqparse.RequestParser()
concert_put_args.add_argument('singer',type=str,help='singer of the concert',required=True)
concert_put_args.add_argument('venue',type=str,help='venue of the concert',required=True)
concert_put_args.add_argument('price',type=float,help='price of the concert',required=True)

concert_update_args=reqparse.RequestParser()
concert_update_args.add_argument('singer',type=str,help='singer of the concert' )
concert_update_args.add_argument('venue',type=str,help='venue of the concert' )
concert_update_args.add_argument('price',type=float,help='price of the concert' )


resource_felds={'id':fields.Integer,'singer':fields.String,'venue':fields.String,'price':fields.Float}

class Concerts(Resource):
    #get all concerts
    @marshal_with(resource_felds)
    def get(self):
        get_all=ConcertModel.query.all()                
        return get_all

    #use post to input data 
    @marshal_with(resource_felds)
    def post(self):
        args=concert_put_args.parse_args()        
        concert=ConcertModel(singer=args['singer'],venue=args['venue'],price=args['price'])
        db.session.add(concert)
        db.session.commit()                
        return concert,200
 

#result buy id
class Concert(Resource):
    #get concert but id
    @marshal_with(resource_felds)
    def get(self,concert_id):
        result=ConcertModel.query.filter_by(id=concert_id).first()
        if not result:
            abort(404, message='could not find concert with that id..')       
        return result

    #input data
    @marshal_with(resource_felds)
    def put(self,concert_id):        
        args=concert_put_args.parse_args()
        result=ConcertModel.query.filter_by(id=concert_id).first()
        if result:
            abort(409,message='concert id taken...')
        concert=ConcertModel(id=concert_id,singer=args['singer'],venue=args['venue'],price=args['price'])
        db.session.add(concert)
        db.session.commit()
        return concert,201

    #update
    @marshal_with(resource_felds)
    def patch(self,concert_id):
        args=concert_update_args.parse_args()
        result=ConcertModel.query.filter_by(id=concert_id).first()
        if not result:
            abort(404, message="concert doens't exist, cannot update..") 

        if args['singer']:
            result.singer=args['singer']         
        if args['venue']:
            result.venue=args['venue']
        if args['price']:
            result.price=args['price']
        
        db.session.commit()
        return result

    #delete
    @marshal_with(resource_felds)
    def delete(self,concert_id):
        result=ConcertModel.query.filter_by(id=concert_id).first()
        if not result:
            abort(404, message="concert doens't exist, cannot Delete..")
        db.session.delete(result) 
        db.session.commit()        
        return '',204

api.add_resource(Concert, '/concert/<int:concert_id>')
api.add_resource(Concerts, '/concert')

if __name__=="__main__":
    app.run(debug=True)