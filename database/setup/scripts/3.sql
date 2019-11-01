CREATE TABLE ForumQuestions (
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    author_username varchar(255) NOT NULL,
    content TEXT NOT NULL,
    post_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (author_username) REFERENCES Users (username)
);