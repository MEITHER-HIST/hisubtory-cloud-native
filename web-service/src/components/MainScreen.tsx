import { useState, useEffect, useMemo, useCallback } from 'react';
import { Shuffle, User as UserIcon, Menu, ChevronDown, Info, X } from 'lucide-react';
import { SubwayMap } from './SubwayMap';
import type { User } from "../App";

// ✅ 1호선부터 9호선까지 공식 색상 데이터 정의
const LINE_COLORS: Record<string, string> = {
  "1": "#0052A4",
  "2": "#00A84D",
  "3": "#EF7C1C",
  "4": "#00A5DE",
  "5": "#996CAC",
  "6": "#CD7C2F",
  "7": "#747F00",
  "8": "#E6186C",
  "9": "#BB8336",
};

interface StationDTO { 
  id: number; 
  name: string; 
  clickable: boolean; 
  color: "green" | "gray"; 
  is_viewed: boolean; 
  has_story: boolean; 
}

interface MainScreenProps {
  user: User | null;
  currentLine: string;
  onMenuClick: () => void;
  onLoginClick: () => void;
  onLogout: () => void | Promise<void>;
  onGoToMyPage: () => void;
  onStationClick: (stationId: string, episodeId: string) => void; 
  onRandomStation: (stationId: string, episodeId: string) => void;
}

export function MainScreen({ 
  user, 
  currentLine, 
  onMenuClick, 
  onLoginClick, 
  onLogout, 
  onGoToMyPage, 
  onStationClick, 
  onRandomStation 
}: MainScreenProps) {
  const [isProfileDropdownOpen, setIsProfileDropdownOpen] = useState(false);
  const [stations, setStations] = useState<StationDTO[]>([]);
  const [showRandomButton, setShowRandomButton] = useState<boolean>(true);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const fetchMain = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await fetch(`/api/pages/v1/main/?line=${currentLine}`, { credentials: "include" });
      const data = await res.json();
      
      if (data.success && data.stations) {
        setStations(data.stations);
        setShowRandomButton(data.show_random_button);
      }
    } catch (e) {
      console.error("fetch 에러:", e);
    } finally {
      setIsLoading(false);
    }
  }, [user, currentLine]);

  useEffect(() => { fetchMain(); }, [fetchMain]);

  const stationByName = useMemo(() => {
    const m = new Map<string | number, StationDTO>();
    stations.forEach(s => {
      const clean = s.name.replace(/역$/, "");
      m.set(s.id, s);
      m.set(clean, s);
    });
    return m;
  }, [stations]);

  const handleStationClick = async (stationId: number) => {
    // ✅ 비로그인 시 로그인 유도
    if (!user) {
      onLoginClick();
      return;
    }
    
    try {
      setIsLoading(true);
      const res = await fetch(`/api/pages/v1/episode/pick/?station_id=${stationId}`, { credentials: "include" });
      const data = await res.json();
      if (data.success && data.episode_id) {
        onStationClick(String(stationId), String(data.episode_id));
      } else {
        alert(data.message || "감상 가능한 에피소드가 없습니다.");
      }
    } catch (err) {
      console.error("에피소드 조회 에러:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRandomStation = async () => {
    try {
      setIsLoading(true);
      const res = await fetch(`/api/pages/v1/episode/random/?line=${currentLine}`, { credentials: "include" });
      const data = await res.json();
      if (res.ok && data.episode_id) {
        onRandomStation(String(data.station_name), String(data.episode_id));
      }
    } catch (err) {
      console.error("랜덤 에러:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-white">
      {/* --- 헤더 --- */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between relative">
          <Menu 
            className="w-6 h-6 text-gray-600 cursor-pointer hover:text-blue-600 transition-colors" 
            onClick={onMenuClick} 
          />
          <h1 className="absolute left-1/2 -translate-x-1/2 text-blue-600 font-bold text-xl tracking-widest">HISUBTORY</h1>
          <div className="flex items-center gap-2">
            {user ? (
              <div className="relative">
                <button onClick={() => setIsProfileDropdownOpen(!isProfileDropdownOpen)} className="flex items-center gap-1 text-sm font-bold bg-gray-50 px-3 py-2 rounded-xl border border-transparent hover:border-gray-200 transition-all">
                  <UserIcon className="w-4 h-4 text-blue-600" />
                  <span className="text-gray-900">{user.name}님</span>
                  <ChevronDown className="w-4 h-4 text-gray-400" />
                </button>
                {isProfileDropdownOpen && (
                  <div className="absolute right-0 mt-2 bg-white rounded-2xl shadow-2xl border border-gray-200 p-2 z-[9999]" style={{ minWidth: '160px' }}>
                    <button onClick={() => { onGoToMyPage(); setIsProfileDropdownOpen(false); }} className="w-full text-left px-4 py-3 text-sm font-bold text-gray-700 hover:bg-blue-50 rounded-xl">마이페이지</button>
                    <button onClick={() => { onLogout(); setIsProfileDropdownOpen(false); }} className="w-full text-left px-4 py-3 text-sm font-bold text-red-500 hover:bg-red-50 rounded-xl border-t border-gray-50 mt-1">로그아웃</button>
                  </div>
                )}
              </div>
            ) : (
              <button onClick={onLoginClick} className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-bold transition-colors hover:bg-blue-700 shadow-sm">
                로그인
              </button>
            )}
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-5xl mx-auto px-4 py-8 w-full flex flex-col items-center">
        
        {/* ✅ [수정] 호선 안내 배지: LINE_COLORS 객체를 사용하여 모든 호선 색상 자동 적용 */}
        <div className="mb-6 self-start flex items-center gap-4 bg-white px-6 py-2.5 rounded-full border border-gray-200 shadow-md">
          <div 
            className="w-5 h-5 rounded-full shadow-sm" 
            style={{ 
              backgroundColor: LINE_COLORS[currentLine] || "#cbd5e1" 
            }} 
          />
          <span className="text-base font-black text-gray-800">{currentLine}호선 이용 중</span>
        </div>

        {/* 지하철 노선도 영역 */}
        <div className="w-full mb-8 bg-gray-50 rounded-[40px] p-6 shadow-inner min-h-[400px] flex flex-col items-center justify-center relative border border-gray-100">
          {stations.length > 0 ? (
            <SubwayMap 
              stationByName={stationByName} 
              onPickEpisode={handleStationClick} 
              isLoggedIn={!!user} 
            />
          ) : !isLoading && <div className="text-blue-600 font-bold">지하철 노선도를 불러오는 중...</div>}
          {isLoading && <div className="absolute inset-0 bg-white/60 flex items-center justify-center z-10 rounded-[40px] font-bold text-blue-600">처리 중...</div>}
        </div>

        {/* 로그인 안내 박스 */}
        {!user && (
          <div className="w-full mb-4 bg-amber-50 border border-amber-100 rounded-xl py-4 flex items-center justify-center gap-3 shadow-sm px-4">
            <Info className="w-5 h-5 text-amber-500 shrink-0" />
            <p className="text-amber-900 font-bold text-sm whitespace-nowrap overflow-hidden text-ellipsis">
              로그인을 하시면 나만의 여행 기록을 남기고 좋아하는 이야기를 보관할 수 있어요! 😊
            </p>
          </div>
        )}

        {/* 랜덤 스토리 버튼 */}
        {showRandomButton && (
          <button 
            onClick={handleRandomStation} 
            className="w-full py-6 bg-blue-600 text-white rounded-xl font-bold shadow-lg flex items-center justify-center gap-3 text-2xl transition-transform active:scale-95 hover:bg-blue-700"
          >
            <Shuffle className="w-6 h-6" /> 오늘의 랜덤 스토리 탐험하기
          </button>
        )}
      </main>
    </div>
  );
}