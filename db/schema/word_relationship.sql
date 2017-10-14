drop table if exists word_relationship;
create table word_relationship (
    source text not null,
    target text not null,
    frequency real not null
);
create unique index i_word_relationship_01 on word_relationship(source);