CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
text text NOT NULL,
url text NOT NULL,
image BLOB DEFAULT NULL,
user_id integer NOT NULL,
time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
username text NOT NULL,
email text NOT NULL,
psw text NOT NULL,
avatar BLOB DEFAULT NULL,
time integer NOT NULL
);