create table if not exists extend_words (
    real_text text not null,
    text text not null
);
create unique index i_extend_01 on extend_words(real_text, text);

create table if not exists reduce_words (
    text text not null
);
create unique index i_reduce_01 on reduce_words(text);