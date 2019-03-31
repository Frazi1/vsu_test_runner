from locust import TaskSet, task, HttpLocust


class RestTasks(TaskSet):
    @task
    def get_templates(self):
        self.client.get("/template")

    @task
    def code_execution_csharp_print(self):
        self.client.post("/code/run",
                         json={"clientId": None,
                               "returnType": {"name": "STRING"},
                               "functionId": None,
                               "language": {"name": "CSHARP"},
                               "code": """using System;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Feistel
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            var rnd = new Random();
            string message = "Test 1 Test 2 Test 3 Test 4 Test 5 Test 6 Test 7";
//Console.WriteLine(message);
            Console.WriteLine($"Decrypted text: {message}");

        }
    }
}""",
                               "executionType": "ONE_BY_ONE"}
                         )

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
