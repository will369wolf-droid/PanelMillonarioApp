import flet as ft
import datetime
import json
import os
import threading
import time
import calendar
import random

# --- CONFIGURACIÓN ---
DB_FILE = "datos_rutina_v2.json"
COLOR_ACENTO = "#00d26a"  # Verde Dinero
COLOR_FONDO = "#121212"

# --- TUS ARCHIVOS ---
# Nota: Se usa la ruta relativa 'assets/' para asegurar compatibilidad
ARCHIVO_FONDO = "assets/Fondo.mp4"        
ARCHIVO_MOTIVACION = "assets/motivacion.gif" 

# --- FRASES COMPLETAS ---
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

# Configuración Hábito (Iconos actualizados para Flet Moderno)
HABITOS_CONFIG = {
    "⏰ Despertar 5:00–6:00 am": [ft.icons.ALARM, ft.colors.ORANGE],
    "💧 Tomar agua + aseo": [ft.icons.WATER_DROP, ft.colors.BLUE],
    "🎯 Definir objetivo principal": [ft.icons.FLAG, ft.colors.RED_ACCENT],
    "🔍 Investigar productos": [ft.icons.SEARCH, ft.colors.PURPLE_ACCENT],
    "📚 Aprender algo nuevo": [ft.icons.SCHOOL, ft.colors.YELLOW_ACCENT],
    "⚡ Aplicar lo aprendido": [ft.icons.FLASH_ON, ft.colors.AMBER],
    "🏗️ Construir negocio": [ft.icons.BUSINESS, ft.colors.CYAN],
    "📢 Lanzar anuncios": [ft.icons.CAMPAIGN, ft.colors.PINK_ACCENT],
    "🏃 Ejercicio físico": [ft.icons.FITNESS_CENTER, ft.colors.GREEN_ACCENT],
    "💼 Jornada de trabajo": [ft.icons.WORK, ft.colors.BLUE_GREY],
    "📊 Revisar números": [ft.icons.INSERT_CHART, ft.colors.TEAL_ACCENT],
    "🧠 Reflexión diaria": [ft.icons.LIGHTBULB, ft.colors.YELLOW],
    "😴 Dormir temprano": [ft.icons.HOTEL, ft.colors.INDIGO_ACCENT],
}
SOLO_NOMBRES = list(HABITOS_CONFIG.keys())

def main(page: ft.Page):
    page.title = "Panel Millonario V34"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 410
    page.window_height = 850
    page.bgcolor = COLOR_FONDO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- CARGA DE RECURSOS ---
    src_fondo = ARCHIVO_FONDO
    src_motivacion = ARCHIVO_MOTIVACION

    # Fondo de la App (Configurado para Video MP4)
    fondo_app = ft.Video(
        playlist=[ft.VideoMedia(src_fondo)],
        playlist_mode=ft.PlaylistMode.LOOP,
        fill_color="black",
        aspect_ratio=9/16,
        volume=0,
        autoplay=True,
        muted=True,
        opacity=0.3
    )

    # --- ANIMACIÓN DE CHECK ---
    icono_recompensa = ft.Icon(name=ft.icons.CHECK, size=150, color=ft.colors.WHITE)
    contenedor_animacion = ft.Container(
        content=icono_recompensa,
        alignment=ft.alignment.center,
        scale=ft.transform.Scale(0),
        animate_scale=ft.animation.Animation(600, ft.AnimationCurve.ELASTIC_OUT),
        opacity=0,
        animate_opacity=300,
        visible=False,
        top=0, bottom=0, left=0, right=0,
    )

    def lanzar_animacion(icono_nombre, color_efecto):
        icono_recompensa.name = icono_nombre
        icono_recompensa.color = color_efecto
        contenedor_animacion.visible = True
        contenedor_animacion.opacity = 1
        contenedor_animacion.scale = ft.transform.Scale(1.5)
        page.update()
        time.sleep(1.5)
        contenedor_animacion.opacity = 0
        contenedor_animacion.scale = ft.transform.Scale(0)
        page.update()
        time.sleep(0.3)
        contenedor_animacion.visible = False
        page.update()

    # --- BASE DE DATOS ---
    def cargar_datos():
        if not os.path.exists(DB_FILE): return {}
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return {}

    def guardar_datos(data):
        with open(DB_FILE, "w") as f: json.dump(data, f)

    db = cargar_datos()
    hoy_str = datetime.date.today().strftime("%Y-%m-%d")

    if hoy_str not in db:
        db[hoy_str] = {n: False for n in SOLO_NOMBRES}
        guardar_datos(db)
    else:
        for n in SOLO_NOMBRES:
            if n not in db[hoy_str]: db[hoy_str][n] = False
        guardar_datos(db)

    # --- LÓGICA ---
    snack_bar = ft.SnackBar(content=ft.Text(""), bgcolor="#333333")
    page.overlay.append(snack_bar)

    def cambiar_habito(e, nombre_habito):
        db[hoy_str][nombre_habito] = e.control.value
        guardar_datos(db)
        actualizar_rutina()
        if e.control.value:
            config = HABITOS_CONFIG[nombre_habito]
            threading.Thread(target=lanzar_animacion, args=(config[0], config[1]), daemon=True).start()
            snack_bar.content.value = "✅ ¡Disciplina es Libertad!"
            snack_bar.open = True
            page.update()

    # PESTAÑA 1: RUTINA
    progreso_texto = ft.Text("0%", size=45, weight="bold", color=COLOR_ACENTO)
    progreso_ring = ft.ProgressRing(width=180, height=180, stroke_width=15, bgcolor=ft.colors.with_opacity(0.3, "black"), color=COLOR_ACENTO)
    lista_controles = []
    
    for nombre in SOLO_NOMBRES:
        datos = HABITOS_CONFIG[nombre]
        chk = ft.Switch(value=db[hoy_str].get(nombre, False), on_change=lambda e, x=nombre: cambiar_habito(e, x), active_color=datos[1])
        tarjeta = ft.Container(
            content=ft.Row([ft.Icon(datos[0], color=datos[1], size=24), ft.Container(width=10), ft.Text(nombre, size=13, color="white", weight="w500", expand=True), chk]),
            bgcolor=ft.colors.with_opacity(0.6, "black"),
            padding=15, border_radius=12, border=ft.border.all(1, ft.colors.with_opacity(0.3, datos[1])),
            blur=ft.Blur(5, 5, ft.BlurTileMode.MIRROR)
        )
        lista_controles.append(tarjeta)

    vista_rutina = ft.Column([
        ft.Container(height=30),
        ft.Container(content=ft.Stack([progreso_ring, ft.Container(content=progreso_texto, alignment=ft.alignment.center, width=180, height=180)]), alignment=ft.alignment.center),
        ft.Container(height=20),
        ft.Text("MODO IMPERIO: ACTIVADO", size=12, color="white70", text_align="center"),
        ft.Container(height=10),
        ft.Container(content=ft.Column(lista_controles, spacing=10, scroll="auto"), padding=20, expand=True)
    ], expand=True, horizontal_alignment="center")

    def actualizar_rutina():
        total = len(SOLO_NOMBRES)
        completados = sum(1 for h in SOLO_NOMBRES if db[hoy_str].get(h, False))
        ratio = completados / total if total > 0 else 0
        progreso_ring.value = ratio
        progreso_texto.value = f"{int(ratio * 100)}%"
        page.update()

    # PESTAÑA 2: CALENDARIO
    stats_texto_mes = ft.Text("Mes", size=20, weight="bold", color="white")
    stats_anillo_mes = ft.ProgressRing(width=100, height=100, stroke_width=8, color=ft.colors.PURPLE, bgcolor=ft.colors.with_opacity(0.3, "black"))
    stats_porcentaje_mes = ft.Text("0%", size=18, weight="bold")
    grid_calendario = ft.Column(spacing=2, horizontal_alignment="center")
    contenedor_detalles = ft.Container(padding=20, alignment=ft.alignment.center)

    def cargar_calendario():
        grid_calendario.controls.clear()
        hoy = datetime.date.today()
        num_dias = calendar.monthrange(hoy.year, hoy.month)[1]
        stats_texto_mes.value = f"{calendar.month_name[hoy.month]} {hoy.year}"
        
        # Logica Porcentaje
        dias_pasados = hoy.day
        habitos_posibles = dias_pasados * len(SOLO_NOMBRES)
        hechos_totales = 0
        for d in range(1, num_dias + 1):
            f_key = f"{hoy.year}-{hoy.month:02d}-{d:02d}"
            if f_key in db: hechos_totales += sum(1 for v in db[f_key].values() if v)
        
        ratio = hechos_totales / habitos_posibles if habitos_posibles > 0 else 0
        stats_anillo_mes.value = min(ratio, 1.0)
        stats_porcentaje_mes.value = f"{int(min(ratio, 1.0) * 100)}%"

        fila = []
        for dia in range(1, num_dias + 1):
            f_key = f"{hoy.year}-{hoy.month:02d}-{dia:02d}"
            color = ft.colors.with_opacity(0.3, "white")
            if f_key in db:
                h = sum(1 for v in db[f_key].values() if v)
                r = h / len(SOLO_NOMBRES)
                if r == 1.0: color = ft.colors.GREEN_ACCENT_700
                elif r >= 0.5: color = ft.colors.AMBER_600
                elif r > 0: color = ft.colors.RED_900
            
            borde = ft.border.all(2, COLOR_ACENTO) if dia == hoy.day else None
            btn = ft.Container(
                content=ft.Text(str(dia), color="white", weight="bold"),
                width=40, height=40, bgcolor=color, border_radius=5, alignment=ft.alignment.center,
                border=borde, on_click=lambda e, f=f_key: mostrar_detalle(f)
            )
            fila.append(btn)
            if len(fila) == 7 or dia == num_dias:
                grid_calendario.controls.append(ft.Row(fila, alignment=ft.MainAxisAlignment.CENTER))
                fila = []
        mostrar_detalle(hoy_str)
        page.update()

    def mostrar_detalle(fecha):
        datos = db.get(fecha, {})
        col = [ft.Text(f"Reporte: {fecha}", size=16, weight="bold", color="white"), ft.Divider(color="grey")]
        if not datos:
            col.append(ft.Text("Sin datos.", color="grey"))
        else:
            aciertos = [h for h, v in datos.items() if v]
            fallos = [h for h in SOLO_NOMBRES if not datos.get(h, False)]
            if aciertos:
                col.append(ft.Text(f"✅ LOGRADO ({len(aciertos)})", color="green", weight="bold"))
                for h in aciertos: col.append(ft.Text(f" • {h}", size=12, color="white70"))
            if fallos:
                col.append(ft.Text(f"❌ PENDIENTE ({len(fallos)})", color="red", weight="bold"))
                for h in fallos: col.append(ft.Text(f" • {h}", size=12, color="white70"))

        contenedor_detalles.content = ft.Container(
            bgcolor=ft.colors.with_opacity(0.8, "black"), padding=20, border_radius=15,
            content=ft.Column(col, horizontal_alignment="center"),
            border=ft.border.all(1, ft.colors.with_opacity(0.1, "white"))
        )
        page.update()

    vista_calendario = ft.Column([
        ft.Container(height=20),
        ft.Row([ft.Stack([stats_anillo_mes, ft.Container(content=stats_porcentaje_mes, alignment=ft.alignment.center, width=100, height=100)]), ft.Container(width=20), stats_texto_mes], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=20, color="transparent"),
        ft.Container(content=grid_calendario, padding=10, alignment=ft.alignment.center),
        ft.Divider(color="grey"),
        contenedor_detalles
    ], scroll="auto", expand=True, horizontal_alignment="center")

    # PESTAÑA 3: MENTORES
    txt_frase = ft.Text("Toca la imagen.", size=18, text_align="center", color="white", font_family="Consolas")
    tarjeta = ft.Container(
        content=ft.Column([
            ft.Icon(ft.icons.FORMAT_QUOTE, color=COLOR_ACENTO, size=30),
            txt_frase,
            ft.Container(height=10),
            ft.Text("MENTOR VIRTUAL", size=12, color=COLOR_ACENTO, weight="bold")
        ], horizontal_alignment="center"),
        padding=25, bgcolor=ft.colors.with_opacity(0.6, "black"), border_radius=15,
        border=ft.border.all(1, ft.colors.with_opacity(0.5, COLOR_ACENTO)),
        blur=ft.Blur(10, 10, ft.BlurTileMode.MIRROR)
    )

    def cambiar_frase(e):
        txt_frase.value = random.choice(FRASES_MILLONARIAS)
        page.update()

    globo = ft.Container(
        content=ft.Image(src=src_motivacion, width=220, height=220, fit=ft.ImageFit.CONTAIN, gapless_playback=True),
        on_click=cambiar_frase, border_radius=110, padding=10,
        shadow=ft.BoxShadow(blur_radius=40, color=ft.colors.with_opacity(0.4, ft.colors.BLUE))
    )

    vista_frases = ft.Container(
        padding=30, alignment=ft.alignment.center,
        content=ft.Column([
            ft.Text("CONSEJO PROFESIONAL", size=14, color="white70", weight="bold"),
            ft.Container(height=20), globo, ft.Container(height=10),
            ft.Text("NUEVA DOSIS DE REALIDAD", size=12, color=ft.colors.BLUE_200, italic=True),
            ft.Container(height=40), tarjeta
        ], horizontal_alignment="center", alignment=ft.MainAxisAlignment.CENTER)
    )

    # NAVEGACIÓN
    def cambiar_tab(e):
        idx = e.control.selected_index
        layout.controls.clear()
        if idx == 0: layout.controls.append(vista_rutina); actualizar_rutina()
        elif idx == 1: layout.controls.append(vista_calendario); cargar_calendario()
        elif idx == 2: layout.controls.append(vista_frases)
        page.update()

    nav = ft.NavigationBar(
        bgcolor="black", indicator_color=ft.colors.with_opacity(0.2, COLOR_ACENTO), selected_index=0, on_change=cambiar_tab,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.CHECK_CIRCLE, label="Mi Día"),
            ft.NavigationDestination(icon=ft.icons.CALENDAR_MONTH, label="Historial"),
            ft.NavigationDestination(icon=ft.icons.PSYCHOLOGY, label="Mentores")
        ]
    )

    layout = ft.Column([vista_rutina], expand=True)
    page.add(ft.Stack([
        fondo_app,
        ft.Column([layout, nav], expand=True, horizontal_alignment="center"),
        contenedor_animacion
    ], expand=True))
    
    actualizar_rutina()

# Ejecución de la App
ft.app(target=main, assets_dir="assets")
