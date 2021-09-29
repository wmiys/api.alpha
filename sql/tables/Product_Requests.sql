CREATE TABLE Product_Requests (
    id INT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    renter_id INT UNSIGNED NOT NULL,
    product_id INT UNSIGNED NOT NULL,
    starts_on DATE NOT NULL,
    ends_on DATE NOT NULL,
    price_full DECIMAL(10,2) UNSIGNED,
    price_half DECIMAL(10,2) UNSIGNED,
    dropoff_location_id INT UNSIGNED NOT NULL,
    status ENUM ('pending', 'accepted', 'denied', 'expired') NOT NULL DEFAULT 'pending',
    responded_on DATE,
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (renter_id) REFERENCES Users (id) ON UPDATE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products (id) ON UPDATE CASCADE,
    FOREIGN KEY (dropoff_location_id) REFERENCES Locations(id) ON UPDATE CASCADE
);
    