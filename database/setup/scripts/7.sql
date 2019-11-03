CREATE TABLE Follows (
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    follower_username varchar(255) NOT NULL,
    following_username varchar(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (person1_username) REFERENCES Users (username),
    FOREIGN KEY (person2_username) REFERENCES Users (username)
);