CREATE TABLE Messages (
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    sender_username varchar(255) NOT NULL,
    receiver_username varchar(255) NOT NULL,
    content text NOT NULL,
    time TIMESTAMP NOT NULL CURRENT_TIME,
    PRIMARY KEY (id),
    FOREIGN KEY (sender_username) REFERENCES Users (username),
    FOREIGN KEY (receiver_username) REFERENCES Users (username)
);