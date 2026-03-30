import os
import django
import sys

# 프로젝트 루트를 경로에 추가
sys.path.append('/home/tester/hisubtory-cloud-native')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from stories.models import Webtoon, Episode, Station

print("=== [Webtoon & Episode Data Check] ===")
# 에피소드 2번 데이터 확인
ep2_list = Episode.objects.filter(episode_num=2).select_related('webtoon', 'webtoon__station')

for ep in ep2_list:
    w = ep.webtoon
    s = w.station if w else None
    print(f"Episode ID: {ep.episode_id} | Num: {ep.episode_num} | Subtitle: {ep.subtitle}")
    print(f"  -> Webtoon ID: {w.webtoon_id if w else 'N/A'} | Title: {w.title if w else 'N/A'}")
    print(f"  -> Thumbnail Path: {w.thumbnail if w else 'N/A'}")
    print(f"  -> Station: {s.station_name if s else 'N/A'} (ID: {s.id if s else 'N/A'})")
    print("-" * 50)

# 특정 역(예: 문제가 되는 역)에 대한 매핑 확인을 위해 전체 웹툰-역 매핑 일부 출력
print("\n=== [Webtoon-Station Mapping (Sample)] ===")
for w in Webtoon.objects.select_related('station').all()[:10]:
    print(f"Webtoon: {w.title} (ID: {w.webtoon_id}) -> Station: {w.station.station_name} (ID: {w.station.id})")
