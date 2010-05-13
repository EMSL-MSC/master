CREATE OR REPLACE VIEW node_status AS
 SELECT distinct on(nsl.node_id) nsl.id, nsl.node_id, nsl.status_id, nsl."time" AS last_change, nsl.comment, nsl.user_id
   FROM 
    node_status_log nsl, 
    ( SELECT node_status_log.node_id, max(node_status_log."time") AS "time" FROM node_status_log GROUP BY node_status_log.node_id) mr
  WHERE nsl.node_id = mr.node_id AND nsl."time" = mr."time";

ALTER VIEW node_status RENAME TO node_status_view;
SELECT * INTO node_status FROM node_status_view;
ALTER TABLE node_status OWNER TO master;
ALTER TABLE node_status ADD PRIMARY KEY (node_id);

CREATE LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION node_status_log_insert_tf()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM node_status WHERE node_id = NEW.node_id;
    INSERT INTO node_status
        (id, node_id, status_id, last_change, comment, user_id)
        VALUES
        (NEW.*);
    RETURN NULL;
END;
$$
LANGUAGE plpgsql;
CREATE TRIGGER node_status_log_after_insert_t AFTER INSERT ON node_status_log FOR EACH ROW EXECUTE PROCEDURE node_status_log_insert_tf();
