import flet as ft

def main(page: ft.Page):
    # Configuración de máxima compatibilidad
    page.bgcolor = "#121212"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_resizable = False
    
    # Contenido ultra-simple para asegurar el arranque
    contenido = ft.Container(
        content=ft.Column([
            ft.Icon(name="verified_user", color="#00d26a", size=60),
            ft.Text("SISTEMA IMPERIO ACTIVO", size=22, weight="bold"),
            ft.Text("Si ves esto, tu celular es compatible.", color="white70"),
            ft.Divider(height=40, color="white24"),
            ft.ElevatedButton(
                "DESBLOQUEAR RUTINA", 
                on_click=lambda _: print("Acceso concedido")
            )
        ], horizontal_alignment="center"),
        padding=50,
        alignment=ft.alignment.center
    )

    page.add(contenido)
    page.update()

ft.app(target=main)
