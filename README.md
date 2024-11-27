# RecipeBoard

## Getting started

The following takes you through the steps of running the server in debug mode.

1. Install required python packages.
`pip install -r requirements.txt`

2. Remove existing migration files.
`cd recipeboard`
`rm -rf api/migrations`

3. Migrate to create database.
`python manage.py makemigrations`
`python manage.py migrate`
`db.sqlite3` should now be in your working directory.

4. Start server
`python manage.py runserver`

## API Endpoints

### GET /api/recipe

Get recipe feed according to user preference.

Request

| Param  | Type   | Description                 |
| ------ | ------ | --------------------------- |
| userId | int    | User id                     |
|      n | int    | Number of recipes requested |

Response

```json
{
    "data": [
        {
            "id": <int>,
            "title": <string>,
            "directions": <string>,
            "url": <string>
       }
    ]
}
```

### GET /api/user/`userId`

Get user profile, including likes and dislikes.

Request

| Param  | Type | Description |
| ------ | ---- | ----------- |
| *None* |      |             |

Response

```json
{
    "data": {
        "id": <int>,
        "name": <string>,
        "likes": [
            {
                "id": <string>,
                "title": <string>
            }
        ],
        "dislikes": [
            {
                "id": <string>,
                "title": <string>
            }
        ]
    }
}
```

### POST /api/user/`userId`

Add a recipe to user's like or dislike list

Request

| Param    | Type | Description |
| -------- | ---- |----------- |
| recipeId | int  | Recipe id   |
| like     | int  | $\begin{cases}1 & \text{if user likes the recipe} \\-1 & \text{if user dislikes the recipe} \\\end{cases}$ |

Response

```json
{}
```

### POST /api/user

Create user and initalize likes.

Request

| Param   | Type   | Description                      |
| ------- | ------ | -------------------------------- |
| cuisine | string | Name of cuisine selected by user |
| name    | string | Username *(optional)* |

Response

```json
{
    "data": {
        "userId": <string>
    }
}
```
