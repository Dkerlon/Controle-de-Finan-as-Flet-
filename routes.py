from flet import *
from inicio import Inicio

def handle_route(page):
    inicio  = Inicio(page)
    index = ['/','/history','/menu']
    def change_view(e):
        page.go(index[e])
        handle_route(page)
    navBar = NavigationBar(
        bgcolor=colors.DEEP_PURPLE_500,
        indicator_color =colors.DEEP_PURPLE_300,
        selected_index=0,
        destinations=[
            NavigationBarDestination(icon=Icons.HOME, label="Home"),
            NavigationBarDestination(icon=Icons.HISTORY, label="Histórico"),
            NavigationBarDestination(icon=Icons.MENU, label="Menu"),
        ],
        on_change=lambda _: change_view(navBar.selected_index),
    )
    routes = {
        '/': View(
            '/',
            [
                navBar,
                inicio
            ]
        ),
        '/history': View(
            '/',
            [
                navBar,
                Text('EM CONTRUÇÃO')
            ]
        ),
        '/menu': View(
            '/menu',
            [
                navBar,
                Text('EM CONTRUÇÃO')
            ]
        )
    }
    page.views.clear()
    navBar.selected_index = index.index(page.route)
    page.views.append(routes[page.route])
    page.update()
    if page.route == '/':
           inicio.load_tasks() 