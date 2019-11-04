CREATE TABLE Messages (
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    sender_username varchar(255) NOT NULL,
    receiver_username varchar(255) NOT NULL,
    content text NOT NULL,
    post_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (sender_username) REFERENCES Users (username),
    FOREIGN KEY (receiver_username) REFERENCES Users (username)
);