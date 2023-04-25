-- Название и год выхода альбомов, вышедших в 2018 году
SELECT a.name, a.year
FROM album AS a
WHERE a.year = 2018;

-- Название и продолжительность самого длительного трека
SELECT mt.name, mt.length
FROM music_track AS mt
WHERE mt.length = (SELECT MAX(mt.length) FROM music_track AS mt);

-- Название треков, продолжительность которых не менее 3,5 минут
SELECT mt.name
FROM music_track AS mt
WHERE mt.length >= 210;

-- Названия сборников, вышедших в период с 2018 по 2020 год включительно
SELECT c.name
FROM collection AS c
WHERE c.year BETWEEN 2018 AND 2020;

-- Исполнители, чьё имя состоит из одного слова
SELECT m.name
FROM  musician AS m
WHERE m.name NOT LIKE '_% _%';

-- Название треков, которые содержат слово «мой» или «my»
SELECT mt.name
FROM music_track AS mt
WHERE LOWER(mt.name) LIKE '%my%' OR LOWER(mt.name) LIKE '%мой%';