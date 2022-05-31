# To fetch metadata of all illusts, and save to DB, in order to write Exif metadata.
import os
import sqlite3


def normalize_tags(metadata):
    tags = ""
    if type(metadata["tags"]) is list:
        for i in range(len(metadata["tags"])):
            tag = metadata["tags"][i]['name']
            tags += tag + ","
            tags = tags[:-1]
    else:  # type(metadata["tags"]) is dict
        tag = metadata["tags"]['name']
        tags = tag
    return tags


def normalize_metadata(metadata):
    metadata = {
        "id": metadata["id"],
        "title": metadata["title"],
        "tags": normalize_tags(metadata),
        "type": metadata["type"],
        "caption": metadata["caption"],
        "user_id": metadata["user"]["id"],
        "user_name": metadata["user"]["name"],
        "user_account": metadata["user"]["account"],
        "create_date": metadata["create_date"],
        "x_restrict": metadata["x_restrict"],
        "width": metadata["width"],
        "height": metadata["height"],
        "sanity_level": metadata["sanity_level"],
        "series_id": metadata["series"]["id"] if metadata["series"] else None,
        "series_title": metadata["series"]["title"] if metadata["series"] else None,
    }
    return metadata

# with open("metadata.json", "w", encoding='utf-8') as f:
#     f.write(str(metadata))
#     sys.exit()


def meta_to_db(metadata: dict, db_path):
    # normalize metadata
    metadata = normalize_metadata(metadata)

    # init db if not exists
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS metadata(
                id INTEGER PRIMARY KEY,
                title TEXT,
                tags TEXT,
                type TEXT,
                caption TEXT,
                user_id INTEGER,
                user_name TEXT,
                user_account TEXT,
                create_date TEXT,
                x_restrict INTEGER,
                width INTEGER,
                height INTEGER,
                sanity_level INTEGER,
                series_id INTEGER,
                series_title TEXT
            )
        ''')
        conn.commit()
        conn.close()

    # insert data
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # check if exists
    cur.execute('''
        SELECT id FROM metadata WHERE id = ?
    ''', (metadata["id"],)
    )
    if cur.fetchone() is not None:
        pass
    else:
        cur.execute('''
            INSERT INTO metadata (
                id,
                title,
                tags,
                type,
                caption,
                user_id,
                user_name,
                user_account,
                create_date,
                x_restrict,
                width,
                height,
                sanity_level,
                series_id,
                series_title
            ) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metadata["id"],
            metadata["title"],
            metadata["tags"],
            metadata["type"],
            metadata["caption"],
            metadata["user_id"],
            metadata["user_name"],
            metadata["user_account"],
            metadata["create_date"],
            metadata["x_restrict"],
            metadata["width"],
            metadata["height"],
            metadata["sanity_level"],
            metadata["series_id"],
            metadata["series_title"]
        ))

    # commit
    conn.commit()
    conn.close()
