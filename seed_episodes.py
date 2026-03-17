import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from subway.models import Station
from stories.models import Webtoon, Episode, Cut

def seed():
    # 실제 에피소드 데이터 매핑 (역 이름: 에피소드 정보)
    # episode_id를 강제로 지정하여 Supabase 히스토리와 매핑되게 함
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
        "불광": {
            "episode_id": 14,
            "subtitle": "은평의 중심지, 불광",
            "captions": [
                "불광사에서 유래한 지명이며 근처에 북한산이 있다.",
                "밀양 박씨의 터전이었다.",
                "넓은 농지를 바탕으로 부유한 지역이었다.",
                "현재는 지하철이 들어오면서 은평지역의 중심지가 되었다."
            ]
        },
        "녹번": {
            "episode_id": 15,
            "subtitle": "자연 동이 나오는 곳, 녹번",
            "captions": [
                "조선의 관리가 빈민을 위해 녹을 놓아두고 간 것에서 유래한 지명",
                "숲에서 자연 동(銅)이 나온다고 해서 녹반(綠礬)이라고 불렸다.",
                "조선 시대부터 녹번이라는 지명이었다.",
                "현재는 생태공원이 잘 갖춰져있다."
            ]
        },
        "홍제": {
            "episode_id": 16,
            "subtitle": "서울의 관문, 홍제",
            "captions": [
                "서울과 개성, 의주를 연결하는 관문으로 청나라 사신들이 많이 이용하였다.",
                "일제강점기 미국 감리교회가 있었다.",
                "해방 이후 홍제동이 되었다.",
                "광화문과 시청이 매우 가깝다."
            ]
        },
        "무악재": {
            "episode_id": 17,
            "subtitle": "호랑이가 나오던 고개, 무악재",
            "captions": [
                "조선 개국 당시 무학대사의 의견으로 무악(毋岳)이라는 지명을 가지게 되었 다.",
                "과거 호랑이가 많이 나와 인명 피해가 많았다.",
                "청나라 사신을 맞이하는 모화관(慕華館)이 있었다.",
                "주변에 서대문형무소(현 서대문독립공원)이 있다."
            ]
        },
        "독립문": {
            "episode_id": 18,
            "subtitle": "독립의 상징, 독립문",
            "captions": [
                "프랑스 개선문의 영향을 받아 건축되었다.",
                "청나라로 부터 독립을 상징하는 건축물이다.",
                "대한제국 개화의 중심지가 되었다.",
                "근처에 서대문형무소등 일제강점기 유적이 많다."
            ]
        },
        "경복궁": {
            "episode_id": 19,
            "subtitle": "조선의 정궁, 경복궁",
            "captions": [
                "조선 건국후 지어진 왕궁이며 가장 먼저 지어진 건물이다.",
                "중앙청역이었으나 1987년 경복궁역으로  이름이 바뀌었다.",
                "역사내에 미술관이 있다.",
                "역 주변에 경복궁과 광화문등 조선시대 문화 유적이 있다."
            ]
        },
        "안국": {
            "episode_id": 20,
            "subtitle": "독립운동의 숨결, 안국",
            "captions": [
                "조선시대 군사 조직인 안국방(安國坊)이 있었던 지역이며 이 이름에서 유래 한 지명이다.",
                "3.1운동과 관련된 태화관 유적지가 근처에 있으며, 안국역은 독립 운동 태마에 맞게 조성되었다.",
                "인사동 거리가 근처에 있어 문화적 상업적 성격이 강하다.",
                "역 근처에 외국 공사관이 많이 있다."
            ]
        },
        "종로3가": {
            "episode_id": 21,
            "subtitle": "민주화의 거리, 종로3가",
            "captions": [
                "동대문에서 경희궁에 이르는 길이다.",
                "일제강점기 6.10 만세운동의 출발지였다.",
                "대한민국 수립 이후 민주화 운동의 시작점이 되었다.",
                "현재는 근처에 익선동 한옥거리등 여러가지 관광 상업시설이 있다."
            ]
        },
        "을지로3가": {
            "episode_id": 22,
            "subtitle": "개화기의 흔적, 을지로3가",
            "captions": [
                "조선말 개화기 청나라 사람이 거주하던 지역이었다.",
                "일본인도 이주하여 거주하기 시작하였다.",
                "대한민국 수립 이후 을지로로 지명이 확정되었다.",
                "주변에 청계천과 충무로가 있으며 청계천을 중심으로 헌책방이 있다."
            ]
        },
        "충무로": {
            "episode_id": 23,
            "subtitle": "영화와 문화의 중심, 충무로",
            "captions": [
                "조선시대에 땅에 물이 많아 진고개라고 불렸다. 또한 먹을 생산하는 곳을 유명했다.",
                "개화기 명동으로 이어진 지역이었며, 일본인이 주로 거주하던 지역이었다.",
                "대한민국 수립 이후 충무로가 되었다. 일본인이 많이 있던 지역이었기에 충 무공 이순신의 충무를 따서 지명을 지었다.",
                "영화 산업으로 유명하며, 근처에 남산타워가 있다."
            ]
        },
        "동대입구": {
            "episode_id": 24,
            "subtitle": "장충단의 기억, 동대입구",
            "captions": [
                "장충단(奬忠壇)이라는 군영이 있던 곳이다.",
                "일제강점기 군영이 있던 지역을 공원으로 만들었다.",
                "장충체육관이 근처에 있으며 거주 및 상업 시설이 발달해 있다.",
                "주변에 신라 호텔과 장충단 공원이 있으며, 여러 호텔 및 조선시대 및 불교 관련 유적지가 있다."
            ]
        },
        "약수": {
            "episode_id": 25,
            "subtitle": "유명한 우물이 있던 곳, 약수",
            "captions": [
                "약수로 유명한 우물에서 비롯한 지명이다.",
                "원래 신당동의 마을이었다.",
                "대한민국 수립 이후 약수동으로 분리 되었다.",
                "현재는 아파트가 밀집되어 있는 주거 공간이다."
            ]
        },
        "금호": {
            "episode_id": 26,
            "subtitle": "한강 옆 평화로운 마을, 금호",
            "captions": [
                "한강에 가까운 마을이라는 뜻에 영향을 받은 지명이다.",
                "일제 강점기 의열단의 김상옥이 전투를 치뤘던 지역이다.",
                "해방 이전까지 농촌의 성격이 강했다.",
                "해방 이후 도시개발이 이루어졌으며 거주지역으로 발달하였다."
            ]
        },
        "옥수": {
            "episode_id": 27,
            "subtitle": "독서당이 있던 마을, 옥수",
            "captions": [
                "옥정수(玉井水)에서 유래되었다. 두모포(豆毛浦)라고도 불렸다.",
                "조선시대 독서당(讀書堂)이 있었는데 임진웨란 때 사라졌다.",
                "해방 이후 옥수동이라 확정되었다.",
                "현재는 주거지역이다."
            ]
        },
        "압구정": {
            "episode_id": 28,
            "subtitle": "한명회의 숨결, 압구정",
            "captions": [
                "한명회가 지은 정자에서 유래된 지명이다.",
                "갈매기와 친하게 지낸다는 뜻의 지명이다. 조선시대에는 갈매기가 날아 들었다.",
                "일제강점기 이후 1970년대 이전까지 개발되지 않았다.",
                "현재는 강남개발과 함께 고층빌딩과 고급 상업지구가 형성 되었다."
            ]
        }
    }

    stations = Station.objects.using('mysql').all()
    if not stations.exists():
        print("No stations found. Seed subway first.")
        return

    print(f"Found {len(stations)} stations. Seeding real episodes...")

    # 숫자를 한글 서수로 변환하는 함수
    def get_korean_ordinal(num):
        ordinals = {1: "첫", 2: "두", 3: "세", 4: "네", 5: "다섯", 6: "여섯", 7: "일곱", 8: "여덟", 9: "아홉", 10: "열"}
        if num in ordinals:
            return ordinals[num]
        return str(num)

    for station in stations:
        data = REAL_DATA.get(station.station_name)
        
        # 1. 웹툰 생성
        webtoon = Webtoon.objects.using('mysql').filter(station=station).first()
        if not webtoon:
            webtoon = Webtoon.objects.using('mysql').create(
                station=station,
                title=f"{station.station_name}역 이야기"
            )
        else:
            Webtoon.objects.using('mysql').filter(station=station).exclude(pk=webtoon.pk).delete()

        # 2. 에피소드 생성
        if data:
            eid = data["episode_id"]
            ep_num = data.get("episode_num", 1) # 데이터에 있는 번호 사용, 없으면 1
            new_subtitle = f"{station.station_name}역의 {get_korean_ordinal(ep_num)} 번째 이야기"
            
            Episode.objects.using('mysql').filter(webtoon=webtoon).exclude(episode_id=eid).delete()
            
            episode, created = Episode.objects.using('mysql').get_or_create(
                episode_id=eid,
                defaults={
                    "webtoon": webtoon,
                    "episode_num": ep_num,
                    "subtitle": new_subtitle
                }
            )
            if not created:
                episode.webtoon = webtoon
                episode.episode_num = ep_num
                episode.subtitle = new_subtitle
                episode.save(using='mysql')

            # 3. 컷 생성/업데이트
            # 기존 컷 삭제 후 재생성 (순서 보장)
            Cut.objects.using('mysql').filter(episode=episode).delete()
            for i, caption in enumerate(data["captions"], 1):
                # 1~6번 에피소드(eid)의 경우 우리가 업로드한 S3 경로 사용
                if eid <= 6:
                    image_path = f"webtoons/{eid}/episodes/1/cuts/{i}.png"
                    # 웹툰 썸네일도 첫 번째 컷으로 업데이트
                    if i == 1:
                        webtoon.thumbnail = image_path
                        webtoon.save(using='mysql')
                else:
                    image_path = f"episodes/{eid}/{i}.png"
                
                Cut.objects.using('mysql').create(
                    episode=episode,
                    cut_order=i,
                    image=image_path,
                    caption=caption
                )
        else:
            # 데이터 없는 역은 무시하거나 기본값 (여기서는 최소한의 데이터만 유지)
            pass

    print("Successfully seeded all real episode data.")

if __name__ == "__main__":
    seed()
