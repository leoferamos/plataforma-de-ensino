from infrastructure.database import get_connection
from domain.curso import Curso

class CursoRepository:
    def adicionar(self, curso: Curso):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO curso (nome, codigo, categoria) VALUES (%s, %s, %s)"
        cursor.execute(sql, (curso.nome, curso.codigo, curso.categoria))
        conn.commit()
        cursor.close()
        conn.close()

    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, codigo, categoria FROM curso")
        cursos = []
        for row in cursor.fetchall():
            curso = Curso(
                nome=row[1],
                codigo=row[2],
                categoria=row[3],
                id=row[0]
            )
            cursos.append(curso)
        cursor.close()
        conn.close()
        return cursos

    def remover(self, curso_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM curso WHERE id = %s", (curso_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def atualizar(self, curso: Curso):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "UPDATE curso SET nome=%s, codigo=%s, categoria=%s WHERE id=%s"
        cursor.execute(sql, (curso.nome, curso.codigo, curso.categoria, curso.id))
        conn.commit()
        cursor.close()
        conn.close()