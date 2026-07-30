CREATE TABLE IF NOT EXISTS users(
    user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_name varchar(64) NOT NULL,
    user_age INT NOT NULL,
    bought_premium BOOLEAN
);

CREATE TABLE IF NOT EXISTS things(
    thing_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category varchar(64) NOT NULL, 
    price NUMERIC
);

CREATE TABLE IF NOT EXISTS sales(
    sale_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT,
    thing_id INT,
    count INT,
    payment_type varchar(64)
);
