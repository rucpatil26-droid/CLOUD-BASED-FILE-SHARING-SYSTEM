
USE cloud_file_sharing;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(100) NOT NULL,
    uploaded_on TIMESTAMP DEFAULT
    CURRENT_TIMESTAMP
);