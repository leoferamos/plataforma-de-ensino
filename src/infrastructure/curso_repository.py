from infrastructure.database import get_connection
from domain.curso import Curso

class CursoRepository:
    def adicionar(self, curso: Curso):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO curso (nome, codigo, categoria, grau) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (curso.nome, curso.codigo, curso.categoria, curso.grau))
        conn.commit()
        curso_id = cursor.lastrowid 
        cursor.close()
        conn.close()
        return curso_id

    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, codigo, categoria, grau FROM curso")
        cursos = []
        for row in cursor.fetchall():
            curso = Curso(
                nome=row[1],
                codigo=row[2],
                categoria=row[3],
                grau=row[4],
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
        sql = "UPDATE curso SET nome=%s, codigo=%s, categoria=%s, grau=%s WHERE id=%s"
        cursor.execute(sql, (curso.nome, curso.codigo, curso.categoria, curso.grau, curso.id))
        conn.commit()
        cursor.close()
        conn.close()