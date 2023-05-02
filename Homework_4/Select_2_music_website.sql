-- Количество исполнителей в каждом жанре
SELECT g.name, COUNT(musician_id) count_musicians
FROM genres_of_music gom
JOIN  genre g ON gom.genre_id = g.id
GROUP BY g.name
ORDER BY count_musicians DESC;

-- Количество треков, вошедших в альбомы 2019–2020 годов
SELECT a.name, COUNT(mt.id) count_tracks
FROM music_track mt
JOIN album a ON mt.album_id = a.id
WHERE a.year BETWEEN 2019 AND 2020
GROUP BY a.name
ORDER BY count_tracks DESC;

-- Средняя продолжительность треков по каждому альбому
SELECT a.name, ROUND(AVG(mt.length), 2) avg_length
FROM music_track mt
JOIN album a ON mt.album_id = a.id
GROUP BY a.name
ORDER BY avg_length DESC;

-- Все исполнители, которые не выпустили альбомы в 2020 году
SELECT DISTINCT m.name
FROM musicians_albums ma
JOIN album a ON ma.album_id  = a.id
JOIN musician m ON ma.musician_id = m.id
WHERE a.year NOT IN (2020)
ORDER BY m.name;

--Названия сборников, в которых присутствует конкретный исполнитель
SELECT DISTINCT c.name collection_name
FROM music_track_collection mtc
JOIN music_track mt ON mtc.music_track_id = mt.id
JOIN album a ON mt.album_id = a.id
JOIN musicians_albums ma ON a.id = ma.album_id
JOIN musician m ON ma.musician_id = m.id
JOIN collection c ON mtc.collection_id = c.id
WHERE m.name = 'Ruelle';

-- Названия альбомов, в которых присутствуют исполнители более чем одного жанра
SELECT a.name
FROM musicians_albums ma
JOIN album a ON ma.album_id = a.id
JOIN musician m ON ma.musician_id = m.id
JOIN genres_of_music gom ON m.id = gom.musician_id
JOIN genre g ON gom.genre_id = g.id
GROUP BY a.name, m.name
HAVING COUNT(g.name) > 1;

-- Наименования треков, которые не входят в сборники
SELECT name FROM music_track mt
LEFT JOIN music_track_collection mtc ON mtc.music_track_id = mt.id
WHERE mtc.collection_id IS NULL;

-- Исполнитель или исполнители, написавшие самый короткий по продолжительности трек
SELECT m.name
FROM music_track mt
JOIN musicians_albums ma ON mt.album_id = ma.album_id
JOIN musician m ON ma.musician_id = m.id
WHERE mt.length = (SELECT MIN(mt.length) FROM music_track mt);

-- Названия альбомов, содержащих наименьшее количество треков
SELECT a.name album_name
FROM music_track mt
JOIN album a ON mt.album_id = a.id
GROUP BY a.name
HAVING COUNT(album_id) =
	(SELECT count(album_id) count_album FROM music_track
	 GROUP BY album_id
	 ORDER BY count_album LIMIT 1);
