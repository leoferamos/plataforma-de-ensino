CREATE TABLE curso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    codigo VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE turma (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    curso_id INT NOT NULL,
    FOREIGN KEY (curso_id) REFERENCES curso(id)
);

CREATE TABLE aluno (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    matricula VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100),
    cpf VARCHAR(14),
    data_nascimento DATE
);

CREATE TABLE professor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    siape VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100),
    cpf VARCHAR(14)
);

CREATE TABLE aluno_turma (
    aluno_id INT NOT NULL,
    turma_id INT NOT NULL,
    PRIMARY KEY (aluno_id, turma_id),
    FOREIGN KEY (aluno_id) REFERENCES aluno(id),
    FOREIGN KEY (turma_id) REFERENCES turma(id)
);

CREATE TABLE professor_turma (
    professor_id INT NOT NULL,
    turma_id INT NOT NULL,
    PRIMARY KEY (professor_id, turma_id),
    FOREIGN KEY (professor_id) REFERENCES professor(id),
    FOREIGN KEY (turma_id) REFERENCES turma(id)
);