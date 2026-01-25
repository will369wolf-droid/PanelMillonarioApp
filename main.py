zimport flet as ft
import datetime
import json
import os
import random

# --- CONFIGURACIÓN ---
DB_FILE = "datos_rutina_v2.json"
COLOR_ACENTO = "#00d26a"  
COLOR_FONDO = "#121212"

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
    page.title = "Panel Imperio V42"
    page.bgcolor = COLOR_FONDO
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    def cargar_datos():
        try:
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r") as f: return json.load(f)
        except: pass
        return {}

    def guardar_datos(data):
        try:
            with open(DB_FILE, "w") as f: json.dump(data, f)
        except: pass

    db = cargar_datos()
    hoy_str = datetime.date.today().strftime("%Y-%m-%d")
    if hoy_str not in db: db[hoy_str] = {n: False for n in SOLO_NOMBRES}

    progreso_texto = ft.Text("0%", size=35, weight="bold", color=COLOR_ACENTO)
    progreso_ring = ft.ProgressRing(width=140, height=140, stroke_width=10, color=COLOR_ACENTO)
    
    def actualizar_progreso():
        total = len(SOLO_NOMBRES)
        completados = sum(1 for h in SOLO_NOMBRES if db.get(hoy_str, {}).get(h, False))
        ratio = completados / total if total > 0 else 0
        progreso_ring.value = ratio
        progreso_texto.value = f"{int(ratio * 100)}%"
        page.update()

    lista_habitos = ft.Column(spacing=10, scroll="auto")
    for nombre in SOLO_NOMBRES:
        datos = HABITOS_CONFIG[nombre]
        lista_habitos.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(name=datos[0], color=datos[1], size=22),
                    ft.Text(nombre, size=14, color="white", expand=True),
                    ft.Checkbox(value=db[hoy_str].get(nombre, False), 
                                on_change=lambda e, n=nombre: (db[hoy_str].update({n: e.control.value}), guardar_datos(db), actualizar_progreso()),
                                fill_color=datos[1])
                ]),
                bgcolor="#1E1E1E", padding=12, border_radius=10
            )
        )

    page.add(
        ft.Column([
            ft.Container(height=10),
            ft.Text("IMPULSO DIARIO", size=18, weight="bold", letter_spacing=1.5),
            ft.Container(content=ft.Stack([progreso_ring, ft.Container(content=progreso_texto, alignment=ft.alignment.center, width=140, height=140)]), alignment=ft.alignment.center, padding=15),
            ft.Text(random.choice(FRASES_MILLONARIAS), size=12, italic=True, color="white70", text_align="center"),
            ft.Divider(height=25, color="white12"),
            lista_habitos
        ], horizontal_alignment="center", expand=True)
    )
    actualizar_progreso()

ft.app(target=main)

