from classes import *
import re


class MongoDB:
    def __init__(self):
        pass

    @staticmethod
    def first_element_if_exists(query_result):
        if len(query_result):
            return query_result[0]
        else:
            return None

    @staticmethod
    def insert_contact(name, surname, email, telegram_username, slack, use_email, use_telegram, use_slack,
                       holidays_begin, holidays_end):
        telegram = Telegram(username=telegram_username)
        preferences = Preferences(use_email=use_email, use_telegram=use_telegram, use_slack=use_slack)
        holidays = Holidays(begin=holidays_begin, end=holidays_end)
        contact = Contact(name=name, surname=surname, email=email, telegram=telegram,
                          slack=slack, preferences=preferences, holidays=holidays)
        contact.save()
        return contact

    @staticmethod
    def update_contact(name, surname, email, telegram_username, slack, use_email, use_telegram, use_slack,
                       holidays_begin, holidays_end):
        # TODO - check contact
        telegram = Telegram(username=telegram_username)
        preferences = Preferences(use_email=use_email, use_telegram=use_telegram, use_slack=use_slack)
        holidays = Holidays(begin=holidays_begin, end=holidays_end)
        contact = Contact(name=name, surname=surname, email=email, telegram=telegram,
                          slack=slack, preferences=preferences, holidays=holidays)
        contact.save()
        return contact

    @classmethod
    def find_contact_by_email(cls, query):
        query_result = Contact.objects(email=query)
        return cls.first_element_if_exists(query_result)

    @staticmethod
    def delete_contact(contact: Contact):
        contact.delete()

    # TODO - find contact

    @staticmethod
    def find_contacts(keyword):
        regex = re.compile(f".*{keyword}.*", re.IGNORECASE)
        query_result = Contact.objects()
        return list(filter(lambda contact: regex.match(contact.name) or regex.match(contact.surname) or regex.match(
            contact.email) or regex.match(
            contact.slack) or regex.match(contact.telegram.username), query_result))

    @staticmethod
    def list_contacts():
        return Contact.objects()

    # PROJECT METHODS
    @staticmethod
    def insert_project(name, url):
        project = Project(name=name, url=url)
        project.save()
        return project

    @staticmethod
    def update_project(name, url):
        # TODO - update project
        project = Project(name=name, url=url)
        project.save()
        return project

    @classmethod
    def find_project_by_url(cls, url):
        query_result = Project.objects(url=url)
        return cls.first_element_if_exists(query_result)

    @staticmethod
    def delete_project(project: Project):
        project.delete()

    # TODO - find project
    @staticmethod
    def find_projects(keyword):
        regex = re.compile(f".*{keyword}.*", re.IGNORECASE)
        query_result = Project.objects()
        return list(filter(lambda project: regex.match(project.name) or regex.match(project.url), query_result))

    @staticmethod
    def list_projects():
        return Project.objects()

    # SUBSCRIPTION METHODS
    @classmethod
    def insert_subscription(cls, contact_email, project_url):
        contact_query_result = Contact.objects(email=contact_email)
        project_query_result = Project.objects(url=project_url)
        contact = cls.first_element_if_exists(contact_query_result)
        project = cls.first_element_if_exists(project_query_result)
        if contact and project:
            subscription = Subscription(contact=contact, project=project)
            subscription.save()
            return subscription
        else:
            raise Exception("Contatto o progetto inesistenti")

    @classmethod
    def update_subscription(cls, contact_email, project_url):
        # TODO - check subscription
        contact_query_result = Contact.objects(email=contact_email)
        project_query_result = Project.objects(url=project_url)
        contact = cls.first_element_if_exists(contact_query_result)
        project = cls.first_element_if_exists(project_query_result)
        if contact and project:
            subscription = Subscription(contact=contact, project=project)
            subscription.save()
            return subscription
        else:
            raise Exception("Contatto o progetto inesistenti")

    @staticmethod
    def delete_subscription(subscription: Subscription):
        subscription.delete()

    @classmethod
    def find_subscription_by_email_url(cls, email, url):
        contact_query_result = Contact.objects(email=email)
        project_query_result = Project.objects(url=url)
        contact = cls.first_element_if_exists(contact_query_result)
        project = cls.first_element_if_exists(project_query_result)
        if contact and project:
            query_result = Subscription.objects(contact=contact, project=project)
            return cls.first_element_if_exists(query_result)
        else:
            return None

    # TODO - find subscription
    @staticmethod
    def find_subscriptions(keyword):
        regex = re.compile(f".*{keyword}.*", re.IGNORECASE)
        query_result = Subscription.objects()
        return list(filter(lambda subscription: regex.match(subscription.contact.name) or regex.match(
            subscription.contact.surname) or regex.match(
            subscription.contact.email) or regex.match(
            subscription.contact.slack) or regex.match(subscription.contact.telegram.username) or regex.match(
            subscription.project.name) or regex.match(subscription.project.url), query_result))

    @staticmethod
    def list_subscriptions():
        return Subscription.objects()

    @classmethod
    def update_telegram_id(cls, telegram_username, telegram_id):
        telegram_query_result = Contact.objects(telegram__username=telegram_username)
        contact = cls.first_element_if_exists(telegram_query_result)
        if contact:
            contact.telegram.id = telegram_id
            contact.save()
        else:
            raise Exception("Questo username di telegram non è presente nel DB")

    @classmethod
    def get_interested_recipients(cls, project_url: str):
        project = cls.find_project_by_url(project_url)
        subscription_query_result = Subscription.objects(project=project)
        if subscription_query_result:
            recipients = dict(telegram=list(), email=list(), slack=list())
            for record in subscription_query_result:
                cls.add_recipients_to_dict(recipients, record.contact.email)
            return recipients
        else:
            return None

    @classmethod
    def add_recipients_to_dict(cls, recipients: dict, contact_email: str):
        contact_query_result = Contact.objects(email=contact_email)
        contact = cls.first_element_if_exists(contact_query_result)
        if contact.preferences.use_email == "yes":
            recipients["telegram"].append(contact.telegram.id)
        if contact.preferences.use_email == "yes":
            recipients["email"].append(contact.email)
        if contact.preferences.use_slack == "yes":
            recipients["slack"].append(contact.slack)
