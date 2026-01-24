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
COLOR_ACENTO = "#00d26a"  
COLOR_FONDO = "#121212"
ARCHIVO_FONDO = "assets/Fondo.mp4"        
ARCHIVO_MOTIVACION = "assets/motivacion.gif" 

# --- TUS 30 FRASES (Sin modificaciones) ---
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
    page.title = "Panel Millonario V34"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = COLOR_FONDO

    # --- VIDEO (Configurado para no bloquear la App) ---
    fondo_app = ft.Video(
        playlist=[ft.VideoMedia(ARCHIVO_FONDO)],
        playlist_mode=ft.PlaylistMode.LOOP,
        fill_color="black",
        aspect_ratio=9/16,
        volume=0,
        autoplay=False, # No arranca solo para no congelar la pantalla
        muted=True,
        opacity=0.3,
    )

    # --- LÓGICA DE ARRANQUE SEGURO ---
    def activar_video():
        time.sleep(2) # Espera 2 segundos a que la App se cargue bien
        fondo_app.autoplay = True
        page.update()

    # --- INTERFAZ ---
    progreso_texto = ft.Text("0%", size=45, weight="bold", color=COLOR_ACENTO)
    progreso_ring = ft.ProgressRing(width=180, height=180, stroke_width=15, color=COLOR_ACENTO)
    
    lista_controles = ft.Column(spacing=10, scroll="auto")
    for nombre, datos in HABITOS_CONFIG.items():
        lista_controles.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(name=datos[0], color=datos[1], size=24),
                    ft.Text(nombre, size=13, color="white", expand=True),
                    ft.Switch(active_color=datos[1])
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

    # --- ENSAMBLAJE ---
    page.add(
        ft.Stack([
            fondo_app, 
            ft.Column([layout, nav], expand=True),
        ], expand=True)
    )

    # Lanzar el video en un hilo separado
    threading.Thread(target=activar_video, daemon=True).start()

ft.app(target=main, assets_dir="assets")
