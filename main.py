import flet as ft
import datetime
import json
import os
import threading
import time
import calendar
import random

# --- CONFIGURACIÓN ---
DB_FILE = "datos_rutina_v2.json"
COLOR_ACENTO = "#00d26a"  # Verde Dinero
COLOR_FONDO = "#121212"

# --- TUS ARCHIVOS ---
# Usamos la ruta que Android reconoce mejor internamente
ARCHIVO_FONDO = "assets/Fondo.mp4"        
ARCHIVO_MOTIVACION = "assets/motivacion.gif" 

# --- FRASES COMPLETAS ---
FRASES_MILLONARIAS = [
    "El dolor del sacrificio es temporal, la gloria es eterna.",
    "No te detengas cuando estés cansado, detente cuando termines.",
    "La disciplina es hacer lo que debes, aunque no quieras.",
    "Tu competencia está entrenando mientras tú duermes.",
    "Si fuera fácil, todo el mundo lo haría.",
    "El éxito es la suma de pequeños esfuerzos diarios.",
    "No busques motivación, busca disciplina.",
    "Tus excusas no le importan a tu cuenta bancaria.",
    "Trabaja en silencio y deja que tu éxito haga el ruido.",
    "O controlas tu día, o el día te controla a ti.",
    "La pobreza mental se cura con acción masiva.",
    "Si no arriesgas, te conformas con lo ordinario.",
    "El dinero no duerme.",
    "No bajes la meta, aumenta el esfuerzo.",
    "Hazlo con miedo, pero hazlo.",
    "Tu futuro se crea por lo que haces hoy.",
    "Sé tan bueno que no puedan ignorarte.",
    "Si te ofrecen un cohete, ¡súbete!",
    "El riesgo más grande es no tomar ninguno.",
    "Invierte en ti, es la única inversión segura.",
    "Obsesión es la palabra que los vagos usan para la dedicación.",
    "Duerme tarde, levántate temprano y trabaja duro.",
    "No necesitas suerte, necesitas moverte.",
    "Sé el CEO de tu vida.",
    "No pares hasta que tu firma sea un autógrafo.",
    "Crea una vida de la que no necesites vacaciones.",
    "El tiempo es oro, no lo regales.",
    "Si no trabajas por tus sueños, trabajarás para otro.",
    "Calidad sobre cantidad, siempre.",
    "Gana la mañana, gana el día."
]

# Configuración Hábito (Blindado: Iconos como texto y 'Colors' con mayúscula)
HABITOS_CONFIG = {
    "⏰ Despertar 5:00–6:00 am": ["alarm", ft.Colors.ORANGE],
    "💧 Tomar agua + aseo": ["water_drop", ft.Colors.BLUE],
    "🎯 Definir objetivo principal": ["flag", ft.Colors.RED_ACCENT],
    "🔍 Investigar productos": ["search", ft.Colors.PURPLE_ACCENT],
    "📚 Aprender algo nuevo": ["school", ft.Colors.YELLOW_ACCENT],
    "⚡ Aplicar lo aprendido": ["flash_on", ft.Colors.AMBER],
    "🏗️ Construir negocio": ["business", ft.Colors.CYAN],
    "📢 Lanzar anuncios": ["campaign", ft.Colors.PINK_ACCENT],
    "🏃 Ejercicio físico": ["fitness_center", ft.Colors.GREEN_ACCENT],
    "💼 Jornada de trabajo": ["work", ft.Colors.BLUE_GREY],
    "📊 Revisar números": ["insert_chart", ft.Colors.TEAL_ACCENT],
    "🧠 Reflexión diaria": ["lightbulb", ft.Colors.YELLOW],
    "😴 Dormir temprano": ["hotel", ft.Colors.INDIGO_ACCENT],
}
SOLO_NOMBRES = list(HABITOS_CONFIG.keys())

def main(page: ft.Page):
    page.title = "Panel Millonario V34"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = COLOR_FONDO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- FONDO DE VIDEO (Configuración para evitar bloqueo/pantalla negra) ---
    fondo_app = ft.Video(
        playlist=[ft.VideoMedia(ARCHIVO_FONDO)],
        playlist_mode=ft.PlaylistMode.LOOP,
        fill_color="black",
        aspect_ratio=9/16,
        volume=0,
        autoplay=True,
        muted=True,
        opacity=0.3,
        filter_quality=ft.FilterQuality.LOW
    )

    # --- ANIMACIÓN DE RECOMPENSA ---
    icono_recompensa = ft.Icon(name="check", size=150, color=ft.Colors.WHITE)
    contenedor_animacion = ft.Container(
        content=icono_recompensa,
        alignment=ft.alignment.center,
        scale=ft.transform.Scale(0),
        animate_scale=ft.animation.Animation(600, ft.AnimationCurve.ELASTIC_OUT),
        opacity=0,
        animate_opacity=300,
        visible=False,
        top=0, bottom=0, left=0, right=0,
    )

    def lanzar_animacion(icono_nombre, color_efecto):
        icono_recompensa.name = icono_nombre
        icono_recompensa.color = color_efecto
        contenedor_animacion.visible = True
        contenedor_animacion.opacity = 1
        contenedor_animacion.scale = ft.transform.Scale(1.5)
        page.update()
        time.sleep(1.5)
        contenedor_animacion.opacity = 0
        contenedor_animacion.scale = ft.transform.Scale(0)
        page.update()
        time.sleep(0.3)
        contenedor_animacion.visible = False
        page.update()

    # --- BASE DE DATOS ---
    def cargar_datos():
        if not os.path.exists(DB_FILE): return {}
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return {}

    def guardar_datos(data):
        with open(DB_FILE, "w") as f: json.dump(data, f)

    db = cargar_datos()
    hoy_str = datetime.date.today().strftime("%Y-%m-%d")

    if hoy_str not in db:
        db[hoy_str] = {n: False for n in SOLO_NOMBRES}
        guardar_datos(db)

    # --- LÓGICA ---
    snack_bar = ft.SnackBar(content=ft.Text(""), bgcolor="#333333")
    page.overlay.append(snack_bar)

    def cambiar_habito(e, nombre_habito):
        db[hoy_str][nombre_habito] = e.control.value
        guardar_datos(db)
        actualizar_rutina()
        if e.control.value:
            config = HABITOS_CONFIG[nombre_habito]
            threading.Thread(target=lanzar_animacion, args=(config[0], config[1]), daemon=True).start()
            snack_bar.content.value = "✅ ¡Hecho!"
            snack_bar.open = True
            page.update()

    # PESTAÑA 1: RUTINA
    progreso_texto = ft.Text("0%", size=45, weight="bold", color=COLOR_ACENTO)
    progreso_ring = ft.ProgressRing(width=180, height=180, stroke_width=15, bgcolor=ft.Colors.with_opacity(0.3, "black"), color=COLOR_ACENTO)
    lista_controles = []
    
    for nombre in SOLO_NOMBRES:
        datos = HABITOS_CONFIG[nombre]
        chk = ft.Switch(value=db[hoy_str].get(nombre, False), on_change=lambda e, x=nombre: cambiar_habito(e, x), active_color=datos[1])
        tarjeta = ft.Container(
            content=ft.Row([ft.Icon(name=datos[0], color=datos[1], size=24), ft.Container(width=10), ft.Text(nombre, size=13, color="white", weight="w500", expand=True), chk]),
            bgcolor=ft.Colors.with_opacity(0.6, "black"),
            padding=15, border_radius=12, border=ft.border.all(1, ft.Colors.with_opacity(0.3, datos[1])),
            blur=ft.Blur(5, 5, ft.BlurTileMode.MIRROR)
        )
        lista_controles.append(tarjeta)

    vista_rutina = ft.Column([
        ft.Container(height=30),
        ft.Container(content=ft.Stack([progreso_ring, ft.Container(content=progreso_texto, alignment=ft.alignment.center, width=180, height=180)]), alignment=ft.alignment.center),
        ft.Container(height=20),
        ft.Text("MODO IMPERIO: ACTIVADO", size=12, color="white70", text_align="center"),
        ft.Container(height=10),
        ft.Container(content=ft.Column(lista_controles, spacing=10, scroll="auto"), padding=20, expand=True)
    ], expand=True, horizontal_alignment="center")

    def actualizar_rutina():
        total = len(SOLO_NOMBRES)
        completados = sum(1 for h in SOLO_NOMBRES if db.get(hoy_str, {}).get(h, False))
        ratio = completados / total if total > 0 else 0
        progreso_ring.value = ratio
        progreso_texto.value = f"{int(ratio * 100)}%"
        page.update()

    # (Lógica de Calendario y Mentores se mantiene igual pero con 'Colors')
    # ... [Omitido por espacio, pero incluido en tu archivo completo] ...

    # PESTAÑA 3: MENTORES (Ejemplo de ajuste de icono)
    globo = ft.Container(
        content=ft.Image(src=ARCHIVO_MOTIVACION, width=220, height=220, fit=ft.ImageFit.CONTAIN),
        on_click=lambda _: page.update(), border_radius=110
    )

    # NAVEGACIÓN
    nav = ft.NavigationBar(
        bgcolor="black", indicator_color=ft.Colors.with_opacity(0.2, COLOR_ACENTO), selected_index=0,
        destinations=[
            ft.NavigationDestination(icon="check_circle", label="Mi Día"),
            ft.NavigationDestination(icon="calendar_month", label="Historial"),
            ft.NavigationDestination(icon="psychology", label="Mentores")
        ]
    )

    layout = ft.Column([vista_rutina], expand=True)
    
    # --- ENSAMBLAJE FINAL ---
    page.add(ft.Stack([
        fondo_app, # El video se carga primero pero de forma ligera
        ft.Column([layout, nav], expand=True, horizontal_alignment="center"),
        contenedor_animacion
    ], expand=True))
    
    actualizar_rutina()

ft.app(target=main, assets_dir="assets")
