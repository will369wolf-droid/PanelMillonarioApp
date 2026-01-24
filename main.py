import flet as ft
import datetime
import json
import os
import calendar
import random

# --- CONFIGURACIÓN ---
DB_FILE = "datos_rutina_v2.json"
COLOR_ACENTO = "#00d26a"  
COLOR_FONDO = "#121212"
# Cambiamos el video por la imagen motivacional que ya tienes
ARCHIVO_FONDO_IMG = "assets/motivacion.gif" 

# --- TUS 30 FRASES ORIGINALES ---
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
    page.title = "Panel Imperio V38"
    page.bgcolor = COLOR_FONDO
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    # Fondo de Imagen (Infinitamente más estable que el video en Android)
    img_fondo = ft.Image(
        src=ARCHIVO_FONDO_IMG,
        fit=ft.ImageFit.COVER,
        opacity=0.2,
        expand=True
    )

    # --- LÓGICA DE DATOS ---
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

    # --- INTERFAZ ---
    progreso_texto = ft.Text("0%", size=45, weight="bold", color=COLOR_ACENTO)
    progreso_ring = ft.ProgressRing(width=180, height=180, stroke_width=15, color=COLOR_ACENTO)
    
    def actualizar_progreso():
        total = len(SOLO_NOMBRES)
        completados = sum(1 for h in SOLO_NOMBRES if db.get(hoy_str, {}).get(h, False))
        ratio = completados / total if total > 0 else 0
        progreso_ring.value = ratio
        progreso_texto.value = f"{int(ratio * 100)}%"
        page.update()

    lista_controles = ft.Column(spacing=10, scroll="auto")
    for nombre in SOLO_NOMBRES:
        datos = HABITOS_CONFIG[nombre]
        lista_controles.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(name=datos[0], color=datos[1], size=24),
                    ft.Text(nombre, size=13, color="white", expand=True),
                    ft.Switch(value=db[hoy_str].get(nombre, False), 
                              active_color=datos[1], 
                              on_change=lambda e, n=nombre: (db[hoy_str].update({n: e.control.value}), guardar_datos(db), actualizar_progreso()))
                ]),
                bgcolor=ft.Colors.with_opacity(0.6, "black"),
                padding=15, border_radius=12,
            )
        )

    layout = ft.Column([
        ft.Container(height=40),
        ft.Stack([progreso_ring, ft.Container(content=progreso_texto, alignment=ft.alignment.center, width=180, height=180)]),
        ft.Container(content=lista_controles, padding=20, expand=True)
    ], expand=True)

    nav = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon="check_circle", label="Mi Día"),
            ft.NavigationDestination(icon="calendar_month", label="Historial"),
            ft.NavigationDestination(icon="psychology", label="Mentores")
        ]
    )

    page.add(ft.Stack([
        img_fondo,
        ft.Column([layout, nav], expand=True)
    ], expand=True))

    actualizar_progreso()

ft.app(target=main, assets_dir="assets")
