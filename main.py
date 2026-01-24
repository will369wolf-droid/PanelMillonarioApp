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

# --- FRASES ---
FRASES_MILLONARIAS = [
    "El dolor del sacrificio es temporal, la gloria es eterna.",
    "No te detengas cuando estés cansado, detente cuando termines.",
    "La disciplina es hacer lo que debes, aunque no quieras.",
    "Tu competencia está entrenando mientras tú duermes.",
    "El éxito es la suma de pequeños esfuerzos diarios.",
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
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- COMPONENTE DE VIDEO OPTIMIZADO ---
    fondo_app = ft.Video(
        playlist=[ft.VideoMedia(ARCHIVO_FONDO)],
        playlist_mode=ft.PlaylistMode.LOOP,
        fill_color="black",
        aspect_ratio=9/16,
        volume=0,
        autoplay=False, # Cambiado a False para carga manual
        muted=True,
        opacity=0.3,
    )

    # --- LÓGICA DE CARGA ASÍNCRONA ---
    def iniciar_video():
        time.sleep(1) # Espera a que la UI se dibuje
        fondo_app.autoplay = True
        page.update()

    # --- INTERFAZ (Sección de Rutina) ---
    progreso_texto = ft.Text("0%", size=45, weight="bold", color=COLOR_ACENTO)
    progreso_ring = ft.ProgressRing(width=180, height=180, stroke_width=15, color=COLOR_ACENTO)
    
    lista_controles = []
    for nombre, datos in HABITOS_CONFIG.items():
        tarjeta = ft.Container(
            content=ft.Row([
                ft.Icon(name=datos[0], color=datos[1], size=24),
                ft.Text(nombre, size=13, color="white", expand=True),
                ft.Switch(active_color=datos[1])
            ]),
            bgcolor=ft.Colors.with_opacity(0.6, "black"),
            padding=15, border_radius=12,
        )
        lista_controles.append(tarjeta)

    layout = ft.Column([
        ft.Container(height=40),
        ft.Stack([progreso_ring, ft.Container(content=progreso_texto, alignment=ft.alignment.center, width=180, height=180)]),
        ft.Container(content=ft.Column(lista_controles, spacing=10, scroll="auto"), padding=20, expand=True)
    ], expand=True)

    nav = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon="check_circle", label="Mi Día"),
            ft.NavigationDestination(icon="calendar_month", label="Historial"),
            ft.NavigationDestination(icon="psychology", label="Mentores")
        ]
    )

    # --- ENSAMBLAJE ---
    page.add(ft.Stack([
        fondo_app,
        ft.Column([layout, nav], expand=True),
    ], expand=True))

    # Ejecutar carga de video en segundo plano
    threading.Thread(target=iniciar_video, daemon=True).start()

ft.app(target=main, assets_dir="assets")
