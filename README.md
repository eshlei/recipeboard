# RecipeBoard

## Getting started

The following takes you through the steps of running the server in debug mode.

1. Install required python packages.

    ```bash
    pip install -r requirements.txt
    ```

2. Migrate to create database.

    ```bash
    cd recipeboard
    python manage.py makemigrations
    python manage.py migrate
    ```

    `db.sqlite3` should now be next to `manage.py`.

3. Start server.

    ```bash
    python manage.py runserver
    ```

## API Endpoints

### GET /api/recipe/

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
            "id": "int",
            "title": "string",
            "directions": "string",
            "url": "string"
       }
    ]
}
```

### GET /api/user/`userId`/

Get user profile, including likes and dislikes.

Request

| Param  | Type | Description |
| ------ | ---- | ----------- |
| *None* |      |             |

Response

```json
{
    "data": {
        "id": "int",
        "name": "string",
        "likes": [
            {
                "id": "string",
                "title": "string"
            }
        ],
        "dislikes": [
            {
                "id": "string",
                "title": "string"
            }
        ]
    }
}
```

### POST /api/user/`userId`/

Add a recipe to user's like or dislike list

Request

| Param    | Type | Description                                           |
| -------- | ---- |------------------------------------------------------ |
| recipeId | int  | Recipe id                                             |
| like     | int  | Whether the user likes the recipe for not. See below. |

$$like=\begin{cases}1 & \text{if user likes the recipe} \\-1 & \text{if user dislikes the recipe} \end{cases}$$

Response

```json
{}
```

### POST /api/user/

Create user and initalize likes.

Request

| Param   | Type   | Description                      |
| ------- | ------ | -------------------------------- |
| cuisine | string | Name of cuisine selected by user |
| name    | string | Username *(optional)*            |

Response

```json
{
    "data": {
        "userId": "string"
    }
}
```
