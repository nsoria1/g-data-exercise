select
	j.job as id
	, d.department
	, count(distinct h.id) as hired
from hired_employees h
inner join departments d on h.department_id = d.id
inner join jobs j on h.job_id = j.id
where extract('year' from cast(h.datetime as timestamp)) = 2021
group by 1, 2
order by 3 desc
limit 1000;