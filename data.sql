-- Active: 1673012520730@@127.0.0.1@3306@tasks
CREATE DATABASE IF NOT EXISTS tasks;

USE tasks;

CREATE TABLE tasks (
    id INTEGER NOT NULL AUTO_INCREMENT,
    owner VARCHAR(100),
    title VARCHAR(100),
    status VARCHAR(100),
    PRIMARY KEY(id)
);

SET character_set_client = utf8;
SET character_set_connection = utf8;
SET collation_connection = utf8_general_ci;