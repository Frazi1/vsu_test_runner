from locust import TaskSet, task, HttpLocust


class RestTasks(TaskSet):
    @task
    def get_templates(self):
        self.client.get("/template")

    @task
    def code_execution_python_print(self):
        self.client.post("/code/run",
                         json={"clientId": None,
                               "returnType": {"name": "INTEGER"},
                               "functionId": None,
                               "language": {"name": "PYTHON"},
                               "code": "def testF():\n    print '100'\ntestF()",
                               "isPlainCode": True}
                         )

class User(HttpLocust):
    task_set = RestTasks
    host = "http://localhost:8080"
    min_wait = 10
    max_wait = 100
