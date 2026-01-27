import flet as ft
import datetime
import random
import json
import os

# --- COLORES PREMIUM ---
COLOR_FONDO = "#121212"
COLOR_TARJETA = "#1E1E1E" 
COLOR_TEXTO = "#FFFFFF"
COLOR_VERDE = "#00d26a" # Éxito
COLOR_ROJO = "#f44336"  # Fallo
COLOR_GRIS = "#424242"  # Neutro

# --- DATOS ---
FRASES_MILLONARIAS = [
    "Gana la mañana, gana el día.",
    "Tu competencia está entrenando ahora.",
    "La disciplina es libertad.",
    "El dolor es temporal, la gloria es eterna.",
    "No te detengas cuando estés cansado, detente cuando termines.",
    "Si fuera fácil, todos lo harían.",
    "Tu cuenta bancaria refleja tus hábitos.",
    "Cierra la boca y trabaja.",
    "El éxito ama la velocidad.",
    "Sé el CEO de tu propia vida."
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
    # --- CONFIGURACIÓN SEGURA ---
    page.title = "Imperio Premium"
    page.bgcolor = "white"
    page.padding = 0
    # Alineación segura (strings)
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    
    # Constante matemática para centrar
    CENTRO = ft.Alignment(0,0)

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
            page.bgcolor = COLOR_FONDO
            page.padding = 0 # Sin padding global para que el menú toque el borde
            page.vertical_alignment = "start"
            
            db = cargar_db()
            hoy_str = datetime.date.today().strftime("%Y-%m-%d")
            if hoy_str not in db: db[hoy_str] = {}

            # Contenedor Principal (Con espacio para Notch)
            contenido = ft.Column(expand=True, scroll="auto")
            contenido.controls.append(ft.Container(height=40)) # Espacio Notch

            # --- VISTA 1: RUTINA (Limpia) ---
            def ver_rutina(e=None):
                contenido.controls.clear()
                contenido.controls.append(ft.Container(height=40)) # Notch
                
                # Header Premium
                completados = sum(1 for h in HABITOS_CONFIG if db.get(hoy_str, {}).get(h, False))
                total = len(HABITOS_CONFIG)
                pct = int((completados / total) * 100) if total > 0 else 0
                
                contenido.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text("MI OBJETIVO DE HOY", size=12, color="grey", weight="bold"),
                            ft.Text(f"{pct}%", size=60, weight="bold", color=COLOR_VERDE),
                            ft.ProgressBar(value=pct/100, color=COLOR_VERDE, bgcolor="#333333", height=5)
                        ], horizontal_alignment="center", spacing=5),
                        padding=20,
                        alignment=CENTRO
                    )
                )

                # Lista Estilizada
                for nombre, col in HABITOS_CONFIG.items():
                    estado = db.get(hoy_str, {}).get(nombre, False)
                    
                    def cambiar(e, n=nombre):
                        db[hoy_str][n] = e.control.value
                        guardar_db(db)
                        ver_rutina()

                    # Tarjeta limpia (Sin cuadrado de color extra)
                    contenido.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Text(nombre, size=16, color="white", weight="bold", expand=True),
                                ft.Checkbox(value=estado, active_color=COLOR_VERDE, check_color="black", on_change=cambiar)
                            ], alignment="spaceBetween"),
                            bgcolor=COLOR_TARJETA,
                            padding=15,
                            border_radius=12,
                            margin=ft.margin.only(left=15, right=15, bottom=8)
                        )
                    )
                
                contenido.controls.append(ft.Container(height=20))
                page.update()

            # --- VISTA 2: RACHA (Burbujas Visuales) ---
            def ver_calendario(e=None):
                contenido.controls.clear()
                contenido.controls.append(ft.Container(height=40)) # Notch
                
                contenido.controls.append(
                    ft.Container(
                        content=ft.Text("MI RACHA SEMANAL", size=20, weight="bold", color="white"),
                        padding=ft.padding.only(left=20, bottom=20)
                    )
                )

                # Fila de Burbujas
                fila_burbujas = ft.Row(alignment="center", spacing=10)
                
                # Últimos 7 días (Del más antiguo al nuevo -> izq a der)
                # O del nuevo al antiguo? Vamos a poner HOY a la derecha (estilo racha)
                for i in range(6, -1, -1):
                    fecha = datetime.date.today() - datetime.timedelta(days=i)
                    f_str = fecha.strftime("%Y-%m-%d")
                    dia_letra = fecha.strftime("%a")[0].upper() # L, M, M...
                    
                    datos = db.get(f_str, {})
                    hechos = sum(1 for h in HABITOS_CONFIG if datos.get(h, False))
                    total = len(HABITOS_CONFIG)
                    ratio = hechos / total if total > 0 else 0
                    
                    # Color de la burbuja
                    if ratio >= 0.8: color_burbuja = COLOR_VERDE
                    elif ratio >= 0.4: color_burbuja = "orange"
                    else: color_burbuja = COLOR_GRIS
                    
                    # Burbuja (Container Redondo)
                    burbuja = ft.Column([
                        ft.Container(
                            width=35, height=35,
                            bgcolor=color_burbuja,
                            border_radius=35, # Esto lo hace redondo
                            alignment=CENTRO,
                            content=ft.Text(str(fecha.day), size=12, weight="bold", color="black" if ratio > 0.3 else "white")
                        ),
                        ft.Text(dia_letra, size=10, color="grey")
                    ], spacing=5, horizontal_alignment="center")
                    
                    fila_burbujas.controls.append(burbuja)

                # Tarjeta contenedora
                contenido.controls.append(
                    ft.Container(
                        content=fila_burbujas,
                        bgcolor=COLOR_TARJETA,
                        padding=20,
                        border_radius=15,
                        margin=20
                    )
                )
                
                # Stats Extra
                dias_perfectos = sum(1 for d in db.values() if sum(1 for h in HABITOS_CONFIG if d.get(h)) == len(HABITOS_CONFIG))
                
                contenido.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text("ESTADÍSTICAS TOTALES", size=12, color="grey"),
                            ft.Text(f"{dias_perfectos} DÍAS PERFECTOS", size=20, weight="bold", color="white")
                        ]),
                        padding=20, margin=20, bgcolor=COLOR_TARJETA, border_radius=15
                    )
                )

                page.update()

            # --- VISTA 3: MENTOR (Elegante) ---
            def ver_frases(e=None):
                contenido.controls.clear()
                contenido.controls.append(ft.Container(height=40)) # Notch
                
                frase = random.choice(FRASES_MILLONARIAS)
                
                contenido.controls.append(
                    ft.Column([
                        ft.Container(height=40),
                        ft.Text("MENTALIDAD", size=14, color="grey", letter_spacing=2),
                        
                        ft.Container(
                            content=ft.Text(f'"{frase}"', size=24, color="white", italic=True, text_align="center"),
                            padding=40,
                            margin=20,
                            alignment=CENTRO
                        ),
                        
                        ft.ElevatedButton(
                            "NUEVA IDEA", 
                            on_click=ver_frases, 
                            bgcolor="#333333", 
                            color="white",
                            height=50,
                            width=200
                        )
                    ], horizontal_alignment="center")
                )
                page.update()

            # --- MENÚ INFERIOR (Estilo App Nativa) ---
            # Usamos botones negros simples pero elegantes
            menu = ft.Container(
                content=ft.Row([
                    ft.ElevatedButton("RUTINA", on_click=ver_rutina, bgcolor=COLOR_FONDO, color="grey", elevation=0),
                    ft.ElevatedButton("RACHA", on_click=ver_calendario, bgcolor=COLOR_FONDO, color="grey", elevation=0),
                    ft.ElevatedButton("MENTOR", on_click=ver_frases, bgcolor=COLOR_FONDO, color="grey", elevation=0),
                ], alignment="spaceEvenly"),
                bgcolor="#000000",
                padding=10,
                border=ft.border.only(top=ft.border.BorderSide(1, "#333333"))
            )

            # Ensamblaje
            page.add(ft.Column([contenido, menu], expand=True, spacing=0))
            ver_rutina()

        except Exception as e:
            page.bgcolor = "black"
            page.clean()
            page.add(ft.Text(f"ERROR: {e}", color="red"))
            page.update()

    # --- PANTALLA INICIO ---
    btn_start = ft.ElevatedButton("ABRIR IMPERIO", bgcolor=COLOR_VERDE, color="black", weight="bold", height=50, width=200, on_click=iniciar_sistema)
    
    page.add(
        ft.Column([
            ft.Text("IMPERIO", size=40, color="black", weight="bold"),
            ft.Text("Edición Premium v63", color="grey"),
            ft.Container(height=50),
            btn_start
        ], alignment="center", horizontal_alignment="center", expand=True)
    )

ft.app(target=main)
