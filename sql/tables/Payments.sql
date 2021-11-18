CREATE TABLE Payments 
(
    id CHAR(36) NOT NULL UNIQUE,
    product_id INT UNSIGNED NOT NULL,
    renter_id INT UNSIGNED NOT NULL,
    dropoff_location_id INT UNSIGNED NOT NULL,
    starts_on DATE NOT NULL,
    ends_on DATE NOT NULL,
    price_full DECIMAL(10,2) UNSIGNED NOT NULL,
    fee_renter DECIMAL(3,2) NOT NULL DEFAULT '0.00',
    fee_lender DECIMAL(3,2) unsigned NOT NULL DEFAULT '0.00',
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (product_id) REFERENCES Products(id) ON UPDATE CASCADE,
    FOREIGN KEY (renter_id) REFERENCES Users(id) ON UPDATE CASCADE,
    FOREIGN KEY (dropoff_location_id) REFERENCES Locations(id) ON UPDATE CASCADE
);