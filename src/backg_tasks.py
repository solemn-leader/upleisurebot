import threading
import time
from datetime import datetime
from models import TeenEvent, YoungEvent
from consts import N_OF_TIME_EVENT_REMAINS_UNDELETED


class DBCleanUp(object):
    """This class is responsible for deleting expired
    database objects in the background.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # all the logic happens here
            YoungEvent.delete() .where(YoungEvent.time_published +
                                       N_OF_TIME_EVENT_REMAINS_UNDELETED <= datetime.utcnow()).execute()
            TeenEvent.delete() .where(TeenEvent.time_published +
                                      N_OF_TIME_EVENT_REMAINS_UNDELETED <= datetime.utcnow()).execute()
            time.sleep(self.interval)
