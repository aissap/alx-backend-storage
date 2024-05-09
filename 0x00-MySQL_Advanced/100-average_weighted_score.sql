-- Create a stored procedure ComputeAverageWeightedScoreForUser that computes and stores the average weighted score for a student
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;

    SELECT SUM(projects.weight * corrections.score) INTO total_weighted_score
    FROM corrections
    INNER JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = p_user_id;

    SELECT SUM(weight) INTO total_weight
    FROM projects;

    IF total_weight > 0 THEN
        UPDATE users
        SET average_score = total_weighted_score / total_weight
        WHERE id = p_user_id;
    ELSE
        UPDATE users
        SET average_score = 0
        WHERE id = p_user_id;
    END IF;
END //

DELIMITER ;