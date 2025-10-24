CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
text text NOT NULL,
time integer NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
email text NOT NULL,
psw text NOT NULL,
time integer NOT NULL
);


INSERT INTO mainmenu (title, url) VALUES ('Главная', '/');
INSERT INTO mainmenu (title, url) VALUES ('Добавить статью', '/add_post');
INSERT INTO mainmenu (title, url) VALUES ('Авторизация', '/login');
INSERT INTO mainmenu (title, url) VALUES ('Выход', '/logout');
INSERT INTO mainmenu (title, url) VALUES ('Регистрация', '/register');