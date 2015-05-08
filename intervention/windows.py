import win32api


# TODO: probably possible via:
# widget.setCursor(Qt.BlankCursor)
# widget.unsetCursor()
def hide_cursor():
    pass


def show_cursor():
    pass


def get_idle_time():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000
