import flet as ft
import random
import datetime

# --- CONFIGURACIÓN ---
COLOR_ACENTO = "#00d26a"  
COLOR_FONDO = "#121212" # Volvemos al modo oscuro elegante

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
    # Configuración visual
    page.title = "Panel Imperio"
    page.bgcolor = COLOR_FONDO
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = "auto"

    # --- GUARDADO SEGURO (Sin archivos JSON que bloqueen) ---
    hoy_str = datetime.date.today().strftime("%Y-%m-%d")

    def guardar_habito(nombre, valor):
        # Guardamos en la memoria privada de la App
        clave = f"{hoy_str}_{nombre}"
        page.client_storage.set(clave, valor)
        
        # Feedback visual para que sepas que funciona
        if valor:
            page.snack_bar = ft.SnackBar(ft.Text(f"¡{nombre} completado!"), bgcolor="green")
            page.snack_bar.open = True
            page.update()

    def leer_habito(nombre):
        clave = f"{hoy_str}_{nombre}"
        return page.client_storage.get(clave) or False

    # --- INTERFAZ ---
    progreso_texto = ft.Text("0%", size=35, weight="bold", color=COLOR_ACENTO)
    progreso_ring = ft.ProgressRing(width=140, height=140, stroke_width=10, color=COLOR_ACENTO)
    
    def actualizar_progreso():
        total = len(SOLO_NOMBRES)
        completados = 0
        for n in SOLO_NOMBRES:
            if leer_habito(n):
                completados += 1
        
        ratio = completados / total if total > 0 else 0
        progreso_ring.value = ratio
        progreso_texto.value = f"{int(ratio * 100)}%"
        page.update()

    lista_habitos = ft.Column(spacing=10)
    for nombre in SOLO_NOMBRES:
        datos = HABITOS_CONFIG[nombre]
        valor_actual = leer_habito(nombre)
        
        lista_habitos.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(name=datos[0], color=datos[1], size=22),
                    ft.Text(nombre, size=14, color="white", expand=True),
                    ft.Checkbox(value=valor_actual, 
                                active_color=COLOR_ACENTO,
                                on_change=lambda e, n=nombre: (guardar_habito(n, e.control.value), actualizar_progreso()))
                ]),
                bgcolor="#1E1E1E",
                padding=12,
                border_radius=10
            )
        )

    # --- ENSAMBLAJE ---
    page.add(
        ft.Column([
            ft.Container(height=20),
            ft.Text("IMPULSO DIARIO", size=20, weight="bold", color="white", letter_spacing=2),
            ft.Container(
                content=ft.Stack([
                    progreso_ring, 
                    ft.Container(content=progreso_texto, alignment=ft.alignment.center, width=140, height=140)
                ]),
                alignment=ft.alignment.center,
                padding=20
            ),
            ft.Container(
                content=ft.Text(random.choice(FRASES_MILLONARIAS), size=14, italic=True, color="white70", text_align="center"),
                padding=10
            ),
            ft.Divider(height=20, color="white12"),
            lista_habitos,
            ft.Container(height=30)
        ], horizontal_alignment="center")
    )

    actualizar_progreso()

ft.app(target=main)
