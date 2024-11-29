import streamlit as st
import sqlite3
import re
import json
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# Configuración de la página (siempre como la primera línea después de importaciones de librerías estándar)
st.set_page_config(
    page_title="Allianz Patrimonial",
    page_icon=":chart_with_upwards_trend:",
    layout="centered"
)

# CSS personalizado
st.markdown("""
    <style>
    .stApp {
        background-color: #1E3A5F;
        color: white;
        font-family: Arial, sans-serif;
    }
    h1 {
        color: white;
        text-align: center;
    }
    label, .stMarkdown h2, .stMarkdown h3 {
        color: white !important;
    }
    input {
        background-color: #f0f0f0 !important;
        color: black !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    button {
        background-color: #005bb5 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-size: 16px;
        cursor: pointer;
    }
    button:hover {
        background-color: #00448A !important;
    }
    a {
        color: #0074D9;
        text-decoration: none;
        font-size: 14px;
    }
    a:hover {
        text-decoration: underline;
    }
    .success-message {
        background-color: white;
        color: green;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Conexión a la base de datos SQLite
conn = sqlite3.connect("users.db")
c = conn.cursor()

# Crear tabla de usuarios y datos del cliente
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        password TEXT
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS cliente_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        edad INTEGER,
        ingreso_mensual REAL,
        ocupacion TEXT,
        objetivo TEXT,
        nivel_riesgo TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')
conn.commit()

# Función para registrar un usuario
def register_user(first_name, last_name, email, phone, password):
    try:
        c.execute('INSERT INTO users (first_name, last_name, email, phone, password) VALUES (?, ?, ?, ?, ?)',
                  (first_name.strip(), last_name.strip(), email.strip(), phone.strip(), password.strip()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# Función para autenticar usuario
def authenticate_user(email, password):
    c.execute('SELECT * FROM users WHERE email = ?', (email.strip(),))
    user = c.fetchone()
    if user and user[5] == password.strip():
        return user
    return None

# Función para validar correo
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Función para validar número de celular
def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

# Función para guardar datos del cliente
def save_cliente_data(user_id, edad, ingreso_mensual, ocupacion, objetivo, nivel_riesgo):
    c.execute('''
        INSERT INTO cliente_data (user_id, edad, ingreso_mensual, ocupacion, objetivo, nivel_riesgo)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, edad, ingreso_mensual, ocupacion, objetivo, nivel_riesgo))
    conn.commit()

# Gestión de vistas
if "view" not in st.session_state:
    st.session_state.view = "login"

# Vista de inicio de sesión
if st.session_state.view == "login":
    st.title("Bienvenido a Allianz Patrimonial")
    st.markdown("### Inicia Sesión")
    email = st.text_input("Correo electrónico", key="login_email", placeholder="ejemplo@correo.com")
    password = st.text_input("Contraseña", type="password", key="login_password", placeholder="••••••••")

    if st.button("Iniciar Sesión"):
        user = authenticate_user(email, password)
        if user:
            st.session_state.user = user
            st.session_state.view = "datos_cliente"
        else:
            st.error("Correo o contraseña incorrectos. Por favor, intenta de nuevo.")

    if st.button("¿No tienes cuenta? Regístrate aquí"):
        st.session_state.view = "register"

# Vista de registro
elif st.session_state.view == "register":
    st.title("Regístrate en Allianz Patrimonial")
    first_name = st.text_input("Nombre", key="register_first_name")
    last_name = st.text_input("Apellido", key="register_last_name")
    email = st.text_input("Correo electrónico", key="register_email", placeholder="ejemplo@correo.com")
    phone = st.text_input("Teléfono", key="register_phone", placeholder="10 dígitos")
    password = st.text_input("Contraseña", type="password", key="register_password", placeholder="••••••••")

    if st.button("Registrarse"):
        if not is_valid_email(email):
            st.error("Por favor, ingresa un correo electrónico válido con '@'.")
        elif not is_valid_phone(phone):
            st.error("Por favor, ingresa un número de celular válido de 10 dígitos.")
        else:
            if register_user(first_name, last_name, email, phone, password):
                st.success("Registro exitoso. Ahora puedes iniciar sesión.")
                st.session_state.view = "login"
            else:
                st.error("El correo electrónico ya está registrado. Usa otro correo.")

    if st.button("Volver a Iniciar Sesión"):
        st.session_state.view = "login"

# Vista de datos del cliente
elif st.session_state.view == "datos_cliente":
    st.title("Datos del Cliente")
    user = st.session_state.user
    st.markdown(f'<div class="success-message">¡Bienvenido, {user[1]} {user[2]}!</div>', unsafe_allow_html=True)

    edad = st.number_input("¿Cuál es tu edad?", min_value=18, max_value=100, step=1)
    ingreso_mensual = st.number_input("¿Cuál es tu ingreso mensual aproximado? (en USD)", min_value=0.0, step=100.0)
    ocupacion = st.selectbox("¿Cuál es tu ocupación?", ["Empleado", "Independiente", "Empresario", "Estudiante", "Jubilado", "Otro"])
    objetivo = st.text_area("¿Cuál es tu principal objetivo al solicitar Allianz Patrimonial?")
    nivel_riesgo = st.selectbox("¿Cuál es tu nivel de tolerancia al riesgo en inversiones?", ["Bajo", "Moderado", "Alto"])

    if st.button("Guardar Datos"):
        save_cliente_data(user[0], edad, ingreso_mensual, ocupacion, objetivo, nivel_riesgo)
        st.success("Datos del cliente guardados exitosamente.")
        st.session_state.view = "datos_poliza"

   

#SEGUNDA PARTE DEL CÓDIGO
        st.session_state.view = "datos_poliza"

# Vista de datos de póliza
elif st.session_state.view == "datos_poliza":
    st.title("Datos de Póliza")

    # Monto inicial de inversión
    inversion_inicial = st.number_input(
        "¿Cuánto dinero deseas invertir inicialmente? (en USD)",
        min_value=100000.0, step=1000.0
    )

    # Duración de la inversión
    plazo_inversion = st.slider(
        "¿Por cuántos años deseas mantener la inversión?",
        min_value=5, max_value=30, value=10
    )

    # Aportaciones subsecuentes
    st.markdown("### Aportaciones subsecuentes")

    num_aportaciones = st.number_input(
        "Número de aportaciones subsecuentes:",
        min_value=1, max_value=10, step=1, value=1
    )

    # Formulario para aportaciones subsecuentes
    with st.form("aportaciones_form"):
        aportaciones = []
        for i in range(int(num_aportaciones)):
            cols = st.columns(2)
            with cols[0]:
                monto = st.number_input(f"Monto de la aportación {i + 1} (en USD):", key=f"monto_{i}", step=100.0)
            with cols[1]:
                anio = st.slider(f"Año de la aportación {i + 1}", min_value=1, max_value=plazo_inversion, key=f"anio_{i}")
            aportaciones.append((monto, anio))
        if st.form_submit_button("Guardar Aportaciones"):
            st.success("Aportaciones subsecuentes guardadas correctamente.")

    # Botón para finalizar
    if st.button("Finalizar y Confirmar Datos"):
        st.success("Datos de póliza guardados correctamente.")


        # CSS personalizado para cambiar a blanco el color del Total Ponderado (%) y su valor
st.markdown(
    """
    <style>
    div[data-testid="stMetricValue"] {
        color: white !important;  /* Cambia el color del valor (ej: 93%) a blanco */
        font-size: 2rem !important;
        font-weight: bold !important;
    }

    /* Estilo personalizado para los mensajes de confirmación */
    .info-message {
        background-color: white;
        color: #1E3A5F;  /* Azul marino, acorde a tu diseño */
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Vista de portafolio de inversiones
st.title("Asignación de Ponderaciones en tu Portafolio")

# Cargar el archivo con los ETFs válidos
try:
    with open('valid_etfs.json', 'r') as f:
        valid_etfs = json.load(f)
except FileNotFoundError:
    st.error("El archivo 'valid_etfs.json' no se encontró. Por favor, verifica la ruta.")
    valid_etfs = []
except json.JSONDecodeError:
    st.error("El archivo 'valid_etfs.json' tiene un formato inválido.")
    valid_etfs = []

# Mostrar la selección de ETFs si existen datos válidos
if valid_etfs:
    options = [etf['name'] for etf in valid_etfs]
    
    # Usar una clave diferente en el multiselect
    selected_etfs_widget = st.multiselect(
        "Selecciona los ETFs para tu portafolio de inversión",
        options=options
    )
    
    # Guardar selección en st.session_state después de interactuar
    if selected_etfs_widget:
        st.session_state.selected_etfs = selected_etfs_widget

    # Si se seleccionan ETFs, permite asignar ponderaciones
    if "selected_etfs" in st.session_state and st.session_state.selected_etfs:
        st.write("### Asignación de Ponderaciones en tu Portafolio")

        # Inicializar variables
        ponderaciones = {}

        # Crear sliders dinámicos para asignar ponderaciones
        cols = st.columns([3, 1])  # Dividir en columnas para sliders y suma dinámica
        with cols[0]:  # Columna de sliders
            for etf_name in st.session_state.selected_etfs:
                ponderaciones[etf_name] = st.number_input(
                    f"Ponderación para {etf_name} (%)",
                    min_value=0,
                    max_value=100,
                    step=1,
                    key=f"peso_{etf_name}",
                    format="%d"  # Mostrar como entero
                )

        # Calcular la suma total de las ponderaciones
        total_ponderacion = sum(ponderaciones.values())

        # Mostrar el total ponderado en formato de porcentaje
        with cols[1]:
            st.metric(
                label="Total Ponderado (%)",
                value=f"{int(total_ponderacion)}%"
            )

        # Validar si la suma excede 100%, es menor o es igual
        if total_ponderacion == 100:
            st.success("Ponderaciones guardadas correctamente.")
            st.session_state.ponderaciones = ponderaciones

            # Selección de período para los datos históricos
            st.write("### Selecciona el Período para los Datos Históricos de los ETFs Seleccionados")
            periodo = st.selectbox(
                "Selecciona el período para los datos históricos de los ETFs seleccionados",
                ['1mo', '3mo', '6mo', '1y', '5y']
            )

            # Botón para calcular proyección
            calcular_proyeccion_button = st.button("Calcular Proyección")

            # Si se presiona el botón de calcular proyección, mostrar resultados
            if calcular_proyeccion_button:
                st.write("## Resultados del Cálculo de Proyección")
                st.write(f"Período seleccionado: {periodo}")

                comparativo_data = []

                for etf_name in st.session_state.selected_etfs:
                    # Obtener símbolo del ETF del archivo JSON
                    symbol = next((etf['symbol'] for etf in valid_etfs if etf['name'] == etf_name), None)

                    if symbol:
                        # Descargar datos históricos del ETF usando yfinance
                        ticker = yf.Ticker(symbol)
                        data = ticker.history(period=periodo)

                        # Calcular rendimiento promedio anual, volatilidad anual y ratio de Sharpe
                        data['daily_return'] = data['Close'].pct_change()
                        avg_annual_return = data['daily_return'].mean() * 252
                        annual_volatility = data['daily_return'].std() * (252 ** 0.5)
                        sharpe_ratio = avg_annual_return / annual_volatility if annual_volatility != 0 else 0

                        # Guardar resultados en el comparativo
                        comparativo_data.append({
                            'ETF': etf_name,
                            'Símbolo': symbol,
                            'Rendimiento Promedio Anual (%)': avg_annual_return * 100,
                            'Volatilidad Anual (%)': annual_volatility * 100,
                            'Ratio de Sharpe': sharpe_ratio
                        })

                # Mostrar tabla consolidada con métricas por ETF
                st.write("### Métricas por ETF Seleccionado")
                df_comparativo = pd.DataFrame(comparativo_data)
                st.dataframe(df_comparativo.style.format({
                    'Rendimiento Promedio Anual (%)': "{:.2f}%",
                    'Volatilidad Anual (%)': "{:.2f}%",
                    'Ratio de Sharpe': "{:.2f}"
                }))

                # Gráfica de rendimiento vs riesgo
                st.write("### Rendimiento vs Riesgo")
                fig, ax = plt.subplots()
                ax.scatter(
                    df_comparativo['Volatilidad Anual (%)'],
                    df_comparativo['Rendimiento Promedio Anual (%)'],
                    color='blue', s=100
                )
                for i, row in df_comparativo.iterrows():
                    ax.text(row['Volatilidad Anual (%)'], row['Rendimiento Promedio Anual (%)'], row['Símbolo'])
                ax.set_xlabel("Volatilidad Anual (%)")
                ax.set_ylabel("Rendimiento Promedio Anual (%)")
                ax.set_title("Gráfico de Rendimiento vs Riesgo")
                st.pyplot(fig)

        elif total_ponderacion > 100:
            st.error("El total de las ponderaciones supera el 100%. Ajusta los valores.")
        elif total_ponderacion < 100:
            st.warning("El total de las ponderaciones debe ser exactamente 100%.")

# Eliminar duplicaciones
# La siguiente parte del código está repetida innecesariamente y puede ser eliminada:
# data.append({
# 'ETF': etf_name,
# 'Símbolo': symbol,
# 'Rendimiento Promedio Anual (%)': avg_annual_return * 100,
# 'Volatilidad Anual (%)': annual_volatility * 100,
# 'Ratio de Sharpe': sharpe_ratio
# })
# Y el bloque de código para mostrar la tabla y la gráfica también está repetido innecesariamente.

# El código anterior debería ser suficiente y no necesita duplicarse.
