{{ config(materialized='table') }}

select *
from styrk.styrk_koder
where parentCode = 2
