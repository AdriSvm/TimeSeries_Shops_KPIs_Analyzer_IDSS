
# TimeSeries Shops KPIs Analyzer IDSS

A project designed exclusively for KOROSHI brand to analyze the evolution of the main KPIs across their shops to detect anomalies or bad patterns to revert.



## API Reference

#### Login Page

```http
  POST /login/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. A valid username in the db |
| `password` | `string` | **Required**. The password of the username |

Logs in the user and returns {"access_token":"token"} if valid

#### Register a new user

```http
  GET /register/
```
| Authorization | Value |
| :-------- | :------- |
| `Bearer Token` | YOUR_TOKEN |

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username` | `string` | **Required**. The username to register |
| `password` | `string` | **Required**. The password of the username |
| `idalmacen` | `string` | **Required**. A valid IdAlmacen of the brand |
| `is_admin` | `string` | **Required**. True or False |

#### Get the Timeseries Analysis

```http
  GET /get_info/
```
| Authorization | Value |
| :-------- | :------- |
| `Bearer Token` | YOUR_TOKEN |

| Argument | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `start` | `string` | **Required**. The starting date for the analysis |
| `end` | `string` | **Required**. The end date for the analysis |

Returns a Response object with json of all the extractions for the analysis to be shown in the web page


### MUST BE ADMINISTRATOR TO REACH:

#### Get all users

```http
  GET /get_users/
```
| Authorization | Value |
| :-------- | :------- |
| `Bearer Token` | YOUR_TOKEN |

#### Delete some user

```http
  GET /delete_user/
```
| Authorization | Value |
| :-------- | :------- |
| `Bearer Token` | YOUR_TOKEN |

| Argument | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username` | `string` | **Required**.The ID of the username to delete |



## License

[MIT](https://choosealicense.com/licenses/mit/)


## Used By

This project has been used by the following company:

- [KOROSHI](https://www.koroshishop.com/)


## Contact

For any type of message, adriam@phoedata.com is your mail


## Authors

- [@AdriSvm](https://github.com/AdriSvm)
- [@Javierpuerta22](https://github.com/Javierpuerta22)
- [@danielspiri](https://github.com/danielspiri)


