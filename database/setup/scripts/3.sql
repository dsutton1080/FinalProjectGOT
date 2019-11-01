CREATE TABLE ForumQuestions (
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    author_username varchar(20) NOT NULL,
    content TEXT NOT NULL,
    time TIMESTAMP NOT NULL CURRENT_TIME,
    PRIMARY KEY (id),
    FOREIGN KEY (author_username) REFERENCES Users
);