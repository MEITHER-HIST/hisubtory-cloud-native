import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from subway.models import Station
from stories.models import Webtoon, Episode, Cut

def seed():
    # 실제 에피소드 데이터 매핑 (역 이름: 에피소드 정보)
    REAL_DATA = {
        "구파발": {
            "episode_id": 12,
            "subtitle": "교통의 요충지, 구파발",
            "captions": ["교통의 요충지였다.", "3.1운동과 관련된 절이 있다.", "북한산과 매우 가깝다.", "고려시대의 절인 진관사가 있다."]
        },
        "연신내": {
            "episode_id": 13,
            "subtitle": "새벽이 늦게 오는 강, 연신내",
            "captions": [
                "산에 가려 새벽이 늦게오는 강이라는 지명이다.",
                "인조반정 당시 이서(李曙)가 늦게 도착했다는 일화에서 연서(延曙)가 되었다.",
                "불광천 너머가 명릉(明陵)이 위치한 서오릉 지역이다.",
                "현재는 3호선 6호선이 지나는 교통의 요충지이다."
            ]
        },
        # 추가 역 데이터 필요 시 여기에 작성...
    }

    stations = Station.objects.all()
    if not stations.exists():
        print("No stations found. Seed subway first.")
        return

    for station in stations:
        data = REAL_DATA.get(station.station_name)
        
        # 1. 웹툰 생성
        webtoon, _ = Webtoon.objects.get_or_create(
            station=station,
            defaults={"title": f"{station.station_name}역 이야기"}
        )

        # 2. 에피소드 생성
        if data:
            # 실제 데이터가 있는 경우
            eid = data["episode_id"]
            episode, created = Episode.objects.get_or_create(
                episode_id=eid,
                defaults={
                    "webtoon": webtoon,
                    "episode_num": 1,
                    "subtitle": data["subtitle"]
                }
            )
            # 만약 이미 존재하는데 webtoon이 다르다면 업데이트
            if not created and episode.webtoon != webtoon:
                episode.webtoon = webtoon
                episode.save()

            # 3. 컷 생성/업데이트
            for i, caption in enumerate(data["captions"], 1):
                image_path = f"episodes/{eid}/{i}.png"
                cut, c_created = Cut.objects.get_or_create(
                    episode=episode,
                    cut_order=i,
                    defaults={
                        "image": image_path,
                        "caption": caption
                    }
                )
                if not c_created:
                    cut.caption = caption
                    cut.image = image_path
                    cut.save()
        else:
            # 데이터가 없는 역은 기본 데이터 생성 (기존 로직 유지하되 S3 경로 형식으로)
            episode, _ = Episode.objects.get_or_create(
                webtoon=webtoon,
                episode_num=1,
                defaults={"subtitle": f"{station.station_name}의 첫 번째 전설"}
            )
            for i in range(1, 4):
                Cut.objects.get_or_create(
                    episode=episode,
                    cut_order=i,
                    defaults={
                        "image": f"episodes/default/{i}.png",
                        "caption": f"{station.station_name}역 {i}번째 장면 설명입니다."
                    }
                )

    print("Successfully seeded real episode data.")

if __name__ == "__main__":
    seed()
