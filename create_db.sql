
USE pateint_db;

CREATE TABLE IF NOT EXISTS predicts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT NOT NULL,
            gender VARCHAR(10) NOT NULL,
            contact VARCHAR(20) NOT NULL UNIQUE,
            diagnosis_condition VARCHAR(255) NOT NULL,
            image LONGBLOB
        )

select * from predicts;