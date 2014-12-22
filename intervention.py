#!/usr/bin/env python3

import atexit
import multiprocessing
import sys
import time

import AppKit
import Quartz

from PySide import QtCore, QtGui

# 30 seconds
DURATION = 30 * 1000
EXIT_STRING = 'this must be very, very important'


def filter_input():
    print('Filtering all keys and mouse movements...')

    typed_keys = ''

    def keyboard_cb(proxy, type_, event, refcon):
        nonlocal typed_keys

        if not event:
            return None

        # Convert the Quartz CGEvent into something more useful
        ns_event = AppKit.NSEvent.eventWithCGEvent_(event)

        if not ns_event:
            return None

        if ns_event.type() == Quartz.kCGEventKeyDown:
            typed_keys += ns_event.characters()

            if typed_keys.endswith(EXIT_STRING):
                print('Emergency exit!')

                Quartz.CFRunLoopStop(Quartz.CFRunLoopGetCurrent())

        # Filter every event
        return None

    print('Creating tap...')
    # Set up a tap, with type of tap, location, options and event mask
    tap = Quartz.CGEventTapCreate(
        Quartz.kCGSessionEventTap,
        # Insert at the head so we can filter
        Quartz.kCGHeadInsertEventTap,
        # Enable filtering
        Quartz.kCGEventTapOptionDefault,
        # Act on all key and mouse events
        Quartz.kCGAnyInputEventType,
        # Our callback function
        keyboard_cb,
        None)

    runLoopSource = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)

    Quartz.CFRunLoopAddSource(Quartz.CFRunLoopGetCurrent(),
                              runLoopSource,
                              Quartz.kCFRunLoopDefaultMode)

    Quartz.CGEventTapEnable(tap, True)

    print('Starting run loop...')
    Quartz.CFRunLoopRun()

    print('Run loop finished.')


def hide_cursor():
    Quartz.CGAssociateMouseAndMouseCursorPosition(False)
    Quartz.CGDisplayHideCursor(Quartz.CGMainDisplayID())


def show_cursor():
    Quartz.CGAssociateMouseAndMouseCursorPosition(True)
    Quartz.CGDisplayShowCursor(Quartz.CGMainDisplayID())


class Application(QtGui.QApplication):
    def event(self, event):
        if event.type() == QtCore.QEvent.Close and event.spontaneous():
            event.ignore()

            return False

        return super(Application, self).event(event)


class Message(QtGui.QLabel):
    def __init__(self, parent=None, f=0):
        QtGui.QLabel.__init__(self, parent, f)

        database = QtGui.QFontDatabase()

        # There's no way to specify the proper font style in CSS
        font = database.font("Museo Slab", "500", 96)

        self.setFont(font)
        self.setStyleSheet("""color: white;
                              background-color: #293776;""")

        # Fill the window background instead of just the text background
        self.setAutoFillBackground(True)

        # Center vertically and horizontally
        self.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

        current_time = time.strftime('%I:%M%p').lstrip('0').lower()

        self.setText('{}<br>Am I being intentional?'.format(current_time))

    def show(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint)
        self.showFullScreen()
        self.activateWindow()
        self.raise_()


def get_idle_time():
    """
    Get number of seconds since last user input
    """
    return Quartz.CGEventSourceSecondsSinceLastEventType(
        1, Quartz.kCGAnyInputEventType)


if __name__ == '__main__':
    # Just skip it if the computer isn't being used
    if get_idle_time() > 90:
        sys.exit()

    application = Application(sys.argv)

    # exec() is required for objc
    multiprocessing.set_start_method('spawn')

    target = lambda: None

    if sys.platform == 'darwin':
        target = filter_input

    pool = multiprocessing.Pool(1)

    def filter_input_done_cb(ignored):
        application.closeAllWindows()

    result = pool.apply_async(target, callback=filter_input_done_cb)

    message = Message()
    message.show()

    hide_cursor()

    @atexit.register
    def exit_handler():
        show_cursor()

        # terminate the pool so we don't sit forever waiting on our get()
        print('Terminating pool...')
        pool.terminate()

        print('Joining pool...')
        pool.join()

        print('Retrieving result...')
        try:
            # raise any exceptions raised by the input filtering code
            result.get(0)
        except multiprocessing.TimeoutError:
            print('Timed out waiting for result.')

    # Run for DURATION and then exit
    QtCore.QTimer.singleShot(DURATION, sys.exit)

    print('Starting application...')
    application.exec_()
