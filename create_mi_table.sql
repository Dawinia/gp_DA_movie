-- 创建电影信息数据表
create table if not exists movieInfo
(
    dbMovieID       int                       not null comment '豆瓣电影ID',
    tppMovieID      int                       not null comment '淘票票电影ID',
    movieName       varchar(32) charset utf8  not null comment '电影名称',
    directors       varchar(64) charset utf8  not null comment '导演',
    writers         varchar(128)charset utf8  not null comment '编剧',
    actors          varchar(128)charset utf8  not null comment '演员',
    genre           varchar(32) charset utf8  not null comment '类型',
    area            varchar(32) charset utf8  not null comment '地区',
    rateCount       int                       not null comment '评分人数',
    doubanRate      float                     not null comment '豆瓣评分',
    duration        smallint                  not null comment '影片时长',
    publishedDate   date                      not null comment '上映日期',
    constraint movieInfo_dbMocieID_uindex
        unique (dbMovieID)
);

alter table movieInfo
    add primary key (dbMovieID);