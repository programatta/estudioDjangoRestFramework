# Demo01

Ejemplo del uso de Django Rest Framework para crear un API REST protegido por Access Token.

API creado a través de __ViewSet__ y __Routes__ que simplifican mucho el código.

## Preparación.
Primera vez, crear el entorno virutual desde el raiz del proyecto:
~~~~
$ python3 -m venv env
$ source env/bin/activate
~~~~

Siguientes veces:
~~~~
$ source env/bin/activate
~~~~

## Modelo.
Se opera sobre un modelo sencillo llamado __Transaction__ que tiene los siguientes campos:

* id: Identificación de transacción (YYYYMMDDHHMMSS).
* paid: Cantidad de euros pagada.
* date: Fecha de la transacción.
* product: Producto comprado

Tiene un campo oculto que indica quien es el propietario de la transacción denominado __owner__.

__Nota:__ Por cada cambio en el modelo tenemos que hacer:
~~~~
$ python manage.py makemigrations demo01app
$ python manage.py migrate
~~~~

## API
Se crea a través de __ViewSet__ y __Routes__. Simplifica el código pero deja el access point con el nombre que se mapea en __Routes__ (en este ejemplo __transactions__).

__Nota__: Se crean usuarios a través de la consola de administración de Django.

### Peticiones.
#### API-TOKEN-AUTH.
|||
|-|-|
| Method | POST |
| Url | http://localhost:8000/api-token-auth/ |
| Data | Requiere un body con JSON {"username":"xxxxx","password":"xxxxxx"} |

Retorna un JSON con el token de acceso e identificador de usuario.

#### User List Transactions.
|||
|-|-|
| Method | GET |
| Url | http://localhost:8000/transactions/ |
| Data | Requiere el header Authorization: Token {{token_value}} |

Retorna un JSON con una lista de transacciones del usuario.

#### Create Transaction.
|||
|-|-|
| Method | POST |
| Url | http://localhost:8000/transactions/ |
| Data | Requiere el header Authorization: Token {{token_value}} |
|      | Requiere un body: {"id":"20200331184614", "paid":10, "date":"2020-03-31", "product":"bufanda"}

Retorna un JSON con la transacción creada.

#### Get User Transaction.
|||
|-|-|
| Method | GET |
| Url | http://localhost:8000/transactions/<ID_TRANSACTION>/ |
| Data | Requiere el header Authorization: Token {{token_value}} |

Retorna un JSON con la transacción pedida.

#### Update User Transaction.
|||
|-|-|
| Method | PUT |
| Url | http://localhost:8000/transactions/<ID_TRANSACTION>/ |
| Data | Requiere el header Authorization: Token {{token_value}} |
|      | Requiere un body: {"id":"20200331184614", "paid":10, "date":"2020-03-31", "product":"bufanda roja"}

Retorna un JSON con la transacción modificada.

#### Delete User Transaction.
|||
|-|-|
| Method | DELETE |
| Url | http://localhost:8000/transactions/<ID_TRANSACTION>/ |
| Data | Requiere el header Authorization: Token {{token_value}} |

No retorna nada.

