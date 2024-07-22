-- Tabela de projetos
CREATE TABLE projects (
    project_id VARCHAR(10) PRIMARY KEY, -- Formato: número_número
    project_title VARCHAR(255) NOT NULL,
    project_start_date DATE NOT NULL, -- Formato: DD/MM/YYYY
    project_end_date DATE,
    project_leader VARCHAR(255) NOT NULL,
    organisation VARCHAR(255) NOT NULL
);

-- Tabela de pesquisadores
CREATE TABLE researchers (
    project_id VARCHAR(10),
    name VARCHAR(255) NOT NULL,
    organisation VARCHAR(255) NOT NULL,
    project_role VARCHAR(255),
    PRIMARY KEY (project_id, name), -- Chave primária composta
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Tabela de co-contribuidores
CREATE TABLE co_contributors (
    project_id VARCHAR(10),
    name VARCHAR(255) NOT NULL,
    organisation VARCHAR(255) NOT NULL,
    contribution VARCHAR(255),
    PRIMARY KEY (project_id, name), -- Chave primária composta
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Tabela de usuários de pesquisa
CREATE TABLE research_users (
    project_id VARCHAR(10),
    type VARCHAR(255),
    organisation VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);
