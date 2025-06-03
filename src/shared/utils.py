class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

def montar_arvore_curso_turmas(cursos, turmas):
    """
    Monta uma árvore onde cada curso é raiz e suas turmas são filhos.
    Retorna uma lista de TreeNode.
    """
    raiz = []
    for curso in cursos:
        curso_node = TreeNode(f"{curso.nome} (ID: {curso.id})")
        for turma in turmas:
            if turma.curso_id == curso.id:
                curso_node.children.append(TreeNode(f"{turma.nome} (ID: {turma.id})"))
        raiz.append(curso_node)
    return raiz

def gerar_texto_arvore(arvore):
    def print_arvore_text(nodes, nivel=0):
        texto = ""
        for node in nodes:
            texto += "  " * nivel + f"- {node.value}\n"
            texto += print_arvore_text(node.children, nivel + 1)
        return texto
    return print_arvore_text(arvore)

def matriz_adjacencias(cursos, prerequisitos):
    """
    cursos: lista de objetos Curso
    prerequisitos: lista de tuplas (id_curso_origem, id_curso_destino)
    """
    ids = [curso.id for curso in cursos]
    n = len(ids)
    matriz = [[0]*n for _ in range(n)]
    id_to_idx = {cid: idx for idx, cid in enumerate(ids)}
    for origem, destino in prerequisitos:
        i = id_to_idx.get(origem)
        j = id_to_idx.get(destino)
        if i is not None and j is not None:
            matriz[i][j] = 1
    return matriz

def gerar_texto_matriz(matriz, cursos):
    nomes = [curso.nome for curso in cursos]
    texto = "     " + "  ".join(f"{n[:4]}" for n in nomes) + "\n"
    for i, row in enumerate(matriz):
        texto += f"{nomes[i][:4]}: " + "  ".join(str(x) for x in row) + "\n"
    return texto

def gerar_grafo_cursos(cursos, prerequisitos, img_path="grafo_cursos.png"):
    import networkx as nx
    import matplotlib.pyplot as plt
    G = nx.DiGraph()
    for curso in cursos:
        G.add_node(curso.nome)
    for origem, destino in prerequisitos:
        nome_origem = next((c.nome for c in cursos if c.id == origem), None)
        nome_destino = next((c.nome for c in cursos if c.id == destino), None)
        if nome_origem and nome_destino:
            G.add_edge(nome_origem, nome_destino)
    plt.figure(figsize=(5,3))
    nx.draw(G, with_labels=True, node_color='lightblue', arrows=True)
    plt.savefig(img_path)
    plt.close()