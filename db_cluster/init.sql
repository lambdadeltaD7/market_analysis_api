CREATE TABLE IF NOT EXISTS things(
    thing_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    thing_name varchar(64) NOT NULL,
    type varchar(64) NOT NULL
)