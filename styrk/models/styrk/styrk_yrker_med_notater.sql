{{ config(materialized='table') }}

select *
from dbt_demo.styrk_s3
where notes is not NULL
