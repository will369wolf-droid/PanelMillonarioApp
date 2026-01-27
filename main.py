import flet as ft
import datetime
import json
import os
import time

def main(page: ft.Page):
    # --- SISTEMA DE LOGS (CHIVATO) ---
    # Esto creará una lista de texto en pantalla para ver qué pasa
    lista_logs = ft.ListView(expand=True, spacing=2)
    page.add(lista_logs)

    def log(mensaje):
        # Función que imprime en tu pantalla lo que está pasando
        print(mensaje) # También lo manda a la consola interna
        lista_logs.controls.append(ft.Text(f"> {mensaje}", color="green", font_family="monospace"))
        page.update()
        time.sleep(0.05) # Pequeña pausa para que te dé tiempo a leer si explota

    try:
        log("Iniciando v67 Modo Debug...")
        
        # 1. CONFIGURACIÓN BÁSICA
        log("Paso 1: Configurando página...")
        page.title = "Debug Imperio"
        page.bgcolor = "#000000"
        page.padding = 10
        page.vertical_alignment = "start"
        
        # 2. DEFINICIÓN DE DATOS
        log("Paso 2: Definiendo variables...")
        COLOR_ACENTO = "#00FF88"
        COLOR_TARJETA = "#111111"
        
        HABITOS = [
            "Despertar 5:00 AM", "Tender cama", "Tomar agua", 
            "Ducha fría", "Meditación", "Planificar día", 
            "Desayuno sano", "Leer 20 min", "Ejercicio", 
            "Objetivo Principal", "Trabajo Profundo", "Ads/Marketing",
            "Networking", "Finanzas", "Dormir Temprano"
        ]
        log(f"Datos definidos: {len(HABITOS)} hábitos.")

        # 3. BASE DE DATOS
        log("Paso 3: Intentando cargar DB...")
        db = {}
        if os.path.exists("imperio_data.json"):
            log("Archivo JSON encontrado. Leyendo...")
            with open("imperio_data.json", "r") as f:
                db = json.load(f)
            log("DB cargada correctamente.")
        else:
            log("Archivo JSON no existe. Creando nuevo diccionario.")
        
        hoy_str = datetime.date.today().strftime("%Y-%m-%d")
        if hoy_str not in db: db[hoy_str] = {}

        # 4. CONSTRUCCIÓN DE INTERFAZ
        log("Paso 4: Preparando interfaz gráfica...")
        
        # Botón de reinicio (por si acaso)
        def reiniciar(e):
            page.clean()
            page.add(lista_logs)
            log("Reiniciando...")
            main(page)

        btn_retry = ft.ElevatedButton("REINTENTAR", on_click=reiniciar, bgcolor="red", color="white")
        
        # Contenedor principal
        columna_principal = ft.Column(scroll="auto", expand=True)
        columna_principal.controls.append(ft.Text("PANEL DE CONTROL", size=20, color="white"))
        columna_principal.controls.append(btn_retry)
        
        log("Paso 5: Generando lista de hábitos...")
        for i, habit in enumerate(HABITOS):
            log(f"Renderizando hábito {i+1}: {habit}...")
            
            # ESTA ES LA PRUEBA DE FUEGO: ¿Falla al crear los checkboxes?
            estado = db.get(hoy_str, {}).get(habit, False)
            
            def cambiar_estado(e, h=habit):
                db[hoy_str][h] = e.control.value
                with open("imperio_data.json", "w") as f: json.dump(db, f)
            
            # Usamos un diseño MUY simple para ver si es el diseño lo que falla
            fila = ft.Container(
                content=ft.Row([
                    ft.Text(habit, color="white", size=14, expand=True),
                    ft.Checkbox(value=estado, active_color=COLOR_ACENTO, on_change=cambiar_estado)
                ]),
                bgcolor=COLOR_TARJETA,
                padding=10,
                border_radius=5,
                margin=2
            )
            columna_principal.controls.append(fila)
        
        log("Paso 6: Todo renderizado en memoria. Agregando a página...")
        
        # Limpiamos los logs para mostrar la App, PERO dejamos un rastro
        page.clean()
        page.add(ft.Text("CARGA EXITOSA", color="green"))
        page.add(columna_principal)
        page.update()
        
        print(">>> ÉXITO TOTAL <<<")

    except Exception as e:
        # SI FALLA, ESTO DEBERÍA SALIR EN PANTALLA
        print(f"ERROR FATAL: {e}")
        page.clean() # Limpiamos para que se vea el error
        lista_logs.controls.append(ft.Text(f"❌ ERROR FATAL EN: {e}", color="red", size=20, weight="bold"))
        page.add(lista_logs)
        page.update()

ft.app(target=main)
