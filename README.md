# django-simple-online-store

# Pasos previos:

1. Configuración de la base de datos.
  
    Crear archivo .py con los parametros de la base de datos.

2. Crear base de datos:
  
    Con el nombre registrado en la configuración

3. Migracion de los modelos a las bases de datos:

```cmd
  python manage.py makemigrations
```

```cmd
  python manage.py migrate
```

4. Inicializar proyecto:

  ```cmd
  python manage.py runserver
  ```
  
## Consideraciones:

  Para modificar a un usuario a modo administrador:
  
  Una vez creado el usuario, modificamos su status a administrador
  
  de la siguiente manera:
  
  ```cmd
  python manage.py shell
  
  ```
  
  ```python
  from manage_resources.models import *
  
  usuario = Usuarios.objects.get(email='{tu email}')
  usuario.admin = True
  usuario.save()
  
  ```
  
  despues de este cambio podra acceder al modo adminstrador
 
  
  
