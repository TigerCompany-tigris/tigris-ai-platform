create table if not exists word_pool (
    text text not null
);
create unique index i_pool_01 on extend_words(text);
