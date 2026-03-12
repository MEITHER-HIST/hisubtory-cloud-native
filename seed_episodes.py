import os
import django
from django.utils import timezone
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from subway.models import Station
from stories.models import Webtoon, Episode, Cut

def seed():
    stations = Station.objects.all()
    if not stations.exists():
        print("No stations found. Seed subway first.")
        return

    print(f"Found {len(stations)} stations. Seeding webtoons and episodes...")

    for station in stations:
        # 웹툰 생성
        webtoon, created = Webtoon.objects.get_or_create(
            station=station,
            defaults={
                "title": f"{station.station_name}의 역사 이야기",
                "created_at": timezone.now()
            }
        )

        # 에피소드 생성 (각 역마다 최소 1개)
        episode, created = Episode.objects.get_or_create(
            webtoon=webtoon,
            episode_num=1,
            defaults={
                "subtitle": f"{station.station_name}의 첫 번째 전설",
                "created_at": timezone.now()
            }
        )

        # 컷 생성 (3개씩)
        for i in range(1, 4):
            Cut.objects.get_or_create(
                episode=episode,
                cut_order=i,
                defaults={
                    "image": f"https://picsum.photos/seed/{station.id}_{i}/800/600",
                    "caption": f"{station.station_name}역 {i}번째 장면 설명입니다.",
                    "created_at": timezone.now()
                }
            )

    print(f"Successfully seeded episodes for {len(stations)} stations.")

if __name__ == "__main__":
    seed()
