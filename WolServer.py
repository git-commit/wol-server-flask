

import os
from flask import Flask, render_template, send_from_directory, flash, request
from wakeonlan import wol
from wtforms.fields.core import StringField
from wtforms.validators import InputRequired, ValidationError
from flask_wtf import Form
import random
from ieeemac import is_mac

app = Flask(__name__)
app.secret_key = b'r\x9du\xdc\x8b\x12\xe8\x12\xa5\xa7]s\xc96\xfe\x1bmA\xc0\x1a\xb5\x94Z\xfd'

valid_macs = ('FF-FF-FF-FF-FF-FF',  # windows
              'FF:FF:FF:FF:FF:FF',  # unix
              'FFFF.FFFF.FFFF',  # cisco
              'FFFFFFFFFFFF')  # bare

@app.route('/', methods=('GET', 'POST'))
def index():
    form = MacForm()

    if form.is_submitted():
        mac = request.form['mac']
        if form.validate():
            api_wake(mac)
            flash("Sent magic packet to: %s" % mac)
        else:
            flash('Please provide a valid mac address. Example: %s ; Your input: %s' % (random.choice(valid_macs), mac))

    return render_template('mac.html', form=form)


@app.route('/api/wake/<mac>')
def api_wake(mac):
    wol.send_magic_packet(mac)
    app.logger.debug('Sending Magic Packet to: %s' % mac)
    return ''


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

class MacForm(Form):
    mac = StringField('mac', validators=[InputRequired()])

    def validate_mac(form, field):
        if not is_mac(field.data):
            raise ValidationError("Please provide a valid mac address: %s" % field.data)


if __name__ == '__main__':
    app.run(debug=True)
