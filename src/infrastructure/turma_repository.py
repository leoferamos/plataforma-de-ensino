from infrastructure.database import get_connection
from domain.turma import Turma

class TurmaRepository:
    def adicionar(self, turma: Turma):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO turma (nome, codigo, curso_id) VALUES (%s, %s, %s)"
        cursor.execute(sql, (turma.nome, turma.codigo, getattr(turma, 'curso_id', None)))
        conn.commit()
        cursor.close()
        conn.close()

    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, codigo, curso_id FROM turma")
        turmas = []
        for row in cursor.fetchall():
            turma = Turma(
                nome=row[1],
                codigo=row[2],
                curso_id=row[3],
                id=row[0]
            )
            turmas.append(turma)
        cursor.close()
        conn.close()
        return turmas

    def remover(self, turma_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM turma WHERE id = %s", (turma_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def atualizar(self, turma: Turma):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "UPDATE turma SET nome=%s, codigo=%s, curso_id=%s WHERE id=%s"
        cursor.execute(sql, (turma.nome, turma.codigo, getattr(turma, 'curso_id', None), turma.id))
        conn.commit()
        cursor.close()
        conn.close()