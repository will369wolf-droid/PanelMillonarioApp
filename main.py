import flet as ft
import datetime
import random

# --- TUS DATOS ---
COLOR_ACENTO = "#00d26a"
COLOR_FONDO = "#121212"

FRASES_MILLONARIAS = [
    "El dolor del sacrificio es temporal, la gloria es eterna.",
    "La disciplina es hacer lo que debes, aunque no quieras.",
    "Tu competencia está entrenando mientras tú duermes.",
    "Si fuera fácil, todo el mundo lo haría.",
    "No busques motivación, busca disciplina.",
    "Tus excusas no le importan a tu cuenta bancaria.",
    "Trabaja en silencio y deja que tu éxito haga el ruido.",
    "La pobreza mental se cura con acción masiva.",
    "Si no arriesgas, te conformas con lo ordinario.",
    "El dinero no duerme.",
    "Hazlo con miedo, pero hazlo.",
    "Tu futuro se crea por lo que haces hoy.",
    "Sé tan bueno que no puedan ignorarte.",
    "Invierte en ti, es la única inversión segura.",
    "Obsesión es la palabra que los vagos usan para la dedicación.",
    "No necesitas suerte, necesitas moverte.",
    "Sé el CEO de tu vida.",
    "No pares hasta que tu firma sea un autógrafo.",
    "El tiempo es oro, no lo regales.",
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

def main(page: ft.Page):
    # Configuración base (Igual que el Hola Leo)
    page.title = "Panel Imperio"
    page.bgcolor = COLOR_FONDO
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- FUNCIÓN PARA CARGAR EL IMPERIO ---
    def cargar_imperio(e):
        # Limpiamos la pantalla de bienvenida
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.padding = 10
        page.update()

        # --- Lógica de carga (Ahora corre SEGURO porque la App ya abrió) ---
        hoy_str = datetime.date.today().strftime("%Y-%m-%d")
        SOLO_NOMBRES = list(HABITOS_CONFIG.keys())

        def guardar(nombre, valor):
            try:
                page.client_storage.set(f"{hoy_str}_{nombre}", valor)
            except: pass # Si falla, no rompemos la app

        def leer(nombre):
            try:
                return page.client_storage.get(f"{hoy_str}_{nombre}") or False
            except: return False

        # Componentes UI
        progreso_texto = ft.Text("0%", size=30, weight="bold", color=COLOR_ACENTO)
        progreso_ring = ft.ProgressRing(width=120, height=120, stroke_width=8, color=COLOR_ACENTO)

        def actualizar_progreso():
            completados = sum(1 for n in SOLO_NOMBRES if leer(n))
            total = len(SOLO_NOMBRES)
            ratio = completados / total if total > 0 else 0
            progreso_ring.value = ratio
            progreso_texto.value = f"{int(ratio * 100)}%"
            page.update()

        lista = ft.Column(spacing=10, scroll="auto", expand=True) # Scroll activado

        for nombre in SOLO_NOMBRES:
            datos = HABITOS_CONFIG[nombre]
            check = ft.Checkbox(
                value=leer(nombre),
                active_color=COLOR_ACENTO,
                on_change=lambda e, n=nombre: (guardar(n, e.control.value), actualizar_progreso())
            )
            lista.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(datos[0], color=datos[1]),
                        ft.Text(nombre, size=14, expand=True),
                        check
                    ]),
                    bgcolor="#1E1E1E", padding=10, border_radius=10
                )
            )

        # Montamos la pantalla final
        page.add(
            ft.Text("IMPULSO DIARIO", size=20, weight="bold", text_align="center"),
            ft.Container(
                content=ft.Stack([progreso_ring, ft.Container(content=progreso_texto, alignment=ft.alignment.center, width=120, height=120)]),
                alignment=ft.alignment.center, padding=10
            ),
            ft.Text(random.choice(FRASES_MILLONARIAS), italic=True, color="white70", text_align="center", size=12),
            ft.Divider(color="white10"),
            lista
        )
        actualizar_progreso()
        page.update()

    # --- PANTALLA DE INICIO (LA QUE VEMOS PRIMERO) ---
    # Esto es lo que garantiza que no haya pantalla negra
    btn_inicio = ft.ElevatedButton(
        "ENTRAR A MI IMPERIO",
        color="white",
        bgcolor=COLOR_ACENTO,
        height=50,
        on_click=cargar_imperio # Al hacer clic, carga lo pesado
    )

    page.add(
        ft.Icon(name="verified_user", color=COLOR_ACENTO, size=60),
        ft.Container(height=20),
        ft.Text("Bienvenido, Leo", size=24, weight="bold"),
        ft.Text("Tu sistema está listo.", color="white70"),
        ft.Container(height=40),
        btn_inicio
    )

ft.app(target=main)
