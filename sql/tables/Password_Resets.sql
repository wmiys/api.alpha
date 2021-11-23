CREATE TABLE Password_Resets(
    id CHAR(36) NOT NULL UNIQUE,
    user_email CHAR(254) NOT NULL,
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    new_password CHAR(255),
    updated_on TIMESTAMP,
    PRIMARY KEY (id)
);