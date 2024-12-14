-- sql/1_create_server_table.sql

CREATE TABLE server (
    server_no INT NOT NULL PRIMARY KEY,
    server_name VARCHAR(20) NOT NULL,
    server_name_kor VARCHAR(20) NOT NULL
);

INSERT INTO server (server_name, server_name_kor, server_no) VALUES 
    ('cain', '카인', 1),
    ('diregie', '디레지에', 2),
    ('siroco', '시로코', 3),
    ('prey', '프레이', 4),
    ('casillas', '카시야스', 5),
    ('hilder', '힐더', 6),
    ('anton', '안톤', 9),
    ('bakal', '바칼', 11);