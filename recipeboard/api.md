# API Endpoints

## GET /api/recipe

Get recipe feed according to user preference.

Request

| Param  | Description                 |
| ------ | --------------------------- |
| userId | User id                     |
|      n | Number of recipes requested |

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

## GET /api/user/`userId`

Get user profile, including likes and dislikes.

Request

| Param  | Description |
| ------ | ----------- |
| *None* |             |

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

## POST /api/user/`userId`

Add a recipe to user's like or dislike list

Request

| Param    | Description |
| -------- | ----------- |
| recipeId | Recipe id   |
| like     | $\begin{cases}1 & \text{if user likes the recipe} \\-1 & \text{if user dislikes the recipe} \\\end{cases}$ |

Response

```json
{}
```

## POST /api/user

Create user and initalize likes.

Request

| Param   | Description                      |
| ------- | -------------------------------- |
| cuisine | Name of cuisine selected by user |

Response

```json
{
    "data": {
        "userId": <string>
    }
}
```
