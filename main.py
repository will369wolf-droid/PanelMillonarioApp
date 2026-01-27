import flet as ft
import datetime
import random
import json
import os

# --- COLORES ---
COLOR_FONDO = "#121212"
COLOR_TARJETA = "#1E1E1E"
COLOR_VERDE = "#00d26a"

FRASES_MILLONARIAS = [
    "Gana la mañana, gana el día.",
    "La disciplina es libertad.",
    "Tu futuro se crea hoy.",
    "El dinero no duerme.",
    "No busques motivación, busca disciplina.",
    "El éxito es la suma de pequeños esfuerzos.",
    "Invierte en ti.",
    "Hazlo con miedo, pero hazlo."
]

HABITOS_CONFIG = {
    "⏰ Despertar 5:00 AM": "orange",
    "🛏️ Tender la cama": "grey",
    "💧 Tomar agua": "blue",
    "🚿 Ducha fría": "cyan",
    "🧘 Meditación": "purple",
    "📝 Planificar día": "yellow",
    "🥗 Desayuno sano": "green",
    "📚 Leer 20 min": "amber",
    "🏋️ Ejercicio": "red",
    "🎯 Objetivo Principal": "red",
    "💻 Trabajo Profundo": "yellow",
    "📢 Ads / Marketing": "pink",
    "🤝 Networking": "blue",
    "💰 Revisar Finanzas": "green",
    "😴 Dormir Temprano": "indigo",
}

def main(page: ft.Page):
    # --- ARRANQUE SEGURO ---
    page.title = "Imperio v64"
    page.bgcolor = "white"
    page.padding = 0
    # Usamos constantes seguras
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    CENTRO_MAT = ft.Alignment(0,0)

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
            # Limpieza y cambio a modo oscuro
            page.clean()
            page.bgcolor = COLOR_FONDO
            page.padding = 10
            page.vertical_alignment = ft.MainAxisAlignment.START
            
            db = cargar_db()
            hoy_str = datetime.date.today().strftime("%Y-%m-%d")
            if hoy_str not in db: db[hoy_str] = {}

            # Contenedor Principal (Con Scroll Auto como en v62)
            contenido = ft.Column(expand=True, scroll="auto")
            
            # Espacio para Notch (Seguridad)
            contenido.controls.append(ft.Container(height=35))

            # --- VISTA 1: RUTINA (Diseño Limpio) ---
            def ver_rutina(e=None):
                contenido.controls.clear()
                contenido.controls.append(ft.Container(height=35))
                
                # Header
                completados = sum(1 for h in HABITOS_CONFIG if db.get(hoy_str, {}).get(h, False))
                total = len(HABITOS_CONFIG)
                pct = int((completados / total) * 100) if total > 0 else 0
                
                contenido.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text("OBJETIVO DIARIO", size=12, color="grey", weight="bold"),
                            ft.Text(f"{pct}%", size=60, weight="bold", color=COLOR_VERDE),
                            ft.Text("COMPLETADO", size=12, color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        alignment=CENTRO_MAT,
                        bgcolor=COLOR_TARJETA,
                        border_radius=15
                    )
                )
                
                contenido.controls.append(ft.Container(height=10))

                # Lista de Hábitos
                for nombre, color_code in HABITOS_CONFIG.items():
                    estado = db.get(hoy_str, {}).get(nombre, False)
                    
                    def cambiar(e, n=nombre):
                        db[hoy_str][n] = e.control.value
                        guardar_db(db)
                        ver_rutina()

                    # Tarjeta sin iconos complejos, solo Emoji + Texto
                    contenido.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Text(nombre, size=15, color="white", weight="bold", expand=True),
                                ft.Checkbox(value=estado, active_color=COLOR_VERDE, on_change=cambiar)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), # Enum Seguro
                            bgcolor=COLOR_TARJETA,
                            padding=15,
                            border_radius=10,
                            margin=ft.margin.only(bottom=5)
                        )
                    )
                page.update()

            # --- VISTA 2: RACHA (Burbujas Seguras) ---
            def ver_calendario(e=None):
                contenido.controls.clear()
                contenido.controls.append(ft.Container(height=35))
                
                contenido.controls.append(ft.Text("RACHA SEMANAL", size=20, weight="bold", color="white"))
                contenido.controls.append(ft.Container(height=10))

                # Fila de Burbujas (Usando Row simple)
                fila = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=10)
                
                for i in range(6, -1, -1):
                    fecha = datetime.date.today() - datetime.timedelta(days=i)
                    dia_num = str(fecha.day)
                    dia_letra = fecha.strftime("%a")[0].upper()
                    f_str = fecha.strftime("%Y-%m-%d")
                    
                    datos = db.get(f_str, {})
                    hechos = sum(1 for h in HABITOS_CONFIG if datos.get(h, False))
                    total = len(HABITOS_CONFIG)
                    ratio = hechos / total if total > 0 else 0
                    
                    color_burbuja = "#333333" # Gris oscuro defecto
                    texto_color = "white"
                    
                    if ratio >= 0.8: 
                        color_burbuja = COLOR_VERDE
                        texto_color = "black"
                    elif ratio >= 0.4: 
                        color_burbuja = "orange"
                        texto_color = "black"

                    # Burbuja hecha a mano (Container seguro)
                    burbuja = ft.Column([
                        ft.Container(
                            width=35, height=35,
                            bgcolor=color_burbuja,
                            border_radius=35,
                            alignment=CENTRO_MAT,
                            content=ft.Text(dia_num, size=12, weight="bold", color=texto_color)
                        ),
                        ft.Text(dia_letra, size=10, color="grey")
                    ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    
                    fila.controls.append(burbuja)

                contenido.controls.append(
                    ft.Container(
                        content=fila,
                        bgcolor=COLOR_TARJETA,
                        padding=20,
                        border_radius=15
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
                        ft.Container(height=20),
                        ft.Text("MENTALIDAD", size=14, color="grey", weight="bold"),
                        
                        ft.Container(
                            content=ft.Text(f'"{frase}"', size=22, color="white", italic=True, text_align=ft.TextAlign.CENTER),
                            bgcolor=COLOR_TARJETA,
                            padding=30,
                            border_radius=15,
                            margin=20,
                            alignment=CENTRO_MAT
                        ),
                        
                        ft.ElevatedButton("NUEVA IDEA", on_click=ver_frases, bgcolor=COLOR_VERDE, color="black")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
                page.update()

            # --- MENÚ DE NAVEGACIÓN (Botones Negros Elegantes) ---
            # Usamos botones simples pero con color negro para que se vea integrado
            menu = ft.Container(
                content=ft.Row([
                    ft.ElevatedButton("RUTINA", on_click=ver_rutina, bgcolor="#222222", color="white", expand=True),
                    ft.ElevatedButton("RACHA", on_click=ver_calendario, bgcolor="#222222", color="white", expand=True),
                    ft.ElevatedButton("MENTOR", on_click=ver_frases, bgcolor="#222222", color="white", expand=True),
                ], spacing=5),
                bgcolor="black",
                padding=5
            )

            # Ensamblaje
            page.add(ft.Column([contenido, menu], expand=True, spacing=0))
            ver_rutina()

        except Exception as e:
            # Si falla, pantalla negra con error rojo
            page.bgcolor = "black"
            page.clean()
            page.add(ft.Text(f"ERROR: {e}", color="red", size=20))
            page.update()

    # --- PANTALLA INICIO ---
    btn_start = ft.ElevatedButton("ABRIR IMPERIO v64", bgcolor=COLOR_VERDE, color="black", weight="bold", height=50, on_click=iniciar_sistema)
    
    page.add(
        ft.Text("IMPERIO", size=40, color="black", weight="bold"),
        ft.Text("Edición Segura", color="grey"),
        ft.Container(height=50),
        btn_start
    )

ft.app(target=main)
