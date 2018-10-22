create table SPIDER.NEWS
(
  ID      INTEGER generated always as identity,
  URL     VARCHAR(255) not null,
  BATCH   VARCHAR(255),
  CONTENT CLOB(1048576),
  COVER   BLOB( max
),
  HOT VARCHAR (255
),
  KEYWORDS VARCHAR (255
),
  TITLE VARCHAR (255
),
TYPE VARCHAR (255
),
UPDATE VARCHAR(255)
    );

