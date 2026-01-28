import flet as ft
import datetime
import random
import json
import os

# --- COLORES PREMIUM ---
COLOR_FONDO = "#000000"   # Negro Puro
COLOR_TARJETA = "#111111" # Gris muy oscuro
COLOR_ACENTO = "#00FF88"  # Verde Neón
COLOR_TEXTO = "#FFFFFF"

# --- DATOS ---
FRASES_MILLONARIAS = [
    "El dolor del sacrificio es temporal, la gloria es eterna.",
    "La disciplina es hacer lo que debes, aunque no quieras.",
    "Tu competencia está entrenando mientras tú duermes.",
    "Si fuera fácil, todo el mundo lo haría.",
    "El éxito es la suma de pequeños esfuerzos diarios.",
    "No busques motivación, busca disciplina.",
    "El dinero no duerme.",
    "Hazlo con miedo, pero hazlo.",
    "Tu futuro se crea por lo que haces hoy.",
    "Sé tan bueno que no puedan ignorarte."
]

HABITOS = [
    "Despertar 5:00 AM", "Tender cama", "Tomar agua", 
    "Ducha fría", "Meditación", "Planificar día", 
    "Desayuno sano", "Leer 20 min", "Ejercicio", 
    "Objetivo Principal", "Trabajo Profundo", "Ads/Marketing",
    "Networking", "Finanzas", "Dormir Temprano"
]

def main(page: ft.Page):
    # --- CONFIGURACIÓN (Basada en el éxito de v67) ---
    page.title = "Imperio v68"
    page.bgcolor = COLOR_FONDO
    page.padding = 10
    page.vertical_alignment = "start"

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

    # --- SISTEMA ---
    def iniciar_sistema(e):
        try:
            page.clean()
            
            db = cargar_db()
            hoy_str = datetime.date.today().strftime("%Y-%m-%d")
            if hoy_str not in db: db[hoy_str] = {}

            # Contenedor Principal
            contenido = ft.Column(expand=True, scroll="auto")
            
            # 1. ESPACIO PARA NOTCH (Para que no se tape el título)
            contenido.controls.append(ft.Container(height=35))

            # --- VISTA 1: RUTINA (Estructura v67 Blindada) ---
            def ver_rutina(e=None):
                contenido.controls.clear()
                contenido.controls.append(ft.Container(height=35))
                
                # Header Simple
                completados = sum(1 for h in HABITOS if db.get(hoy_str, {}).get(h, False))
                total = len(HABITOS)
                pct = int((completados / total) * 100) if total > 0 else 0
                
                contenido.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text("MI IMPERIO", size=15, color="grey", weight="bold"),
                            ft.Text(f"{pct}% COMPLETADO", size=25, weight="bold", color=COLOR_ACENTO),
                        ]),
                        padding=10,
                        alignment=ft.alignment.center
                    )
                )

                # Lista de Hábitos (IDÉNTICA A LA FOTO QUE ME MANDASTE)
                for habit in HABITOS:
                    estado = db.get(hoy_str, {}).get(habit, False)
                    
                    def cambiar(e, h=habit):
                        db[hoy_str][h] = e.control.value
                        guardar_db(db)
                        ver_rutina() # Recarga para actualizar %

                    # Diseño minimalista que sabemos que funciona
                    tarjeta = ft.Container(
                        content=ft.Row([
                            ft.Text(habit, color="white", size=15, expand=True),
                            ft.Checkbox(value=estado, active_color=COLOR_ACENTO, check_color="black", on_change=cambiar)
                        ]),
                        bgcolor=COLOR_TARJETA,
                        padding=15,
                        border_radius=8,
                        margin=3
                    )
                    contenido.controls.append(tarjeta)
                
                page.update()

            # --- VISTA 2: HISTORIAL ---
            def ver_calendario(e=None):
                contenido.controls.clear()
                contenido.controls.append(ft.Container(height=35))
                contenido.controls.append(ft.Text("HISTORIAL", size=20, color="white", weight="bold"))
                
                for i in range(7):
                    fecha = datetime.date.today() - datetime.timedelta(days=i)
                    f_str = fecha.strftime("%Y-%m-%d")
                    datos = db.get(f_str, {})
                    hechos = sum(1 for h in HABITOS if datos.get(h, False))
                    pct = int((hechos / len(HABITOS)) * 100)
                    
                    color_texto = COLOR_ACENTO if pct > 80 else "grey"
                    
                    contenido.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Text(f_str, color="white"),
                                ft.Container(expand=True),
                                ft.Text(f"{pct}%", color=color_texto, weight="bold")
                            ]),
                            bgcolor=COLOR_TARJETA, padding=20, margin=3, border_radius=8
                        )
                    )
                page.update()

            # --- VISTA 3: MENTOR ---
            def ver_frases(e=None):
                contenido.controls.clear()
                contenido.controls.append(ft.Container(height=35))
                frase = random.choice(FRASES_MILLONARIAS)
                
                contenido.controls.append(
                    ft.Column([
                        ft.Container(height=50),
                        ft.Text("MENTALIDAD", size=20, color="grey"),
                        ft.Container(
                            content=ft.Text(f'"{frase}"', size=20, color="white", italic=True, text_align="center"),
                            bgcolor=COLOR_TARJETA, padding=30, border_radius=15, margin=20
                        ),
                        ft.ElevatedButton("NUEVA FRASE", on_click=ver_frases, bgcolor=COLOR_ACENTO, color="black")
                    ], horizontal_alignment="center")
                )
                page.update()

            # --- MENÚ (Botones Simples) ---
            menu = ft.Container(
                content=ft.Row([
                    ft.ElevatedButton("RUTINA", on_click=ver_rutina, bgcolor="#222222", color="white", expand=True),
                    ft.ElevatedButton("HISTORIAL", on_click=ver_calendario, bgcolor="#222222", color="white", expand=True),
                    ft.ElevatedButton("MENTOR", on_click=ver_frases, bgcolor="#222222", color="white", expand=True),
                ], spacing=5),
                padding=10,
                bgcolor="black"
            )

            # Ensamblaje
            page.add(ft.Column([contenido, menu], expand=True, spacing=0))
            ver_rutina()

        except Exception as error:
            page.bgcolor = "black"
            page.clean()
            page.add(ft.Text(f"ERROR: {error}", color="red"))
            page.update()

    # --- PANTALLA INICIO ---
    btn_start = ft.ElevatedButton("ENTRAR AL IMPERIO", bgcolor=COLOR_ACENTO, color="black", weight="bold", height=50, on_click=iniciar_sistema)
    
    page.add(
        ft.Text("IMPERIO v68", size=30, color="white", weight="bold"),
        ft.Text("Sistema Estable", color="grey"),
        ft.Container(height=20),
        btn_start
    )

ft.app(target=main)
