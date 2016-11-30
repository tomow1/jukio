from flask import Flask

app = Flask(__name__)

app.config.update(dict())
app.config.from_envvar('JUKIO_SETTINGS', silent=True)

import jukio.views
