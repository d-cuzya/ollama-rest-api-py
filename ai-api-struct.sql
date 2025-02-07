-- Создание таблицы REQUESTS
CREATE TABLE REQUESTS (
    uuid UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    request TEXT NOT NULL
);

-- Создание таблицы STATUS
CREATE TABLE STATUS (
    uuid UUID PRIMARY KEY REFERENCES REQUESTS(uuid) ON DELETE CASCADE,  -- Внешний ключ
    status TEXT NOT NULL
);

-- Создание таблицы ANSWERS
CREATE TABLE ANSWERS (
    uuid UUID PRIMARY KEY REFERENCES REQUESTS(uuid) ON DELETE CASCADE,  -- Внешний ключ
    answer TEXT NOT NULL
);