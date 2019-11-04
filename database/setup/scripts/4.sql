CREATE TABLE ForumPosts (
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    author_username varchar(255) NOT NULL,
    forum_question_id int UNSIGNED NOT NULL,
    content text NOT NULL,
    post_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (forum_question_id) REFERENCES ForumQuestions (id),
    FOREIGN KEY (author_username) REFERENCES Users (username)
);