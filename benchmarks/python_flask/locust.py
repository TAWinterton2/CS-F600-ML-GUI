"""Command to run: locust -f locust.py --headless -u 10 -r 3 -t 5m --html locust_report.html """
from locust import HttpUser, task, constant

class QuickstartUser(HttpUser):
    wait_time = constant(5)
    host = "http://127.0.0.1:5000/"

    @task
    def upload_get_method(self):
        """Test to get homepage."""
        self.client.get("/")


    @task(5)
    def upload_post_method(self):
        """Test to upload file."""
        headers = {'content-type': 'text/html; charset=utf-8'}

        with open('test.csv', 'r') as file:
            data = file.read()
        self.client.request(
            method="POST", 
            url="/", 
            data=data, 
            headers=headers)


    def on_start(self):
        """If something needs to occur when a new user is made, place the code here."""
        pass