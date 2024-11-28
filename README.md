# Sistema de Inventario para Librería "El Gran Poeta"

Este proyecto es un sistema de inventario para la organización de las bodegas de una librería. Proporciona funcionalidades para la gestión de productos, movimientos entre bodegas y generación de informes.

## Características

1. **Gestión de Productos**:
   - Creación de productos (Libros, Revistas, Enciclopedias).
   - Asignación de editorial y autores a los productos.
   - Breve descripción o resumen de los productos.
   - Asignación de productos a bodegas específicas.

2. **Gestión de Bodegas**:
   - Creación y gestión de bodegas.
   - Visualización de los productos disponibles en cada bodega.

3. **Movimientos entre Bodegas**:
   - Registro de movimientos de productos entre bodegas.
   - Detalle de cada movimiento:
     - Bodega de origen.
     - Bodega de destino.
     - Lista de productos y cantidades.
     - Usuario que realiza el movimiento.

4. **Informes**:
   - Cantidad de productos por bodega.
   - Tipos de productos por editorial.
   - Listado de movimientos recientes.
   - Listar productos de una bodega por una editorial específica.

5. **Roles de Usuario**:
   - Jefe de Bodega: Gestión de productos, bodegas e informes.
   - Bodeguero: Realización de movimientos de productos entre bodegas.

6. **Autenticación**:
   - Login basado en roles.
   - Restricciones de acceso según el rol del usuario.

## Requisitos

- Python 3.11+
- Django 5.1+
- SQLite (u otro motor de base de datos configurado)
- Paquetes adicionales:
  - `djangorestframework`
  - `coreapi`

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu_usuario/sistembiblio.git
cd sistembiblio
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

4. Realizar las migraciones de la base de datos:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Ejecutar el servidor de desarrollo:
```bash
python manage.py runserver
```

## Uso
- Acceder a la URL ` http://127.0.0.1:8000.`
- Iniciar sesión con un usuario existente o el superusuario creado.
- Gestionar productos, bodegas y movimientos desde la interfaz de la aplicación.