# Dipeat

This document provides an overview of the API endpoints and functionalities for the user profile management system. The API is designed for user authentication, profile creation, and related operations, including the forgot password functionality.

## API Documentation
1. Signup:
- Endpoint: `/signup`
- Method: `POST`
- Request Body:
  ```json
  {
    "first_name": "new_user",
    "email": "new_user@example.com",
    "password": "new_user_password"
  }
  ```
- Response:
  * Status Code: 200 OK
    - ```json
      {
        "message": "User created successfully. Check your mail for username"
      }
      ```

2. Login:
- Endpoint: `/login`
- Method: `POST`
- Request Body:
  ```json
  {
  "username": "example_user",
  "password": "user_password"
  }
  ```
- Response:
  * Status Code: 200 OK
    - ```json
      {
        "refresh": "refresh_token",
        "access": "access_token"
      }
      ```

3. POST Profile:
- Endpoint: `/profile`
- Method: `POST`
- Description: Create user profile.
- Authentication: Requires a valid access token.
- Request:
  * Headers:
    - Authorization: Bearer <access_token>
  * Body:
    ```json
    {
      "bio": "Test"
    }
    ```
- Response:
  * Status Code: 200 OK
    - ```json
      {
        "message": "Profile created successfully"
      }
      ```

4. GET Profile:
- Endpoint: `/profile`
- Method: `GET`
- Description: Retrieve user profile information.
- Authentication: Requires a valid access token.
- Request:
  * Headers:
    - Authorization: Bearer <access_token>
- Response:
  * Status Code: 200 OK
    - ```json
      {
        "user": {
            "username": "example_user",
            "email": "example_user@example.com"
        },
        "profile": {
            "bio": "Test"
        }
      }
      ```

## Installation and Setup
1. Clone the repository:
   `git clone https://github.com/AM-5006/Dipeat.git`
2. Navigate to the project directory:
   `cd Dipeat`
3. Install the required packages using pip:
  `pip install -r requirements.txt`
4. Start the server:
  `python manage.py runserver`

The App should now be accessible at http://localhost:8000/
     
