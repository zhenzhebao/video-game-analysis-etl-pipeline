create view game_data as (select g.game_id,name,g.playtime,g.released,date(g.updated) as updated,g.rating,g.rating_top,
g.rating_exceptional,g.rating_recommended,g.rating_skip,g.rating_meh,
g.added_by_status_yet, g.added_by_status_owned,g.added_by_status_beaten,
g.added_by_status_toplay,g.added_by_status_dropped,g.added_by_status_playing,
ge.genre
from game g 
join game_genre gg
on g.game_id=gg.game_id
join genre ge
on gg.genre_id=ge.genre_id);

create view overview as (select count(game_id)as total_game_released,
(select count(distinct genre) 
from game_data
where released between date '2025-01-01' and date'2025-12-31') as total_genres
from game
where released between date '2025-01-01' and date'2025-12-31');

create view game_released_by_month as (select date(date_trunc('month',released)) as month,count(game_id) as number_of_games
from game
where released between date '2025-01-01' and date'2025-12-31'
group by date(date_trunc('month',released)));

/* Game with Highest Average Playtime*/
create view game_highest_playtime as (with t as (select game_id,name,playtime, dense_rank() over(order by playtime desc) as ranking
from game
where released between date '2025-01-01' and date'2025-12-31')
select game_id,name,playtime
from t
where ranking=1);

/* highest rating*/
create view game_highest_rating as (with t as (select game_id,name,rating,dense_rank() over(order by rating desc) as ranking 
from game
where released between date '2025-01-01' and date'2025-12-31')
select game_id,name,rating
from t
where ranking=1);

/*most engaged game*/
create view game_most_engaged as (with t as (select game_id,name,
(coalesce(rating_exceptional,0)+coalesce(rating_recommended,0)+coalesce(rating_skip,0)
+coalesce(rating_meh,0)) as total_rating_responses
from game 
where released between date '2025-01-01' and date'2025-12-31'),
t2 as (select game_id,name,total_rating_responses, dense_rank() over (order by total_rating_responses DESC) as ranking
from t)
select game_id,name,total_rating_responses
from t2
where ranking=1);