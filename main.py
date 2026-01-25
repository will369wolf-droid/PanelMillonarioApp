import flet as ft
import datetime
import random

# --- CONFIGURACIÓN ---
COLOR_ACENTO = "#00d26a"
COLOR_FONDO_IMPERIO = "#121212"

# --- TUS 30 FRASES ORIGINALES (Regresaron) ---
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
    "Despertar 5:00 am": ft.Colors.ORANGE,
    "Tomar agua": ft.Colors.BLUE,
    "Objetivo principal": ft.Colors.RED_ACCENT,
    "Investigar productos": ft.Colors.PURPLE_ACCENT,
    "Aprender algo nuevo": ft.Colors.YELLOW_ACCENT,
    "Aplicar lo aprendido": ft.Colors.AMBER,
    "Construir negocio": ft.Colors.CYAN,
    "Lanzar anuncios": ft.Colors.PINK_ACCENT,
    "Ejercicio fisico": ft.Colors.GREEN_ACCENT,
    "Jornada de trabajo": ft.Colors.BLUE_GREY,
    "Revisar numeros": ft.Colors.TEAL_ACCENT,
    "Reflexion diaria": ft.Colors.YELLOW,
    "Dormir temprano": ft.Colors.INDIGO_ACCENT,
}

def main(page: ft.Page):
    # --- PANTALLA SEGURA DE ARRANQUE ---
    page.title = "Panel Imperio"
    page.bgcolor = "white"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # --- CARGA DEL IMPERIO ---
    def iniciar_sistema(e):
        page.clean()
        page.bgcolor = COLOR_FONDO_IMPERIO
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.padding = 15
        
        try:
            hoy_str = datetime.date.today().strftime("%Y-%m-%d")
            total_habitos = len(HABITOS_CONFIG)

            # --- Lógica de Memoria ---
            def guardar(nombre, valor):
                try: page.client_storage.set(f"{hoy_str}_{nombre}", valor)
                except: pass

            def leer(nombre):
                try: return page.client_storage.get(f"{hoy_str}_{nombre}") or False
                except: return False

            # --- Componentes Dinámicos ---
            progreso_texto = ft.Text("0%", size=30, weight="bold", color=COLOR_ACENTO)
            progreso_ring = ft.ProgressRing(width=120, height=120, stroke_width=10, color=COLOR_ACENTO, value=0)

            def actualizar_ui():
                completados = sum(1 for k in HABITOS_CONFIG if leer(k))
                ratio = completados / total_habitos if total_habitos > 0 else 0
                progreso_ring.value = ratio
                progreso_texto.value = f"{int(ratio * 100)}%"
                page.update()

            # --- Construcción de la Interfaz ---
            # 1. Cabecera con Frase y Progreso
            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Text("MI IMPERIO", size=22, weight="bold", color="white"),
                        ft.Text(random.choice(FRASES_MILLONARIAS), color="white70", italic=True, size=12, text_align="center"),
                        ft.Container(height=10),
                        ft.Stack([
                            progreso_ring,
                            ft.Container(content=progreso_texto, alignment=ft.alignment.center, width=120, height=120)
                        ], alignment=ft.alignment.center),
                    ], horizontal_alignment="center"),
                    alignment=ft.alignment.center,
                    padding=10
                ),
                ft.Divider(color="white12", height=20)
            )

            # 2. Lista de Hábitos
            # Usamos Scroll para que quepan todos los hábitos en pantallas pequeñas
            lista_scroll = ft.Column(scroll="auto", expand=True) # expand=True es clave para que el scroll funcione

            for nombre, color_habito in HABITOS_CONFIG.items():
                estado = leer(nombre)
                
                # Checkbox con lógica de actualización
                check = ft.Checkbox(
                    value=estado,
                    active_color=COLOR_ACENTO,
                    fill_color=color_habito,
                    on_change=lambda e, n=nombre: (guardar(n, e.control.value), actualizar_ui())
                )
                
                lista_scroll.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Container(width=12, height=12, bgcolor=color_habito, border_radius=3),
                            ft.Text(nombre, size=15, color="white", expand=True),
                            check
                        ]),
                        bgcolor="#1E1E1E",
                        padding=12,
                        border_radius=8,
                        margin=ft.margin.only(bottom=8)
                    )
                )

            # Agregamos la lista con scroll
            page.add(lista_scroll)
            
            # Primera actualización para calcular el % inicial
            actualizar_ui()
            
        except Exception as error:
            page.add(ft.Text(f"Error: {error}", color="red"))
            page.update()

    # --- BOTÓN DE INICIO (El que nos salvó la vida) ---
    boton = ft.ElevatedButton(
        "ENTRAR A MI RUTINA", 
        color="white", 
        bgcolor="black", 
        on_click=iniciar_sistema,
        height=50,
        width=200
    )

    page.add(
        ft.Column([
            ft.Text("¡HOLA LEO!", size=35, color="black", weight="bold"),
            ft.Text("Tu imperio te espera.", size=16, color="grey"),
            ft.Container(height=30),
            boton
        ], alignment="center", horizontal_alignment="center", expand=True)
    )

ft.app(target=main)
