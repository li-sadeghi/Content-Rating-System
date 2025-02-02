# Content-Rating-System
A Django-based content rating system built with Django REST Framework, allowing users to view and rate posts efficiently.

# How to run this project?
You have two options to run this project, first using docker and the other using configs:
1. Run project using Docker:
   At first, you should fill the .env file in the base directory of the project properly and then run the command below:
   ```
   docker-compose up --build
   ```
   Then you can use this command:
   ```
   docker-compose exec app python manage.py migrate
   ```
   or you can use this ```docker-compose exec app /bin/bash``` and then ```docker-compose exec app python manage.py migrate``` to migrate the migration files of project on your db container or ```docker-compose exec app python manage.py test``` to run all tests of the project.
   for restarting celery:
   ```
   docker-compose restart celery
   ```
   for finish using docker:
   ```
   docker-compose down
   ```
   if you had any problem while starting docker containers, you can use ```docker-compose logs app``` to see the problem.
   
2. Run project using configs:
   At first you should create a ```development.env``` file in the config folder of the project, and then copy and fill all variables that we need that all of them is in the example.env file that is in the config folder.
   then activate a virtualenv for the project using command below:
   ```
   python -m venv .venv
   ```
   and then
   ```
   source .venv/bin/activate
   ```
   and then install all requirements of the project using this command:
   ```
   pip install -r requirements.in
   ```
   and then you can migrate and test project:
   ```
   python manage.py migrate
   ```
   ```
   python manage.py test
   ```
# About the project:
This project is about managing posts and their ratings by users. First, I'll give a brief explanation of the endpoints in this project, and then I'll talk about the challenges I faced and how I handled and solved them.

**Endpoints:**

1. **Register Endpoint:**  
   `api/users/register/`

2. **Login Endpoint:**  
   `api/users/login/`

3. **Refresh Token Endpoint:**  
   `api/users/refresh_token/`

4. **List Posts Endpoint:**  
   `api/content_rating/posts/`

5. **Create/Update Rating by User for Posts Endpoint:**  
   `api/content_rating/rating/<int:pk>/`

This project is entirely built using Django REST Framework (DRF), and the views are based on the REST framework. Unit tests have been written for all functionalities, including registration, login, token refresh, listing posts, and creating/updating ratings.

**Challenges:**
In this project, the first major challenge was handling situations where there are a very large number of ratings for each post. This could cause issues in the API response for listing posts because we needed to calculate the average rating and the total number of ratings for each post. This could slow down the system and cause performance problems. To solve this issue, we added two fields to each post to store and update the average rating and the total number of ratings. This problem has several potential solutions:
Here’s a simpler translation of the text into English:

---

### **Suggested Solutions to Improve System Performance:**

#### **1. Using Precomputed Fields in the Model**
- **Explanation:** Add two fields to the post model to store the average rating and total number of ratings. These fields are updated whenever a rating is added or changed.
- **Advantages:** Fast access without heavy calculations for each request.
- **Disadvantages:** Requires careful management to ensure data consistency.

---

#### **2. Using Caching (e.g., Redis)**
- **Explanation:** Store the average rating and total number of ratings in a caching system like Redis.
- **Advantages:** Reduces database queries and improves response speed.
- **Disadvantages:** Requires cache management and ensuring timely updates.

---

#### **3. Asynchronous Processing with Celery**
- **Explanation:** Use Celery for periodic calculations and updates of average ratings and total counts in the background.
- **Advantages:** Reduces load on the main server and improves real-time performance.
- **Disadvantages:** Adds complexity and requires additional setup for Celery and message queues.

---

#### **4. Database Indexing**
- **Explanation:** Add an index to the `content_id` field in the rating model to improve search speed.
- **Advantages:** Faster queries for large datasets.
- **Disadvantages:** Indexing alone is not enough for heavy calculations like averaging.



### **Reasons for Using Precomputed Fields:**

1. **Real-Time Access:**  
   Precomputed fields allow instant access to the average rating and total number of ratings without recalculating them every time a request is made. This improves response times significantly.

2. **Reduced Database Load:**  
   By storing the calculated values directly in the model, the system avoids performing complex calculations (like averaging or counting) on the fly, which reduces the load on the database.

3. **Simplified Queries:**  
   Fetching data becomes simpler and faster because the required values (average rating and total ratings) are already available in the post model, eliminating the need for additional queries or joins.

4. **Scalability:**  
   As the number of ratings grows, precomputing these values ensures the system remains performant, even with large datasets.

5. **Consistency:**  
   By updating the fields whenever a rating is added or modified, the system maintains accurate and consistent data without relying on external processes.

6. **Ease of Implementation:**  
   Adding precomputed fields is relatively straightforward and doesn’t require additional infrastructure (like caching systems or task queues).


---
**Second Challenge:**

The second challenge we faced was when a large number of users might rush to rate certain posts in specific channels, often giving emotional ratings. This could cause the average rating of those posts to drop significantly, which wouldn’t reflect the true rating of the post. To solve this problem, we implemented a few solutions. First, we limited the number of ratings a user could give per minute (we also wrote tests for this). Additionally, we used a periodic Celery task to detect such anomalies.

Here’s how the anomaly detection works:  
We run the task every hour and check each post for anomalies. To detect anomalies, we calculate the average number of users who rated the post in the past week for a specific hour and compare it to the previous hour. If the number exceeds a certain threshold, it’s flagged as an anomaly. To fix the anomaly, we adjust the total ratings by adding a weighted value based on the current average rating and recent ratings. This helps balance the anomaly. We also made the weighting factors variable so that we can easily adjust them if we decide to change our approach in the future.

However, there are other potential solutions that could also be helpful for this issue.

--- 

