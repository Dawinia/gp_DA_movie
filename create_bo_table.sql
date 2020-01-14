-- 创建电影票房数据表
create table if not exists boxOffice
(
    movieID         int                       not null comment '电影ID',
    movieName       varchar(32) charset utf8  not null comment '电影名称',
    seatRate        varchar(5)                not null comment '上座率',
    boxInfo         float                     not null comment '综合票房',
    boxRate         varchar(5)                not null comment '票房占比',
    releaseInfo     varchar(10) charset utf8  not null comment '上映时间',
    showInfo        int                       not null comment '排片场次',
    showRate        varchar(5)                not null comment '排片占比',
    splitBoxInfo    float                     not null comment '分账票房',
    splitSumBoxInfo float                     not null comment '总分账票房',
    sumBoxInfo      float                     not null comment '总综合票房',
    showView        smallint                  not null comment '场均人次',
    crawlDate       date                      not null comment '爬取日期',
    constraint boxOffice_movieID_uindex
        unique (movieID)
);

alter table boxOffice
    add primary key (movieID);