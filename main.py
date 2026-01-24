import flet as ft
import random

# --- TUS 30 FRASES ---
FRASES = ["Gana la mañana, gana el día.", "La disciplina es libertad.", "Hazlo con miedo, pero hazlo."] # (Restauraremos las 30 luego)

def main(page: ft.Page):
    # Configuración ultra-simple
    page.bgcolor = "#121212"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Interfaz básica de prueba de vida
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Icon(name="stars", color="#00d26a", size=50),
                ft.Text("PANEL IMPERIO: ACTIVO", size=20, weight="bold"),
                ft.Text(random.choice(FRASES), italic=True, color="white70"),
                ft.ElevatedButton("ENTRAR A MI RUTINA", on_click=lambda _: print("Click"))
            ], horizontal_alignment="center"),
            padding=40,
            bgcolor="#1E1E1E",
            border_radius=20
        )
    )
    page.update()

ft.app(target=main)
