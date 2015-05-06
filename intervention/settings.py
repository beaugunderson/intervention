import os
import sys

from tini import Tini

filenames = [
    './intervention-dev.ini',  # useful when developing
    os.path.join(os.path.expanduser('~'), '.intervention.ini'),
    os.path.join(os.path.expanduser('~'), '.config', 'intervention.ini'),
]

defaults = {
    'intervention': {
        'message': 'Am I being intentional?',
        'background-color': '#293776',
        'log': os.path.join(os.path.expanduser('~'), 'intervention.log'),
    }
}

sys.modules[__name__] = Tini(filenames, defaults=defaults)
