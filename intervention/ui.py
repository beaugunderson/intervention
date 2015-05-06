import os
import sys
import time

import arrow

from PySide import QtCore, QtGui

from . import settings

ZERO = (0, 0, 0, 0)


class Application(QtGui.QApplication):
    """
    The main application.
    """
    def __init__(self, args, ignore_close=True):
        super(Application, self).__init__(args)

        self.ignore_close = ignore_close

    def run(self):
        window = Window(geometry=self.desktop().screenGeometry())
        window.show()

        self.exec_()

    def event(self, event):
        if (event.type() == QtCore.QEvent.Close and
                event.spontaneous() and self.ignore_close):
            event.ignore()

            return False

        return super(Application, self).event(event)


class Message(QtGui.QLabel):
    """
    The banner displayed at the top of the screen.
    """
    def __init__(self, **kwargs):
        current_time = time.strftime('%I:%M%p').lstrip('0').lower()

        text = '{}<br>{}'.format(current_time,
                                 settings.intervention['message'])

        super(Message, self).__init__(text=text,
                                      alignment=(QtCore.Qt.AlignVCenter |
                                                 QtCore.Qt.AlignHCenter),
                                      **kwargs)


class Status(QtGui.QWidget):
    """
    The banner displayed at the top of the screen.
    """
    def __init__(self, **kwargs):
        super(Status, self).__init__(focusPolicy=QtCore.Qt.TabFocus, **kwargs)

        self.answer = None

        self.highlight_style = 'background-color: green;'

        label_kwargs = {
            'alignment': QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter,
            'font': self.font()
        }

        self.yes = QtGui.QLabel(text='Yes', **label_kwargs)
        self.no = QtGui.QLabel(text='No', **label_kwargs)
        self.ok = QtGui.QLabel(text="It's OK", **label_kwargs)

        label_layout = QtGui.QHBoxLayout(spacing=20)

        label_layout.addWidget(self.yes)
        label_layout.addWidget(self.no)
        label_layout.addWidget(self.ok)

        self.setLayout(label_layout)

    def refresh(self):
        self.yes.setStyleSheet('')
        self.no.setStyleSheet('')
        self.ok.setStyleSheet('')

        if self.answer == 'yes':
            self.yes.setStyleSheet(self.highlight_style)
        elif self.answer == 'no':
            self.no.setStyleSheet(self.highlight_style)
        elif self.answer == 'ok':
            self.ok.setStyleSheet(self.highlight_style)

    def keyPressEvent(self, e):
        # Call the parent so we can exit on 'enter' or 'return'
        self.parent().keyPressEvent(e)

        if e.key() == QtCore.Qt.Key_Y or e.key() == QtCore.Qt.Key_1:
            self.answer = 'yes'
        elif e.key() == QtCore.Qt.Key_N or e.key() == QtCore.Qt.Key_2:
            self.answer = 'no'
        elif e.key() == QtCore.Qt.Key_I or e.key() == QtCore.Qt.Key_3:
            self.answer = 'ok'

        self.refresh()

    def focusInEvent(self, _):
        self.setStyleSheet('background-color: #cccccc;')

    def focusOutEvent(self, _):
        self.setStyleSheet('')


class Inputs(QtGui.QWidget):
    """
    The text inputs.
    """
    def __init__(self, **kwargs):
        super(Inputs, self).__init__(objectName='inputs', **kwargs)

        top_label_layout = QtGui.QHBoxLayout(spacing=20)
        bottom_label_layout = QtGui.QHBoxLayout(spacing=20)

        now_label = QtGui.QLabel(parent=self,
                                 text='What am I doing right now?',
                                 font=self.font())

        next_label = QtGui.QLabel(parent=self,
                                  text="What's next?",
                                  font=self.font())

        feel_label = QtGui.QLabel(parent=self,
                                  text='How do I feel?',
                                  font=self.font())

        now_label.setContentsMargins(*ZERO)
        next_label.setContentsMargins(*ZERO)
        feel_label.setContentsMargins(*ZERO)

        top_label_layout.addWidget(now_label)

        bottom_label_layout.addWidget(next_label)
        bottom_label_layout.addWidget(feel_label)

        self.now_input = QtGui.QLineEdit(parent=self, font=self.font())
        self.next_input = QtGui.QLineEdit(parent=self, font=self.font())
        self.feel_input = QtGui.QLineEdit(parent=self, font=self.font())

        self.now_input.setContentsMargins(*ZERO)
        self.next_input.setContentsMargins(*ZERO)
        self.feel_input.setContentsMargins(*ZERO)

        top_input_layout = QtGui.QHBoxLayout(spacing=20)
        bottom_input_layout = QtGui.QHBoxLayout(spacing=20)

        top_input_layout.addWidget(self.now_input)

        bottom_input_layout.addWidget(self.next_input)
        bottom_input_layout.addWidget(self.feel_input)

        layout = QtGui.QVBoxLayout(spacing=10)

        layout.addLayout(top_label_layout)
        layout.addLayout(top_input_layout)

        layout.addSpacing(20)

        layout.addLayout(bottom_label_layout)
        layout.addLayout(bottom_input_layout)

        self.setLayout(layout)


class Window(QtGui.QWidget):
    """
    The application's full-screen container.
    """
    def __init__(self, **kwargs):
        super(Window, self).__init__(objectName='window', **kwargs)

        self.setContentsMargins(50, 75, 50, 50)

        self.setStyleSheet('#window {{ background-color: {}; }}'
                           .format(settings.intervention['background-color']))

        fonts = QtGui.QFontDatabase()

        # There's no way to specify the proper font style in CSS
        self.text_font = fonts.font('Museo Slab', '500', 36)
        self.status_font = fonts.font('Museo Slab', '500', 82)
        self.title_font = fonts.font('Museo Slab', '500', 96)

        message = Message(parent=self, font=self.title_font)
        self.status = Status(parent=self, font=self.status_font)
        self.inputs = Inputs(parent=self, font=self.text_font)

        self.layout = QtGui.QVBoxLayout()

        self.layout.addWidget(message)
        self.layout.addSpacing(40)
        self.layout.addWidget(self.status)
        self.layout.addSpacing(30)
        self.layout.addWidget(self.inputs)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

    def keyPressEvent(self, e):
        if e.key() != QtCore.Qt.Key_Return and e.key() != QtCore.Qt.Key_Enter:
            return

        log_path = os.path.expanduser(settings.intervention['log'])

        now_text = self.inputs.now_input.text()
        next_text = self.inputs.next_input.text()
        feel_text = self.inputs.feel_input.text()

        with open(log_path, 'a') as log:
            log.write('"{}","{}","{}","{}","{}"\n'.format(
                arrow.now().isoformat(),
                self.status.answer,
                now_text, next_text,
                feel_text))

        sys.exit()

    def show(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint)
        self.showFullScreen()
        self.activateWindow()
        self.raise_()
