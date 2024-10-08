import networkx as nx
import matplotlib
from matplotlib import pyplot as plt, animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg

plt.rcParams["figure.figsize"] = [10, 5]  # pour définir la taille de la figure du plt[marge , hauteur] it creates a 1000×500 pixel figure
plt.rcParams["figure.autolayout"] = True  # pour ajustez la marge intérieure entre et autour des sous-tracés.
fig = plt.figure()  # obtenir la figure courante . an empty figure with no Axes

font1 = {'family': 'serif', 'color': 'darkblue', 'size': 20}
font2 = {'family': 'serif', 'color': 'darkgreen', 'size': 20}

G = nx.Graph()#le graphe entrée
g = nx.Graph()
T = nx.Graph()
R = nx.Graph()
A = nx.Graph()# l'arbre résultat

edge_with_weight = []# création d'une liste vide pour ordonnées les arêtes
file_name = 'graphe.txt'
with open(file_name) as f:
    for a in f:
        column = a.strip().split(' ')# lire les valeurs séparées par des espaces d'une ligne dans une liste "column"
        G.add_edge(int(column[0]), int(column[1]), weight=int(column[2]))
        edge_with_weight.append((int(column[0]), int(column[1]), int(column[2])))  # ajouter les valeurs lues au liste.
f.close()
edge_with_weight.sort(key=lambda item: item[2])  # pour ordonnées les aretes par la valeur du poid "item[2]"
som1 = int(G.size(weight="weight")) # return la somme des poids des arets


def animate(frame):
    fig.clear()  # pour effacer la figure actuelle,pour la maj
    global s  # pour declarer la var s
    global c
    (node1, node2, weightt) = edge_with_weight[frame]
    s += int(weightt)
    c += int(weightt)
    A.add_edge(node1, node2, weight=weightt)
    T.add_edge(node1, node2, weight=weightt)
    if nx.cycle_basis(A) != []:
        A.remove_edge(node1, node2)
        T.remove_edge(node1, node2)
        G.remove_edge(node1, node2)
        R.add_edge(node1, node2, weight=weightt)
        s -= int(weightt)

    subax1 = plt.subplot(121)

    plt.title(f"le graphe à traiter \n\n  Cout={som1}", fontdict=font1)
    pos = nx.circular_layout(G)
    nx.draw_networkx(G, pos, with_labels=True, font_weight='bold', )
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    pos = nx.circular_layout(T)
    nx.draw_networkx(T, pos, with_labels=True, font_weight='bold', edge_color='green')
    labels = nx.get_edge_attributes(T, 'weight')
    nx.draw_networkx_edge_labels(T, pos, edge_labels=labels, font_color='green')

    pos = nx.circular_layout(R)
    nx.draw_networkx(R, pos, with_labels=True, font_weight='bold', edge_color='red')
    labels = nx.get_edge_attributes(R, 'weight')
    nx.draw_networkx_edge_labels(R, pos, edge_labels=labels, font_color='red')

    subax2 = plt.subplot(122)

    plt.title(f"l'arbre couvrant minimum  \n\n Cout={s}", fontdict=font1)
    pos = nx.circular_layout(A)
    nx.draw_networkx(A, pos, with_labels=True, font_weight='bold', edge_color='green')
    labels = nx.get_edge_attributes(A, 'weight')
    nx.draw_networkx_edge_labels(A, pos, edge_labels=labels, font_color='green')


def init_animate():

    subax1 = plt.subplot(121)  # pour spécifier la subplot du travail
    plt.title(f"le graphe à traiter \n\n  Cout={som1}", fontdict=font1)
    pos = nx.circular_layout(G) # pour spécifier la structure du position initiales  des neouds du graphe
    nx.draw_networkx(G, pos, with_labels=True, font_weight='bold')  # pour dessiner le graphe
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)  # pour montrer les valeurs des poids.

    subax2 = plt.subplot(122)
    plt.title(f"l'arbre couvrant minimum  \n\n Cout={0}", fontdict=font1)
    A.add_nodes_from(G)
    pos = nx.circular_layout(A)
    nx.draw_networkx(A, pos, with_labels=True,
                     font_weight='bold')


def animatee(canvas, fig):
    global ani
    if ani is not None:
        ani.pause()  # pour annuler l'annimation s'elle existe
    A.clear()
    A.add_nodes_from(G)
    T.clear()
    T.add_nodes_from(G)
    R.clear()
    R.add_nodes_from(G)

    global s
    s = 0
    global n
    n = 0
    global c
    c = 0

    with open(file_name) as f:
        for line in f:
            colum = line.strip().split(' ')
            G.add_edge(int(colum[0]), int(colum[1]), weight=int(colum[2]))
    f.close()

    ani = animation.FuncAnimation(fig, animate, frames=G.number_of_edges(), init_func=init_animate, interval=vitesse,
                                  repeat=False)
    return draw_figure(canvas, fig)


def sans_animation():
    fig2 = plt.figure()  # pour éviter le problème de la fig avec annimation
    global ani
    if ani is not None:
        ani.pause()
    G.clear()
    with open(file_name) as f:
        for line in f:
            colum = line.strip().split(' ')
            G.add_edge(int(colum[0]), int(colum[1]), weight=int(colum[2]))
    f.close()

    subax1 = plt.subplot(121)

    plt.title(f"le graphe à traiter \n\n Cout={som1}", fontdict=font1)
    pos = nx.circular_layout(G)
    nx.draw_networkx(G, pos, with_labels=True, font_weight='bold', edge_color='darkblue')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='darkblue')

    subax2 = plt.subplot(122)
    A = nx.minimum_spanning_tree(G)
    som = int(A.size(weight="weight"))
    plt.title(f"l'arbre couvrant minimum \n\n Cout={som}", fontdict=font2)
    pos = nx.circular_layout(A)
    nx.draw_networkx(A, pos, with_labels=True, font_weight='bold', edge_color='green')
    labels = nx.get_edge_attributes(A, 'weight')
    nx.draw_networkx_edge_labels(A, pos, edge_labels=labels, font_color='green')
    return draw_figure(canvas2, fig2)


matplotlib.use("TkAgg")


def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


sg.theme('BluePurple')
# Define the window layout
layout0 = [
    [sg.Text("Arbre Couvrant Minimum ", font='italic 50', key='titre')],
    [sg.Image(r'acm22.png', size=(500, 500), key='img')],
    [sg.Button("KRUSKAL")],
    [sg.Button("PRIM")],
    [sg.Button("BORUVKA")]]
layout1 = [
    [sg.Image(r'Kruskal_Algorithmus.png', size=(500, 500), key='img')],
    [sg.Button("animation")],
    [sg.Button("sans animation")],
    [sg.Button("retour", key="retour1")]]
layout2 = [
    [sg.Image(r'Kruskal_Algorithmus.png', size=(500, 400), key='img')],
    [sg.Text("la vitesse d'animation : ", text_color='white', font='italic 20', key='vitesse_label',
             pad=((80, 5), (200, 10))),
     sg.Slider(range=(0, 5000), orientation='h', size=(10, 20), default_value=1000, change_submits=True, key='slider',
               font='Helvetica 20', tooltip="modifier la vitesse",
               text_color='white', pad=((5, 5), (200, 10))),
     sg.Button("ok", pad=((5, 5), (200, 10)))],
    [sg.Button("retour", key="retour2")], ]
layout3 = [
    [sg.Text('KRUSKAL', size=(40, 1), justification='center', font='Helvetica 20')],
    [sg.Canvas(key="-CANVAS-", size=(5, 5))],
    [sg.Button("retour", key="retour3")], ]
layout4 = [
    [sg.Text('KRUSKAL', size=(40, 1), justification='center', font='Helvetica 20')],
    [sg.Canvas(key="-CANVAS2-", size=(5, 5))],
    [sg.Button("retour", key="retour4")], ]

layout = [
    [sg.Column(layout0, key='-COL0-', vertical_alignment='center', element_justification='center'),
     sg.Column(layout1, visible=False, key='-COL1-', vertical_alignment='center', element_justification='center'),
     sg.Column(layout2, visible=False, key='-COL2-', vertical_alignment='center', element_justification='center'),
     sg.Column(layout3, visible=False, key='-COL3-', vertical_alignment='center', element_justification='center'),
     sg.Column(layout4, visible=False, key='-COL4-', vertical_alignment='center', element_justification='center')],
    [sg.Button('Exit')]]

window = sg.Window(
    "ACM",
    layout,
    location=(400, 0),
    finalize=True,  # il faut faire true
    size=(800, 800),
    element_justification="center",
    font="Helvetica 18",
    resizable=True
)

window.maximize()  # pour redimensionner la fenêtre en plein écran
# initialisation des objets
canvas = window["-CANVAS-"].TKCanvas
canvas2 = window["-CANVAS2-"].TKCanvas

fig_agg = None
global ani
ani = None

while True:
    event, values = window.read()
    if event == "KRUSKAL":
        window['-COL0-'].update(visible=False)
        window['-COL1-'].update(visible=True)
        window['-COL2-'].update(visible=False)
        window['-COL3-'].update(visible=False)
        window['-COL4-'].update(visible=False)
    if event == "retour1":
        window['-COL0-'].update(visible=True)
        window['-COL1-'].update(visible=False)
        window['-COL2-'].update(visible=False)
        window['-COL3-'].update(visible=False)
        window['-COL4-'].update(visible=False)
    if event == "animation":
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        window['-COL0-'].update(visible=False)
        window['-COL1-'].update(visible=False)
        window['-COL2-'].update(visible=True)
        window['-COL3-'].update(visible=False)
        window['-COL4-'].update(visible=False)
    if event == "retour2":
        window['-COL0-'].update(visible=False)
        window['-COL1-'].update(visible=True)
        window['-COL2-'].update(visible=False)
        window['-COL3-'].update(visible=False)
        window['-COL4-'].update(visible=False)
    if event == "ok":
        fig.clear()
        fig = plt.figure()
        vitesse = int(values['slider'])
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        window['-COL0-'].update(visible=False)
        window['-COL1-'].update(visible=False)
        window['-COL2-'].update(visible=False)
        window['-COL3-'].update(visible=True)
        window['-COL4-'].update(visible=False)
        fig_agg = animatee(canvas, fig)
    if event == "retour3":
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        window['-COL0-'].update(visible=False)
        window['-COL1-'].update(visible=False)
        window['-COL2-'].update(visible=True)
        window['-COL3-'].update(visible=False)
        window['-COL4-'].update(visible=False)
    if event == "sans animation":
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        window['-COL0-'].update(visible=False)
        window['-COL1-'].update(visible=False)
        window['-COL2-'].update(visible=False)
        window['-COL3-'].update(visible=False)
        window['-COL4-'].update(visible=True)
        fig_agg = sans_animation()
    if event == "retour4":
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        window['-COL0-'].update(visible=False)
        window['-COL1-'].update(visible=True)
        window['-COL2-'].update(visible=False)
        window['-COL3-'].update(visible=False)
        window['-COL4-'].update(visible=False)
    elif (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == sg.WIN_CLOSED or event == 'Exit') and sg.popup_yes_no(
            'Do you really want to exit?') == 'Yes':
        break
window.close()

A = nx.minimum_spanning_tree(G)
