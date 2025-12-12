from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from supabase import create_client, Client
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key =  os.getenv("SUPABASE_SERVISE_ROLE_ENTORNO")

# ========================================
# CONFIGURACIÓN DE SUPABASE
# ========================================
# Reemplaza estos valores con tus credenciales reales de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL_ENTORNO")
SUPABASE_KEY = os.getenv("SUPABASE_KEY_ENTORNO")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ========================================
# CONFIGURACIÓN DE FORMULARIOS
# ========================================
FORMS_CONFIG = [
    {'id': 1, 'name': 'RECEPCIÓN', 'table': 'recepcion'},
    {'id': 2, 'name': 'EVALUACIÓN', 'table': 'evaluacion'},
    {'id': 3, 'name': 'INFORMACIÓN - SITE', 'table': 'informacion_site'},
    {'id': 4, 'name': 'COTIZACIÓN REPUESTOS', 'table': 'cotizacion_repuestos'},
    {'id': 5, 'name': 'APROBACIÓN', 'table': 'aprobacion'},
    {'id': 6, 'name': 'ENTREGA - INFORME/OL J', 'table': 'entrega_informe'},
    {'id': 7, 'name': 'SOLICITUD REPUESTOS', 'table': 'solicitud_repuestos'},
    {'id': 8, 'name': 'SOLICITUD REPUESTOS 2', 'table': 'solicitud_repuestos_2'},
    {'id': 9, 'name': 'INGRESO TALLER', 'table': 'ingreso_taller'},
    {'id': 10, 'name': 'INICIO DEL TRABAJO', 'table': 'inicio_trabajo'},
    {'id': 11, 'name': 'DESARMADO', 'table': 'desarmado'},
    {'id': 12, 'name': 'ARMADO', 'table': 'armado'},
    {'id': 13, 'name': 'LIMPIEZA', 'table': 'limpieza'},
    {'id': 14, 'name': 'INSPECCIÓN', 'table': 'inspeccion'}
]

# ========================================
# DECORADOR DE AUTENTICACIÓN
# ========================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ========================================
# RUTAS DE AUTENTICACIÓN
# ========================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        try:
            # Autenticar con Supabase
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            # Guardar información del usuario en la sesión
            session['user'] = {
                'id': response.user.id,
                'email': response.user.email,
                'access_token': response.session.access_token
            }
            
            return jsonify({'success': True, 'message': 'Login exitoso'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 401
    
    # Si el usuario ya está logueado, redirigir al inicio
    if 'user' in session:
        return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    try:
        if 'user' in session:
            # Cerrar sesión en Supabase
            supabase.auth.sign_out()
        session.clear()
    except:
        pass
    return redirect(url_for('login'))

# ========================================
# RUTAS PROTEGIDAS
# ========================================
@app.route('/')
@login_required
def index():
    return render_template('index.html', forms=FORMS_CONFIG)

@app.route('/view_records')
@login_required
def view_records():
    """Página para visualizar registros completos"""
    return render_template('view_records.html')

@app.route('/form/<int:form_id>')
@login_required
def form_page(form_id):
    form = next((f for f in FORMS_CONFIG if f['id'] == form_id), None)
    if not form:
        return "Formulario no encontrado", 404
    return render_template('form.html', form=form)

@app.route('/api/save_form', methods=['POST'])
@login_required
def save_form():
    try:
        data = request.json
        form_id = data.get('form_id')
        form_data = data.get('data')
        
        form = next((f for f in FORMS_CONFIG if f['id'] == form_id), None)
        if not form:
            return jsonify({'error': 'Formulario no encontrado'}), 404
        
        # Agregar timestamp y usuario
        form_data['created_at'] = datetime.now().isoformat()
        form_data['user_email'] = session['user']['email']
        
        # Guardar en Supabase
        result = supabase.table(form['table']).insert(form_data).execute()
        
        return jsonify({'success': True, 'data': result.data})
    except Exception as e:
        print(f"Error al guardar: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_records/<table_name>')
@login_required
def get_records(table_name):
    try:
        # Buscar por placa u orden
        placa = request.args.get('placa')
        orden = request.args.get('orden')
        
        query = supabase.table(table_name).select('*')
        
        if placa:
            query = query.eq('placa', placa)
        if orden:
            query = query.eq('orden', orden)
            
        result = query.execute()
        return jsonify({'success': True, 'data': result.data})
    except Exception as e:
        print(f"Error al obtener registros: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/search')
@login_required
def search():
    try:
        placa = request.args.get('placa')
        orden = request.args.get('orden')
        
        results = {}
        for form in FORMS_CONFIG:
            try:
                query = supabase.table(form['table']).select('*')
                if placa:
                    query = query.eq('placa', placa)
                if orden:
                    query = query.eq('orden', orden)
                result = query.execute()
                if result.data:
                    results[form['name']] = result.data
            except Exception as e:
                print(f"Error en tabla {form['table']}: {str(e)}")
                continue
        
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        print(f"Error en búsqueda: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/test_connection')
def test_connection():
    """Ruta para probar la conexión con Supabase"""
    try:
        # Intenta hacer una consulta simple
        result = supabase.table('recepcion').select('*').limit(1).execute()
        return jsonify({
            'success': True, 
            'message': 'Conexión exitosa con Supabase',
            'data': result.data
        })
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': str(e),
            'message': 'Error de conexión. Verifica tus credenciales.'
        }), 500

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Iniciando aplicación...")
    print(f"📡 URL de Supabase: {SUPABASE_URL}")
    print("⚠️  IMPORTANTE: Asegúrate de configurar SUPABASE_KEY")
    print("=" * 50)
    port = int(os.environ.get("PORT", 5000))  # Render asigna el puerto

    # IMPORTANTE: escuchar en 0.0.0.0 y usar el puerto dinámico
    app.run(host="0.0.0.0", port=port, debug=True)