from flet import *
import json
import os
bg = colors.DEEP_PURPLE_500
fwg = '#97b4ff'
fg = colors.DEEP_PURPLE_100
pink = '#eb06ff'
mesObject = {
    'Janeiro': [],
    'Fevereiro':[],
    'Março':[],
    'Abril':[],
    'Maio':[],
    'Junho':[],
    'Julho':[],
    'Agosto':[],
    'Setembro':[],
    'Outubro':[],
    'Novembro':[],
    'Dezembro':[]
}
#Save,Delete e load de dados em JSON
def delete_json(transacao):
    json_transacoes = None
    try:
        with open('Finanças_Com_Flet/transacao.json', 'r', encoding='utf-8') as f:
            json_transacoes = json.load(f)
            if not isinstance(json_transacoes, list):  
                json_transacoes = []
    except json.JSONDecodeError:  # Caso o JSON esteja corrompido ou vazio
        json_transacoes = []
    for i in json_transacoes:
        for k,v in i.items():
            if v == transacao.title.value:
                json_transacoes.remove(i)

    with open('Finanças_Com_Flet/transacao.json', 'w', encoding='utf-8') as f:
        json.dump(json_transacoes, f, indent=4, ensure_ascii=False)
def load_json():
    json_transacoes = None
    try:
        with open('Finanças_Com_Flet/transacao.json', 'r', encoding='utf-8') as f:
            json_transacoes = json.load(f)
            if not isinstance(json_transacoes, list):  
                json_transacoes = []
    except json.JSONDecodeError:  # Caso o JSON esteja corrompido ou vazio
        json_transacoes = []
    for i in json_transacoes:
        valor = None
        nota = None
        icon_name = None
        title = None
        mes = None
        despesa_receita = None
        nomeCategoria = None
        #CriarTransacao(valor,nota,icone,despesa_receita,nomeCategoria)
        for k,v in i.items():
            if k == 'valor':
                valor = v
            if k == 'leading':
                icon_name = icons.SETTINGS
            if k == 'subtitle':
                nota = v
            if k == 'despesa/receita':
                despesa_receita = v
            if k == 'additional_info':
                nomeCategoria = v
            if k == 'mes':
                mes = v
    
        transacao = CriarTransacao(valor,nota,IconButton(icon=icon_name,icon_size=19,icon_color=fg,tooltip=nomeCategoria),despesa_receita,nomeCategoria)
        mesObject[mes].append(transacao)
def add_Json(new_T,mes):
    json_transacoes = None
    transacao = {
        "valor": new_T.valor,
        "leading": new_T.leading.icon.upper(),
        "title": new_T.title.value,
        "subtitle": new_T.subtitle.value,
        "additional_info": new_T.additional_info.value,
        "cor": new_T.cor,
        "mes":mes,
        "despesa/receita":new_T.despesa_receita
    }

    
    try:
        with open('Finanças_Com_Flet/transacao.json', 'r', encoding='utf-8') as f:
            json_transacoes = json.load(f)
            if not isinstance(json_transacoes, list):  
                json_transacoes = []
    except json.JSONDecodeError:  # Caso o JSON esteja corrompido ou vazio
        json_transacoes = []

    json_transacoes.append(transacao)

    with open('Finanças_Com_Flet/transacao.json', 'w', encoding='utf-8') as f:
        json.dump(json_transacoes, f, indent=4, ensure_ascii=False)


class CriarTransacao(CupertinoListTile):
    def __init__(self,valor,nota,icone,despesa_receita,nomeCategoria):
        super().__init__()
        self.despesa_receita = despesa_receita
        self.cor = 'green' if despesa_receita == 0 else 'red'
        self.leading = icone
        self.title = Text(value=valor,color=self.cor)
        self.subtitle = Text(value=nota)
        self.additional_info = Text(value=nomeCategoria)
        self.bgcolor = colors.DEEP_PURPLE_300
        self.valor = -int(valor) if despesa_receita == 1 else +int(valor)
        self.trailing = IconButton(icon=icons.DELETE,icon_size=19,icon_color=fg,tooltip='Deletar', on_click=self.delete)
    def delete(self,e):
        for i in mesObject.values():
            for transacao in i:
                if transacao == self:
                    i.remove(self)
                    delete_json(self)
                    self.load_task_d()
    def load_task_d(self):
        #atualizando UI
        page = self.parent.parent.parent
        container = self.parent
        container.controls.clear()
        mes_atual = self.parent.parent.parent.controls[0].controls[1].value
        if mesObject[mes_atual]: 
            for transacao in mesObject[mes_atual]:
                container.controls.append(transacao)

        #Atualizando SaldoAtual:

        saldo_ui = 0
        
        print(saldo_ui)
        for c,l in mesObject.items():
            if mesObject[c]:
                for i in l:
                    saldo_ui +=  i.valor
        self.parent.parent.parent.controls[1].content.controls[0].controls[1].controls[1].value = saldo_ui
        self.parent.parent.parent.controls[1].content.controls[0].controls[1].controls[1].color = "green" if saldo_ui >= 0 else "red"

        #Atualizando Balanço Mensal:
        balanco_ui = 0
        for c,l in mesObject.items():
            if c == mes_atual:
                for i in l:
                    balanco_ui = balanco_ui + i.valor
        self.parent.parent.parent.controls[1].content.controls[0].controls[3].controls[1].value = balanco_ui
        self.parent.parent.parent.controls[1].content.controls[0].controls[3].controls[1].color = "green" if balanco_ui >= 0 else "red"
        page.update()
                    
class Task(Container):
    def __init__(self):
        super().__init__()
        #Estilo
        self.visible = False
        self.bgcolor = colors.DEEP_PURPLE_500
        self.width = 350
        self.height = 750
        #variavel de controle
        self.icon_selected = None
        #Controls
        self.icons_despesa = Row(
            wrap=True,
            controls=[
                    IconButton(icon=Icons.HOUSE,icon_size=35,icon_color=fg,tooltip='Casa',on_click=lambda e,icon=Icons.HOUSE,tooltip='Casa':self.save_icon(e, icon,tooltip)),
                    IconButton(icon=Icons.ACCESS_TIME_SHARP,icon_size=35,icon_color=fg,tooltip='Períodico',on_click=lambda e,icon=Icons.ACCESS_TIME_SHARP,tooltip='Períodico':self.save_icon(e, icon,tooltip)),
                    IconButton(icon=Icons.ADD_CARD_OUTLINED,icon_size=35,icon_color=fg,tooltip='Cartão',on_click=lambda e,icon=Icons.ADD_CARD_OUTLINED,tooltip='Cartão':self.save_icon(e, icon,tooltip)),
                    IconButton(icon=Icons.SHOPPING_BAG,icon_size=35,icon_color=fg,tooltip='Shopping',on_click=lambda e,icon=Icons.SHOPPING_BAG,tooltip='Shopping':self.save_icon(e, icon,tooltip)),
                    IconButton(icon=Icons.FASTFOOD,icon_size=35,icon_color=fg,tooltip='Comida',on_click=lambda e,icon=Icons.FASTFOOD,tooltip='Comida':self.save_icon(e, icon,tooltip)),
                    IconButton(icon=Icons.KITESURFING,icon_size=35,icon_color=fg,tooltip='Viagem',on_click=lambda e,icon=Icons.KITESURFING,tooltip='Viagem':self.save_icon(e, icon,tooltip)),
                    IconButton(icon=Icons.HEALTH_AND_SAFETY_OUTLINED,icon_size=35,icon_color=fg,tooltip='Saúde',on_click=lambda e,icon=Icons.HEALTH_AND_SAFETY_OUTLINED,tooltip='Saúde':self.save_icon(e, icon,tooltip)),
                    IconButton(icon=Icons.CAR_CRASH,icon_size=35,icon_color=fg,tooltip='Uber',on_click=lambda e,icon=Icons.CAR_CRASH,tooltip='Uber':self.save_icon(e, icon,tooltip)),
                ])
        self.icons_receita = Row(
            wrap=True,
            controls=[
                    IconButton(icon=Icons.HOUSE,icon_size=35,icon_color=fg,tooltip='Casa',on_click=lambda e,icon=Icons.HOUSE,tooltip='Casa':self.save_icon(e, icon,tooltip)),
                    IconButton(icon=Icons.ACCESS_TIME_SHARP,icon_size=35,icon_color=fg,tooltip='Períodico',on_click=lambda e,icon=Icons.ACCESS_TIME_SHARP,tooltip='Períodico':self.save_icon(e, icon,tooltip)),
                    IconButton(icon=Icons.ADD_CARD_OUTLINED,icon_size=35,icon_color=fg,tooltip='Cartão',on_click=lambda e,icon=Icons.ADD_CARD_OUTLINED,tooltip='Cartão':self.save_icon(e, icon,tooltip)),
                    IconButton(icon=Icons.SHOPPING_BAG,icon_size=35,icon_color=fg,tooltip='Shopping',on_click=lambda e,icon=Icons.SHOPPING_BAG,tooltip='Shopping':self.save_icon(e, icon,tooltip)),
                    IconButton(icon=Icons.FASTFOOD,icon_size=35,icon_color=fg,tooltip='Comida',on_click=lambda e,icon=Icons.FASTFOOD,tooltip='Comida':self.save_icon(e, icon,tooltip)),
                    IconButton(icon=Icons.KITESURFING,icon_size=35,icon_color=fg,tooltip='Viagem',on_click=lambda e,icon=Icons.KITESURFING,tooltip='Viagem':self.save_icon(e, icon,tooltip)),
                    IconButton(icon=Icons.HEALTH_AND_SAFETY_OUTLINED,icon_size=35,icon_color=fg,tooltip='Saúde',on_click=lambda e,icon=Icons.HEALTH_AND_SAFETY_OUTLINED,tooltip='Saúde':self.save_icon(e, icon,tooltip)),
                    IconButton(icon=Icons.CAR_CRASH,icon_size=35,icon_color=fg,tooltip='Uber',on_click=lambda e,icon=Icons.CAR_CRASH,tooltip='Uber':self.save_icon(e, icon,tooltip)),
                ])
        self.tab = Tabs(
                    tab_alignment='center',
                    selected_index=1,
                    animation_duration=300,
                    tabs=[
                        Tab(
                            text="Receita",
                            content=Column(
                                controls=[
                                    Container(height=30),
                                    self.icons_receita
                                ]
                            ),
                        ),
                        Tab(
                            tab_content=Text('Desepesa'),
                            content=Column(
                                controls=[
                                    Container(height=30),
                                    self.icons_despesa
                                ]
                            )
                            ),
                    ],
                    expand=1,
                )
        self.content = Stack(
            controls=[
                Container(
                    width=350,
                    padding=padding.only(top=10),
                    content=Column(
                        horizontal_alignment='center',
                        controls=[
                            Text('Adcionar'),
                            Container(
                                height=200,
                                content=self.tab
                            )
                        ]
                    )
                ),
                Container(
                    width=350,
                    height=300,
                    bottom=0,
                    bgcolor=colors.DEEP_PURPLE_500,
                    visible=False,
                    content= Column(
                        horizontal_alignment='center',
                        spacing=10,
                        controls=[
                            TextField(label='0',bgcolor=colors.DEEP_PURPLE_300,border_color=colors.DEEP_PURPLE_100,color=colors.DEEP_PURPLE_500,focused_border_color=colors.DEEP_PURPLE_500,keyboard_type=KeyboardType.NUMBER),
                            TextField(label='Nota: insira uma nota',bgcolor=colors.DEEP_PURPLE_300,border_color=colors.DEEP_PURPLE_100,color=colors.DEEP_PURPLE_500,focused_border_color=colors.DEEP_PURPLE_500,),
                            Row(
                                controls=[
                                    ElevatedButton(text='Salvar',expand=True,bgcolor=colors.DEEP_PURPLE_400,on_click=self.transacao)
                                ]
                            )
                        ]
                    )
                )
            ]
        )
    def transacao(self,e):
        valor = self.content.controls[1].content.controls[0].value
        nota = self.content.controls[1].content.controls[1].value
        icone = self.icon_selected
        despesa_receita = self.tab.selected_index
        nomeCategoria = self.icon_selected.tooltip

        mes = self.parent.controls[0].controls[0].controls[1].value
        if not str(valor).isnumeric():
            self.content.controls[1].content.controls[0].error_text = 'Digite apenas números'
        else:
            self.content.controls[1].content.controls[0].error_text = None
            new_T = CriarTransacao(valor,nota,icone,despesa_receita,nomeCategoria)
            mesObject[mes].append(new_T)
            add_Json(new_T,mes)
        self.content.controls[1].content.controls[0].value = ''
        self.content.controls[1].content.controls[1].value = ''
        self.update()
    def save_icon(self,evt,i,tooltip):
        self.icon_selected = IconButton(icon=i,icon_size=19,icon_color=fg,tooltip=tooltip)
        self.content.controls[1].visible = True if self.content.controls[1].visible == False else False
        self.update()

class Inicio(Container):
    global saldoAtual
    def __init__(self,page):
        super().__init__()
        #Estilização
        self.width = 350
        self.height = 750
        self.bgcolor = colors.DEEP_PURPLE_500
        
        #Variaveis de Controle
        self.page = page
        self.mes = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto', 'Setembro','Outubro','Novembro','Dezembro']
        self.mes_ativo = 0
        self.saldoAtual = 0
        self.BalancoMensal = 0
        #Controles da Página
        self.mes_menu = Row(
            alignment='center',
            spacing=30,
            controls= [IconButton(icon=Icons.ARROW_LEFT,icon_size=20,icon_color='white', on_click= lambda _: self.change_mesAtivo(1)), Text(value=self.mes[self.mes_ativo],size=17),IconButton(icon=Icons.ARROW_RIGHT,icon_size=20,icon_color='white',on_click= lambda _: self.change_mesAtivo(2))]
        )
        self.icon_create_task = IconButton(icon=Icons.ADD, icon_size=20,icon_color='white',bgcolor=colors.DEEP_PURPLE_400,right=20,bottom=150, on_click= self.change_create_task_visible)
        self.create_task = Task()
        self.main_column = Column(
                    visible=True,
                    controls=[
                        self.mes_menu,
                        Container(
                            bgcolor='white',
                            border_radius=border_radius.only(top_left=15,top_right=15),
                            content=Column(
                                controls=[
                                    Row(
                                        spacing=20,
                                        alignment='center',
                                        controls=[
                                            Icon(name=Icons.SHOP,color='#4a203b'),
                                            Column(
                                                spacing=0,
                                                controls= [
                                                    Text('Saldo Atual',color='#4a203b',size=14),
                                                    Text(f'{self.saldoAtual}',size=14, color='green', weight='bold')
                                                ]
                                            ),
                                            Icon(name=Icons.MONEY,color='#4a203b'),
                                            Column(
                                                spacing=0,
                                                controls= [
                                                    Text('Balanço Mensal',color='#4a203b', size=14),
                                                    Text(f'{self.BalancoMensal}',size=14, color='green', weight='bold')
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ),
                        Container(height=480, bgcolor=colors.DEEP_PURPLE_500,content=Column()),
                    ]
                )
        #ContainerPrincipal
        self.content = Stack(
            controls=[
                self.main_column,
                self.create_task,
                self.icon_create_task
            ]
        )
    def change_create_task_visible(self,e):
        self.create_task.visible = True if self.create_task.visible == False else False
        self.main_column.visible = True if self.create_task.visible == False else False
        self.icon_create_task.icon = Icons.ADD if self.icon_create_task.icon == Icons.ARROW_LEFT else Icons.ARROW_LEFT
        self.att_saldoAtual()
        self.att_BalancoMensal()
        self.load_tasks()
    def change_mesAtivo(self,sinal):
        try:
            if sinal == 1:
                self.mes_ativo = self.mes_ativo -1
                self.mes_menu.controls[1].value = self.mes[self.mes_ativo]
            else:
                self.mes_ativo += +1
                self.mes_menu.controls[1].value = self.mes[self.mes_ativo]
        except:
            self.mes_ativo = 0
            self.mes_menu.controls[1].value = self.mes[self.mes_ativo]
        self.att_saldoAtual()
        self.att_BalancoMensal()
        self.load_tasks()
    def load_tasks(self):
        self.main_column.controls[2].content.controls.clear()
        mes_atual = self.mes_menu.controls[1].value 
        if mesObject[mes_atual]: 
            for transacao in mesObject[mes_atual]:
                self.main_column.controls[2].content.controls.append(transacao)
        self.att_saldoAtual()
        self.att_BalancoMensal()
        self.update()
    def att_saldoAtual(self):
        self.saldoAtual = 0
        for c,l in mesObject.items():
            if mesObject[c]:
                for i in l:
                    self.saldoAtual = self.saldoAtual + i.valor
        self.main_column.controls[1].content.controls[0].controls[1].controls[1].value = self.saldoAtual
        self.main_column.controls[1].content.controls[0].controls[1].controls[1].color = "green" if self.saldoAtual >= 0 else "red"
        self.update()
    def att_BalancoMensal(self):
        self.BalancoMensal = 0
        for c,l in mesObject.items():
            if c == self.mes_menu.controls[1].value:
                for i in l:
                    self.BalancoMensal = self.BalancoMensal + i.valor
        self.main_column.controls[1].content.controls[0].controls[3].controls[1].value = self.BalancoMensal
        self.main_column.controls[1].content.controls[0].controls[3].controls[1].color = "green" if self.BalancoMensal >= 0 else "red"

        self.update()
