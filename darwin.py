import Quartz


def hide_cursor():
    """
    Hide the mouse cursor.
    """
    Quartz.CGAssociateMouseAndMouseCursorPosition(False)
    Quartz.CGDisplayHideCursor(Quartz.CGMainDisplayID())


def show_cursor():
    """
    Show the mouse cursor.
    """
    Quartz.CGAssociateMouseAndMouseCursorPosition(True)
    Quartz.CGDisplayShowCursor(Quartz.CGMainDisplayID())


def get_idle_time():
    """
    Get the number of seconds since last user input.
    """
    return Quartz.CGEventSourceSecondsSinceLastEventType(
        1, Quartz.kCGAnyInputEventType)
