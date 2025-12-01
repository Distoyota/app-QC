# Sistema de Formularios Relacionales - 14 Etapas

## 📋 Instrucciones de Instalación y Configuración

### 1. Estructura de Carpetas del Proyecto

```
formularios-app/
│
├── app.py                  # Backend Flask
├── requirements.txt        # Dependencias Python
│
├── templates/
│   ├── index.html         # Menú principal
│   └── form.html          # Template de formularios
│
└── static/
    └── style.css          # Estilos CSS
```

### 2. Configuración de Supabase

#### Paso 1: Crear proyecto en Supabase
1. Ve a [supabase.com](https://supabase.com)
2. Crea una cuenta o inicia sesión
3. Crea un nuevo proyecto
4. Guarda el **URL** y la **API Key (anon/public)**

#### Paso 2: Crear las tablas
1. En tu proyecto de Supabase, ve a **SQL Editor**
2. Copia y pega el contenido del archivo `supabase_tables.sql`
3. Ejecuta el script (Run)
4. Verifica que las 14 tablas se hayan creado correctamente

### 3. Instalación del Backend

#### Paso 1: Instalar Python
Asegúrate de tener Python 3.8 o superior instalado:
```bash
python --version
```

#### Paso 2: Crear archivo requirements.txt
Crea un archivo `requirements.txt` con:
```
Flask==3.0.0
supabase==2.3.0
python-dotenv==1.0.0
```

#### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configuración de la Aplicación

#### Paso 1: Editar app.py
En el archivo `app.py`, reemplaza estas líneas:
```python
SUPABASE_URL = "TU_SUPABASE_URL"
SUPABASE_KEY = "TU_SUPABASE_KEY"
```

Con tus credenciales de Supabase que guardaste anteriormente.

#### Paso 2: Crear carpetas necesarias
```bash
mkdir templates
mkdir static
```

#### Paso 3: Colocar los archivos
- `index.html` y `form.html` → carpeta `templates/`
- `style.css` → carpeta `static/`

### 5. Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

### 6. Uso del Sistema

#### Flujo de trabajo:
1. **Crear Orden**: Inicia con el formulario 1 (RECEPCIÓN)
   - Ingresa la placa y número de orden
   - Estos datos serán la clave para relacionar todos los formularios

2. **Formularios Subsecuentes**: 
   - Usa la misma placa y orden en todos los formularios siguientes
   - El sistema relacionará automáticamente todos los registros

3. **Buscar Registros**:
   - Usa el buscador en la página principal
   - Busca por placa o número de orden
   - Ver todos los formularios relacionados

### 7. Características del Sistema

✅ **14 Formularios Independientes**
- Cada formulario tiene sus propios campos específicos
- Todos conectados por placa y número de orden

✅ **Base de Datos Relacional**
- Todas las tablas están relacionadas mediante el número de orden
- Integridad referencial garantizada

✅ **Búsqueda Avanzada**
- Buscar por placa o número de orden
- Ver historial completo de trámites

✅ **Interfaz Moderna**
- Diseño responsive (móvil y escritorio)
- Colores distintivos para cada formulario
- Validación de campos requeridos

### 8. Personalización

#### Agregar más campos a un formulario:
Edita el diccionario `formFieldsConfig` en `form.html`:

```javascript
1: [ // RECEPCIÓN
    { name: 'nuevo_campo', label: 'Nuevo Campo', type: 'text', required: false }
]
```

#### Cambiar colores:
Edita la clase `.form-card` en `style.css`

### 9. Solución de Problemas

**Error: "No module named 'supabase'"**
```bash
pip install supabase
```

**Error de conexión a Supabase:**
- Verifica que la URL y API Key sean correctas
- Verifica que las tablas estén creadas

**Formulario no guarda:**
- Verifica la consola del navegador (F12)
- Revisa los logs de Flask en la terminal

### 10. Siguiente Nivel

Para producción, considera:
- Agregar autenticación de usuarios
- Implementar roles y permisos
- Agregar notificaciones por email
- Generar reportes PDF
- Agregar carga de archivos/imágenes

---

## 🚀 ¡Listo para usar!

El sistema está diseñado para ser simple pero potente. Cada formulario representa una etapa del proceso y todos están conectados mediante las relaciones en la base de datos.