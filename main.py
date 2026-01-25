import flet as ft
import datetime
import random
import traceback # Para capturar el detalle técnico del error

def main(page: ft.Page):
    # --- PASO 0: ARRANQUE SEGURO ---
    page.title = "Diagnóstico Imperio"
    page.bgcolor = "white"
    page.scroll = "auto"
    page.padding = 20

    # Lista para mostrar los logs en pantalla
    logs = ft.Column()
    
    def log(mensaje, color="black"):
        logs.controls.append(ft.Text(f"> {mensaje}", color=color, size=14, font_family="monospace"))
        page.update()

    page.add(
        ft.Text("SISTEMA DE DIAGNÓSTICO", size=20, weight="bold", color="red"),
        ft.Text("Si la app falla, toma captura de esto.", size=12, color="grey"),
        ft.Divider(),
        logs
    )

    # --- INICIO DEL TEST ---
    log("1. App iniciada correctamente.", "green")

    try:
        log("2. Importando librerías secundarias...", "blue")
        # Aquí definimos las variables
        COLOR_ACENTO = "#00d26a"
        FRASES = ["Gana la mañana.", "Disciplina es libertad."]
        log("3. Variables definidas.", "green")

        # Botón de arranque
        def intentar_cargar(e):
            log("--- INICIANDO CARGA ---", "blue")
            try:
                log("4. Calculando fecha...", "black")
                hoy = datetime.date.today().strftime("%Y-%m-%d")
                log(f"   Fecha: {hoy}", "green")

                log("5. Probando Client Storage...", "black")
                try:
                    page.client_storage.set("test_diagnostico", "ok")
                    val = page.client_storage.get("test_diagnostico")
                    if val == "ok":
                        log("   Memoria OK.", "green")
                    else:
                        log("   Memoria falló (valor incorrecto).", "red")
                except Exception as ex_mem:
                    log(f"   ERROR MEMORIA: {ex_mem}", "red")

                log("6. Creando interfaz compleja...", "black")
                
                # Intentamos crear un checkbox
                chk = ft.Checkbox(label="Prueba Checkbox", value=True)
                log("   Checkbox creado en memoria.", "green")

                # Intentamos crear un icono
                ico = ft.Icon(name=ft.icons.VERIFIED, color="blue")
                log("   Icono creado en memoria.", "green")

                log("7. Agregando elementos a pantalla...", "black")
                page.add(
                    ft.Container(
                        content=ft.Row([ico, chk]),
                        bgcolor="#eeeeee", padding=10
                    )
                )
                page.update()
                log("8. ¡ÉXITO! Interfaz dibujada.", "green")
                log("YA PUEDES CONFIAR EN EL CÓDIGO.", "green", weight="bold")

            except Exception as e_carga:
                log(f"!!! ERROR CRÍTICO EN CARGA: {e_carga}", "red")
                log(traceback.format_exc(), "red")

        # Botón para detonar el error
        btn = ft.ElevatedButton("EJECUTAR PRUEBA DE FUEGO", on_click=intentar_cargar)
        page.add(ft.Container(height=20), btn)
        log("Esperando clic del usuario...", "blue")

    except Exception as e:
        log(f"ERROR GLOBAL: {e}", "red")

ft.app(target=main)
