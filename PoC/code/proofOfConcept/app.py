from flask import Flask, render_template, request
from mongo import *


class Application:
    def __init__(self, mongo: MongoDB):
        self._app = Flask(__name__)
        self._mongo = mongo

        @self._app.route('/')
        def index():
            return render_template('index.html')

        @self._app.route('/form', methods=['GET', 'POST'])
        def form_data():
            return render_template('form.html')

        @self._app.route('/insert_contact', methods=['GET', 'POST'])
        def insert_contact():
            if request.method == 'POST':
                name = request.form['contact_name']  # 'contact_name' is the 'name' of the input field
                surname = request.form['contact_surname']
                email = request.form['contact_email']
                telegram = request.form['contact_telegram_username']
                slack = request.form['contact_slack_email']
                use_email = request.form['contact_use_email']
                use_telegram = request.form['contact_use_telegram']
                use_slack = request.form['contact_use_slack']
                holidays_begin = request.form['contact_holidays_begin']
                holidays_end = request.form['contact_holidays_end']
                try:
                    self._mongo.insert_contact(name, surname, email, telegram, slack, use_email, use_telegram,
                                               use_slack,
                                               holidays_begin, holidays_end)
                except Exception as e:
                    return str(e)
                return "Contatto inserito"

        @self._app.route('/insert_project', methods=['GET', 'POST'])
        def insert_project():
            if request.method == 'POST':
                name = request.form['project_name']  # 'contact_name' is the 'name' of the input field
                url = request.form['project_url']
                try:
                    self._mongo.insert_project(name, url)
                except Exception as e:
                    return str(e)
                return "Progetto inserito"

        @self._app.route('/insert_subscription', methods=['GET', 'POST'])
        def insert_subscription():
            if request.method == 'POST':
                email = request.form['contact_email']  # 'contact_name' is the 'name' of the input field
                url = request.form['project_url']
                try:
                    self._mongo.insert_subscription(email, url)
                except Exception as e:
                    return str(e)
                return "Iscrizione inserita"

        @self._app.route('/contacts')
        def contacts():
            return render_template('contacts.html', contact_array=self._mongo.list_contacts())

        @self._app.route('/find_contacts', methods=['GET', 'POST'])
        def find_contacts():
            keyword = request.form['keyword']
            return render_template('contacts.html', contact_array=self._mongo.find_contacts(keyword))

        @self._app.route('/projects')
        def projects():
            return render_template('projects.html', project_array=self._mongo.list_projects())

        @self._app.route('/find_projects', methods=['GET', 'POST'])
        def find_projects():
            keyword = request.form['keyword']
            return render_template('projects.html', project_array=self._mongo.find_projects(keyword))

        @self._app.route('/subscriptions')
        def subscriptions():
            return render_template('subscriptions.html', subscription_array=self._mongo.list_subscriptions())

        @self._app.route('/find_subscriptions', methods=['GET', 'POST'])
        def find_subscriptions():
            keyword = request.form['keyword']
            return render_template('subscriptions.html', subscription_array=self._mongo.find_subscriptions(keyword))

    def start(self):
        self._app.run(host="0.0.0.0", port=80)


if __name__ == '__main__':
    mongo_client = connect('test-db', host='localhost', port=27017)
    mongo = MongoDB()
    Application(mongo).start()
