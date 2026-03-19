import { ArrowLeft, Bookmark, Check, Clock, Library as LibraryIcon } from 'lucide-react';
import { useEffect, useState } from 'react';

interface MyPageProps {
  user: { name: string; username: string } | null;
  onBack: () => void;
  onEpisodeClick: (episodeId: string) => void;
}

interface HistoryItem {
  id: string;
  title: string;
  stationName: string;
  imageUrl: string;
  content: string;
}

export function MyPage({ user, onBack, onEpisodeClick }: MyPageProps) {
  const [activeTab, setActiveTab] = useState<'recent' | 'saved'>('recent');
  const [recentStories, setRecentStories] = useState<HistoryItem[]>([]);
  const [myStories, setMyStories] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        // ALB가 stories/* 경로를 story-service로 보내므로 경로를 변경합니다.
        const res = await fetch("/api/stories/library/history/", { credentials: "include" });
        const data = await res.json();
        
        if (res.ok) {
          setRecentStories(data.recent || []);
          setMyStories(data.saved || []);
        }
      } catch (error) {
        console.error("활동 기록 로드 실패:", error);
      } finally {
        setLoading(false);
      }
    };

    if (user) fetchHistory();
  }, [user]);

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-gray-600 mb-4">로그인이 필요합니다</p>
          <button onClick={onBack} className="px-6 py-3 bg-blue-600 text-white rounded-lg font-bold">
            돌아가기
          </button>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center font-bold text-blue-600 bg-white">
        <p>기록을 불러오는 중...</p>
      </div>
    );
  }

  const renderStoryCard = (episode: HistoryItem) => (
    <button
      key={episode.id}
      onClick={() => onEpisodeClick(episode.id)}
      className="bg-white rounded-2xl p-4 hover:bg-blue-50 transition-all text-left border border-gray-100 shadow-sm group flex flex-col h-full"
    >
      <div className="aspect-video bg-gray-100 rounded-xl mb-4 overflow-hidden relative flex-shrink-0">
        {episode.imageUrl ? (
          <img 
            src={episode.imageUrl} 
            alt={episode.title} 
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400 text-xs bg-gray-50">
            등록된 이미지가 없습니다.
          </div>
        )}
        <div className="absolute top-2 left-2">
          <span className="px-2 py-1 bg-black/60 text-white text-[10px] font-bold rounded-lg">
            {episode.stationName.replace(/역$/, "")}역
          </span>
        </div>
      </div>
      <div className="flex flex-col flex-1">
        <h4 className="text-gray-900 font-bold mb-1 line-clamp-1">{episode.title}</h4>
        <p className="text-gray-500 text-xs line-clamp-2 leading-relaxed">
          {episode.stationName}의 이야기입니다.
        </p>
      </div>
    </button>
  );

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
      <header className="sticky top-0 z-50 w-full bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-4xl mx-auto px-4 h-16 flex items-center justify-between">
          <button onClick={onBack} className="flex items-center gap-2 text-gray-700 hover:text-blue-600 font-bold transition-colors">
            <ArrowLeft className="w-5 h-5" />
            <span>돌아가기</span>
          </button>
          <h1 className="text-blue-600 font-bold tracking-widest text-xl">HISUBTORY</h1>
          <div className="w-24"></div> 
        </div>
      </header>

      <main className="flex-1 max-w-4xl mx-auto w-full px-4 py-8">
        <div className="bg-white rounded-2xl shadow-md p-8 mb-8 border border-gray-100">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">{user.name}님의 여행 기록</h2>
          <div className="flex flex-wrap gap-4">
            <div className="flex items-center gap-2 bg-green-50 px-4 py-2 rounded-xl border border-green-100">
              <Check className="w-5 h-5 text-green-600" />
              <span className="text-gray-700 font-bold">시청 완료: {recentStories.length}</span>
            </div>
            <div className="flex items-center gap-2 bg-blue-50 px-4 py-2 rounded-xl border border-blue-100">
              <Bookmark className="w-5 h-5 text-blue-600" />
              <span className="text-gray-700 font-bold">내 보관함: {myStories.length}</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
          <div className="flex border-b border-gray-200 bg-gray-50/50">
            <button
              onClick={() => setActiveTab('recent')}
              className={`flex-1 py-4 flex items-center justify-center gap-2 font-bold transition-all ${
                activeTab === 'recent' ? 'bg-white text-blue-600 border-b-4 border-blue-600' : 'text-gray-500 hover:bg-gray-100'
              }`}
            >
              <Clock className="w-5 h-5" />
              <span>최근 본 이야기</span>
            </button>
            <button
              onClick={() => setActiveTab('saved')}
              className={`flex-1 py-4 flex items-center justify-center gap-2 font-bold transition-all ${
                activeTab === 'saved' ? 'bg-white text-blue-600 border-b-4 border-blue-600' : 'text-gray-500 hover:bg-gray-100'
              }`}
            >
              <LibraryIcon className="w-5 h-5" />
              <span>내 보관함</span>
            </button>
          </div>

          <div className="p-6 bg-white">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {activeTab === 'recent' ? (
                recentStories.length === 0 ? <p className="col-span-full text-center py-20 text-gray-400 font-medium">시청 기록이 없습니다.</p> : recentStories.map(renderStoryCard)
              ) : (
                myStories.length === 0 ? <p className="col-span-full text-center py-20 text-gray-400 font-medium">보관함이 비어있습니다.</p> : myStories.map(renderStoryCard)
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}