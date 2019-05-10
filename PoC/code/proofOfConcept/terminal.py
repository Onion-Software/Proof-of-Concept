from mongo import MongoDB
from mongoengine import connect


class Terminal:
    def __init__(self, mongo: MongoDB):
        self._mongo = mongo
        self.show()

    def show(self):
        print("Start terminal")
        command = input("Enter command: ")
        while command != "exit":
            if command == "insert contact":
                self.insert_contact()
            elif command == "update contact":
                self.update_contact()
            elif command == "delete contact":
                self.delete_contact()
            elif command == "find contact":
                self.find_contacts()
            elif command == "list contact":
                self.list_contacts()
            elif command == "insert project":
                self.insert_project()
            elif command == "update project":
                self.update_project()
            elif command == "delete project":
                self.delete_project()
            elif command == "find project":
                self.find_projects()
            elif command == "list project":
                self.list_projects()
            elif command == "insert subscription":
                self.insert_subscription()
            elif command == "update subscription":
                self.update_subscription()
            elif command == "delete subscription":
                self.delete_subscription()
            elif command == "find subscription":
                self.find_subscriptions()
            elif command == "list subscription":
                self.list_subscriptions()
            command = input("Enter command: ")
        print("End terminal")

    @staticmethod
    def print_query_no_result():
        print("The query didn't find any result")

    @staticmethod
    def print_record_inserted(record_id):
        print("Record inserted, ID:", str(record_id))

    @staticmethod
    def print_record_updated():
        print("Record updated")

    @staticmethod
    def print_record_deleted():
        print("Record deleted")

    @staticmethod
    def print_record_not_found():
        print("Record not found")

    @staticmethod
    def print_error(e: Exception):
        print("Error.", str(e))

    def insert_contact(self):
        contact_name = input("Name: ")
        contact_surname = input("Surname: ")
        contact_email = input("Email: ")
        contact_telegram_username = input("Telegram: ")
        contact_slack = input("Slack: ")
        contact_use_email = input("Send notifications to email (yes/no): ")
        contact_use_telegram = input("Send notifications to Telegram (yes/no): ")
        contact_use_slack = input("Send notifications to Slack (yes/no): ")
        contact_holidays_begin = input("Holidays begin: ")
        contact_holidays_end = input("Holidays end: ")
        try:
            contact = self._mongo.insert_contact(contact_name, contact_surname, contact_email,
                                                 contact_telegram_username,
                                                 contact_slack,
                                                 contact_use_email, contact_use_telegram, contact_use_slack,
                                                 contact_holidays_begin, contact_holidays_end)
            self.print_record_inserted(contact.id)
        except Exception as e:
            self.print_error(e)

    def update_contact(self):
        contact_name = input("Name: ")
        contact_surname = input("Surname: ")
        contact_email = input("Email: ")
        contact_telegram_username = input("Telegram: ")
        contact_slack = input("Slack: ")
        contact_use_email = input("Send notifications to email (yes/no): ")
        contact_use_telegram = input("Send notifications to Telegram (yes/no): ")
        contact_use_slack = input("Send notifications to Slack (yes/no): ")
        contact_holidays_begin = input("Holidays begin: ")
        contact_holidays_end = input("Holidays end: ")
        try:
            contact = self._mongo.insert_contact(contact_name, contact_surname, contact_email,
                                                 contact_telegram_username,
                                                 contact_slack,
                                                 contact_use_email, contact_use_telegram, contact_use_slack,
                                                 contact_holidays_begin, contact_holidays_end)
            self.print_record_inserted(contact.id)
        except Exception as e:
            self.print_error(e)

    def delete_contact(self):
        query = input("Email of the contact to delete: ")
        contact = self._mongo.find_contact_by_email(query)
        if contact:
            if self.ask_for_confirmation(contact.id):
                self._mongo.delete_contact(contact)
                self.print_record_deleted()
        else:
            self.print_record_not_found()

    def find_contacts(self):
        query = input("Insert query keyword: ")
        contact_array = self._mongo.find_contacts(query)
        if len(contact_array):
            list(map(lambda contact: print(contact.to_json()), contact_array))
        else:
            self.print_query_no_result()

    def list_contacts(self):
        contact_array = self._mongo.list_contacts()
        if len(contact_array):
            list(map(lambda contact: print(contact.to_json()), contact_array))
        else:
            self.print_query_no_result()

    def insert_project(self):
        project_name = input("Name: ")
        project_url = input("URL: ")
        try:
            project = self._mongo.insert_project(project_name, project_url)
            self.print_record_inserted(project.id)
        except Exception as e:
            self.print_error(e)

    def update_project(self):
        project_name = input("Name: ")
        project_url = input("URL: ")
        try:
            project = self._mongo.insert_project(project_name, project_url)
            self.print_record_inserted(project.id)
        except Exception as e:
            self.print_error(e)

    def delete_project(self):
        url = input("URL of the project to delete: ")
        project = self._mongo.find_project_by_url(url)
        if project:
            if self.ask_for_confirmation(project.id):
                self._mongo.delete_project(project)
                self.print_record_deleted()
        else:
            self.print_record_not_found()

    def find_projects(self):
        query = input("Insert query keyword: ")
        project_array = self._mongo.find_projects(query)
        if len(project_array):
            list(map(lambda project: print(project.to_json()), project_array))
        else:
            self.print_query_no_result()

    def list_projects(self):
        project_array = self._mongo.list_projects()
        if len(project_array):
            list(map(lambda contact: print(contact.to_json()), project_array))
        else:
            self.print_query_no_result()

    def insert_subscription(self):
        contact_email = input("Email: ")
        project_url = input("URL: ")
        try:
            subscription = self._mongo.insert_subscription(contact_email, project_url)
            self.print_record_inserted(subscription.id)
        except Exception as e:
            self.print_error(e)

    def update_subscription(self):
        contact_email = input("Email: ")
        project_url = input("URL: ")
        try:
            subscription = self._mongo.insert_subscription(contact_email, project_url)
            self.print_record_inserted(subscription.id)
        except Exception as e:
            self.print_error(e)

    def delete_subscription(self):
        email = input("Email of the contact to delete: ")
        project = input("URL of the project to delete: ")
        subscription = self._mongo.find_subscription_by_email_url(email, project)
        if subscription:
            if self.ask_for_confirmation(subscription.id):
                self._mongo.delete_subscription(subscription)
                self.print_record_deleted()
        else:
            self.print_record_not_found()

    def find_subscriptions(self):
        query = input("Insert query keyword: ")
        subscription_array = self._mongo.find_subscriptions(query)
        if len(subscription_array):
            list(map(lambda subscription: print(subscription.to_json()), subscription_array))
        else:
            self.print_query_no_result()

    def list_subscriptions(self):
        subscription_array = self._mongo.list_subscriptions()
        if len(subscription_array):
            list(map(lambda contact: print(contact.to_json()), subscription_array))
        else:
            self.print_query_no_result()

    def ask_for_confirmation(self, record_id):
        confirm = input(f"Delete record: {record_id} (yes/not)")
        if confirm == "yes" or confirm == "y":
            return True
        else:
            return False


if __name__ == "__main__":
    mongo_client = connect('test-db', host='localhost', port=27017)
    mongo = MongoDB()
    view = Terminal(mongo)
