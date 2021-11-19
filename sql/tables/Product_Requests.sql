CREATE TABLE Product_Requests (
    id CHAR(36) NOT NULL UNIQUE,
    payment_id CHAR(36) NOT NULL,
    session_id CHAR(255) NOT NULL,
    status ENUM('pending','accepted','denied','expired') NOT NULL DEFAULT 'pending',
    responded_on DATETIME DEFAULT NULL,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (payment_id) REFERENCES Payments(id) ON UPDATE CASCADE
);