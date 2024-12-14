CREATE VIEW character_job_view AS
SELECT 
    cj.charac_job,
    cjg.grow_type,
    CONCAT(cj.charac_job, '_', cjg.grow_type) as charac_code,
    cj.charac_job_name,
    cjg.charac_job_grow_name
FROM character_job cj
JOIN character_job_grow cjg ON cj.charac_job = cjg.charac_job
ORDER BY cj.`charac_job`, cjg.`grow_type`;