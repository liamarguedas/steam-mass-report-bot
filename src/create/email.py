
from protonmail import ProtonMail

username = "omelhordaminhacasa@protonmail.com"
password = "ntEfycYJbk4Z6P6"

proton = ProtonMail()
proton.login(username, password)

# Get a list of all messages
messages = proton.get_messages()

# Read the latest message
message = proton.read_message(messages[0])
print(message.sender.address)  # sender address
print(message.subject)  # subject
print(message.body)
# <html><body><div>it's my image: <img src="cid:1234@proton.me">....

# Render the template, images downloading, converting to BASE64 and insert into html
proton.render(message)
# This is a ready-made html page, with all the pictures, you can save it right away
with open('message.html', 'w', encoding='utf-8') as f:
    f.write(message.body)
print(message.body)
# <html><body><div>it's my image: <img src="data:image/png;base64, iVBORw0K..">....

# Download file from message
first_file = message.attachments[0]
proton.download_files([first_file])
with open(f'{first_file.name}', 'wb') as f:
    f.write(first_file.content)

# Create attachments
with open('image.png', 'rb') as f:
    img = f.read()
with open('resume.pdf', 'rb') as f:
    pdf = f.read()

img_attachment = proton.create_attachment(content=img, name='image.png')
pdf_attachment = proton.create_attachment(content=pdf, name='resume.pdf')

html = f"""
<html>
    <body>
        <h2>Hi, I'm a python developer, here's my photo:</h2>
        <img {img_attachment.get_embedded_attrs()} height="150" width="300">
        <br/>
        Look at my resume, it is attached to the letter.
    </body>
</html>
"""

# Send message
new_message = proton.create_message(
    recipients=["to1@proton.me", "to2@gmail.com", "Name of recipient <to3@outlook.com>"],
    cc=["cc1@proton.me", "cc2@gmail.com", "Name of recipient <cc3@outlook.com>"],
    bcc=["bcc1@proton.me", "bcc2@gmail.com", "Name of recipient <bcc3@outlook.com>"],
    subject="My first message",
    body=html,  # html or just text
    attachments=[img_attachment, pdf_attachment],
    external_id="some-message-id-header-if-you-want-to-specify",
    in_reply_to="message-id-of-the-mail-to-reply-to",
)

sent_message = proton.send_message(new_message)

# Wait for new message
new_message = proton.wait_for_new_message(interval=1, timeout=60, rise_timeout=False, read_message=True)
if 'spam' in new_message.body:
    # Delete spam
    proton.delete_messages([new_message])

# Save session, you do not have to re-enter your login, password, pgp key, passphrase
# WARNING: the file contains sensitive data, do not share it with anyone,
# otherwise someone will gain access to your mail.
proton.save_session('session.pickle')

# Load session
proton = ProtonMail()
proton.load_session('session.pickle', auto_save=True)
# Autosave is needed to save tokens if they are updated
# (the access token is only valid for 24 hours and will be updated automatically)

# Getting a list of all sessions in which you are authorized
proton.get_all_sessions()

# Revoke all sessions except the current one
proton.revoke_all_sessions()
