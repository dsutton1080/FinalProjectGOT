CREATE TABLE Users (
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    school varchar(255),
    school_grade ENUM('freshman', 'sophomore', 'junior', 'senior') NOT NULL,
    state varchar(255) NOT NULL,
    role ENUM('highschool', 'college') NOT NULL,
    PRIMARY KEY (username)
);