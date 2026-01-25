import flet as ft
import datetime
import random
import json
import os

# --- CONFIGURACIÓN ---
COLOR_ACENTO = "#00d26a"
COLOR_FONDO = "#121212"
COLOR_TARJETA = "#1E1E1E"

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
    # --- ARRANQUE SEGURO ---
    page.title = "Panel Imperio"
    page.bgcolor = "white"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0 # Padding 0 para que el menú toque el borde

    # --- BASE DE DATOS ---
    def cargar_db():
        try:
            if os.path.exists("imperio_data.json"):
                with open("imperio_data.json", "r") as f: return json.load(f)
        except: pass
        return {}

    def guardar_db(db):
        try:
            with open("imperio_data.json", "w") as f: json.dump(db, f)
        except: pass

    # --- SISTEMA PRINCIPAL ---
    def iniciar_sistema(e):
        page.clean()
        page.bgcolor = COLOR_FONDO
        page.vertical_alignment = ft.MainAxisAlignment.START
        
        # Contenedor principal donde cambiaremos el contenido (Rutina, Calendario, Frases)
        contenedor_principal = ft.Column(expand=True, scroll="auto")
        
        db = cargar_db()
        hoy_str = datetime.date.today().strftime("%Y-%m-%d")
        if hoy_str not in db: db[hoy_str] = {}

        # --- VISTA 1: RUTINA (Tu lista) ---
        def vista_rutina():
            
            def al_cambiar(nombre, valor):
                db[hoy_str][nombre] = valor
                guardar_db(db)
                actualizar_grafico()

            # Gráfico
            txt_progreso = ft.Text("0%", size=25, weight="bold", color=COLOR_ACENTO)
            alineacion_centro = ft.Alignment(0, 0)
            anillo = ft.ProgressRing(width=100, height=100, stroke_width=8, color=COLOR_ACENTO, value=0)

            def actualizar_grafico():
                total = len(HABITOS_CONFIG)
                completados = sum(1 for h in HABITOS_CONFIG if db.get(hoy_str, {}).get(h, False))
                ratio = completados / total if total > 0 else 0
                anillo.value = ratio
                txt_progreso.value = f"{int(ratio * 100)}%"
                page.update()

            # Lista
            lista_items = ft.Column()
            for nombre, color_code in HABITOS_CONFIG.items():
                estado = db.get(hoy_str, {}).get(nombre, False)
                chk = ft.Checkbox(value=estado, active_color=COLOR_ACENTO, fill_color=color_code, 
                                  on_change=lambda e, n=nombre: al_cambiar(n, e.control.value))
                lista_items.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Container(width=10, height=10, bgcolor=color_code, border_radius=2),
                            ft.Text(nombre, size=14, color="white", expand=True),
                            chk
                        ]),
                        bgcolor=COLOR_TARJETA, padding=12, border_radius=8, margin=5
                    )
                )
            
            # Ensamblaje Rutina
            columna = ft.Column([
                ft.Container(height=10),
                ft.Text("MI IMPERIO HOY", size=20, weight="bold", color="white", text_align="center"),
                ft.Container(
                    content=ft.Stack([anillo, ft.Container(content=txt_progreso, alignment=alineacion_centro)], alignment=alineacion_centro),
                    alignment=alineacion_centro, padding=10
                ),
                lista_items
            ], horizontal_alignment="center")
            
            actualizar_grafico()
            return columna

        # --- VISTA 2: HISTORIAL (Calendario Simple) ---
        def vista_calendario():
            lista_dias = ft.Column()
            
            # Mostramos los últimos 7 días
            for i in range(7):
                fecha = datetime.date.today() - datetime.timedelta(days=i)
                fecha_fmt = fecha.strftime("%Y-%m-%d")
                
                # Datos de ese día
                datos_dia = db.get(fecha_fmt, {})
                completados = sum(1 for h in HABITOS_CONFIG if datos_dia.get(h, False))
                total = len(HABITOS_CONFIG)
                porcentaje = int((completados / total) * 100) if total > 0 else 0
                
                color_dia = COLOR_ACENTO if porcentaje > 80 else "grey"
                
                lista_dias.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(fecha_fmt, color="white", size=16, weight="bold"),
                            ft.Container(expand=True),
                            ft.Text(f"{porcentaje}%", color=color_dia, size=16, weight="bold"),
                            ft.Icon(name="check_circle" if porcentaje > 80 else "circle", color=color_dia)
                        ]),
                        bgcolor=COLOR_TARJETA, padding=15, border_radius=10, margin=5
                    )
                )
            
            return ft.Column([
                ft.Container(height=20),
                ft.Text("HISTORIAL DE BATALLA", size=20, weight="bold", color="white"),
                ft.Divider(color="white24"),
                lista_dias
            ], horizontal_alignment="center")

        # --- VISTA 3: MENTORES (Frases) ---
        def vista_mentores():
            frase_actual = ft.Text(random.choice(FRASES_MILLONARIAS), size=18, text_align="center", italic=True, color="white")
            
            def nueva_frase(e):
                frase_actual.value = random.choice(FRASES_MILLONARIAS)
                page.update()

            return ft.Column([
                ft.Container(height=50),
                ft.Icon(name="psychology", size=80, color=COLOR_ACENTO),
                ft.Container(height=20),
                ft.Text("MENTALIDAD", size=22, weight="bold", color="white"),
                ft.Container(
                    content=frase_actual,
                    bgcolor=COLOR_TARJETA, padding=30, border_radius=20, margin=20
                ),
                ft.ElevatedButton("NUEVA FRASE", color="white", bgcolor=COLOR_ACENTO, on_click=nueva_frase)
            ], horizontal_alignment="center", alignment="center")

        # --- NAVEGACIÓN ---
        def cambiar_tab(e):
            indice = e.control.selected_index
            contenedor_principal.controls.clear()
            
            if indice == 0:
                contenedor_principal.controls.append(vista_rutina())
            elif indice == 1:
                contenedor_principal.controls.append(vista_calendario())
            elif indice == 2:
                contenedor_principal.controls.append(vista_mentores())
            
            page.update()

        # Barra de Navegación Inferior
        nav_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(icon="check_circle", label="Día"),
                ft.NavigationDestination(icon="calendar_month", label="Historial"),
                ft.NavigationDestination(icon="psychology", label="Mentores"),
            ],
            bgcolor="#111111",
            indicator_color=COLOR_ACENTO,
            on_change=cambiar_tab,
            selected_index=0
        )

        # Carga inicial
        contenedor_principal.controls.append(vista_rutina())
        page.add(contenedor_principal, nav_bar)

    # --- BOTÓN DE ENTRADA ---
    boton = ft.ElevatedButton("ENTRAR AL SISTEMA", color="white", bgcolor="black", on_click=iniciar_sistema, height=50)
    page.add(
        ft.Column([
            ft.Text("¡HOLA LEO!", size=35, color="black", weight="bold"),
            ft.Text("Versión Completa v56", size=16, color="grey"),
            ft.Container(height=30),
            boton
        ], alignment="center", horizontal_alignment="center", expand=True)
    )

ft.app(target=main)
