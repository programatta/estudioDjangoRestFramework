# Demo02

Ejemplo del uso de Django Rest Framework para crear un API REST que hace uso de AWS Cognito.


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

__Nota__: Crear un archivo con las variables siguientes:
* AWS_CLIENT_ID
* AWS_CLIENT_SECRET
* AWS_USER_POOL_ID
* AWS_IDENTITY_POOL_ID
* AWS_REGION
* AWS_ACCESSKEYID
* AWS_SECRETACCESSKEY

y antes de levantar el servidor ejecutar:
~~~
$ source env/<fichero_variables_aws>
~~~

Instalamos boto3 (sdk para python para acceder a los servicios de AWS)

~~~
$ pip install boto3
~~~~

## API
### Peticiones.
#### SIGN UP.
|||
|-|-|
| Method | POST |
| Url | http://localhost:8000/auth/signup/ |
| Data | Requiere un body con JSON {“name”:”Nombre Apellidos”,”email”:”nombre@domain.es”,”password”:”Us3r@D3mo”,”birthdate”:”YYYY-MM-DD”,”phoneNumber”:”+34555555555”,”address”:”Rue del Percebe, 13”} |


#### CONFIRM CODE.
|||
|-|-|
| Method | POST |
| Url | http://localhost:8000/auth/confirmcode/ |
| Data | Requiere un body con JSON {“email”:”nombre@domain.es”,”code”:”XXXXXX”} |


#### SIGN IN.
|||
|-|-|
| Method | POST |
| Url | http://localhost:8000/auth/signin/ |
| Data | Requiere un body con JSON {“email”:”nombre@domain.es”,”password”:”Us3r@D3mo”} |


#### RECOVER PASS.
|||
|-|-|
| Method | POST |
| Url | http://localhost:8000/auth/recoverpass/ |
| Data | Requiere un body con JSON {“email”:”nombre@domain.es”} |


#### RECOVER PASS CONFIRM.
|||
|-|-|
| Method | POST |
| Url | http://localhost:8000/auth/recoverpassconfirm/ |
| Data | Requiere un body con JSON {“email”:”nombre@domain.es”,”newpassword”:”N3w_P4ssw0rd”,”code”:”XXXXXX”} |


#### RESEND CODE.
|||
|-|-|
| Method | POST |
| Url | http://localhost:8000/auth/resendcode/ |
| Data | Requiere un body con JSON {“email”:”nombre@domain.es”} |

