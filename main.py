import flet as ft
import datetime
import random
import json
import os

# --- DISEÑO ULTRA ---
COLOR_FONDO = "#121212"
COLOR_TARJETA = "#1E1E1E"
COLOR_ACENTO = "#00d26a" # Verde Éxito

# --- ARSENAL DE 100 FRASES ---
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
    "Gana la mañana, gana el día.",
    "El fracaso es solo la oportunidad de comenzar de nuevo con más inteligencia.",
    "No cuentes los días, haz que los días cuenten.",
    "La cima es solitaria, pero la vista es increíble.",
    "Tu mente es tu activo más valioso.",
    "El miedo es un mentiroso.",
    "No esperes oportunidades, créalas.",
    "El éxito ama la velocidad.",
    "Mantén la visión, confía en el proceso.",
    "Sé un lobo, no una oveja.",
    "El confort es el enemigo del progreso.",
    "Aprende a descansar, no a renunciar.",
    "Tu red de contactos es tu patrimonio.",
    "Haz más de lo que te pagan por hacer.",
    "La suerte favorece a los valientes.",
    "Sé adicto a mejorar.",
    "Cierra la boca y abre tu mente.",
    "El talento sin disciplina no vale nada.",
    "Sé el trabajador más duro de la sala.",
    "No persigas el dinero, persigue la excelencia.",
    "Cada 'no' te acerca más a un 'sí'.",
    "La paciencia paga dividendos.",
    "Construye en silencio, sorprende al mundo.",
    "No dejes para mañana lo que puedes facturar hoy.",
    "Tu actitud determina tu altitud.",
    "Sé implacable.",
    "El único límite es tu mente.",
    "Rodéate de gigantes.",
    "No compitas, domina.",
    "La mediocridad es una enfermedad, la ambición es la cura.",
    "Haz que suceda.",
    "Sueña en grande, empieza pequeño, actúa ahora.",
    "El éxito no es un accidente.",
    "Sé un solucionador de problemas.",
    "Vende el problema que resuelves, no el producto.",
    "La consistencia es la clave.",
    "No te compares con nadie más que contigo mismo ayer.",
    "El respeto se gana, no se pide.",
    "Lidera con el ejemplo.",
    "Sé humilde en la victoria, fuerte en la derrota.",
    "Nunca es tarde para ser quien podrías haber sido.",
    "El dinero es una herramienta, no un amo.",
    "Libertad financiera es libertad real.",
    "Deja un legado.",
    "Vive como si fueras a morir mañana, aprende como si fueras a vivir siempre.",
    "La acción cura el miedo.",
    "Sé proactivo, no reactivo.",
    "Enfócate en lo que puedes controlar.",
    "La gratitud es riqueza.",
    "Sal de tu zona de confort.",
    "Rompe las reglas, no la ley.",
    "Sé original.",
    "Aporta valor masivo.",
    "El cliente es el rey.",
    "La marca personal es poder.",
    "Automatiza, delega, elimina.",
    "Piensa a largo plazo.",
    "Cuida tu cuerpo, es tu único vehículo.",
    "Lee, aprende, aplica.",
    "Sé curioso.",
    "La adaptabilidad es supervivencia.",
    "Crea múltiples fuentes de ingresos.",
    "El tiempo no perdona.",
    "Sé dueño de tu destino.",
    "Nunca te rindas."
]

# --- 20 HÁBITOS DE ÉLITE (Completo) ---
HABITOS_CONFIG = {
    "⏰ Despertar 5:00 AM": {"icon": "alarm", "color": "orange"},
    "🛏️ Tender la cama": {"icon": "bed", "color": "grey"},
    "💧 Tomar 1L agua": {"icon": "water_drop", "color": "blue"},
    "🚿 Ducha fría": {"icon": "ac_unit", "color": "cyan"},
    "🧘 Meditación/Orar": {"icon": "self_improvement", "color": "purple"},
    "📝 Planificar el día": {"icon": "edit_note", "color": "yellow"},
    "🥗 Desayuno nutritivo": {"icon": "restaurant", "color": "green"},
    "📚 Leer 20 min": {"icon": "menu_book", "color": "amber"},
    "🏃 Ejercicio Pesas/Cardio": {"icon": "fitness_center", "color": "red"},
    "🎯 Objetivo Principal": {"icon": "flag", "color": "red"},
    "🔍 Investigar Productos": {"icon": "search", "color": "purple"},
    "📢 Lanzar/Revisar Ads": {"icon": "campaign", "color": "pink"},
    "🧠 Aprender Habilidad (IA)": {"icon": "psychology", "color": "teal"},
    "⚡ Trabajo Profundo (2h)": {"icon": "flash_on", "color": "yellow"},
    "🤝 Networking": {"icon": "groups", "color": "blue"},
    "📊 Revisar Finanzas": {"icon": "attach_money", "color": "green"},
    "📱 Crear Contenido": {"icon": "video_camera_front", "color": "pink"},
    "🚫 Cero Azúcar": {"icon": "no_food", "color": "brown"},
    "💡 Reflexión Nocturna": {"icon": "lightbulb", "color": "yellow"},
    "😴 Dormir Temprano": {"icon": "nights_stay", "color": "indigo"},
}

def main(page: ft.Page):
    # --- CONFIGURACIÓN BASE ---
    page.title = "Imperio Ultra v61"
    page.bgcolor = "white"
    page.padding = 0
    CENTRO = ft.Alignment(0,0) # Matemático puro
    
    # --- MOTOR DE DATOS ---
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
            page.padding = 10
            
            db = cargar_db()
            hoy_str = datetime.date.today().strftime("%Y-%m-%d")
            if hoy_str not in db: db[hoy_str] = {}

            # Contenedor principal con SCROLL AUTOMÁTICO
            contenido = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

            # --- VISTA 1: RUTINA ULTRA ---
            def ver_rutina(e=None):
                contenido.controls.clear()
                
                # Header
                completados = sum(1 for h in HABITOS_CONFIG if db.get(hoy_str, {}).get(h, False))
                total = len(HABITOS_CONFIG)
                porcentaje = int((completados / total) * 100) if total > 0 else 0
                
                contenido.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(f"OBJETIVO: {total} VICTORIAS", size=12, color="grey", weight="bold"),
                            ft.Row([
                                ft.Text(f"{porcentaje}%", size=50, weight="bold", color=COLOR_ACENTO),
                                ft.Icon(name="verified", color=COLOR_ACENTO, size=40)
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            ft.ProgressBar(value=porcentaje/100, color=COLOR_ACENTO, bgcolor="#333333", height=8, border_radius=4)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        bgcolor=COLOR_TARJETA,
                        border_radius=15,
                        margin=ft.margin.only(bottom=15)
                    )
                )

                # Lista de 20 Hábitos
                for nombre, data in HABITOS_CONFIG.items():
                    estado = db.get(hoy_str, {}).get(nombre, False)
                    
                    def cambiar(e, n=nombre):
                        db[hoy_str][n] = e.control.value
                        guardar_db(db)
                        ver_rutina()

                    contenido.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Container(
                                    content=ft.Icon(name=data["icon"], color=data["color"], size=20),
                                    bgcolor="#2a2a2a", padding=8, border_radius=8, width=40, height=40, alignment=CENTRO
                                ),
                                ft.Text(nombre, size=15, color="white", weight="bold", expand=True),
                                ft.Checkbox(value=estado, active_color=COLOR_ACENTO, shape=ft.OutlinedBorder(radius=4), on_change=cambiar)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            bgcolor=COLOR_TARJETA,
                            padding=8,
                            border_radius=10,
                            margin=ft.margin.only(bottom=5)
                        )
                    )
                
                # Espacio extra al final para que el menú no tape el último hábito
                contenido.controls.append(ft.Container(height=20))
                page.update()

            # --- VISTA 2: RACHA ---
            def ver_calendario(e=None):
                contenido.controls.clear()
                contenido.controls.append(ft.Text("TU RACHA DE FUEGO", size=20, weight="bold", color="white"))
                contenido.controls.append(ft.Container(height=10))

                fila_dias = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, scroll=ft.ScrollMode.AUTO)
                
                for i in range(6, -1, -1):
                    fecha = datetime.date.today() - datetime.timedelta(days=i)
                    dia_letra = fecha.strftime("%a")[0].upper()
                    f_str = fecha.strftime("%Y-%m-%d")
                    datos = db.get(f_str, {})
                    hechos = sum(1 for h in HABITOS_CONFIG if datos.get(h, False))
                    total = len(HABITOS_CONFIG)
                    pct = (hechos / total) if total > 0 else 0
                    
                    if pct >= 0.8: color = COLOR_ACENTO
                    elif pct >= 0.4: color = "orange"
                    else: color = "#333333"

                    fila_dias.controls.append(
                        ft.Column([
                            ft.Container(
                                width=40, height=40, bgcolor=color, border_radius=20, alignment=CENTRO,
                                content=ft.Text(str(fecha.day), size=12, weight="bold", color="white" if pct < 0.4 else "black")
                            ),
                            ft.Text(dia_letra, size=10, color="grey")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5)
                    )

                contenido.controls.append(ft.Container(content=fila_dias, bgcolor=COLOR_TARJETA, padding=20, border_radius=15))
                page.update()

            # --- VISTA 3: 100 FRASES ---
            def ver_frases(e=None):
                contenido.controls.clear()
                frase = random.choice(FRASES_MILLONARIAS)
                
                contenido.controls.append(
                    ft.Column([
                        ft.Container(height=30),
                        ft.Icon("format_quote", size=50, color=COLOR_ACENTO),
                        ft.Text("SABIDURÍA MILLONARIA", size=14, color="grey", weight="bold"),
                        
                        ft.Container(
                            content=ft.Text(f'"{frase}"', size=20, color="white", italic=True, text_align=ft.TextAlign.CENTER),
                            bgcolor=COLOR_TARJETA, padding=30, border_radius=20, margin=20, alignment=CENTRO,
                            border=ft.border.all(1, COLOR_ACENTO)
                        ),
                        
                        ft.ElevatedButton("SIGUIENTE FRASE", icon="refresh", on_click=ver_frases, bgcolor=COLOR_ACENTO, color="black", height=50)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
                page.update()

            # --- MENÚ ESTILIZADO ---
            def crear_btn(icon, text, action, color_act):
                return ft.Container(
                    content=ft.Column([
                        ft.IconButton(icon=icon, icon_color=color_act, on_click=action, icon_size=24),
                        ft.Text(text, size=10, color="grey")
                    ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    expand=True
                )

            menu = ft.Container(
                content=ft.Row([
                    crear_btn("check_circle", "Rutina", ver_rutina, COLOR_ACENTO),
                    crear_btn("local_fire_department", "Racha", ver_calendario, "orange"),
                    crear_btn("psychology", "Mentor", ver_frases, "cyan"),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                bgcolor="#111111", padding=5, border=ft.border.only(top=ft.border.BorderSide(1, "#333333"))
            )

            page.add(ft.Column([contenido, menu], expand=True, spacing=0))
            ver_rutina()

        except Exception as e:
            page.bgcolor = "black"
            page.clean()
            page.add(ft.Text(f"ERROR: {e}", color="red"))
            page.update()

    # --- PANTALLA INICIO ---
    btn_start = ft.ElevatedButton("ENTRAR AL IMPERIO ULTRA", bgcolor=COLOR_ACENTO, color="black", weight="bold", height=50, width=250, on_click=iniciar_sistema)
    page.add(
        ft.Column([
            ft.Icon("diamond", size=80, color=COLOR_ACENTO),
            ft.Container(height=20),
            ft.Text("PANEL ULTRA v61", size=25, color="black", weight="bold"),
            ft.Text("100 Frases | 20 Hábitos", color="grey"),
            ft.Container(height=40),
            btn_start
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
    )

ft.app(target=main)
