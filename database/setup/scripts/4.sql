CREATE TABLE ForumPosts (
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    author_username varchar(255) NOT NULL,
    forum_question_id int UNSIGNED NOT NULL,
    content text NOT NULL,
    time TIMESTAMP NOT NULL CURRENT_TIME,
    PRIMARY KEY (id),
    FOREIGN KEY (forum_question_id) REFERENCES ForumQuestions (id),
    FOREIGN KEY (author_username) REFERENCES Users (username)
);