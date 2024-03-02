
# Social Media API

This API has been built as an example of how to use fastapi,including database interaction with CRUD operation and implementation of OAuth2 security to use some endpoints.


## Built with

- Pydantic 
- FastAPI
- sqlalchemy
- Alembic
- postgresSQL


## Installation

1.Clone the repository

```bash
  https://github.com/branesh2k/Social_Media_API.git
```

2.Create virtual environment to install dependencies in the name of **venv**.
```
python3 -m venv venv
```
3.Use the **requirements.txt** file to install packages needed for the project on your virtual environment.
```
pip install -r requirements.txt
```
4.Run the project and to start the server, execute the following command:
```
uvicorn app.main:app --reload
```
visit the url http://127.0.0.1:8000/docs to see the app working.This page is SwaggerUI to visualise the frontend.   

![swaggerUI](https://github.com/branesh2k/Social_Media_API/assets/139527284/eccf0b81-65fc-47e2-9249-e2e422e781af)

## Usage/Examples
1.**Authentication:**
Inorder to work with our app you need to `create new user` and configure the credentials in endpoint `POST/users/`.
```json
{
  "email": "user@example.com",
  "password": "string"
}
```
After that you can use your credentials to login and  to execute operations in the endpoints where credentials are required.
***note:*** your tokens will expire after *60mins*.

2.**CRUD operations**.In this case you can use some of the endpoints in the list to execute specific operations over the database.

- `POST/posts/`  - create a new record in DB.
- `GET/posts/`   - show all records from DB.
- `GET/posts/{id}` - Fetch a record by its ID.
- `PUT/posts/{id}` - update a record in DB by its ID.
- `DELETE/posts/{id}` - delete a record in DB by its ID. 
- `POST/vote/`- vote a post by its ID
```json
{
  "post_id": int,
  "dir": 0  $0 or 1
}
```
here, `"dir":0` refers not to vote or not to like the post,changing `"dir":1` is to like/vote the post.
## Acknowledgements

 - [FastAPI course - Sanjeev Thiyagarajan](https://www.youtube.com/watch?v=ToXOb-lpipM&pp=ygUUc2FuamVldiB0aGl5YWdhcmFqYW4%3D)



## Authors

- linkedin- [Branesh P](www.linkedin.com/in/braneshp24)

