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

def print_arvore(nodes, nivel=0):
    for node in nodes:
        print("  " * nivel + f"- {node.value}")
        print_arvore(node.children, nivel + 1)

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

def print_matriz(matriz, cursos):
    nomes = [curso.nome for curso in cursos]
    print("Matriz de Adjacências:")
    print("     " + "  ".join(f"{n[:4]}" for n in nomes))
    for i, row in enumerate(matriz):
        print(f"{nomes[i][:4]}: " + "  ".join(str(x) for x in row))