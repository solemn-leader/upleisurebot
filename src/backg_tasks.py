import threading
import time


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
            
            time.sleep(self.interval)
