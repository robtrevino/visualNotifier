import redis, json, subprocess
from time import sleep, time

# -------------- Settings ----------- #
mac = "XX:XX:XX:XX:XX:XX"                                                       # the bluetooth address of our speaker
redisServer = "127.0.0.1"
redisPort = 6379
redisDB = 0
# ------------EO Settings ----------- #

def connectSpeaker():
    echo = subprocess.Popen(["echo", "-e", "connect", mac, "\nquit"], stdout=subprocess.PIPE)
    bluetoothctl = subprocess.Popen(["bluetoothctl"], stdin=echo.stdout, stdout=subprocess.PIPE)
    bluetoothctl.stdout.close()
    return True

def playSound(file):
    connectSpeaker()                                                         # try and connect to the bluetooth speaker, nothing happens if it's already connected
    sleep(2)                                                                    # wait for the connection
    subprocess.call(                                                            # ask the alsa player to play the file
                    ["aplay",
                    "-D",
                    "bluealsa:HCI=hci0,DEV=" + mac + ",PROFILE=a2dp",
                    file]
                    )
    return True

def playSoundFromUrl(url):
    connectSpeaker()                                                         # try and connect to the bluetooth speaker, nothing happens if it's already connected
    sleep(2)                                                                    # wait for the connection
    audio = subprocess.Popen(["curl", url], stdout=subprocess.PIPE)             # ask curl to open the pipe to the file
    player = subprocess.Popen(                                                  # ask the alsa player to play the file
                                ["aplay",
                                "-D",
                                "bluealsa:HCI=hci0,DEV="+mac+",PROFILE=a2dp"],
                                stdin=audio.stdout,                             # use the output of curl as the input
                                stdout=subprocess.PIPE
                            )
    player.stdout.close()

def soundNotification(id):
    # In here, you should match the id of the notification to the audio.
    if id == 1:
        playSound('/home/pi/pythonScripts/notifier/smw_magikoopa_beam.wav')
    elif id == 2:
        playSoundFromUrl('http://wav-sounds.com/wp-content/uploads/2017/09/Various-06.wav')
    elif id == 3: # exclamation
        playSound('/home/pi/pythonScripts/notifier/doorbell.wav')
    return True

while True:
    db = redis.Redis(host=redisServer, port=redisPort, db=redisDB)              # connect to the server. Redis has a built in connection pool, so we don't create multiple connections.
    numberOfNotifications = db.llen('notificationsAudio')                       # how many notificatiosn do we have
    if numberOfNotifications == 0:                                              # if we don't have any notifications
        sleep(1)                                                                # wait for 1 second and try again
    else:                                                                       # if we do have notifications
        for i in range(0,numberOfNotifications):                                # iterate through each
            binaryNotification = db.lindex('notificationsAudio',i)
            if binaryNotification:                                              # this step is necesarry because if we delete a notification further down because it expired, we might be requesting an index that is not there anymore
                notification = json.loads(binaryNotification.decode('utf-8'))
                if time() > notification['expiration']:                         # if the notification has expired
                    removed = db.lrem(                                          # delete it
                                        'notificationsAudio',
                                        num=0,
                                        value=binaryNotification
                                        )
                else:
                    db.lrem(                                                    # delete the notification since we're going to play it
                            'notificationsAudio',
                            num=0,
                            value=binaryNotification
                            )
                    soundNotification(notification['id'])                       # play the notification
                    sleep(1)                                                    # wait 1 second between notifications
