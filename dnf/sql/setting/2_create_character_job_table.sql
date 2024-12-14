-- sql/2_create_charac_job_table.sql

CREATE TABLE character_job (
    charac_job INT NOT NULL PRIMARY KEY,
    charac_job_name VARCHAR(20) NOT NULL
);

INSERT INTO character_job (charac_job, charac_job_name) VALUES 
    (0, '귀검사(남)'),
    (1, '격투가(여)'),
    (2, '거너(남)'),
    (3, '마법사(여)'),
    (4, '프리스트(남)'),
    (5, '거너(여)'),
    (6, '도적'),
    (7, '격투가(남)'),
    (8, '마법사(남)'),
    (9, '외전'),
    (10, '외전'),
    (11, '귀검사(여)'),
    (12, '나이트'),
    (13, '마창사'),
    (14, '프리스트(여)'),
    (15, '총검사'),
    (16, '아처');