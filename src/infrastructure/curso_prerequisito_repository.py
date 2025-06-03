from infrastructure.database import get_connection

class CursoPrerequisitoRepository:
    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT curso_id, prerequisito_id FROM curso_prerequisito")
        prereqs = cursor.fetchall()
        cursor.close()
        conn.close()
        return prereqs

    def adicionar(self, curso_id, prerequisito_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO curso_prerequisito (curso_id, prerequisito_id) VALUES (%s, %s)",
            (curso_id, prerequisito_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def remover_todos(self, curso_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM curso_prerequisito WHERE curso_id = %s", (curso_id,))
        conn.commit()
        cursor.close()
        conn.close()