import flet as ft
import datetime
import random
import json
import os

# --- CONFIGURACIÓN ---
COLOR_FONDO = "#121212"
COLOR_TARJETA = "#1E1E1E"
COLOR_ACENTO = "#00d26a"

FRASES_MILLONARIAS = [
    "Gana la mañana, gana el día.",
    "La disciplina es libertad.",
    "Hazlo con miedo, pero hazlo.",
    "Tu futuro se crea hoy.",
    "El dinero no duerme.",
    "No busques motivación, busca disciplina.",
    "El éxito es la suma de pequeños esfuerzos.",
    "Invierte en ti, es la única inversión segura."
]

HABITOS_CONFIG = {
    "Despertar 5:00 am": "orange",
    "Tomar agua": "blue",
    "Objetivo principal": "red",
    "Investigar productos": "purple",
    "Aprender algo nuevo": "yellow",
    "Ejercicio fisico": "green",
    "Dormir temprano": "indigo",
}

def main(page: ft.Page):
    # --- ARRANQUE SEGURO ---
    page.title = "Panel Imperio"
    page.bgcolor = "white"
    page.padding = 20
    # Usamos ENUMS (instrucciones internas) para evitar errores de texto
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- BASE DE DATOS (JSON SIMPLE) ---
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
        try:
            # 1. Limpieza y Configuración
            page.clean()
            page.bgcolor = COLOR_FONDO
            page.vertical_alignment = ft.MainAxisAlignment.START
            page.padding = 10
            
            # 2. Datos
            db = cargar_db()
            hoy_str = datetime.date.today().strftime("%Y-%m-%d")
            if hoy_str not in db: db[hoy_str] = {}

            # Contenedor dinámico
            area_contenido = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

            # --- VISTA 1: RUTINA ---
            def ver_rutina(e=None):
                area_contenido.controls.clear()
                
                # Porcentajes
                completados = sum(1 for h in HABITOS_CONFIG if db.get(hoy_str, {}).get(h, False))
                total = len(HABITOS_CONFIG)
                porcentaje = int((completados / total) * 100) if total > 0 else 0
                
                # Encabezado SIMPLE (Sin Stack, texto debajo del anillo)
                area_contenido.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text("MI IMPERIO", size=20, weight="bold", color="white"),
                            ft.ProgressRing(width=80, height=80, stroke_width=8, color=COLOR_ACENTO, value=completados/total if total > 0 else 0),
                            ft.Text(f"{porcentaje}% COMPLETADO", size=20, weight="bold", color=COLOR_ACENTO),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        alignment=ft.alignment.center # Alineación básica del contenedor padre
                    )
                )

                # Lista de Hábitos
                for nombre, color_code in HABITOS_CONFIG.items():
                    estado = db.get(hoy_str, {}).get(nombre, False)
                    
                    def cambiar(e, n=nombre):
                        db[hoy_str][n] = e.control.value
                        guardar_db(db)
                        ver_rutina()

                    chk = ft.Checkbox(value=estado, active_color=COLOR_ACENTO, fill_color=color_code, on_change=cambiar)
                    
                    area_contenido.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Container(width=10, height=10, bgcolor=color_code),
                                ft.Text(nombre, color="white", size=14, expand=True),
                                chk
                            ]),
                            bgcolor=COLOR_TARJETA, padding=10, border_radius=5, margin=2
                        )
                    )
                page.update()

            # --- VISTA 2: HISTORIAL ---
            def ver_calendario(e=None):
                area_contenido.controls.clear()
                area_contenido.controls.append(ft.Text("HISTORIAL 7 DÍAS", size=20, color="white", weight="bold"))
                
                for i in range(7):
                    fecha = datetime.date.today() - datetime.timedelta(days=i)
                    f_str = fecha.strftime("%Y-%m-%d")
                    datos = db.get(f_str, {})
                    hechos = sum(1 for h in HABITOS_CONFIG if datos.get(h, False))
                    pct = int((hechos / len(HABITOS_CONFIG)) * 100)
                    
                    color_pct = COLOR_ACENTO if pct > 80 else "grey"
                    
                    area_contenido.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Text(f_str, color="white"),
                                ft.Container(expand=True),
                                ft.Text(f"{pct}%", color=color_pct, weight="bold")
                            ]),
                            bgcolor=COLOR_TARJETA, padding=15, margin=2, border_radius=5
                        )
                    )
                page.update()

            # --- VISTA 3: FRASES ---
            def ver_frases(e=None):
                area_contenido.controls.clear()
                frase = random.choice(FRASES_MILLONARIAS)
                
                area_contenido.controls.append(
                    ft.Column([
                        ft.Container(height=50),
                        ft.Text("MENTALIDAD", size=20, color="white", weight="bold"),
                        ft.Container(
                            content=ft.Text(frase, size=18, color="white", italic=True, text_align=ft.TextAlign.CENTER),
                            bgcolor=COLOR_TARJETA, padding=30, border_radius=10, margin=20
                        ),
                        ft.ElevatedButton("NUEVA FRASE", on_click=ver_frases, bgcolor=COLOR_ACENTO, color="white")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
                page.update()

            # --- NAVEGACIÓN (Corregida con MainAxisAlignment) ---
            menu_botones = ft.Row(
                [
                    ft.ElevatedButton("RUTINA", on_click=ver_rutina, bgcolor="blue", color="white", expand=True),
                    ft.ElevatedButton("HISTORIAL", on_click=ver_calendario, bgcolor="grey", color="white", expand=True),
                    ft.ElevatedButton("MENTOR", on_click=ver_frases, bgcolor="orange", color="white", expand=True),
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY # <--- ESTO ES LO SEGURO
            )

            # --- ENSAMBLAJE ---
            page.add(
                ft.Column([
                    area_contenido,
                    ft.Container(content=menu_botones, padding=5, bgcolor="black")
                ], expand=True)
            )

            ver_rutina()

        except Exception as error_carga:
            # PANTALLA ROJA DE ERROR (Mejor que pantalla negra)
            page.bgcolor = "black"
            page.clean()
            page.add(ft.Text(f"ERROR v59: {error_carga}", color="red", size=20))
            page.update()

    # --- PANTALLA INICIAL ---
    btn_start = ft.ElevatedButton("ENTRAR v59", bgcolor="black", color="white", on_click=iniciar_sistema)
    
    page.add(
        ft.Text("¡HOLA LEO!", size=30, color="black", weight="bold"),
        ft.Text("Modo Seguro Activado", color="grey"),
        ft.Container(height=20),
        btn_start
    )

ft.app(target=main)
