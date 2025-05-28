from infrastructure.database import get_connection
from domain.professor import Professor

class ProfessorRepository:
    def adicionar(self, professor: Professor):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO professor (nome, siape, email, cpf) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (professor.nome, professor.siape, getattr(professor, 'email', None), getattr(professor, 'cpf', None)))
        conn.commit()
        professor_id = cursor.lastrowid  # <-- pega o id gerado
        cursor.close()
        conn.close()
        return professor_id

    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, siape, email, cpf FROM professor")
        professores = []
        for row in cursor.fetchall():
            professor = Professor(
                nome=row[1],
                siape=row[2],
                email=row[3],
                cpf=row[4],
                id=row[0]
            )
            professores.append(professor)
        cursor.close()
        conn.close()
        return professores

    def remover(self, professor_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM professor WHERE id = %s", (professor_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def atualizar(self, professor: Professor):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "UPDATE professor SET nome=%s, siape=%s, email=%s, cpf=%s WHERE id=%s"
        cursor.execute(sql, (professor.nome, professor.siape, getattr(professor, 'email', None), getattr(professor, 'cpf', None), professor.id))
        conn.commit()
        cursor.close()
        conn.close()

    def associar_cursos(self, professor_id, cursos_ids):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM curso_professor WHERE professor_id = %s", (professor_id,))
        for curso_id in cursos_ids:
            cursor.execute("INSERT INTO curso_professor (curso_id, professor_id) VALUES (%s, %s)", (curso_id, professor_id))
        conn.commit()
        cursor.close()
        conn.close()

    def get_cursos_ids(self, professor_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT curso_id FROM curso_professor WHERE professor_id = %s", (professor_id,))
        ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return ids