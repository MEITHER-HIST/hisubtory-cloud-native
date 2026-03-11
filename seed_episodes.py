import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from subway.models import Station
from stories.models import Webtoon, Episode, Cut

def seed():
    # 3호선 역 하나를 선택 (예: 경복궁역)
    station = Station.objects.filter(station_name__contains="경복궁").first()
    if not station:
        station = Station.objects.first()
    
    if not station:
        print("No stations found. Seed subway first.")
        return

    # 웹툰 생성
    webtoon, created = Webtoon.objects.update_or_create(
        station_id=station.id,
        defaults={
            "title": f"{station.station_name}의 역사 이야기",
            "author": "관리자",
            "summary": "역사에 얽힌 신비로운 이야기들을 확인해보세요.",
            "created_at": timezone.now()
        }
    )

    # 에피소드 생성
    episode, created = Episode.objects.update_or_create(
        webtoon=webtoon,
        episode_num=1,
        defaults={
            "subtitle": "첫 번째 이야기: 기원",
            "history_summary": "이 역의 기원에 대한 설명입니다.",
            "is_published": True,
            "created_at": timezone.now()
        }
    )

    # 컷 생성
    Cut.objects.update_or_create(
        episode=episode,
        cut_order=1,
        defaults={
            "image": "https://via.placeholder.com/800x600?text=History+Scene+1",
            "caption": "먼 옛날, 이 곳에서는...",
            "created_at": timezone.now()
        }
    )

    print(f"Successfully seeded episode for {station.station_name}")

if __name__ == "__main__":
    seed()
