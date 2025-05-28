from infrastructure.database import get_connection
from domain.aluno import Aluno

class AlunoRepository:
    def adicionar(self, aluno: Aluno):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO aluno (nome, matricula, email, cpf, data_nascimento, turma_id) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (aluno.nome, aluno.matricula, getattr(aluno, 'email', None), getattr(aluno, 'cpf', None), getattr(aluno, 'data_nascimento', None), aluno.turma_id))
        conn.commit()
        cursor.close()
        conn.close()

    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, matricula, email, cpf, data_nascimento, turma_id FROM aluno")
        alunos = []
        for row in cursor.fetchall():
            aluno = Aluno(nome=row[1], matricula=row[2], turma_id=row[6])
            aluno.id = row[0]
            aluno.email = row[3]
            aluno.cpf = row[4]
            aluno.data_nascimento = row[5]
            alunos.append(aluno)
        cursor.close()
        conn.close()
        return alunos

    def remover(self, aluno_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM aluno WHERE id = %s", (aluno_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def atualizar(self, aluno: Aluno):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "UPDATE aluno SET nome=%s, matricula=%s, email=%s, cpf=%s, data_nascimento=%s WHERE id=%s"
        cursor.execute(sql, (aluno.nome, aluno.matricula, getattr(aluno, 'email', None), getattr(aluno, 'cpf', None), getattr(aluno, 'data_nascimento', None), aluno.id))
        conn.commit()
        cursor.close()
        conn.close()