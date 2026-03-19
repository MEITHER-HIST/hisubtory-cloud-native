import { useState, useEffect } from "react";
import { ArrowLeft, Bookmark, BookmarkCheck, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import type { User } from "../App";

const LINE_COLORS: Record<string, string> = {
  "1": "#0052A4", "2": "#00A84D", "3": "#EF7C1C", 
  "4": "#00A5DE", "5": "#996CAC", "6": "#CD7C2F",
  "7": "#747F28", "8": "#E6186C", "9": "#BB8336",
};

interface CutDTO {
  cut_id: number;
  image_url: string | null;
  caption: string;
  cut_order: number;
}

interface EpisodeDTO {
  episode_id: number;
  episode_num: number;
  episode_title: string;
  webtoon_title: string;
  station_name: string;
  webtoon_id: number;
  is_viewed: boolean;
  line: string;
}

interface StoryScreenProps {
  user: User | null;
  stationId: string | null;
  episodeId: string | null;
  onBack: () => void;
  onNextEpisode: (newId: string) => void;
}

export function StoryScreen({ user, stationId, episodeId, onBack, onNextEpisode }: StoryScreenProps) {
  const [isSaved, setIsSaved] = useState(false);
  const [isViewed, setIsViewed] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [episode, setEpisode] = useState<EpisodeDTO | null>(null);
  const [cuts, setCuts] = useState<CutDTO[]>([]);

  useEffect(() => {
    if (!episodeId) {
      setError("에피소드 정보가 없습니다.");
      setLoading(false);
      return;
    }

    const fetchDetail = async () => {
      try {
        setLoading(true);
        setError(null);

        const res = await fetch(`/api/stories/episode/detail/?episode_id=${episodeId}`, {
          method: "GET",
          credentials: "include",
        });

        if (!res.ok) {
          const errorData = await res.json().catch(() => ({}));
          throw new Error(errorData.message || `서버 에러 (${res.status})`);
        }

        const data = await res.json();
        
        if (data.success) {
          setEpisode(data.episode);
          setCuts(data.cuts || []);
          setIsSaved(data.is_bookmarked || false);
          setIsViewed(data.episode.is_viewed || false);
        } else {
          throw new Error(data.message || "데이터를 가져오지 못했습니다.");
        }
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDetail();
  }, [episodeId]);

  const handleSaveToggle = async () => {
    const currentId = episode?.episode_id || episodeId;
    if (!currentId || !user) {
      toast.error("로그인이 필요한 서비스입니다.");
      return;
    }
    try {
      const res = await fetch(`/api/stories/bookmark/${currentId}/`, {
        method: "POST",
        credentials: "include",
      });
      if (res.ok) {
        const data = await res.json();
        setIsSaved(data.is_bookmarked);
        toast.success(data.is_bookmarked ? `내 보관함에 저장되었습니다.` : "저장이 취소되었습니다.");
      }
    } catch (err) { toast.error("오류가 발생했습니다."); }
  };

  const handleOtherStory = async () => {
    const currentStationId = episode?.webtoon_id || stationId;
    if (!currentStationId) return;
    try {
      const res = await fetch(`/api/stories/v1/episode/random/?station_id=${currentStationId}&exclude=${episodeId}`, {
        method: "GET",
        credentials: "include",
      });
      const data = await res.json();
      if (res.ok && data.success && data.episode_id) {
        onNextEpisode?.(data.episode_id.toString());
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else { toast.info("새로운 이야기를 준비 중입니다!"); }
    } catch (err) { console.error("로드 실패:", err); }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center bg-white font-bold text-blue-600"><p>기록을 불러오는 중...</p></div>;
  if (error || !episode) return <div className="min-h-screen flex items-center justify-center px-6 text-center"><div><p className="text-gray-900 mb-6 font-medium">{error || "에피소드를 불러올 수 없습니다."}</p><button onClick={onBack} className="px-8 py-3 bg-blue-600 text-white rounded-lg font-bold">돌아가기</button></div></div>;

  return (
    <div className="min-h-screen flex flex-col bg-gray-50/50">
      <header className="bg-white shadow-sm sticky top-0 z-50 border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between relative">
          <button onClick={onBack} className="flex items-center gap-2 text-gray-700 hover:text-blue-600 font-bold transition-colors">
            <ArrowLeft className="w-6 h-6" />
            <span>돌아가기</span>
          </button>
          <h1 className="absolute left-1/2 -translate-x-1/2 text-blue-600 font-bold text-xl tracking-widest">HISUBTORY</h1>
          <div className="flex items-center gap-2 text-sm font-bold bg-gray-50 px-3 py-2 rounded-xl border border-gray-100">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: LINE_COLORS["3"] }} />
            <span className="text-gray-900">{episode.station_name}</span>
          </div>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-8">
        <div className="bg-white rounded-3xl shadow-sm p-8 border border-gray-100 mb-8">
          <h2 className="text-2xl font-black text-gray-900 mb-2">{episode.webtoon_title}</h2>
          <div className="flex items-center gap-3">
            <span className="text-gray-500 font-bold">{episode.episode_title}</span>
            {isViewed && <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-black">✓ 시청 완료</span>}
          </div>
        </div>

        {cuts.length > 0 ? (
          cuts.map((c, idx) => (
            <div key={idx} className="bg-white rounded-3xl shadow-lg overflow-hidden border border-gray-100 mb-12 flex flex-col">
              {/* 이미지 영역 */}
              <div className="w-full relative bg-gray-100">
                <img 
                  src={c.image_url || ""} 
                  alt={`장면 ${idx + 1}`} 
                  className="w-full h-auto object-cover min-h-[300px] block"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    if (!target.src.includes('placeholder')) {
                      target.src = "https://via.placeholder.com/800x600?text=이미지를+불러오는+중...";
                      setTimeout(() => { target.src = c.image_url || ""; }, 1000); // 1초 뒤 재시도
                    }
                  }}
                />
              </div>
              {/* 캡션 영역 - 하나의 카드 안에 통합 */}
              {c.caption && (
                <div className="p-8 bg-white border-t border-gray-50">
                  <p className="text-gray-800 text-lg leading-relaxed font-bold">{c.caption}</p>
                </div>
              )}
            </div>
          ))
        ) : (
          <div className="text-center py-20 bg-white rounded-3xl border-2 border-dashed border-gray-200">
            <p className="text-gray-400 font-bold">등록된 장면이 없습니다.</p>
          </div>
        )}

        <div className="bg-white/95 backdrop-blur-md rounded-3xl shadow-2xl p-6 sticky bottom-6 mt-16 border border-gray-100 flex gap-4">
          <button onClick={handleSaveToggle} className={`flex-1 py-4 rounded-2xl flex items-center justify-center gap-2 font-black transition-all ${isSaved ? "bg-blue-50 text-blue-600 border-2 border-blue-600" : "bg-gray-50 text-gray-400 border-2 border-transparent"}`}>
            {isSaved ? <BookmarkCheck className="w-6 h-6" /> : <Bookmark className="w-6 h-6" />} {isSaved ? "내 보관함" : "저장하기"}
          </button>
          <button onClick={handleOtherStory} className="flex-1 py-4 bg-blue-600 text-white rounded-2xl font-black flex items-center justify-center gap-2">
            <RefreshCw className="w-6 h-6" /> 다른 이야기
          </button>
        </div>
      </main>
    </div>
  );
}
