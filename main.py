import flet as ft
import datetime
import random
import json
import os

# --- COLORES "STEALTH" (Modo Oscuro de Lujo) ---
COLOR_FONDO = "#000000"       # Negro puro
COLOR_TARJETA = "#111111"     # Gris casi negro
COLOR_ACENTO = "#00FF88"      # Verde Neón (Cyberpunk)
COLOR_TEXTO = "#FFFFFF"

# --- 100 FRASES DE PODER ---
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
    "El fracaso es solo la oportunidad de comenzar de nuevo.",
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
    "La mediocridad es una enfermedad.",
    "Haz que suceda.",
    "Sueña en grande, empieza pequeño, actúa ahora.",
    "El éxito no es un accidente.",
    "Sé un solucionador de problemas.",
    "Vende el problema que resuelves.",
    "La consistencia es la clave.",
    "No te compares con nadie más que contigo mismo ayer.",
    "El respeto se gana, no se pide.",
    "Lidera con el ejemplo.",
    "Sé humilde en la victoria.",
    "Nunca es tarde para ser quien podrías haber sido.",
    "El dinero es una herramienta, no un amo.",
    "Libertad financiera es libertad real.",
    "Deja un legado.",
    "Vive como si fueras a morir mañana.",
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

# --- 20 HÁBITOS IMPERIALES (Configuración v58: Texto + Color) ---
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
    # --- ARRANQUE SEGURO (Motor v58) ---
    page.title = "Imperio v66"
    page.bgcolor = "white"
    page.padding = 20
    # Usamos constantes seguras (Strings)
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # Constante matemática para centrar sin errores
    CENTRO_MATEMATICO = ft.Alignment(0, 0)

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
            # 1. Limpieza y Modo Oscuro Profundo
            page.clean()
            page.bgcolor = COLOR_FONDO
            page.vertical_alignment = "start"
            page.padding = 10
            
            # 2. Datos
            db = cargar_db()
            hoy_str = datetime.date.today().strftime("%Y-%m-%d")
            if hoy_str not in db: db[hoy_str] = {}

            # Área de contenido con Scroll simple (v58 style)
            area_contenido = ft.Column(expand=True, scroll="auto")

            # Espacio Notch (La única mejora estructural permitida)
            area_contenido.controls.append(ft.Container(height=35))

            # --- VISTA 1: RUTINA (Estilo v58 pero con colores Premium) ---
            def ver_rutina(e=None):
                area_contenido.controls.clear()
                area_contenido.controls.append(ft.Container(height=35))
                
                completados = sum(1 for h in HABITOS_CONFIG if db.get(hoy_str, {}).get(h, False))
                total = len(HABITOS_CONFIG)
                porcentaje = int((completados / total) * 100) if total > 0 else 0
                
                # Encabezado (Texto Gigante en vez de gráficos complejos)
                area_contenido.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text("MI IMPERIO", size=15, color="grey", weight="bold"),
                            ft.Text(f"{porcentaje}%", size=60, weight="bold", color=COLOR_ACENTO),
                            ft.Text("OBJETIVO DIARIO", size=15, color="white"),
                        ], horizontal_alignment="center"),
                        alignment=CENTRO_MATEMATICO,
                        padding=20
                    )
                )

                # Lista de Hábitos (Estructura v58 Indestructible)
                for nombre, color_code in HABITOS_CONFIG.items():
                    estado = db.get(hoy_str, {}).get(nombre, False)
                    
                    def cambiar(e, n=nombre):
                        db[hoy_str][n] = e.control.value
                        guardar_db(db)
                        ver_rutina()

                    chk = ft.Checkbox(value=estado, active_color=COLOR_ACENTO, fill_color=color_code, on_change=cambiar)
                    
                    # Usamos el contenedor v58 pero con fondo más oscuro para contraste
                    area_contenido.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Container(width=5, height=30, bgcolor=color_code), # Barra lateral fina
                                ft.Text(nombre, color="white", size=15, weight="bold", expand=True),
                                chk
                            ]),
                            bgcolor=COLOR_TARJETA, padding=15, border_radius=8, margin=3
                        )
                    )
                page.update()

            # --- VISTA 2: HISTORIAL (Lista Vertical v58) ---
            def ver_calendario(e=None):
                area_contenido.controls.clear()
                area_contenido.controls.append(ft.Container(height=35))
                
                area_contenido.controls.append(ft.Text("HISTORIAL DE BATALLA", size=20, color="white", weight="bold"))
                area_contenido.controls.append(ft.Divider(color="white24"))
                
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
                                ft.Text(f_str, color="white", weight="bold"),
                                ft.Container(expand=True),
                                ft.Text(f"{pct}%", color=color_pct, weight="bold", size=18)
                            ]),
                            bgcolor=COLOR_TARJETA, padding=20, margin=3, border_radius=8
                        )
                    )
                page.update()

            # --- VISTA 3: MENTOR (Texto Grande) ---
            def ver_frases(e=None):
                area_contenido.controls.clear()
                area_contenido.controls.append(ft.Container(height=35))
                
                frase = random.choice(FRASES_MILLONARIAS)
                
                area_contenido.controls.append(
                    ft.Column([
                        ft.Container(height=20),
                        ft.Text("MENTALIDAD", size=20, color="grey", weight="bold"),
                        ft.Container(
                            content=ft.Text(frase, size=22, color="white", italic=True, text_align="center"),
                            bgcolor=COLOR_TARJETA, padding=40, border_radius=15, margin=20, alignment=CENTRO_MATEMATICO
                        ),
                        ft.ElevatedButton("NUEVA FRASE", on_click=ver_frases, bgcolor=COLOR_ACENTO, color="black")
                    ], horizontal_alignment="center")
                )
                page.update()

            # --- NAVEGACIÓN (Botones v58 pero Negros) ---
            menu_botones = ft.Row(
                [
                    ft.ElevatedButton("RUTINA", on_click=ver_rutina, bgcolor="#222222", color="white", expand=True),
                    ft.ElevatedButton("HISTORIAL", on_click=ver_calendario, bgcolor="#222222", color="white", expand=True),
                    ft.ElevatedButton("MENTOR", on_click=ver_frases, bgcolor="#222222", color="white", expand=True),
                ],
                alignment="spaceEvenly"
            )

            # --- ENSAMBLAJE FINAL ---
            page.add(
                ft.Column([
                    area_contenido,
                    ft.Container(content=menu_botones, padding=10, bgcolor="black")
                ], expand=True)
            )

            ver_rutina()

        except Exception as error_carga:
            page.bgcolor = "black"
            page.clean()
            page.add(ft.Text(f"ERROR: {error_carga}", color="red", size=20))
            page.update()

    # --- PANTALLA INICIO ---
    btn_start = ft.ElevatedButton("ENTRAR AL IMPERIO", bgcolor=COLOR_ACENTO, color="black", weight="bold", on_click=iniciar_sistema)
    
    page.add(
        ft.Text("¡HOLA LEO!", size=30, color="black", weight="bold"),
        ft.Text("Versión v66 (Base v58)", color="grey"),
        ft.Container(height=20),
        btn_start
    )

ft.app(target=main)
