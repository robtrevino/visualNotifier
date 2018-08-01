import redis, json
from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields
from flask_httpauth import HTTPBasicAuth

# -------------- Setup --------- #
redisServer = "127.0.0.1"
redisPort = 6379
redisDB = 0
# ------------EO Setup --------- #

app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'pi':                                                        # authorized user
        return 'raspberry'                                                      # authorized pass
    return None

@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)

class NotificationApi(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id',                                        # this is a required argument and is used for identifying the notification type
                                    type=int,
                                    required=True,
                                    help='Please provide an id',
                                    location='json')
        self.reqparse.add_argument('duration',                                  # how long the notification should show up before rotating to the another
                                    type=int,
                                    default=5,
                                    location='json')
        self.reqparse.add_argument('expiration',                                # when should the notification expire
                                    type=int,
                                    default=0,
                                    location='json')
        super(NotificationApi, self).__init__()

    def get(self):
        return {}, 200                                                          # we're not putting anything, but maybe we'll show current status in the future

    def post(self):
        args = self.reqparse.parse_args()
        notification = {
            'id' : args['id'],
            'duration' : args['duration'],
            'expiration' : args['expiration']
        }
        db = redis.Redis(host=redisServer, port=redisPort, db=redisDB)          # connect to the server. Redis has a built in connection pool, so we don't create multiple connections.
        db.lpush('notifications',json.dumps(notification))                      # store the visual notification
        notification.pop('duration', None)                                      # remove duration, it is not needed for audio notifications
        db.lpush('notificationsAudio',json.dumps(notification))                 # store the audio notification
        return '',200

api.add_resource(NotificationApi, '/notification/api/notify', endpoint='notify')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)
