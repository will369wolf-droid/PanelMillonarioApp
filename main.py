import flet as ft
import datetime
import random
import json
import os

# --- CONFIGURACIÓN VISUAL ---
COLOR_ACENTO = "#00d26a"
COLOR_FONDO_IMPERIO = "#121212"

# --- TUS FRASES ---
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

# --- TUS HÁBITOS (Colores corregidos) ---
HABITOS_CONFIG = {
    "Despertar 5:00 am": "orange",
    "Tomar agua": "blue",
    "Objetivo principal": "red",
    "Investigar productos": "purple",
    "Aprender algo nuevo": "yellow",
    "Aplicar lo aprendido": "amber",
    "Construir negocio": "cyan",
    "Lanzar anuncios": "pink",
    "Ejercicio fisico": "green",
    "Jornada de trabajo": "blue_grey",
    "Revisar numeros": "teal",
    "Reflexion diaria": "yellow",
    "Dormir temprano": "indigo",
}

def main(page: ft.Page):
    # 1. PANTALLA BLANCA DE SEGURIDAD (La que evita la pantalla negra)
    page.title = "Panel Imperio"
    page.bgcolor = "white"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # --- SISTEMA DE GUARDADO ROBUSTO (JSON) ---
    # Usamos esto porque el diagnóstico dijo que 'client_storage' fallaba
    def cargar_base_datos():
        try:
            if os.path.exists("imperio_data.json"):
                with open("imperio_data.json", "r") as f:
                    return json.load(f)
        except:
            pass
        return {}

    def guardar_base_datos(db):
        try:
            with open("imperio_data.json", "w") as f:
                json.dump(db, f)
        except:
            pass # Si falla, la app sigue viva

    # --- FUNCIÓN PRINCIPAL DEL IMPERIO ---
    def iniciar_sistema(e):
        # Limpiamos y ponemos modo oscuro
        page.clean()
        page.bgcolor = COLOR_FONDO_IMPERIO
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.padding = 15
        
        try:
            # Preparamos datos
            hoy_str = datetime.date.today().strftime("%Y-%m-%d")
            db = cargar_base_datos()
            if hoy_str not in db:
                db[hoy_str] = {}

            # Funciones para los checkboxes
            def al_cambiar(nombre, valor):
                db[hoy_str][nombre] = valor
                guardar_base_datos(db)
                actualizar_grafico()

            def leer_estado(nombre):
                return db.get(hoy_str, {}).get(nombre, False)

            # Componentes del Gráfico
            txt_progreso = ft.Text("0%", size=30, weight="bold", color=COLOR_ACENTO)
            anillo = ft.ProgressRing(width=120, height=120, stroke_width=10, color=COLOR_ACENTO, value=0)

            def actualizar_grafico():
                total = len(HABITOS_CONFIG)
                completados = sum(1 for h in HABITOS_CONFIG if leer_estado(h))
                ratio = completados / total if total > 0 else 0
                anillo.value = ratio
                txt_progreso.value = f"{int(ratio * 100)}%"
                page.update()

            # --- CONSTRUIMOS LA INTERFAZ ---
            
            # 1. Cabecera
            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Text("MI IMPERIO", size=22, weight="bold", color="white"),
                        ft.Text(random.choice(FRASES_MILLONARIAS), color="white70", italic=True, size=12, text_align="center"),
                        ft.Container(height=10),
                        ft.Stack([
                            anillo,
                            ft.Container(content=txt_progreso, alignment=ft.alignment.center, width=120, height=120)
                        ], alignment=ft.alignment.center),
                    ], horizontal_alignment="center"),
                    alignment=ft.alignment.center,
                    padding=10
                ),
                ft.Divider(color="white12", height=20)
            )

            # 2. Lista de Hábitos (Con Scroll)
            lista = ft.Column(scroll="auto", expand=True)

            for nombre, color_code in HABITOS_CONFIG.items():
                estado = leer_estado(nombre)
                
                # Checkbox
                chk = ft.Checkbox(
                    value=estado,
                    active_color=COLOR_ACENTO,
                    fill_color=color_code,
                    on_change=lambda e, n=nombre: al_cambiar(n, e.control.value)
                )

                lista.controls.append(
                    ft.Container(
                        content=ft.Row([
                            # Cuadradito de color (Más seguro que Iconos)
                            ft.Container(width=12, height=12, bgcolor=color_code, border_radius=3),
                            ft.Text(nombre, size=15, color="white", expand=True),
                            chk
                        ]),
                        bgcolor="#1E1E1E",
                        padding=12,
                        border_radius=8,
                        margin=ft.margin.only(bottom=8)
                    )
                )

            page.add(lista)
            actualizar_grafico() # Primera carga
            
        except Exception as error:
            # Si algo falla, lo mostramos en rojo
            page.add(ft.Text(f"Error: {error}", color="red"))
            page.update()

    # --- BOTÓN DE ENTRADA (Mismo de antes) ---
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
            ft.Text("Sistema listo.", size=16, color="grey"),
            ft.Container(height=30),
            boton
        ], alignment="center", horizontal_alignment="center", expand=True)
    )

ft.app(target=main)
