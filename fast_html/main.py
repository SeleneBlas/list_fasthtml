from fasthtml.common import *

def render(lista):
    lista_id = f'lista-{lista.id}' 
    delete = A('🗑️ ', hx_delete=f'/{lista.id}', hx_swap='outerHTML', target_id=lista_id, style="text-decoration: none;")
    edit = AX('✏️', f'/edit/{lista.id}', target_id=lista_id, style="text-decoration: none;")
    checkbox = CheckboxX(checked=lista.done, hx_get=f'/toggle/{lista.id}', hx_swap='outerHTML', target_id=lista_id, style="cursor: pointer;")
    title_style = "text-decoration: line-through;" if lista.done else "" 
    return Li(delete, Span(lista.title, style=title_style), checkbox, edit, id=lista_id)

app, rt, listac, Lista = fast_app('listac.db', live=True, render=render, id=int, title=str, done=bool, pk='id')


@rt('/', methods=['GET'])
def get(): 
    frm = Form(Group(Input(placeholder="Ingresa valores", name='title'), Button("Añadir")), 
               hx_post='/', target_id='lista-items', hx_swap='beforeend')

    items = [render(lista) for lista in listac()]
    
    return Div(
        Titled('Lista de compras', Img(src="carrito.png", style="width:30px; height:30px; margin-bottom: 5px;"), 
        style="display:flex; align-items: center; justify-content: space-between; margin-top:15px; margin-bottom:5px;")
    ), Div(
        Card(
            Div(Ul(*items, id='lista-items')), 
            header=frm
        )
    )

@rt('/', methods=['POST'])
def post(lista: Lista): 
    listac.insert(lista)  
    return render(lista)  


@rt('/{lista_id}', methods=['DELETE'])
def delete(lista_id: int): 
    listac.delete(lista_id) 
    return "" 

@rt('/edit/{id}')
def get_edit(id: int):
    lista = listac.get(id)
    form = Form(Group(Input(name="title", value=lista.title), Button("Guardar")),
               Hidden(name="id", value=lista.id),
               hx_put=f"/{id}", target_id=f'lista-{id}')
    return fill_form(form, lista)

@rt('/{id}', methods=['PUT'])
def update(id: int, lista: Lista):
    listac.update(lista)
    return render(lista)

@rt('/toggle/{lista_id}')
def toggle(lista_id: int):
    lista = listac[lista_id]
    lista.done = not lista.done 
    listac.update(lista) 

    return render(lista) 

serve()
