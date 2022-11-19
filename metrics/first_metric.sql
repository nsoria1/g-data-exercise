select
	d.department
	, j.job
	, sum(case when extract(quarter from cast(h.datetime as timestamp)) = 1 then 1 else 0 end) as q1
	, sum(case when extract(quarter from cast(h.datetime as timestamp)) = 2 then 1 else 0 end) as q2
	, sum(case when extract(quarter from cast(h.datetime as timestamp)) = 3 then 1 else 0 end) as q3
	, sum(case when extract(quarter from cast(h.datetime as timestamp)) = 4 then 1 else 0 end) as q4
from hired_employees h
inner join departments d on h.department_id = d.id
inner join jobs j on h.job_id = j.id
where extract('year' from cast(h.datetime as timestamp)) = 2021
group by 1, 2
order by 1, 2
limit 1000;