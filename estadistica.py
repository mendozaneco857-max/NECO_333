
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================
st.title("📊 DASHBOARD ESTADÍSTICO")

st.markdown("""
### Universidad Amazónica de Pando

**Carrera:** Ingeniería de Sistemas  
**Materia:** Estadística I  
**Proyecto:** Análisis Estadístico de Encuesta Estudiantil  
**Gestión:** 2026
""")

# ==========================================================
# CARGA DE DATOS
# ==========================================================

@st.cache_data
def cargar_datos():
    return pd.read_excel(
        "ENCUESTA ESTUDIANTIL.xlsx",
        sheet_name="Respuestas de formulario 1"
    )

df = cargar_datos()

# ==========================================================
# COLUMNAS DEL FORMULARIO
# ==========================================================

DISPOSITIVO = "Dispositivo que usas PRINCIPALMENTE para estudiar:"
INTERNET = "¿Quién cubre el costo de tu conexión a internet?"
CONEXION = "Tipo de conexión que usas con más frecuencia:"
ESPACIO = "¿Cuentas con un espacio tranquilo en casa para estudiar en línea?"
FACULTAD = "FACULTAD"
CALIDAD = "Calidad percibida de tu conexión para actividades académicas"
INTERRUPCIONES = "¿Con qué frecuencia experimentas interrupciones durante clases/trabajo en línea?"
LIMITACIONES = "Limitaciones técnicas que has enfrentado (marca hasta 3):"
PLATAFORMAS = "Plataformas que has utilizado (marca hasta 3):"

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("📊 MENÚ DE NAVEGACIÓN")

menu = st.sidebar.radio(
    "Seleccione una sección",
    [
        "🏠 Inicio",
        "📊 Dashboard Ejecutivo",
        "📋 Base de Datos",
        "📱 Tipo de Dispositivo",
        "🌐 Responsable del Internet",
        "📡 Tipo de Conexión",
        "🏠 Espacio de Estudio",
        "🎓 Facultad",
        "📶 Calidad de Conexión",
        "⛔ Frecuencia de Interrupciones",
        "⚙️ Limitaciones Técnicas",
        "💻 Plataformas Utilizadas",
        "📌 Conclusiones"
    ]
)
# ==========================================================
# FUNCIONES
# ==========================================================

def imprimir_terminal(titulo, tabla):
    print("\n")
    print("=" * 90)
    print(titulo.upper())
    print("=" * 90)
    print(tabla)
    print("=" * 90)

def tabla_frecuencias(serie):

    frecuencia = serie.value_counts(dropna=False)

    tabla = pd.DataFrame({
        "Categoría": frecuencia.index,
        "fi": frecuencia.values
    })

    tabla["hi"] = (tabla["fi"] / tabla["fi"].sum()).round(4)
    tabla["%"] = (tabla["hi"] * 100).round(2)
    tabla["Fi"] = tabla["fi"].cumsum()
    tabla["Hi"] = tabla["hi"].cumsum().round(4)

    return frecuencia, tabla

def tabla_frecuencias_multiple(serie):

    datos = (
        serie.dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
    )

    frecuencia = datos.value_counts()

    tabla = pd.DataFrame({
        "Categoría": frecuencia.index,
        "fi": frecuencia.values
    })

    tabla["hi"] = (tabla["fi"] / tabla["fi"].sum()).round(4)
    tabla["%"] = (tabla["hi"] * 100).round(2)
    tabla["Fi"] = tabla["fi"].cumsum()
    tabla["Hi"] = tabla["hi"].cumsum().round(4)

    return frecuencia, tabla

def grafico_torta(frecuencia, titulo):

    fig, ax = plt.subplots(figsize=(14, 10))

    # Crear torta sin porcentajes internos
    wedges, _ = ax.pie(
        frecuencia.values,
        labels=None,
        startangle=90
    )

    total = frecuencia.sum()

    # Agregar porcentajes con flechas afuera
        # Agregar porcentajes con flechas separadas
    for i, (wedge, valor) in enumerate(zip(wedges, frecuencia.values)):

        angulo = (wedge.theta2 + wedge.theta1) / 2

        x = np.cos(np.deg2rad(angulo))
        y = np.sin(np.deg2rad(angulo))

        porcentaje = (valor / total) * 100

        # Separación adicional para evitar choques
        distancia = 1.45

        # Ajuste vertical para porcentajes pequeños
        if porcentaje < 5:
            distancia = 1.7 + (i * 0.08)

        ax.annotate(
            f"{porcentaje:.1f}%",
            xy=(x * 0.85, y * 0.85),       # punto donde apunta la flecha
            xytext=(x * distancia, y * distancia),  # posición del texto
            fontsize=10,
            fontweight="bold",
            ha="center",
            va="center",
            arrowprops=dict(
                arrowstyle="->",
                lw=1,
                connectionstyle="arc3,rad=0.15"
            )
        )

    ax.set_title(
        titulo,
        fontsize=14,
        fontweight="bold"
    )

    # Leyenda con colores
    ax.legend(
        wedges,
        frecuencia.index,
        title="Categorías",
        loc="center left",
        bbox_to_anchor=(1.05, 0.5),
        fontsize=9
    )

    plt.tight_layout()

    st.pyplot(fig)

def grafico_barras(frecuencia, titulo):

    fig, ax = plt.subplots(figsize=(12, 6))

    barras = ax.barh(
        frecuencia.index,
        frecuencia.values
    )

    for barra in barras:

        ancho = barra.get_width()

        ax.text(
            ancho + 0.5,
            barra.get_y() + barra.get_height()/2,
            str(int(ancho)),
            va="center"
        )

    ax.set_title(titulo, fontsize=14, fontweight="bold")
    ax.set_xlabel("Frecuencia")

    plt.tight_layout()

    st.pyplot(fig)

def mostrar_variable(columna, titulo, descripcion):

    st.header(titulo)

    st.info(descripcion)

    frecuencia, tabla = tabla_frecuencias(df[columna])

    st.subheader("📋 Tabla de Frecuencias")

    st.dataframe(
        tabla,
        use_container_width=True,
        hide_index=True
    )

    imprimir_terminal(titulo, tabla)

    st.subheader("🥧 Gráfico de Torta")

    grafico_torta(
        frecuencia,
        titulo
    )

    st.markdown("---")

    categoria = frecuencia.idxmax()

    cantidad = frecuencia.max()

    porcentaje = round(
        (cantidad / frecuencia.sum()) * 100,
        2
    )

    st.success(
        f"""
### 📖 Interpretación Estadística

Se observa que la categoría predominante es:

**{categoria}**

con una frecuencia absoluta de
**{cantidad} respuestas**,
equivalente al **{porcentaje}%**
del total de estudiantes encuestados.

Este resultado indica que dicha categoría
representa la tendencia principal dentro
de la población analizada.
"""
    )

def mostrar_multiple(columna, titulo, descripcion):

    st.header(titulo)

    st.info(descripcion)

    frecuencia, tabla = tabla_frecuencias_multiple(
        df[columna]
    )

    st.subheader("📋 Tabla de Frecuencias")

    st.dataframe(
        tabla,
        use_container_width=True,
        hide_index=True
    )

    imprimir_terminal(
        titulo,
        tabla
    )

    st.subheader("📈 Gráfico de Barras")

    grafico_barras(
        frecuencia,
        titulo
    )

    st.markdown("---")

    categoria = frecuencia.idxmax()

    cantidad = frecuencia.max()

    porcentaje = round(
        (cantidad / frecuencia.sum()) * 100,
        2
    )

    st.success(
        f"""
### 📖 Interpretación Estadística

La opción más seleccionada fue:

**{categoria}**

registrando **{cantidad} menciones**,
lo que representa aproximadamente el
**{porcentaje}%** del total de respuestas
registradas para esta variable.

Este resultado evidencia que dicha característica
tiene una presencia significativa dentro de la
muestra estudiada y constituye la tendencia
predominante observada en los datos.
"""
    )
# ==========================================================
# INICIO
# ==========================================================

if menu == "🏠 Inicio":
 

    st.divider()

    st.markdown("""
    ### Descripción

    Este dashboard presenta el análisis estadístico
    descriptivo de una encuesta estudiantil.

    Incluye:

    - Base de datos completa.
    - Tablas de frecuencia.
    - Frecuencias absolutas (fi).
    - Frecuencias relativas (hi).
    - Frecuencias acumuladas (Fi).
    - Frecuencias relativas acumuladas (Hi).
    - Gráficos estadísticos.
    - Interpretación automática de resultados.
    """)

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Encuestados",
        len(df)
    )

    c2.metric(
        "Total Facultades",
        df["FACULTAD"].nunique()
    )

    c3.metric(
        "Total Carreras",
        df["CARRERA"].nunique()
    )

# ==========================================================
# DASHBOARD EJECUTIVO
# ==========================================================

elif menu == "📊 Dashboard Ejecutivo":

    st.title("📊 Dashboard Ejecutivo")

    st.info(
        "Resumen general de los principales indicadores "
        "obtenidos en la encuesta estudiantil."
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Encuestados",
        len(df)
    )

    c2.metric(
        "Total Facultades",
        df["FACULTAD"].nunique()
    )

    c3.metric(
        "Total Carreras",
        df["CARRERA"].nunique()
    )

    st.markdown("---")

    # ==========================================
    # DISPOSITIVO PRINCIPAL
    # ==========================================

    st.subheader("📱 Dispositivo Principal de Estudio")

    frecuencia = df[DISPOSITIVO].value_counts()

    grafico_barras(
        frecuencia,
        "Dispositivo Principal de Estudio"
    )

    st.success(
        f"La opción predominante es "
        f"'{frecuencia.idxmax()}', "
        f"con {frecuencia.max()} respuestas."
    )

    st.markdown("---")

    # ==========================================
    # CALIDAD DE CONEXIÓN
    # ==========================================

    st.subheader("📶 Calidad de Conexión")

    frecuencia2 = df[CALIDAD].value_counts()

    grafico_barras(
        frecuencia2,
        "Calidad Percibida de la Conexión"
    )

    st.success(
        f"La categoría predominante es "
        f"'{frecuencia2.idxmax()}', "
        f"con {frecuencia2.max()} respuestas."
    )

    st.markdown("---")

    st.caption(
        "Resumen ejecutivo generado automáticamente "
        "a partir de los datos de la encuesta."
    )

# ==========================================================
# BASE DE DATOS
# ==========================================================

elif menu == "📋 Base de Datos":

    st.title("📋 Base de Datos Completa")

    st.dataframe(
        df,
        use_container_width=True
    )

# ==========================================================
# VARIABLES TABULACIÓN
# ==========================================================

elif menu == "📱 Tipo de Dispositivo":

    mostrar_variable(
        DISPOSITIVO,
        "📱 Tipo de Dispositivo",
        "Distribución de dispositivos utilizados para estudiar."
    )

elif menu == "🌐 Responsable del Internet":

    mostrar_variable(
        INTERNET,
        "🌐 Responsable del Internet",
        "Persona o entidad que financia el acceso a internet."
    )

elif menu == "📡 Tipo de Conexión":

    mostrar_variable(
        CONEXION,
        "📡 Tipo de Conexión",
        "Tipo de conexión utilizada con mayor frecuencia."
    )

elif menu == "🏠 Espacio de Estudio":

    mostrar_variable(
        ESPACIO,
        "🏠 Espacio de Estudio",
        "Disponibilidad de un espacio adecuado para estudiar."
    )

elif menu == "🎓 Facultad":

    mostrar_variable(
        FACULTAD,
        "🎓 Facultad",
        "Distribución de estudiantes por facultad."
    )

elif menu == "📶 Calidad de Conexión":

    mostrar_variable(
        CALIDAD,
        "📶 Calidad de Conexión",
        "Percepción de la calidad de internet."
    )

elif menu == "⛔ Frecuencia de Interrupciones":

    mostrar_variable(
        INTERRUPCIONES,
        "⛔ Frecuencia de Interrupciones",
        "Frecuencia con que ocurren interrupciones durante actividades académicas."
    )

elif menu == "⚙️ Limitaciones Técnicas":

    mostrar_multiple(
        LIMITACIONES,
        "⚙️ Limitaciones Técnicas",
        "Problemas técnicos reportados por los estudiantes."
    )

elif menu == "💻 Plataformas Utilizadas":

    mostrar_multiple(
        PLATAFORMAS,
        "💻 Plataformas Utilizadas",
        "Plataformas virtuales utilizadas por los estudiantes."
    )

# ==========================================================
# CONCLUSIONES
# ==========================================================

elif menu == "📌 Conclusiones":

    st.title("📌 Conclusiones Generales")

    st.markdown("""
    ### Conclusiones

    - Se analizaron los datos obtenidos mediante una encuesta estudiantil.
    - Se calcularon frecuencias absolutas, relativas y acumuladas.
    - Se representaron gráficamente los resultados.
    - El dashboard permite actualizar automáticamente los análisis
      cuando cambian los datos del archivo Excel.

    ### Importancia

    Este sistema facilita la interpretación de la información
    estadística y apoya la toma de decisiones basadas en datos.
    """)

    st.success("Proyecto finalizado correctamente.")
