# Flask Note Making

## SQL COMMANDS
- create table users(username varchar(50) NOT NULL UNIQUE, password varchar(50) NOT NULL, uuid varchar(50) PRIMARY KEY);
- create table notes(note varchar(500) NOT NULL, uuid varchar(50) NOT NULL, FOREIGN KEY (uuid) REFERENCES users(uuid));