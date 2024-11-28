Use ICT_2023_CWC;

CREATE TABLE player(
jersey_number INT PRIMARY KEY ,
name VARCHAR(255),
career_matches INT,
icc_ranking INT,
age INT
);

INSERT INTO player VALUES(18, 'Virat Kohli' , 292, 4, 35);
INSERT INTO player VALUES(45, 'Rohit Sharma' , 262, 2, 37);
INSERT INTO player VALUES(77, 'Shubman Gill' , 47, 3, 24);
INSERT INTO player VALUES(32, 'Ishan Kishan' , 27, 57, 26);
INSERT INTO player VALUES(96, 'Shreyas Iyer' , 62, 16, 29);
INSERT INTO player VALUES(1, 'KL Rahul' , 77, 18, 32);
INSERT INTO player VALUES(63, 'Suryakumar Yadav' , 37, 112, 33);
INSERT INTO player VALUES(8, 'Ravindra Jadeja' , 197, 16, 35);
INSERT INTO player VALUES(99, 'Ravichandran Ashwin' , 116, 237, 37);
INSERT INTO player VALUES(33, 'Hardik Pandya' , 86, 19, 30);
INSERT INTO player VALUES(54, 'Shardul Thakur' , 47, 111, 32);
INSERT INTO player VALUES(23, 'Kuldeep Yadav' , 106, 4, 29);
INSERT INTO player VALUES(93, 'Jasprit Bumrah' , 89, 8, 30);
INSERT INTO player VALUES(11, 'Mohammed Shami' , 101, 12, 34);
INSERT INTO player VALUES(73, 'Mohammed Siraj' , 44, 10, 30);

CREATE TABLE bowler(
    jersey_number INT,
    matches_played INT,
    wickets INT,
    economy FLOAT,
    average FLOAT,
    strike_rate FLOAT,
    FOREIGN KEY (jersey_number) REFERENCES player(jersey_number)
);

INSERT INTO bowler VALUES(93, 11 , 20, 4.06, 18.65, 27.55);
INSERT INTO bowler VALUES(11, 7 , 24, 5.26, 10.7, 12.2);
INSERT INTO bowler VALUES(73, 11 , 14, 5.68, 33.5, 35.35);
INSERT INTO bowler VALUES(23, 11 , 15, 4.45, 28.26, 38.06);
INSERT INTO bowler VALUES(8, 11 , 16, 4.25, 24.87, 35.06);
INSERT INTO bowler VALUES(99, 1 , 1, 3.4, 34.0, 60);
INSERT INTO bowler VALUES(54, 3 , 2, 6, 51, 51);
INSERT INTO bowler VALUES(33, 4 , 5, 6.84, 22.6, 19.8);
INSERT INTO bowler VALUES(18, 1, 1, 4.28, 15, 21);
INSERT INTO bowler VALUES(45, 1 , 1, 8.4, 7, 5);

CREATE TABLE batsman(
    jersey_number INT,
    matches_played INT,
    runs INT,
    highest_score INT,
    average FLOAT,
    strike_rate FLOAT,
    FOREIGN KEY (jersey_number) REFERENCES player(jersey_number)
);

INSERT into batsman VALUES(18, 11, 765, 117, 95.92, 90.31);
INSERT into batsman VALUES(45, 11, 597, 131, 54.27, 125.94);
INSERT into batsman VALUES(96, 11, 530, 128, 66.25, 113.24);
INSERT into batsman VALUES(1, 11, 452, 102, 75.33, 90.76);
INSERT into batsman VALUES(77, 9, 354, 92, 44.25, 106.94);
INSERT into batsman VALUES(8, 11, 120, 39, 40.0, 101.69);
INSERT into batsman VALUES(63, 7, 106, 49, 17.66, 100.95);
INSERT into batsman VALUES(32, 2, 47, 47, 23.5, 97.91);
INSERT into batsman VALUES(23, 11, 19, 10, 19, 61.29);
INSERT into batsman VALUES(93, 11, 18, 16, 9.00, 62.06);
INSERT into batsman VALUES(33, 4, 11, 11, 11, 137.5);
INSERT into batsman VALUES(11, 7, 10, 6, 3.33, 50.00);
INSERT into batsman VALUES(73, 11, 9, 9, 9.00, 112.50);

CREATE TABLE matches(
    opponent VARCHAR(255),
    venue VARCHAR(255),
    match_number INT PRIMARY KEY,
    team_score VARCHAR(255),
    opponent_team_score VARCHAR(255),
	overs_played INT,
    result VARCHAR(255),
    player_of_the_match VARCHAR(255)
);

INSERT INTO matches values('Australia','Chennai',5,'201/4','199/10',90,'Won','KL Rahul');
INSERT INTO matches values('Afghanistan','Delhi',9,'273/2','272/8',85,'Won','Rohit Sharma');
INSERT INTO matches values('Pakistan','Ahmedabad',12,'192/3','191/10',72,'Won','Jasprit Bumrah');
INSERT INTO matches values('Bangladesh','Pune',17,'256/8','261/3',91,'Won','Virat Kohli');
INSERT INTO matches values('New Zealand','Dharamshala',21,'274/6','273/10',98,'Won','Mohammed Shami');
INSERT INTO matches values('England','Lucknow',29,'229/9','129/10',84,'Won','Rohit Sharma');
INSERT INTO matches values('Sri Lanka','Mumbai',33,'357/8','55/10',69,'Won','Mohammed Shami');
INSERT INTO matches values('South Africa','Kolkata',37,'326/5','83/10',77,'Won','Virat Kohli');
INSERT INTO matches values('Netherlands','Bengaluru',45,'410/4','250/10',97,'Won','Shreyas Iyer');
INSERT INTO matches values('New Zealand(Semi Final)','Mumbai',46,'397/4','327/10',98,'Won','Mohammed Shami');
INSERT INTO matches values('Australia(Final)','Ahmeddabd',48,'240/10','241/4',93,'Lost','Travis Head');

CREATE TABLE coach(
    name VARCHAR(255),
    designation VARCHAR(255),
    coach_id INT PRIMARY KEY,
    nationality VARCHAR(255),
    experience VARCHAR(512),
	coaching_period INT
);
INSERT INTO coach values('Rahul Dravid','Head Coach',123,'Indian','Player and Captain of Indian Team',3);
INSERT INTO coach values('Vikram Rathore','Batting Coach',234,'Indian','Player of Indian Team',3);
INSERT INTO coach values('Paras Mhambrey','Bowling Coach',345,'Indian','Player of Indian Team',3);
INSERT INTO coach values('T Dilip','Fielding Coach',456,'Indian','',3);

CREATE VIEW batsmen_stats as
SELECT p.name, b.jersey_number, b.matches_played, b.runs, b.highest_score, b.average, b.strike_rate
FROM batsman as b
NATURAL JOIN player as p;

CREATE VIEW bowler_stats as
SELECT p.name, b.jersey_number, b.matches_played, b.wickets, b.economy, b.average, b.strike_rate
FROM bowler as b
NATURAL JOIN player as p;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL
);

INSERT INTO users (username, password, role) VALUES
('rayyan', 'gosling123', 'admin'),
('shiven', 'shukla123', 'admin'),
('anuj', 'singh123', 'admin');
