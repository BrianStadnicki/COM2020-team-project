# Views & URLs

Django uses view functions (also referred to as views) to take web requests and return a web response. For this web application, the response consists of the following options: a HTML page, a redirect, or an HTTP error. To utilise these views, URLs are used to execute them whenever the corresponding web address is visited.

The structure of the web application will be abstracted as follows:

```
CS  CS
GET PUT     /user
CS  S
GET PUT     /seller  
CS
GET         /bundles/
CS  S
GET POST    /bundles/new
S
POST        /bundles/new/confirm
CS  C   C
GET PUT DEL /bundles/<int:id>
CS
GET         /reservations/
CS  S   CS
GET PUT DEL /reservations/<int:id>
S
GET         /analytics/
S   S
GET POST    /activity
CS
GET         /reports/
CS  CS
GET POST    /reports/new
CS  CS
GET PUT     /reports/<int:id>
C
GET         /impact
CS
GET         /accessibility
```
