from django.db import connections
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

def create_tables():
    # 'mysql' 데이터베이스 연결 사용
    with connections['mysql'].cursor() as cursor:
        print("Using database: hisubtory_db (MySQL)")
        
        # Create webtoons
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS webtoons (
            webtoon_id BIGINT AUTO_INCREMENT PRIMARY KEY,
            station_id BIGINT NOT NULL,
            title VARCHAR(200) NOT NULL,
            author VARCHAR(100),
            thumbnail VARCHAR(100),
            summary TEXT,
            created_at DATETIME(6) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        
        # Create episodes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS episodes (
            episode_id BIGINT AUTO_INCREMENT PRIMARY KEY,
            webtoon_id BIGINT NOT NULL,
            episode_num INT NOT NULL,
            subtitle VARCHAR(255) NOT NULL,
            history_summary TEXT NOT NULL,
            is_published BOOLEAN DEFAULT TRUE,
            published_at DATETIME(6),
            source_url VARCHAR(200),
            created_at DATETIME(6) NOT NULL,
            CONSTRAINT fk_episodes_webtoon FOREIGN KEY (webtoon_id) REFERENCES webtoons(webtoon_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        
        # Create cuts
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cuts (
            cut_id BIGINT AUTO_INCREMENT PRIMARY KEY,
            episode_id BIGINT NOT NULL,
            image VARCHAR(255) NOT NULL,
            caption TEXT,
            cut_order SMALLINT NOT NULL,
            created_at DATETIME(6) NOT NULL,
            CONSTRAINT fk_cuts_episode FOREIGN KEY (episode_id) REFERENCES episodes(episode_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        
        # Create stories_episode
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stories_episode (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            station_id BIGINT NOT NULL,
            title VARCHAR(200) NOT NULL,
            episode_num INT NOT NULL,
            subtitle VARCHAR(255) NOT NULL,
            history_summary TEXT NOT NULL,
            last_viewed_at DATETIME(6),
            source_url VARCHAR(200)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
    print("Successfully created missing tables in MySQL (hisubtory_db).")

if __name__ == "__main__":
    create_tables()
