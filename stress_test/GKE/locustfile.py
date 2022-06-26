from locust import HttpUser, task

# http://34.140.74.77.nip.io

class HelloWorldUser(HttpUser):
    @task
    def listing_language(self):
        self.client.get("/list-tweet-language/en")

    @task
    def listing_location(self):
        self.client.get("/list-tweet-location/us")

    @task
    def listing_random(self):
        self.client.get("/list-tweet-random")

    @task
    def listing_search(self):
        self.client.get("/list-tweet-search/ukraine")

    @task
    def listing_username(self):
        self.client.get("/list-tweet-username/BARRAL42604501")
        
    @task
    def admin_add(self):
        self.client.get("/add-tweet/user/pass/renatousername/renatotweettext")
        
    @task
    def admin_delete(self):
        self.client.get("/delete-tweet/renato/password/111")