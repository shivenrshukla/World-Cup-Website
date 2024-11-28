Use ICT_2023_CWC;

select * from player;

CREATE VIEW batsmen_stats as
SELECT p.name, b.jersey_number, b.matches_played, b.runs, b.highest_score, b.average, b.strike_rate
FROM batsman as b
NATURAL JOIN player as p;

SELECT * FROM batsmen_stats;

SHOW FULL TABLES WHERE TABLE_TYPE = 'VIEW';

DROP view batsmen_stats;

SELECT * FROM batsmen_stats ORDER BY runs DESC;

CREATE VIEW bowler_stats as
SELECT p.name, b.jersey_number, b.matches_played, b.wickets, b.economy, b.average, b.strike_rate
FROM bowler as b
NATURAL JOIN player as p;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select * from users;

select * from player;
select * from coach;