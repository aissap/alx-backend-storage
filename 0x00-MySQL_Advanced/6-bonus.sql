-- Create a stored procedure AddBonus that adds a new correction for a student
DELIMITER //
CREATE PROCEDURE AddBonus(
    IN p_user_id INT,
    IN p_project_name VARCHAR(255),
    IN p_score INT
)
BEGIN
     IF NOT EXISTS(SELECT name FROM projects WHERE name = p_project_name) THEN
        INSERT INTO projects (name) VALUES (p_project_name);
    END IF;

    INSERT INTO corrections (user_id, project_id, score)
    VALUES (p_user_id, (SELECT id FROM projects WHERE name = p_project_name), p_score);
END //
DELIMITER ;