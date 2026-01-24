import flet as ft

def main(page: ft.Page):
    # Configuración de máxima estabilidad
    page.bgcolor = "#121212"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 40
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Si ves esto, habremos roto el ciclo de la pantalla negra
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Icon(name="verified", color="#00d26a", size=80),
                ft.Text("CONEXIÓN ESTABLECIDA", size=24, weight="bold"),
                ft.Text("El sistema Imperio está listo para cargar.", color="white70", text_align="center"),
                ft.Divider(height=40, color="white24"),
                ft.ElevatedButton(
                    "INICIAR MI CAMINO", 
                    on_click=lambda _: print("Arrancando..."),
                    style=ft.ButtonStyle(color="white", bgcolor="#00d26a")
                )
            ], horizontal_alignment="center"),
            bgcolor="#1E1E1E",
            padding=30,
            border_radius=20,
            border=ft.border.all(2, "#00d26a")
        )
    )
    page.update()

ft.app(target=main)
