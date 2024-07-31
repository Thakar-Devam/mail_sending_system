from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mail import Mail, Message
import threading
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'thakardevam007@gmail'
app.config['MAIL_PASSWORD'] = 'your_email_password'

mail = Mail(app)

sender_email = app.config['MAIL_USERNAME']

def send_email_later(subject, sender, recipients, body, send_time):
    delay = (send_time - datetime.now()).total_seconds()
    time.sleep(delay)
    with app.app_context():
        msg = Message(subject, sender=sender, recipients=[recipients])
        msg.body = body
        mail.send(msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        from_email = sender_email
        to_email = request.form['to']
        subject = request.form['subject']
        message = request.form['message']
        schedule_time = request.form.get('time')

        if schedule_time:
            send_time = datetime.strptime(schedule_time, '%Y-%m-%dT%H:%M')
            threading.Thread(target=send_email_later, args=(subject, from_email, to_email, message, send_time)).start()
            flash('Email scheduled successfully!', 'success')
        else:
            try:
                msg = Message(subject, sender=from_email, recipients=[to_email])
                msg.body = message
                mail.send(msg)
                flash('Email sent successfully!', 'success')
            except Exception as e:
                flash(str(e), 'danger')

        return redirect('/')

    return render_template('index.html', sender_email=sender_email)

@app.route('/update_from', methods=['GET', 'POST'])
def update_from():
    global sender_email
    if request.method == 'POST':
        new_sender_email = request.form['new_sender_email']
        sender_email = new_sender_email
        flash('Sender email updated successfully!', 'success')
        return redirect('/')

    return render_template('update_from.html', sender_email=sender_email)

if __name__ == '__main__':
    app.run(debug=True)
