import flet as ft
import datetime
import json
import os

# --- COLORES ---
COLOR_FONDO = "#121212"
COLOR_TARJETA = "#1E1E1E"
COLOR_ACENTO = "#00d26a" # Verde Éxito

# --- TUS 20 HÁBITOS ---
HABITOS = [
    "⏰ Despertar 5:00 AM", "🛏️ Tender la cama", "💧 Tomar agua", 
    "🚿 Ducha fría", "🧘 Meditación/Orar", "📝 Planificar el día", 
    "🥗 Desayuno nutritivo", "📚 Leer 20 min", "🏃 Ejercicio Pesas", 
    "🎯 Objetivo Principal", "🔍 Investigar Productos", "📢 Revisar Ads", 
    "🧠 Aprender IA", "⚡ Trabajo Profundo", "🤝 Networking", 
    "📊 Revisar Finanzas", "📱 Crear Contenido", "🚫 Cero Azúcar", 
    "💡 Reflexión", "😴 Dormir Temprano"
]

FRASES = [
    "El dolor es temporal, la gloria es eterna.",
    "No busques motivación, busca disciplina.",
    "Hazlo con miedo, pero hazlo.",
    "Tu futuro se crea hoy.",
    "El dinero no duerme."
]

def main(page: ft.Page):
    # --- CONFIGURACIÓN SEGURA (Base v58) ---
    page.title = "Imperio v70"
    page.bgcolor = "white"
    page.padding = 10
    page.vertical_alignment = "start"
    
    # Variable para saber qué día estamos viendo (Hoy por defecto)
    # Usamos una lista para poder modificarla dentro de las funciones
    estado_app = {"fecha_ver": datetime.date.today()}

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
        page.clean()
        page.bgcolor = COLOR_FONDO
        
        db = cargar_db()
        contenido = ft.Column(expand=True, scroll="auto")
        
        # Agregamos espacio para el Notch
        contenido.controls.append(ft.Container(height=35))

        # --- FUNCIÓN: CAMBIAR DÍA ---
        def cambiar_dia(e, fecha_seleccionada):
            estado_app["fecha_ver"] = fecha_seleccionada
            renderizar_interfaz() # Recargamos toda la pantalla

        # --- RENDERIZADOR PRINCIPAL ---
        def renderizar_interfaz():
            # Limpiamos el contenido (excepto el notch)
            del contenido.controls[1:] 
            
            fecha_actual = estado_app["fecha_ver"]
            fecha_str = fecha_actual.strftime("%Y-%m-%d")
            hoy = datetime.date.today()
            
            if fecha_str not in db: db[fecha_str] = {}

            # 1. BARRA DE CALENDARIO (Horizontal)
            # Mostramos los últimos 5 días + Hoy + Mañana (opcional)
            fila_dias = ft.Row(scroll="auto", spacing=10)
            
            for i in range(5, -1, -1):
                f = hoy - datetime.timedelta(days=i)
                es_seleccionado = (f == fecha_actual)
                
                # Datos para el color del día
                f_s = f.strftime("%Y-%m-%d")
                d_data = db.get(f_s, {})
                hechos = sum(1 for h in HABITOS if d_data.get(h, False))
                total = len(HABITOS)
                ratio = hechos / total if total > 0 else 0
                
                color_dia = COLOR_ACENTO if ratio > 0.8 else "#333333"
                if es_seleccionado: color_dia = "white" # Resaltar selección
                
                # Botón de Día
                btn_dia = ft.Container(
                    content=ft.Column([
                        ft.Text(f.strftime("%a")[:2], size=10, color="black" if es_seleccionado else "grey"),
                        ft.Text(str(f.day), size=14, weight="bold", color="black" if es_seleccionado else "white")
                    ], alignment="center", spacing=2),
                    width=45, height=55,
                    bgcolor=color_dia,
                    border_radius=10,
                    on_click=lambda e, f=f: cambiar_dia(e, f) # Magia para cambiar fecha
                )
                fila_dias.controls.append(btn_dia)

            contenido.controls.append(
                ft.Container(content=fila_dias, padding=10, height=80)
            )

            # 2. ENCABEZADO DEL DÍA
            # Calculamos progreso del día seleccionado
            completados = sum(1 for h in HABITOS if db.get(fecha_str, {}).get(h, False))
            porcentaje = int((completados / len(HABITOS)) * 100)
            
            titulo_dia = "HOY" if fecha_actual == hoy else fecha_str
            
            contenido.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"RUTINA: {titulo_dia}", size=14, color="grey", weight="bold"),
                        ft.Row([
                            ft.Text(f"{porcentaje}%", size=40, weight="bold", color=COLOR_ACENTO),
                            ft.Icon(name="bolt", color=COLOR_ACENTO)
                        ], alignment="center")
                    ], horizontal_alignment="center"),
                    padding=10,
                    alignment=ft.alignment.center
                )
            )

            # 3. LISTA DE HÁBITOS (CON SWITCHES)
            for habit in HABITOS:
                estado = db.get(fecha_str, {}).get(habit, False)
                
                def switch_changed(e, h=habit):
                    db[fecha_str][h] = e.control.value
                    guardar_db(db)
                    # Actualizamos solo el texto de porcentaje para no recargar todo (más rápido)
                    # O recargamos todo para seguridad:
                    renderizar_interfaz()

                # Switch Moderno
                switch = ft.Switch(
                    value=estado,
                    active_color=COLOR_ACENTO,
                    active_track_color="white",
                    on_change=switch_changed
                )
                
                # Tarjeta
                tarjeta = ft.Container(
                    content=ft.Row([
                        ft.Text(habit, color="white", size=15, expand=True),
                        switch
                    ], alignment="spaceBetween"),
                    bgcolor=COLOR_TARJETA,
                    padding=10,
                    border_radius=10,
                    margin=ft.margin.only(left=10, right=10, bottom=5)
                )
                contenido.controls.append(tarjeta)
            
            page.update()

        # Inicio
        renderizar_interfaz()
        page.add(contenido)

    # --- PANTALLA INICIO ---
    btn_start = ft.ElevatedButton("ENTRAR v70", bgcolor=COLOR_ACENTO, color="black", on_click=iniciar_sistema)
    page.add(ft.Text("IMPERIO", size=30, color="black"), btn_start)

ft.app(target=main)
