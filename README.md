# Links Email Parsing

- https://tools.ietf.org/html/rfc2060.html # IMAP Protocol
- https://docs.python.org/3.6/library/imaplib.html
- https://docs.python.org/3.6/library/email.message.html
- https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/
- https://gist.github.com/baali/2633554
- http://stackoverflow.com/questions/32885661/python-imap-locate-emails-with-attachments-in-inbox-and-move-them-to-a-folder
- http://code.activestate.com/recipes/302086-strip-attachments-from-an-email-message/
- https://github.com/izderadicka/imap_detach/blob/master/src/imap_detach/mail_info.py
- http://code.activestate.com/recipes/498189-imap-mail-server-attachment-handler/
- http://bruno.im/2009/dec/18/decoding-emails-python/

# Usage

- Use Python 3
- Adjust config.ini sample, rename to config.ini and copy into env folder
	- Set IMAP mailbox login configuration
	- Decide to run single folder or all folders
	- Activate test mode with enhanced logging if needed
- Run email_attachment_remover.py

# Hint

Run it on a fast internet connection as it has to download all mails and attachments and partly upload it again
