-- Create a stored procedure ComputeAverageWeightedScoreForUsers that computes and stores the average weighted score for all students
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE user_id_var INT;
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;

    DECLARE user_cursor CURSOR FOR
        SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN user_cursor;

    user_loop: LOOP

        FETCH user_cursor INTO user_id_var;

        IF done THEN
            LEAVE user_loop;
        END IF;

        SET total_weighted_score = 0;
        SET total_weight = 0;

        SELECT SUM(projects.weight * corrections.score) INTO total_weighted_score
        FROM corrections
        INNER JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id_var;

        SELECT SUM(weight) INTO total_weight
        FROM projects;

        IF total_weight > 0 THEN
            UPDATE users
            SET average_score = total_weighted_score / total_weight
            WHERE id = user_id_var;
        ELSE
            UPDATE users
            SET average_score = 0
            WHERE id = user_id_var;
        END IF;
    END LOOP;

    CLOSE user_cursor;
END //

DELIMITER ;