import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from subway.models import Station, Line
from stories.models import Webtoon, Episode, Cut

def seed():
    print("Checking database for existing episode data...")
    
    # 1. Line (3호선) 생성
    line, created = Line.objects.get_or_create(
        line_name="3호선",
        defaults={"line_color": "#F36C21"}
    )
    if created:
        print("Created Line: 3호선")

    # 2. Stations 생성 (대화 ~ 오금)
    stations_data = [
        ('3-01', '대화'), ('3-02', '주엽'), ('3-03', '정발산'), ('3-04', '마두'), ('3-05', '백석'),
        ('3-06', '대곡'), ('3-07', '화정'), ('3-08', '원당'), ('3-09', '원흥'), ('3-10', '삼송'),
        ('3-11', '지축'), ('3-12', '구파발'), ('3-13', '연신내'), ('3-14', '불광'), ('3-15', '녹번'),
        ('3-16', '홍제'), ('3-17', '무악재'), ('3-18', '독립문'), ('3-19', '경복궁'), ('3-20', '안국'),
        ('3-21', '종로3가'), ('3-22', '을지로3가'), ('3-23', '충무로'), ('3-24', '동대입구'), ('3-25', '약수'),
        ('3-26', '금호'), ('3-27', '옥수'), ('3-28', '압구정'), ('3-29', '신사'), ('3-30', '잠원'),
        ('3-31', '고속터미널'), ('3-32', '교대'), ('3-33', '남부터미널'), ('3-34', '양재'), ('3-35', '매봉'),
        ('3-36', '도곡'), ('3-37', '대치'), ('3-38', '학여울'), ('3-39', '대청'), ('3-40', '일원'),
        ('3-41', '수서'), ('3-42', '가락시장'), ('3-43', '경찰병원'), ('3-44', '오금')
    ]

    for code, name in stations_data:
        station, s_created = Station.objects.get_or_create(
            station_code=code,
            defaults={"station_name": name, "is_enabled": True}
        )
        if s_created:
            print(f"Created Station: {name}")
        
        # Line에 Station 연결
        if station not in line.stations.all():
            line.stations.add(station)

    # 3. Webtoon 데이터 (예시)
    if not Webtoon.objects.exists():
        print("No Webtoon data found. Creating default webtoons...")
        for i, (code, name) in enumerate(stations_data[:11], 1): # 일단 11개만 샘플로
             Webtoon.objects.get_or_create(
                 title=f"{name}역의 역사",
                 defaults={
                     "thumbnail": f"webtoons/{i}/episodes/1/cuts/1/1.png",
                     "station_id": i
                 }
             )

    print("Seeding complete.")

if __name__ == "__main__":
    seed()
