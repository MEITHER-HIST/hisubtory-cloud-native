import { Episode } from '../types';

export const episodes: Episode[] = [
  // 대화
  { id: 'ep-dh-1', stationId: '대화', title: '대화역의 시작', content: '일산신도시 개발과 함께 1996년 1월 30일 개통한 대화역. 이곳은 서울 지하철 3호선의 시작점이자 일산의 관문입니다.', imageUrl: 'https://images.unsplash.com/photo-1562095241-8c6714fd4178?w=400' },
  { id: 'ep-dh-2', stationId: '대화', title: '일산신도시의 중심', content: '대화역 주변은 라페스타와 웨스턴돔이 있어 쇼핑과 문화의 중심지로 자리잡았습니다.', imageUrl: 'https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=400' },
  
  // 주엽
  { id: 'ep-jy-1', stationId: '주엽', title: '주엽동의 유래', content: '주엽(酒葉)은 옛날 이곳에 술을 빚는 집이 많아 붙여진 이름입니다.', imageUrl: 'https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=400' },
  { id: 'ep-jy-2', stationId: '주엽', title: '현대백화점의 역사', content: '1997년 개점한 현대백화점 킨텍스점은 일산 지역 상권의 중심이 되었습니다.', imageUrl: 'https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=400' },
  
  // 정발산
  { id: 'ep-jbs-1', stationId: '정발산', title: '정발산의 전설', content: '정발산(正鉢山)은 그릇을 엎어놓은 것 같은 모양의 산이라는 뜻입니다.', imageUrl: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400' },
  { id: 'ep-jbs-2', stationId: '정발산', title: '정발산 공원', content: '정발산 공원은 일산 주민들의 휴식처로 사랑받는 도심 속 자연입니다.', imageUrl: 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400' },
  
  // 경복궁
  { id: 'ep-gbg-1', stationId: '경복궁', title: '조선의 법궁', content: '1395년 창건된 경복궁은 조선왕조의 첫 번째 궁궐이자 가장 큰 궁궐입니다.', imageUrl: 'https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=400' },
  { id: 'ep-gbg-2', stationId: '경복궁', title: '광화문의 역사', content: '경복궁의 정문 광화문은 일제강점기 파괴되었다가 1968년 복원되었습니다.', imageUrl: 'https://images.unsplash.com/photo-1517154421773-0529f29ea451?w=400' },
  { id: 'ep-gbg-3', stationId: '경복궁', title: '국립고궁박물관', content: '경복궁 내 국립고궁박물관에서는 조선 왕실의 유물을 만날 수 있습니다.', imageUrl: 'https://images.unsplash.com/photo-1523568129082-6b5c8b515e06?w=400' },
  
  // 안국
  { id: 'ep-ag-1', stationId: '안국', title: '북촌한옥마을', content: '안국역 인근의 북촌한옥마을은 600년 역사를 간직한 전통 주거지입니다.', imageUrl: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400' },
  { id: 'ep-ag-2', stationId: '안국', title: '인사동 거리', content: '안국역에서 걸어갈 수 있는 인사동은 전통문화와 예술의 거리입니다.', imageUrl: 'https://images.unsplash.com/photo-1582407947304-fd86f028f716?w=400' },
  
  // 종로3가
  { id: 'ep-j3-1', stationId: '종로3가', title: '탑골공원', content: '1897년 조성된 탑골공원은 서울 최초의 근대식 공원입니다.', imageUrl: 'https://images.unsplash.com/photo-1519677100203-a0e668c92439?w=400' },
  { id: 'ep-j3-2', stationId: '종로3가', title: '3.1운동의 발원지', content: '1919년 3월 1일, 탑골공원에서 독립선언서가 낭독되며 3.1운동이 시작되었습니다.', imageUrl: 'https://images.unsplash.com/photo-1594722626114-f16bb6a4e9e4?w=400' },
  
  // 압구정
  { id: 'ep-agj-1', stationId: '압구정', title: '압구정의 유래', content: '조선시대 효령대군의 정자 압구정(狎鷗亭)에서 유래한 지명입니다.', imageUrl: 'https://images.unsplash.com/photo-1551431009-a802eeec77b1?w=400' },
  { id: 'ep-agj-2', stationId: '압구정', title: '압구정 로데오거리', content: '1990년대 패션과 청춘 문화의 중심지로 떠올랐던 압구정 로데오거리.', imageUrl: 'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=400' },
  
  // 신사
  { id: 'ep-ss-1', stationId: '신사', title: '가로수길의 탄생', content: '2000년대 초반 젊은 예술가들이 모이며 시작된 가로수길은 이제 서울의 명소가 되었습니다.', imageUrl: 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=400' },
  { id: 'ep-ss-2', stationId: '신사', title: '신사동의 변천', content: '농경지였던 신사동은 강남 개발과 함께 문화와 패션의 중심지로 성장했습니다.', imageUrl: 'https://images.unsplash.com/photo-1449034446853-66c86144b0ad?w=400' },
  
  // 고속터미널
  { id: 'ep-gst-1', stationId: '고속터미널', title: '강남고속버스터미널', content: '1976년 개장한 강남고속버스터미널은 전국 교통의 요충지입니다.', imageUrl: 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=400' },
  { id: 'ep-gst-2', stationId: '고속터미널', title: '센트럴시티', content: '터미널과 결합된 쇼핑몰 센트럴시티는 교통과 쇼핑을 연결한 복합문화공간입니다.', imageUrl: 'https://images.unsplash.com/photo-1567958451986-2de427a4a0be?w=400' },
  
  // 양재
  { id: 'ep-yj-1', stationId: '양재', title: '양재천', content: '양재천은 서울 남부의 대표적인 도심 하천으로 시민들의 휴식처입니다.', imageUrl: 'https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=400' },
  { id: 'ep-yj-2', stationId: '양재', title: '화훼공판장', content: '1991년 개장한 양재동 화훼공판장은 국내 최대 규모의 꽃 시장입니다.', imageUrl: 'https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400' },
];

// 나머지 역들도 각각 1~3개의 에피소드를 가지도록 추가할 수 있습니다
// 간단하게 모든 역에 기본 에피소드 하나씩 추가
const remainingStations = ['마두', '백석', '대곡', '화정', '원당', '원흥', '삼송', '지축', '구파발', '연신내', '불광', '녹번', '홍제', '무악재', '독립문', '을지로3가', '충무로', '동대입구', '약수', '금호', '옥수', '잠원', '교대', '남부터미널', '매봉', '도곡', '대치', '학여울', '대청', '일원', '수서', '가락시장', '경찰병원', '오금'];

remainingStations.forEach((station, index) => {
  episodes.push({
    id: `ep-${station}-1`,
    stationId: station,
    title: `${station}역의 이야기`,
    content: `${station}역에 얽힌 역사와 문화를 알아봅니다.`,
    imageUrl: `https://images.unsplash.com/photo-${1500000000000 + index}?w=400`
  });
});
