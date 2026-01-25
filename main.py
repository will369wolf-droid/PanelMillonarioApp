import flet as ft

def main(page: ft.Page):
    # Configuración mínima: Fondo blanco, texto negro
    page.title = "Prueba de Vida"
    page.bgcolor = "white" 
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Solo texto gigante, nada de iconos ni lógica compleja
    page.add(
        ft.Text("¡HOLA LEO!", size=40, color="black", weight="bold"),
        ft.Text("Si ves esto, funciona.", size=20, color="blue"),
        ft.ElevatedButton("TOCAR AQUÍ", on_click=lambda _: print("Vivo"))
    )

ft.app(target=main)
