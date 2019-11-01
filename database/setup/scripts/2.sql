CREATE TABLE Users (
    username varchar(20) NOT NULL,
    password varchar(20) NOT NULL,
    first_name varchar(20) NOT NULL,
    last_name varchar(20) NOT NULL,
    email varchar(50) NOT NULL,
    school varchar(50),
    school_grade varchar(10),
    state varchar(20),
    role varchar(20) NOT NULL,
    PRIMARY KEY (username)
);