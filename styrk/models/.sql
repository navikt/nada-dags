{{ config(materialized='table') }}

select *
from styrk.styrk_koder
where notes is not null
