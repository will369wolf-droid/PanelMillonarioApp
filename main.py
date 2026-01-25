import flet as ft
import datetime
import random

# --- CONFIGURACIÓN ---
# Definimos todo aquí pero NO lo usamos hasta que des clic
COLOR_ACENTO = "#00d26a"
COLOR_FONDO_IMPERIO = "#121212"

FRASES_MILLONARIAS = [
    "Gana la mañana, gana el día.",
    "La disciplina es libertad.",
    "Hazlo con miedo, pero hazlo.",
    "Tu futuro se crea hoy.",
    "El dinero no duerme."
]

HABITOS_CONFIG = {
    "Despertar 5:00 am": ft.Colors.ORANGE,
    "Tomar agua": ft.Colors.BLUE,
    "Objetivo principal": ft.Colors.RED_ACCENT,
    "Investigar productos": ft.Colors.PURPLE_ACCENT,
    "Aprender algo nuevo": ft.Colors.YELLOW_ACCENT,
    "Ejercicio fisico": ft.Colors.GREEN_ACCENT,
    "Dormir temprano": ft.Colors.INDIGO_ACCENT,
}

def main(page: ft.Page):
    # --- PASO 1: CONFIGURACIÓN EXACTA DEL "HOLA LEO" (La que funcionó) ---
    page.title = "Panel Imperio"
    page.bgcolor = "white" # Fondo blanco seguro para arrancar
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # --- PASO 2: LA FUNCIÓN QUE CARGA EL IMPERIO DESPUÉS ---
    def iniciar_sistema(e):
        # 1. Cambiamos al modo oscuro "Imperio"
        page.clean() # Borramos el "Hola Leo"
        page.bgcolor = COLOR_FONDO_IMPERIO
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.padding = 15
        
        # 2. Lógica de carga (protegida para que no falle)
        try:
            hoy_str = datetime.date.today().strftime("%Y-%m-%d")
            
            def guardar(nombre, valor):
                try: page.client_storage.set(f"{hoy_str}_{nombre}", valor)
                except: pass

            def leer(nombre):
                try: return page.client_storage.get(f"{hoy_str}_{nombre}") or False
                except: return False

            # Título y Frase
            page.add(
                ft.Text("MI IMPERIO", size=25, weight="bold", color="white", text_align="center"),
                ft.Text(random.choice(FRASES_MILLONARIAS), color="white70", italic=True, text_align="center"),
                ft.Divider(color="white24")
            )

            # Lista de Hábitos (Simplificada para evitar bloqueo de iconos)
            # Usamos cuadrados de color en vez de iconos complejos por seguridad
            for nombre, color_habito in HABITOS_CONFIG.items():
                estado_actual = leer(nombre)
                
                check = ft.Checkbox(
                    value=estado_actual,
                    active_color=COLOR_ACENTO,
                    fill_color=color_habito,
                    on_change=lambda e, n=nombre: guardar(n, e.control.value)
                )
                
                page.add(
                    ft.Container(
                        content=ft.Row([
                            # Cuadradito de color simple en vez de Icono pesado
                            ft.Container(width=10, height=10, bgcolor=color_habito, border_radius=2),
                            ft.Text(nombre, size=16, color="white", expand=True),
                            check
                        ]),
                        bgcolor="#1E1E1E",
                        padding=15,
                        border_radius=10,
                        margin=ft.margin.only(bottom=5)
                    )
                )
            
            page.update()
            
        except Exception as error:
            # Si algo falla, mostramos el error en pantalla en vez de pantalla negra
            page.add(ft.Text(f"Error cargando: {error}", color="red"))
            page.update()

    # --- PASO 3: PANTALLA DE INICIO (Idéntica a la prueba exitosa) ---
    # Sin iconos, sin cargas raras. Solo texto y botón.
    titulo = ft.Text("¡HOLA LEO!", size=40, color="black", weight="bold")
    subtitulo = ft.Text("Sistema listo para iniciar.", size=16, color="grey")
    boton = ft.ElevatedButton(
        "COMENZAR", 
        color="white", 
        bgcolor="black", 
        on_click=iniciar_sistema, # Esto detona la carga
        height=50
    )

    page.add(titulo, subtitulo, ft.Container(height=20), boton)

ft.app(target=main)
