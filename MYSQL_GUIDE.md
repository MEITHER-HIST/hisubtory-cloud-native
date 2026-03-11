# MySQL Database Editing Guide for Hisubtory-Cloud-Native

This project uses a multi-database setup:
- **Default (PostgreSQL):** Used for `accounts`, `library`, and Django system apps.
- **MySQL:** Used for `stories`, `subway`, and other content-related data.

## 1. Direct Access via MySQL CLI
You can connect to the MySQL database directly from the host machine (where port `3307` is mapped):

```bash
mysql -h 127.0.0.1 -P 3307 -u admin -pmysql_password hisubtory_db
```

Or, you can run the CLI inside the Docker container:

```bash
docker exec -it hisubtory-db-mysql-verify mysql -u admin -pmysql_password hisubtory_db
```

## 2. Django Shell Access
To interact with the database using Django ORM (which handles routing automatically):

### Option A: Run inside the container (Recommended)
This uses the container's internal network to connect to `db-mysql:3306`.

```bash
docker exec -it hisubtory-user python manage.py shell
```

Example command inside the shell:
```python
from stories.models import Webtoon
print(Webtoon.objects.count())
```

### Option B: Run from the host
If you want to run from the host, ensure your `.env` file points to `localhost:3307`.
**Note:** Changing `.env` might break the Docker containers. It's better to use a temporary environment variable:

```bash
DB_HOST=127.0.0.1 DB_PORT=3307 python manage.py shell
```

## 3. Running existing scripts
Your scripts in the home directory (e.g., `update_episode_12_captions.py`) are already configured to connect to `localhost:3307`. You can continue to run them as follows:

```bash
python /home/tester/update_episode_12_captions.py
```

## 4. Current Setup Status
- **MySQL Container:** `hisubtory-db-mysql-verify` (running on port 3307)
- **Database Name:** `hisubtory_db`
- **User:** `admin`
- **Password:** `mysql_password`
- **Tables:** `webtoons`, `episodes`, `cuts`, `subway_station`, `subway_line`
