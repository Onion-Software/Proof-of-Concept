from mongoengine import *


# CONTACT
class Telegram(EmbeddedDocument):
    username = StringField()
    id = IntField(default=0)


class Preferences(EmbeddedDocument):
    use_email = StringField(default='no')
    use_telegram = StringField(default='no')
    use_slack = StringField(default='no')


class Holidays(EmbeddedDocument):
    begin = StringField()  # replace with DateField()
    end = StringField()  # replace with DateField()


class Contact(Document):
    meta = {'collection': 'contacts'}
    name = StringField(required=True)
    surname = StringField(required=True)
    email = EmailField(required=True, unique=True)
    telegram = EmbeddedDocumentField(Telegram)
    slack = StringField()
    preferences = EmbeddedDocumentField(Preferences)
    holidays = EmbeddedDocumentField(Holidays)


# PROJECT
class Project(Document):
    meta = {'collection': 'projects'}
    name = StringField(required=True)
    url = StringField(required=True, unique=True)  # replace with URLField()


# SUBSCRIPTION
class Subscription(Document):
    meta = {'collection': 'subscriptions'}
    contact = ReferenceField(Contact, required=True)
    project = ReferenceField(Project, required=True)
