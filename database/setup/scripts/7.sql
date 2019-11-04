CREATE TABLE Follows (
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    follower_username varchar(255) NOT NULL,
    following_username varchar(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (follower_username) REFERENCES Users (username),
    FOREIGN KEY (following_username) REFERENCES Users (username)
);