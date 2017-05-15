#!/usr/bin/env python
# -*- coding: utf-8 -*-

import imaplib
import email
import time
import configparser

config = configparser.ConfigParser()
config.sections()
config.read('env/config.ini')
config.sections()

# Global vars
all_folders = config['DEFAULT']['all_folders']
max_size = int(config['DEFAULT']['max_size'])
standard_folder = config['DEFAULT']['standard_folder']
test_mode = config['DEFAULT']['test_mode']
server = config['mailserver']['server']
user = config['mailserver']['user']
password = config['mailserver']['password']

def check_size(msg, size):
    find = False
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        size_real = len(str(part)) / 4 * 3 / 1000
        if (size_real > size):
            find = True
    return find

ReplaceString = """
This message contained an attachment that was stripped out.
The original type was: %(content_type)s
The filename was: %(filename)s,
(and it had additional parameters of:
%(params)s)
"""

def sanitise_size(msg, size):
    ct = msg.get_content_type()
    fn = msg.get_filename()
    size_real = len(str(msg)) / 4 * 3 / 1000
    print('file size: ', size_real)
    if (size_real > size) & (msg.get_content_maintype() != 'multipart'):
        print('hit!')
        params = msg.get_params()[1:]
        params = ', '.join([ '='.join(p) for p in params ])
        replace = ReplaceString % dict(content_type=ct,
                                       filename=fn,
                                       params=params)
        msg.set_payload(replace)
        for k, v in msg.get_params()[1:]:
            msg.del_param(k)
        msg.set_type('text/plain')
        del msg['Content-Transfer-Encoding']
        del msg['Content-Disposition']
    else:
        if msg.is_multipart():
            payload = [ sanitise_size(x, size) for x in msg.get_payload() ]
            msg.set_payload(payload)
    return msg


# File handler 1: check for completed folders
def read_and_search(file_name, folder_name):
    found_folder = False
    try:
        f = open(file_name)
        try:
            for line in f:
                if (line == folder_name + "\n"):
                    found_folder = True
        except:
            print('issue')
        finally:
            f.close()
    except (IOError, OSError) as e:
        print('no file')
    print('found_folder:', found_folder)
    return found_folder

# File handler 2: append completed folders
def apppend_folder(file_name, entry):
    print('append')
    with open(file_name, 'a+') as f:
        f.write(entry + "\n")

# Main script
def run_saver(mail):
    a = 0; b = 0
    mail.list()
    res, list = mail.list()
    if all_folders == 'False':
        print('Scanning just one folder: ',standard_folder )
        folders = [ standard_folder ]
    else:
        folders = [ item.split()[-1].decode() for item in list ]
    for folder in folders:
        if test_mode == 'True':
            a += 1
            if a == 2:
                break
        print('folder:', folder)
        if read_and_search('folders.txt', folder):
            continue
        mail.select(folder)
        result_mails, data_mails = mail.uid('search', None, "ALL")

        for email_uid in data_mails[0].split():
            if test_mode == 'True':
                b += 1
                if b == 2:
                    break
            mytime = imaplib.Time2Internaldate(time.time())
            print('uid: ', email_uid)
            result, data = mail.uid('fetch', email_uid, '(RFC822)')
            try:
                raw_email = (data[0][1]).decode('utf-8')
            except:
                try:
                    raw_email = (data[0][1]).decode('iso-8859-1')
                except:
                    raw_email = (data[0][1]).decode('utf-8', 'backslashreplace')

            email_message = email.message_from_string(raw_email)
            if check_size(email_message, max_size):
                print('optimizing email')
                new_mess = sanitise_size(email_message, max_size)
                mail.append(folder, '', mytime, new_mess.as_string().encode())
                mail.uid('STORE', email_uid  , '+FLAGS', '(\Deleted)')
        mail.expunge()
        # apppend_folder('folders.txt', folder)
        print('folder completed: ', folder)


def main():
    try:
        while True:
            mail = imaplib.IMAP4_SSL(server)
            r, d = mail.login(user, password)
            assert r == 'OK', 'login failed'
            try:
                run_saver(mail)
            except mail.abort as e:
                continue
            mail.logout()
            break
    except KeyboardInterrupt:
        print('\nCancelling...')
    except (SystemExit):
        e = get_exception()
        if getattr(e, 'code', 1) != 0:
            raise SystemExit('ERROR: %s' % e)

if __name__ == '__main__':
    main()
