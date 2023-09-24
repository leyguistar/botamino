drop table if exists discord_guilds ;
drop table if exists discord_verify ;
drop table if exists discord_users ;
create table discord_guilds (chatid varchar(50) primary key, id varchar(20));
create table discord_verify (id varchar(20) primary key, code int, time int, nickname varchar(100) );
create table discord_users (userid varchar(50) primary key, discordid varchar(20));