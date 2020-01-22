Wenu API
--------

API REST basada en eve\_sqlalchemy que permite acceder a información
relacionada con los sensores del sistema Wenu.

La información puede ser almacenada en cualquier DBMS soportado por
SQLAlchemy. Las mediciones pueden, alternativamente, estar almacenadas
en un servidor InfluxDB, en dicho caso el servidor WenuAPI actúa como
un proxy para esta información proveyendo una interfaz homogenea a los
clientes.

Instalación del servidor
------------------------

```
sudo ./scripts/install.sh
```

Instalación del cliente
------------------------

TODO: setup.py


Uso del cliente
---------------

```python
# conexión con el sevidor
server = Server('http://localhost:5000')

# listado de entidades/tablas disponibles en el servidor
# (este listado se genera de forma dinámica consultando al servidor)
ent = server.entities

# acceso al listado de entradas en la entidad Mote
print(server.Mote.list())

# instanciación local de una nueva Mote
newmote = server.Mote(**arguments)
# creación de una nueva entrada en el servidor a partir de la
# instancia creada
newmote.create()

# creación de una nueva entrada en una sola línea
server.Action(mote_id=2, command='turn_off', arguments='').create()

# obtención de un elemento por id
mote = server.Mote.get_by_id(5)

# modificación de parámetros de forma local
mote.x = 20
mote.y = 5

# almacenamiento de cambios en el servidor
mote.save()

# diccionario de campos dentro de una entrada
mote.fields

# campos regulares dentro de una entrada (los que no empiezan con _)
mote.regular_fields()
```

