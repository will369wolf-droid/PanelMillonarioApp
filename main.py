import flet as ft
import datetime
import random
import json
import os

# --- COLORES "STEALTH" (Modo Oscuro de Lujo) ---
COLOR_FONDO = "#000000"       # Negro puro
COLOR_TARJETA = "#111111"     # Gris casi negro
COLOR_TARJETA_BRN = "#1A1A1A" # Un poco más claro para contraste
COLOR_ACENTO = "#00FF88"      # Verde Neón (Cyberpunk)
COLOR_TEXTO = "#FFFFFF"

# --- DATOS BLINDADOS ---
FRASES_MILLONARIAS = [
    "Gana la mañana, gana el día.",
    "La disciplina es libertad.",
    "Tu futuro se crea hoy.",
    "El dinero no duerme.",
    "No busques motivación, busca disciplina.",
    "El éxito es la suma de pequeños esfuerzos.",
    "Invierte en ti.",
    "Hazlo con miedo, pero hazlo.",
    "Sé tan bueno que no puedan ignorarte.",
    "Tu competencia está entrenando ahora."
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
    # --- ARRANQUE SEGURO (Mismo de v62) ---
    page.title = "Imperio v65"
    page.bgcolor = "white"
    page.padding = 0
    # Strings simples para evitar errores de atributos
    page.vertical_alignment = "center" 
    page.horizontal_alignment = "center"
    
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

    # --- SISTEMA PRINCIPAL ---
    def iniciar_sistema(e):
        try:
            # 1. Configuración Visual
            page.clean()
            page.bgcolor = COLOR_FONDO
            page.padding = 15
            page.vertical_alignment = "start"
            
            # 2. Datos
            db = cargar_db()
            hoy_str = datetime.date.today().strftime("%Y-%m-%d")
            if hoy_str not in db: db[hoy_str] = {}

            # Contenedor con Scroll (Igual que v62)
            # Usamos una columna simple, sin "layouts" complejos
            contenido = ft.Column(expand=True, scroll="auto")
            
            # Espacio Notch
            contenido.controls.append(ft.Container(height=35))

            # --- VISTA 1: RUTINA (Estilo Tarjeta Negra) ---
            def ver_rutina(e=None):
                contenido.controls.clear()
                contenido.controls.append(ft.Container(height=35))
                
                # Header Simple y Seguro
                completados = sum(1 for h in HABITOS_CONFIG if db.get(hoy_str, {}).get(h, False))
                total = len(HABITOS_CONFIG)
                pct = int((completados / total) * 100) if total > 0 else 0
                
                contenido.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text("MI PROGRESO", size=12, color="grey"),
                            ft.Text(f"{pct}%", size=50, weight="bold", color=COLOR_ACENTO),
                            ft.Text("OBJETIVO DIARIO", size=12, color="white")
                        ], horizontal_alignment="center"),
                        padding=20,
                        alignment=CENTRO_MAT,
                        bgcolor=COLOR_TARJETA,
                        border_radius=15,
                        border=ft.border.all(1, "#333333") # Borde fino elegante
                    )
                )
                
                contenido.controls.append(ft.Container(height=20))

                # Lista de Hábitos
                for nombre, color_code in HABITOS_CONFIG.items():
                    estado = db.get(hoy_str, {}).get(nombre, False)
                    
                    def cambiar(e, n=nombre):
                        db[hoy_str][n] = e.control.value
                        guardar_db(db)
                        ver_rutina()

                    # Tarjeta Hábito (Misma estructura v62, mejor color)
                    contenido.controls.append(
                        ft.Container(
                            content=ft.Row([
                                # Indicador de color pequeño
                                ft.Container(width=5, height=25, bgcolor=color_code, border_radius=2),
                                ft.Text(nombre, size=15, color="white", weight="bold", expand=True),
                                ft.Checkbox(value=estado, active_color=COLOR_ACENTO, check_color="black", on_change=cambiar)
                            ]),
                            bgcolor=COLOR_TARJETA_BRN,
                            padding=15,
                            border_radius=8,
                            margin=ft.margin.only(bottom=8)
                        )
                    )
                page.update()

            # --- VISTA 2: HISTORIAL (Lista Vertical Estilizada) ---
            # Volvemos a la lista vertical (que funcionó), pero la hacemos bonita
            def ver_calendario(e=None):
                contenido.controls.clear()
                contenido.controls.append(ft.Container(height=35))
                
                contenido.controls.append(ft.Text("HISTORIAL RECIENTE", size=20, weight="bold", color="white"))
                contenido.controls.append(ft.Container(height=10))

                for i in range(7):
                    fecha = datetime.date.today() - datetime.timedelta(days=i)
                    f_str = fecha.strftime("%Y-%m-%d")
                    dia_letra = fecha.strftime("%A") # Nombre del día
                    
                    datos = db.get(f_str, {})
                    hechos = sum(1 for h in HABITOS_CONFIG if datos.get(h, False))
                    total = len(HABITOS_CONFIG)
                    ratio = hechos / total if total > 0 else 0
                    
                    # Colores dinámicos
                    color_pct = COLOR_ACENTO if ratio > 0.8 else "grey"
                    color_borde = COLOR_ACENTO if ratio > 0.8 else "#333333"

                    # Tarjeta de Día (Vertical, seguro)
                    contenido.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Column([
                                    ft.Text(f_str, color="white", weight="bold", size=16),
                                    ft.Text("Registro diario", color="grey", size=12)
                                ]),
                                ft.Container(expand=True),
                                ft.Container(
                                    content=ft.Text(f"{int(ratio*100)}%", color="black", weight="bold"),
                                    bgcolor=color_pct,
                                    padding=10,
                                    border_radius=8
                                )
                            ]),
                            bgcolor=COLOR_TARJETA,
                            padding=15,
                            border_radius=10,
                            margin=ft.margin.only(bottom=10),
                            border=ft.border.all(1, color_borde)
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
                        ft.Container(height=40),
                        ft.Text("MENTALIDAD", size=14, color="grey", weight="bold"),
                        
                        ft.Container(
                            content=ft.Text(f'"{frase}"', size=20, color="white", italic=True, text_align="center"),
                            bgcolor=COLOR_TARJETA,
                            padding=40,
                            border_radius=15,
                            margin=20,
                            alignment=CENTRO_MAT,
                            border=ft.border.all(1, COLOR_ACENTO)
                        ),
                        
                        ft.ElevatedButton("OTRA FRASE", on_click=ver_frases, bgcolor=COLOR_ACENTO, color="black")
                    ], horizontal_alignment="center")
                )
                page.update()

            # --- MENÚ DE NAVEGACIÓN (Botones Simples v62) ---
            # Mantenemos los botones simples pero con colores oscuros
            menu = ft.Container(
                content=ft.Row([
                    ft.ElevatedButton("RUTINA", on_click=ver_rutina, bgcolor=COLOR_TARJETA, color="white", expand=True),
                    ft.ElevatedButton("HISTORIAL", on_click=ver_calendario, bgcolor=COLOR_TARJETA, color="white", expand=True),
                    ft.ElevatedButton("MENTOR", on_click=ver_frases, bgcolor=COLOR_TARJETA, color="white", expand=True),
                ], spacing=10),
                bgcolor="black",
                padding=10
            )

            # Ensamblaje
            page.add(ft.Column([contenido, menu], expand=True, spacing=0))
            ver_rutina()

        except Exception as e:
            page.bgcolor = "black"
            page.clean()
            page.add(ft.Text(f"ERROR: {e}", color="red", size=20))
            page.update()

    # --- PANTALLA INICIO ---
    btn_start = ft.ElevatedButton("ENTRAR v65", bgcolor=COLOR_ACENTO, color="black", weight="bold", height=50, width=200, on_click=iniciar_sistema)
    
    page.add(
        ft.Text("IMPERIO", size=40, color="black", weight="bold"),
        ft.Text("Sistema Final v65", color="grey"),
        ft.Container(height=50),
        btn_start
    )

ft.app(target=main)
