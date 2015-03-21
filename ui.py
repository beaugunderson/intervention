import sys
import time

from PySide import QtCore, QtGui


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

        text = '{}<br>Am I being intentional?'.format(current_time)

        super(Message, self).__init__(text=text,
                                      alignment=(QtCore.Qt.AlignVCenter |
                                                 QtCore.Qt.AlignHCenter),
                                      **kwargs)


class Status(QtGui.QWidget):
    """
    The banner displayed at the top of the screen.
    """
    def __init__(self, **kwargs):
        alignment = (QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

        super(Status, self).__init__(focusPolicy=QtCore.Qt.TabFocus, **kwargs)

        self.answer = None

        self.blank_style = ''
        self.highlight_style = 'background-color: green;'

        label_layout = QtGui.QHBoxLayout(spacing=20)

        self.yes = QtGui.QLabel(text='Yes', alignment=alignment,
                                font=self.font())
        self.no = QtGui.QLabel(text='No', alignment=alignment,
                               font=self.font())
        self.ok = QtGui.QLabel(text="It's OK", alignment=alignment,
                               font=self.font())

        label_layout.addWidget(self.yes)
        label_layout.addWidget(self.no)
        label_layout.addWidget(self.ok)

        self.setLayout(label_layout)

    def refresh(self):
        self.yes.setStyleSheet(self.blank_style)
        self.no.setStyleSheet(self.blank_style)
        self.ok.setStyleSheet(self.blank_style)

        if self.answer == 'yes':
            self.yes.setStyleSheet(self.highlight_style)
        elif self.answer == 'no':
            self.no.setStyleSheet(self.highlight_style)
        elif self.answer == 'ok':
            self.ok.setStyleSheet(self.highlight_style)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Y or e.key() == QtCore.Qt.Key_1:
            self.answer = 'yes'
        elif e.key() == QtCore.Qt.Key_N or e.key() == QtCore.Qt.Key_2:
            self.answer = 'no'
        elif e.key() == QtCore.Qt.Key_I or e.key() == QtCore.Qt.Key_3:
            self.answer = 'ok'

        self.refresh()

    def focusInEvent(self, _):
        self.setStyleSheet('background-color: #ccc;')

    def focusOutEvent(self, _):
        self.setStyleSheet('background-color: #293776;')


class Inputs(QtGui.QWidget):
    """
    The banner displayed at the top of the screen.
    """
    def __init__(self, **kwargs):
        super(Inputs, self).__init__(**kwargs)

        self.setContentsMargins(0, 0, 0, 0)

        top_label_layout = QtGui.QHBoxLayout(spacing=20)
        bottom_label_layout = QtGui.QHBoxLayout(spacing=20)

        # XXX: 0 is too little, 1px is too much
        label_style = """padding: 0px;"""

        now_label = QtGui.QLabel(parent=self,
                                 styleSheet=label_style,
                                 text='What am I doing right now?',
                                 font=self.font())

        next_label = QtGui.QLabel(parent=self,
                                  styleSheet=label_style,
                                  text='What am I going to do next?',
                                  font=self.font())

        feel_label = QtGui.QLabel(parent=self,
                                  styleSheet=label_style,
                                  text='How do I feel?',
                                  font=self.font())

        top_label_layout.addWidget(now_label)

        bottom_label_layout.addWidget(next_label)
        bottom_label_layout.addWidget(feel_label)

        input_style = """background-color: white;
                         padding: 5px;
                         color: black;
                         border: 0;"""

        self.now_input = QtGui.QLineEdit(parent=self,
                                         styleSheet=input_style,
                                         font=self.font())

        self.next_input = QtGui.QLineEdit(parent=self,
                                          styleSheet=input_style,
                                          font=self.font())

        self.feel_input = QtGui.QLineEdit(parent=self,
                                          styleSheet=input_style,
                                          font=self.font())

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
        style_sheet = """color: white;
                         background-color: #293776;"""

        super(Window, self).__init__(styleSheet=style_sheet, **kwargs)

        self.setContentsMargins(50, 75, 50, 50)

        fonts = QtGui.QFontDatabase()

        # There's no way to specify the proper font style in CSS
        self.text_font = fonts.font('Museo Slab', '500', 36)
        self.status_font = fonts.font('Museo Slab', '500', 82)
        self.title_font = fonts.font('Museo Slab', '500', 96)

        # Fill the window background instead of just the text background
        self.setAutoFillBackground(True)

        self.layout = QtGui.QVBoxLayout()

        self.add_title()
        self.layout.addSpacing(40)
        self.add_status()
        self.layout.addSpacing(30)
        self.add_inputs()
        self.layout.addStretch(1)

        self.setLayout(self.layout)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            sys.exit()

    def add_status(self):
        status = Status(parent=self, font=self.status_font)

        self.layout.addWidget(status)

    def add_inputs(self):
        inputs = Inputs(parent=self, font=self.text_font)

        self.layout.addWidget(inputs)

    def add_title(self):
        message = Message(parent=self, font=self.title_font)

        self.layout.addWidget(message)

    def show(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint)
        self.showFullScreen()
        self.activateWindow()
        self.raise_()
