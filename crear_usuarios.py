"""
Script para crear usuarios iniciales en Supabase
Ejecutar este script UNA SOLA VEZ para crear los usuarios
"""

from supabase import create_client, Client
import os

# Configuración - Lee desde variables de entorno del sistema
SUPABASE_URL = os.getenv("SUPABASE_URL_ENTORNO")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVISE_ROLE_ENTORNO")  # ⚠️ Usar SERVICE KEY para crear usuarios

# Validar que las variables existan
print("=" * 60)
print("🔍 VERIFICANDO VARIABLES DE ENTORNO")
print("=" * 60)
print(f"SUPABASE_URL: {'✓ Configurada' if SUPABASE_URL else '✗ FALTA'}")
print(f"SUPABASE_SERVICE_KEY: {'✓ Configurada' if SUPABASE_SERVICE_KEY else '✗ FALTA'}")
print("=" * 60)

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    print("\n❌ ERROR: Faltan variables de entorno")
    print("\n📝 Debes configurar en las variables de entorno del sistema:")
    print("   - SUPABASE_URL_ENTORNO")
    print("   - SUPABASE_SERVICE_KEY")
    print("\n💡 Para obtener la SERVICE KEY:")
    print("   1. Ve a tu proyecto en Supabase")
    print("   2. Settings > API")
    print("   3. Copia el 'service_role' key (NO el 'anon' key)")
    exit(1)

# IMPORTANTE: Para crear usuarios necesitas la SERVICE ROLE KEY (no la anon key)
# La encuentras en: Settings > API > service_role key
# ⚠️ NUNCA la uses en el frontend, solo en scripts de backend

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Usuarios a crear
USUARIOS = [
    {
        "email": "miguell.mmahecha@distoyota.com.co",
        "password": "Distoyota2025",  # Cambiar por contraseñas seguras
        "email_confirm": True
    }
]

def crear_usuarios():
    print("=" * 60)
    print("🚀 CREANDO USUARIOS EN SUPABASE")
    print("=" * 60)
    
    for usuario in USUARIOS:
        try:
            # Crear usuario con Supabase Auth
            response = supabase.auth.admin.create_user({
                "email": usuario["email"],
                "password": usuario["password"],
                "email_confirm": usuario["email_confirm"]
            })
            
            print(f"✅ Usuario creado: {usuario['email']}")
            print(f"   ID: {response.user.id}")
            
        except Exception as e:
            if "already registered" in str(e).lower() or "already exists" in str(e).lower():
                print(f"⚠️  Usuario ya existe: {usuario['email']}")
            else:
                print(f"❌ Error creando {usuario['email']}: {str(e)}")
    
    print("=" * 60)
    print("✅ PROCESO COMPLETADO")
    print("=" * 60)
    print("\nCREDENCIALES DE ACCESO:")
    print("-" * 60)
    for usuario in USUARIOS:
        print(f"Email: {usuario['email']}")
        print(f"Contraseña: {usuario['password']}")
        print("-" * 60)

if __name__ == "__main__":
    crear_usuarios()