#locust -f ファイル.py
#http://127.0.0.1:8089

from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)#1-2秒ごとに命令実行

    @task(2)
    def index_page(self):
        self.client.get("/")

    def on_start(self):
        self.login()

    def login(self):
        # login to the application
        response = self.client.get('/accounts/login/')
        csrftoken = response.cookies['csrftoken']
        self.client.post('/accounts/login/',
                         {'email': 'aoneko@exampl.com', 'password': 'aoneko1293'},
                         headers={'X-CSRFToken': csrftoken})
