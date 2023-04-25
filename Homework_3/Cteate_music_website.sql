CREATE TABLE IF NOT EXISTS genre (
	id SERIAL PRIMARY KEY,
	name VARCHAR(40) DISTINCT NOT NULL
	);

CREATE TABLE IF NOT EXISTS musician (
	id SERIAL PRIMARY KEY,
	name VARCHAR(50) NOT NULL
	);

CREATE TABLE IF NOT EXISTS genres_of_music (
	genre_id       INTEGER    REFERENCES   genre(id),
	musician_id    INTEGER    REFERENCES   musician(id),
	PRIMARY KEY(genre_id, musician_id)
	);

CREATE TABLE IF NOT EXISTS album (
	id SERIAL PRIMARY KEY,
	name    VARCHAR(50)    NOT NULL,
	year    INTEGER        NOT NULL
	        CONSTRAINT year_range
                CHECK(year BETWEEN 1600 AND 2023)

	);

CREATE TABLE IF NOT EXISTS musicians_albums (
	musician_id    INTEGER    REFERENCES   musician(id),
	album_id       INTEGER    REFERENCES   album(id),
	PRIMARY KEY(musician_id, album_id)
	);

CREATE TABLE IF NOT EXISTS music_track (
	id SERIAL PRIMARY KEY,
	name     VARCHAR(50)   NOT NULL,
	length   INTEGER       NOT NULL,
	album_id INTEGER       NOT NULL    REFERENCES album(id)
	);

CREATE TABLE IF NOT EXISTS collection (
	id SERIAL PRIMARY KEY,
	name    VARCHAR(50)    NOT NULL,
	year    INTEGER        NOT NULL
	        CONSTRAINT collection_range
                CHECK(collection BETWEEN 1600 AND 2023)
	);

CREATE TABLE IF NOT EXISTS music_track_collection (
	music_track_id    INTEGER    REFERENCES    music_track(id),
	collection_id     INTEGER    REFERENCES    collection(id),
	PRIMARY KEY(music_track_id, collection_id)
	);
