CREATE TABLE Users (
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    school varchar(255),
    school_grade varchar(255),
    state varchar(255),
    role varchar(255) NOT NULL,
    PRIMARY KEY (username)
);