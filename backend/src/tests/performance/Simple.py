from locust import TaskSet, task, HttpLocust


class RestTasks(TaskSet):
    @task
    def get_templates(self):
        self.client.get("/template")


class User(HttpLocust):
    task_set = RestTasks
    host = "http://localhost:8080"
    min_wait = 10
    max_wait = 100
