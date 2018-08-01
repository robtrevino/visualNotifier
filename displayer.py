import unicornhat as unicorn
import redis, json
from time import sleep, time

# -------------- Settings ----------- #
unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(180)                                                           # define the rotation of the display
unicorn.brightness(0.35)
width,height=unicorn.get_shape()
redisServer = "127.0.0.1"
redisPort = 6379
redisDB = 0
# ------------EO Settings ----------- #

# ----------- Shapes --------------- #
# Store the shapes here as a matrix of 8x8 and R,G,B from 0 to 255
# stole them from here: https://twitter.com/justin_cyr/status/658031097805197313
shapes = {}
shapes['exclamation'] = [
                            [[0,0,0],[0,0,0],[0,0,0],[255,255,255],[255,255,255],[0,0,0],[0,0,0],[0,0,0]],
                            [[0,0,0],[0,0,0],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[0,0,0],[0,0,0]],
                            [[0,0,0],[0,0,0],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[0,0,0],[0,0,0]],
                            [[0,0,0],[0,0,0],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[0,0,0],[0,0,0]],
                            [[0,0,0],[0,0,0],[0,0,0],[255,255,255],[255,255,255],[0,0,0],[0,0,0],[0,0,0]],
                            [[0,0,0],[0,0,0],[0,0,0],[255,255,255],[255,255,255],[0,0,0],[0,0,0],[0,0,0]],
                            [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
                            [[0,0,0],[0,0,0],[0,0,0],[255,255,255],[255,255,255],[0,0,0],[0,0,0],[0,0,0]],
                        ]
shapes['money'] = [
                    [[0,0,0],[0,0,0],[130,224,170],[0,0,0],[0,0,0],[130,224,170],[0,0,0],[0,0,0]],
                    [[39,174,96],[130,224,170],[130,224,170],[130,224,170],[130,224,170],[130,224,170],[130,224,170],[0,0,0]],
                    [[130,224,170],[0,0,0],[130,224,170],[0,0,0],[0,0,0],[130,224,170],[0,0,0],[0,0,0]],
                    [[39,174,96],[130,224,170],[130,224,170],[130,224,170],[130,224,170],[130,224,170],[130,224,170],[39,174,96]],
                    [[0,0,0],[0,0,0],[130,224,170],[0,0,0],[0,0,0],[130,224,170],[0,0,0],[130,224,170]],
                    [[0,0,0],[0,0,0],[130,224,170],[0,0,0],[0,0,0],[130,224,170],[0,0,0],[130,224,170]],
                    [[130,224,170],[130,224,170],[130,224,170],[130,224,170],[130,224,170],[130,224,170],[130,224,170],[39,174,96]],
                    [[0,0,0],[0,0,0],[130,224,170],[0,0,0],[0,0,0],[130,224,170],[0,0,0],[0,0,0]]
                    ]
shapes['house'] = [
                    [[0,0,0],[0,0,0],[255,0,77],[255,0,77],[0,0,0],[194,195,199],[194,195,199],[0,0,0]],
                    [[0,0,0],[0,0,0],[255,0,77],[255,0,77],[255,0,77],[255,0,77],[194,195,199],[0,0,0]],
                    [[0,0,0],[255,0,77],[255,0,77],[255,0,77],[255,0,77],[194,195,199],[126,37,83],[0,0,0]],
                    [[0,0,0],[255,0,77],[255,0,77],[255,0,77],[255,0,77],[255,241,232],[194,195,199],[126,37,83]],
                    [[255,0,77],[255,0,77],[255,0,77],[255,0,77],[194,195,199],[255,241,232],[255,241,232],[0,0,0]],
                    [[0,0,0],[194,195,199],[255,0,77],[255,0,77],[255,241,232],[0,0,0],[255,241,232],[0,0,0]],
                    [[0,0,0],[194,195,199],[194,195,199],[194,195,199],[255,241,232],[0,0,0],[255,241,232],[0,0,0]],
                    [[0,0,0],[0,0,0],[0,0,0],[194,195,199],[255,241,232],[0,0,0],[0,0,0],[0,0,0]]
                    ]

shapes['off'] = [
                    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
                    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
                    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
                    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
                    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
                    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
                    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
                    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
                    ]

# ---------EO Shapes --------------- #

def showImage(image):                                                           # iterate through the shape array en set the colors.
    for y in range(height):
        for x in range(width):
            unicorn.set_pixel(
                                x,
                                y,
                                shapes[image][y][x][0],
                                shapes[image][y][x][1],
                                shapes[image][y][x][2]
                                )
    unicorn.show()
    return True

def show_notification(id):
    # In here, you should match the id of the notification to the image.
    if id == 0: # turn off
        unicorn.off()
    elif id == 1:
        showImage('exclamation')
    elif id == 2:
        showImage('money')
    elif id == 3: # exclamation
        showImage('house')
    return True

while True:
    db = redis.Redis(host=redisServer, port=redisPort, db=redisDB)              # connect to the server. Redis has a built in connection pool, so we don't create multiple connections.
    numberOfNotifications = db.llen('notifications')                            # how many notificatiosn do we have
    if numberOfNotifications == 0:                                              # if we don't have any notifications
        unicorn.off()                                                           # turn off the display
        sleep(1)                                                                # wait for 1 second and try again
    else:                                                                       # if we do have notifications
        for i in range(0,numberOfNotifications):                                # iterate through each
            binaryNotification = db.lindex('notifications',i)
            if binaryNotification:                                              # this step is necesarry because if we delete a notification further down because it expired, we might be requesting an index that is not there anymore
                notification = json.loads(binaryNotification.decode('utf-8'))
                if time() > notification['expiration']:                         # if the notification has expired
                    removed = db.lrem(                                          # delete it
                                        'notifications',
                                        num=0,
                                        value=binaryNotification
                                        )
                else:
                    nextNotification = time() + notification['duration']        # when are we supposed to check again?
                    show_notification(notification['id'])                       # show the notification
                    while time() < nextNotification:                            # until the duration time passes
                        sleep(1)
