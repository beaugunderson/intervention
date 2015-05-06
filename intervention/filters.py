import logging

import AppKit
import Quartz

LOG_FORMAT = '%(relativeCreated)dms %(message)s'

logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
logging.info('filter: Logging started')

EXIT_STRING = 'this must be very, very important'


def filter_input():
    logging.info('Filtering all keys and mouse movements...')

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
                logging.info('Emergency exit!')

                Quartz.CFRunLoopStop(Quartz.CFRunLoopGetCurrent())

        # Filter every event
        return None

    logging.info('Creating tap...')
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

    logging.info('Starting run loop...')
    Quartz.CFRunLoopRun()

    logging.info('Run loop finished.')
