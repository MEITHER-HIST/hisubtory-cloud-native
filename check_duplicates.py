import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from stories.models import Cut
from django.db.models import Count

def check_duplicates():
    # episode_id와 cut_order가 같은 데이터가 1개 이상인 그룹 찾기
    duplicates = Cut.objects.using('mysql').values('episode_id', 'cut_order').annotate(count=Count('cut_id')).filter(count__gt=1)
    
    if not duplicates:
        print("중복된 장면(Cut) 데이터가 없습니다.")
        return

    print(f"총 {len(duplicates)}개의 중복 케이스를 발견했습니다.")
    for item in duplicates:
        eid = item['episode_id']
        order = item['cut_order']
        count = item['count']
        print(f"에피소드 {eid}, 순서 {order}: {count}개 중복")

if __name__ == "__main__":
    check_duplicates()
