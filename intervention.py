#!/usr/bin/env python3

import atexit
import logging
# import multiprocessing
import sys
# import time

# from PySide import QtCore

if sys.platform == 'darwin':
    import darwin as platform
else:
    import windows as platform

LOG_FORMAT = '%(relativeCreated)dms %(message)s'

logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
logging.info('Logging started')

DURATION = 15 * 1000
SKIP_FILTER = True


# def do_nothing():
#     time.sleep(DURATION / 1000)


if __name__ == '__main__':
    # Just skip it if the computer isn't being used
    if platform.get_idle_time() > 90:
        sys.exit()

    platform.hide_cursor()

    from ui import Application

    application = Application(sys.argv, ignore_close=not SKIP_FILTER)

    with open('./intervention.css') as css:
        application.setStyleSheet(css.read())

    # exec() is required for objc so we must use spawn
    # multiprocessing.set_start_method('spawn')

    # target = do_nothing

    # if sys.platform == 'darwin' and not SKIP_FILTER:
    #     from filters import filter_input
    #     target = filter_input

    # pool = multiprocessing.Pool(1)  # pylint: disable=not-callable

    # def filter_input_done_cb(ignored):
    #     application.closeAllWindows()

    # result = pool.apply_async(target, callback=filter_input_done_cb)

    @atexit.register
    def exit_handler():
        """
        Clean up.
        """
        logging.info('atexit triggered')

        platform.show_cursor()

    #     # terminate the pool so we don't sit forever waiting on our get()
    #     logging.info('Terminating pool...')
    #     pool.terminate()

    #     logging.info('Joining pool...')
    #     pool.join()

    #     logging.info('Retrieving result...')
    #     try:
    #         # raise any exceptions raised by the input filtering code
    #         result.get(0)
    #     except multiprocessing.TimeoutError:
    #         logging.info('Timed out waiting for result.')

    # def duration_reached():
    #     logging.info('Duration reached, exiting...')

    #     sys.exit(0)

    # Run for DURATION and then exit
    # QtCore.QTimer.singleShot(DURATION, duration_reached)

    application.run()
