import flet as ft
import datetime
import random
import json
import os

# --- CONFIGURACIÓN ESTÉTICA ---
COLOR_FONDO = "#121212"
COLOR_TARJETA = "#1E1E1E"
COLOR_ACENTO = "#00d26a" # Verde Éxito

# --- 100 FRASES DE PODER (Base de Datos) ---
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

# --- 20 HÁBITOS IMPERIALES (Con Emojis Seguros) ---
HABITOS_CONFIG = {
    "⏰ Despertar 5:00 AM": "orange",
    "🛏️ Tender la cama": "grey",
    "💧 Tomar agua": "blue",
    "🚿 Ducha fría": "cyan",
    "🧘 Meditación/Orar": "purple",
    "📝 Planificar el día": "yellow",
    "🥗 Desayuno nutritivo": "green",
    "📚 Leer 20 min": "amber",
    "🏃 Ejercicio Pesas": "red",
    "🎯 Objetivo Principal": "red",
    "🔍 Investigar Productos": "purple",
    "📢 Revisar Ads": "pink",
    "🧠 Aprender IA": "teal",
    "⚡ Trabajo Profundo": "yellow",
    "🤝 Networking": "blue",
    "📊 Revisar Finanzas": "green",
    "📱 Crear Contenido": "pink",
    "🚫 Cero Azúcar": "brown",
    "💡 Reflexión": "yellow",
    "😴 Dormir Temprano": "indigo",
}

def main(page: ft.Page):
    # --- ARRANQUE SEGURO ---
    page.title = "Imperio Final v61"
    page.bgcolor = "white"
    page.padding = 0
    
    # Coordenada matemática segura (reemplaza a alignment.center)
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

    # --- SISTEMA PRINCIPAL ---
    def iniciar_sistema(e):
        try:
            # 1. Configuración Visual
            page.clean()
            page.bgcolor = COLOR_FONDO
            page.padding = 10
            
            # 2. Datos
            db = cargar_db()
            hoy_str = datetime.date.today().strftime("%Y-%m-%d")
            if hoy_str not in db: db[hoy_str] = {}

            # Contenedor con Scroll
            contenido = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

            # --- CORRECCIÓN NOTCH (Espacio superior) ---
            contenido.controls.append(ft.Container(height=35)) 

            # --- VISTA 1: RUTINA ---
            def ver_rutina(e=None):
                contenido.controls.clear()
                contenido.controls.append(ft.Container(height=35)) # Espacio notch
                
                # Header
                completados = sum(1 for h in HABITOS_CONFIG if db.get(hoy_str, {}).get(h, False))
                total = len(HABITOS_CONFIG)
                porcentaje = int((completados / total) * 100) if total > 0 else 0
                
                contenido.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text("MI IMPERIO", size=14, color="grey", weight="bold"),
                            ft.Text(f"{porcentaje}%", size=50, weight="bold", color=COLOR_ACENTO),
                            ft.Text("COMPLETADO", size=12, color="white", weight="bold"),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        bgcolor=COLOR_TARJETA,
                        border_radius=15,
                        alignment=CENTRO,
                        margin=ft.margin.only(bottom=15)
                    )
                )

                # Lista de Hábitos
                for nombre, color_code in HABITOS_CONFIG.items():
                    estado = db.get(hoy_str, {}).get(nombre, False)
                    
                    def cambiar(e, n=nombre):
                        db[hoy_str][n] = e.control.value
                        guardar_db(db)
                        ver_rutina()

                    # Tarjeta de Hábito
                    contenido.controls.append(
                        ft.Container(
                            content=ft.Row([
                                # Cuadrado de color (Seguro)
                                ft.Container(width=10, height=30, bgcolor=color_code, border_radius=2),
                                ft.Text(nombre, size=15, color="white", weight="bold", expand=True),
                                ft.Checkbox(value=estado, active_color=COLOR_ACENTO, on_change=cambiar)
                            ]),
                            bgcolor=COLOR_TARJETA,
                            padding=10,
                            border_radius=10,
                            margin=ft.margin.only(bottom=5)
                        )
                    )
                
                contenido.controls.append(ft.Container(height=20))
                page.update()

            # --- VISTA 2: RACHA ---
            def ver_calendario(e=None):
                contenido.controls.clear()
                contenido.controls.append(ft.Container(height=35)) # Espacio notch
                contenido.controls.append(ft.Text("HISTORIAL 7 DÍAS", size=20, weight="bold", color="white"))
                
                for i in range(7):
                    fecha = datetime.date.today() - datetime.timedelta(days=i)
                    f_str = fecha.strftime("%Y-%m-%d")
                    datos = db.get(f_str, {})
                    hechos = sum(1 for h in HABITOS_CONFIG if datos.get(h, False))
                    total = len(HABITOS_CONFIG)
                    pct = (hechos / total) if total > 0 else 0
                    
                    if pct >= 0.8: color = COLOR_ACENTO
                    elif pct >= 0.4: color = "orange"
                    else: color = "#333333"

                    contenido.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Text(f_str, color="white", size=16),
                                ft.Container(expand=True),
                                ft.Container(
                                    content=ft.Text(f"{int(pct*100)}%", color="black" if pct > 0.4 else "white", weight="bold", size=12),
                                    bgcolor=color, padding=5, border_radius=5, width=50, alignment=CENTRO
                                )
                            ]),
                            bgcolor=COLOR_TARJETA, padding=15, margin=2, border_radius=5
                        )
                    )
                page.update()

            # --- VISTA 3: FRASES ---
            def ver_frases(e=None):
                contenido.controls.clear()
                contenido.controls.append(ft.Container(height=35)) # Espacio notch
                frase = random.choice(FRASES_MILLONARIAS)
                
                contenido.controls.append(
                    ft.Column([
                        ft.Container(height=20),
                        ft.Text("MENTALIDAD", size=14, color="grey", weight="bold"),
                        
                        ft.Container(
                            content=ft.Text(f'"{frase}"', size=20, color="white", italic=True, text_align=ft.TextAlign.CENTER),
                            bgcolor=COLOR_TARJETA, padding=30, border_radius=20, margin=20, alignment=CENTRO,
                            border=ft.border.all(1, COLOR_ACENTO)
                        ),
                        
                        ft.ElevatedButton("OTRA FRASE", on_click=ver_frases, bgcolor=COLOR_ACENTO, color="black")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
                page.update()

            # --- MENÚ SEGURO (Botones simples) ---
            # Volvemos a los botones simples que sabemos que funcionan
            menu = ft.Container(
                content=ft.Row([
                    ft.ElevatedButton("RUTINA", on_click=ver_rutina, bgcolor="#222222", color="white", expand=True),
                    ft.ElevatedButton("RACHA", on_click=ver_calendario, bgcolor="#222222", color="white", expand=True),
                    ft.ElevatedButton("MENTOR", on_click=ver_frases, bgcolor="#222222", color="white", expand=True),
                ], spacing=5),
                bgcolor="black", padding=5
            )

            page.add(ft.Column([contenido, menu], expand=True, spacing=0))
            ver_rutina()

        except Exception as e:
            page.bgcolor = "black"
            page.clean()
            page.add(ft.Text(f"ERROR: {e}", color="red", size=20))
            page.update()

    # --- PANTALLA INICIO ---
    btn_start = ft.ElevatedButton("ENTRAR v61", bgcolor=COLOR_ACENTO, color="black", weight="bold", height=50, width=200, on_click=iniciar_sistema)
    page.add(
        ft.Column([
            ft.Text("PANEL FINAL", size=30, color="black", weight="bold"),
            ft.Text("100% Seguro + Emojis", color="grey"),
            ft.Container(height=40),
            btn_start
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
    )

ft.app(target=main)
