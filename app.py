from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
import os
from datetime import datetime

app = Flask(__name__)

# ========================================
# CONFIGURACIÓN DE SUPABASE
# ========================================
# Reemplaza estos valores con tus credenciales reales de Supabase

# Opción 1: Usando la URL del proyecto (RECOMENDADO)
SUPABASE_URL = "https://oonzxoergmpguhvvfgis.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9vbnp4b2VyZ21wZ3VodnZmZ2lzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ1OTA5ODEsImV4cCI6MjA4MDE2Njk4MX0.B7gWkGirbTqbigAJAl4xAPUzy-8B1drr4pS70gGtsuE"  # Esta es la clave "anon" o "public" que encuentras en Settings > API

# Para encontrar tu SUPABASE_KEY:
# 1. Ve a tu proyecto en Supabase
# 2. Click en Settings (⚙️) en el menú lateral
# 3. Click en API
# 4. Copia la clave "anon" "public" (NO uses la service_role key)

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
# RUTAS
# ========================================
@app.route('/')
def index():
    return render_template('index.html', forms=FORMS_CONFIG)

@app.route('/form/<int:form_id>')
def form_page(form_id):
    form = next((f for f in FORMS_CONFIG if f['id'] == form_id), None)
    if not form:
        return "Formulario no encontrado", 404
    return render_template('form.html', form=form)  # ← Aquí pasas 'form'

@app.route('/api/save_form', methods=['POST'])
def save_form():
    try:
        data = request.json
        form_id = data.get('form_id')
        form_data = data.get('data')
        
        form = next((f for f in FORMS_CONFIG if f['id'] == form_id), None)
        if not form:
            return jsonify({'error': 'Formulario no encontrado'}), 404
        
        # Agregar timestamp
        form_data['created_at'] = datetime.now().isoformat()
        
        # Guardar en Supabase
        result = supabase.table(form['table']).insert(form_data).execute()
        
        return jsonify({'success': True, 'data': result.data})
    except Exception as e:
        print(f"Error al guardar: {str(e)}")  # Para debug
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_records/<table_name>')
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
        print(f"Error al obtener registros: {str(e)}")  # Para debug
        return jsonify({'error': str(e)}), 500

@app.route('/api/search')
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
        print(f"Error en búsqueda: {str(e)}")  # Para debug
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
    app.run(debug=True, port=5000)