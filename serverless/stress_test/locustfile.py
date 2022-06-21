from locust import HttpUser, task

# https://ukraine-api-gateway-624ct11y.ew.gateway.dev

class HelloWorldUser(HttpUser):
    @task
    def listing_language(self):
        self.client.get("/list-tweet-language?language=en")

    @task
    def listing_location(self):
        self.client.get("/list-tweet-location?location=us")

    @task
    def listing_random(self):
        self.client.get("/list-tweet-random")

    @task
    def listing_search(self):
        self.client.get("/list-tweet-search?search=ukraine")

    @task
    def listing_username(self):
        self.client.get("/list-tweet-username?username=BARRAL42604501")
        
    @task
    def admin_add(self):
        self.client.get("/admin-add-tweet?username=user&password=pass&tweetusername=renato_username&tweettext=renato_tweettext")
        
    @task
    def admin_delete(self):
        self.client.get("/admin-delete-tweet?username=renato&password=password&tweetid=111")
        