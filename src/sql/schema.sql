CREATE TABLE IF NOT EXISTS curso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    categoria VARCHAR(50),
    grau VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS professor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    siape VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100),
    cpf VARCHAR(14)
);

CREATE TABLE IF NOT EXISTS curso_professor (
    curso_id INT,
    professor_id INT,
    PRIMARY KEY (curso_id, professor_id),
    FOREIGN KEY (curso_id) REFERENCES curso(id),
    FOREIGN KEY (professor_id) REFERENCES professor(id)
);

CREATE TABLE IF NOT EXISTS turma (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    curso_id INT,
    FOREIGN KEY (curso_id) REFERENCES curso(id)
);

CREATE TABLE IF NOT EXISTS aluno (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    matricula VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100),
    cpf VARCHAR(14),
    data_nascimento DATE,
    turma_id INT,
    FOREIGN KEY (turma_id) REFERENCES turma(id)
);

CREATE TABLE IF NOT EXISTS curso_prerequisito (
    curso_id INT,
    prerequisito_id INT,
    PRIMARY KEY (curso_id, prerequisito_id),
    FOREIGN KEY (curso_id) REFERENCES curso(id),
    FOREIGN KEY (prerequisito_id) REFERENCES curso(id)
);