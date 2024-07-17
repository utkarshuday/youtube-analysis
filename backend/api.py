from flask import Flask
from flask_restful import Api, reqparse
from flask_cors import CORS
from routes import Channel, Channels, Sentiment

app = Flask(__name__)
cors = CORS(app, origins=['http://localhost:5173'])
api = Api(app)


args = reqparse.RequestParser()
# for data coming to API
args.add_argument('name', type=str, required=True, help='Name cannot be blank')


api.add_resource(Channel, '/channel-details/<string:id>')
api.add_resource(Channels, '/channels/<string:name>')
api.add_resource(Sentiment, '/sentiments/<string:videoId>')


@app.route('/')
def home():
  return '<h1>Hello World</h1>'


if __name__ == '__main__':
  app.run(debug=True)
