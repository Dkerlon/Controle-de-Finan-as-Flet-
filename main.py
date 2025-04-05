from flet import *
from routes import handle_route
from inicio import load_json
def main(page:Page):
    page.window.width = 350
    page.window.height = 750
    page.window.max_width = 350
    page.window.max_height = 750
    page.window.maximizable = False
    page.title = 'Gestor de Finanças'
    load_json()
    page.on_route_change = handle_route(page)
    page.go('/')
app(target=main)