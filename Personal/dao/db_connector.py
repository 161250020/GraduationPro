import re
import pymongo
from _datetime import datetime
from Personal.model.Email import Mail


def clean_str(string):
    string = re.sub(r"[^\u4e00-\u9fff]", " ", string)
    string = re.sub(r"\s{2,}", " ", string)
    string = ' '.join(filter(lambda x: x, string.split(' ')))
    return string.strip()

def get_mycol():
    myclient = pymongo.MongoClient('mongodb://localhost:27017')

    mydb = myclient["admin"]
    mycol = mydb["mail"]
    return mycol


def get_mail_by_date(ct: datetime, et: datetime):
    mycol = get_mycol()
    mails = []
    for i in mycol.find({"ct": {"$gte": ct}, "et": {"$lte": et}}, {'_id': 1, 'title': 1, 'from': 1, 'to': 1, 'cc': 1, 'date': 1, 'doc': 1, 'split': 1, 'emailKind': 1}):
        mail = Mail(i['_id'], i['title'], i['from'], i['to'], i['cc'], i['date'], i['doc'], i['split'], i['emailKind'])
        mails.append(mail)
    emails = trans(mails)
    return emails

def get_all_email():
    mycol = get_mycol()
    mails = []
    for i in mycol.find({}, {'_id': 1, 'title': 1, 'from': 1, 'to': 1, 'cc': 1, 'date': 1, 'doc': 1, 'split': 1, 'emailKind': 1}):
        mail = Mail(i['_id'], i['title'], i['from'], i['to'], i['cc'], i['date'], i['doc'], i['split'], i['emailKind'])
        mails.append(mail)
    emails = trans(mails)
    return emails

def trans(mails):
    emails = []
    for mail in mails:
        email = ''
        for line in mail.split:
            temp = clean_str(line)
            if not temp.isspace():
                email += ' ' + temp
        email = email[1:]
        if not email.isspace():
            emails.append([mail, email])
    return emails



def main():
    print(get_all_email())

if __name__ == '__main__':
    main()