create table game(
 game_id int constraint game_id_pk primary key,
 name varchar(200) not null,
 playtime int,
 released date not null,
 updated timestamp not null,
 rating decimal(3,2),
 rating_top decimal(3,2),
 rating_exceptional int,
 rating_recommended int,
 rating_skip int,
 rating_meh int,
 added_by_status_yet int,
 added_by_status_owned int,
 added_by_status_beaten int,
 added_by_status_toplay int,
 added_by_status_dropped int,
 added_by_status_playing int 
);

create table genre(
 genre_id int constraint genre_id_pk primary key,
 genre varchar(200) not null);

create table game_genre(
game_genre_id int constraint game_genre_id_pk primary key,
genre_id int not null,
game_id int not null,
constraint fk_genre_genre_id foreign key (genre_id) references genre(genre_id),
constraint fk_game_game_id foreign key (game_id) references game(game_id)
);