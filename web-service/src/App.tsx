import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { Toaster } from "sonner";
import { X } from "lucide-react";
import { MainScreen } from "./components/MainScreen";
import { StoryScreen } from "./components/StoryScreen";
import { MyPage } from "./components/MyPage";
import { LoginModal } from "./components/LoginModal";

type Screen = "main" | "story" | "mypage";

export type User = {
  id: number;
  username: string;
  email: string;
  name: string;
};

function getCookie(name: string) {
  const v = `; ${document.cookie}`;
  const parts = v.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()!.split(";").shift() ?? null;
  return null;
}

async function ensureCsrf() {
  await fetch("/api/accounts/csrf/", {
    method: "GET",
    credentials: "include",
  });
}

async function postForm(url: string, body: Record<string, string>) {
  await ensureCsrf();
  const csrftoken = getCookie("csrftoken") ?? "";
  const res = await fetch(url, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
      "X-CSRFToken": csrftoken,
    },
    body: new URLSearchParams(body).toString(),
  });
  return res;
}

export default function App() {
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [user, setUser] = useState<User | null>(null);

  const [currentScreen, setCurrentScreen] = useState<Screen>("main");
  const [selectedStationId, setSelectedStationId] = useState<string | null>(null);
  const [selectedEpisodeId, setSelectedEpisodeId] = useState<string | null>(null);
  const [currentLine, setCurrentLine] = useState<string>("3");

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch("/api/accounts/me/", { credentials: "include" });
        const data = await res.json().catch(() => null);
        if (res.ok && data?.is_authenticated) {
          const u: User = {
            id: data.id || 0,
            username: data.username,
            email: data.email ?? "",
            name: data.username,
          };
          setUser(u);
        } else {
          setUser(null);
        }
      } catch {
        setUser(null);
      }
    })();
  }, []);

  const handleLogin = (u: User) => {
    setUser(u);
    setIsLoginModalOpen(false);
  };

  const handleLogout = async () => {
    try {
      await postForm("/api/accounts/logout/", {});
    } catch {
      // 에러 무시
    } finally {
      setUser(null);
      setCurrentScreen("main");
    }
  };

  const handleStationClick = (stationId: string, episodeId: string) => {
    setSelectedStationId(stationId);
    setSelectedEpisodeId(episodeId);
    setCurrentScreen("story");
  };

  const handleRandomStation = (stationName: string, episodeId: string) => {
    setSelectedStationId(stationName);
    setSelectedEpisodeId(episodeId);
    setCurrentScreen("story");
  };

  const [mainKey, setMainKey] = useState(0);

  const handleBackToMain = () => {
    setMainKey(prev => prev + 1);
    setCurrentScreen("main");
    setSelectedStationId(null);
    setSelectedEpisodeId(null);
  };

  const handleGoToMyPage = () => {
    if (!user) {
      setIsLoginModalOpen(true);
      return;
    }
    setCurrentScreen("mypage");
  };

  const handleEpisodeClick = (episodeId: string) => {
    setSelectedEpisodeId(episodeId);
    setSelectedStationId(null);
    setCurrentScreen("story");
  };

  return (
    <div className="min-h-screen bg-white overflow-x-hidden">
      {isSidebarOpen && currentScreen === "main" && createPortal(
        <div 
          className="fixed inset-0 z-[10000] bg-black/40 animate-in fade-in duration-300" 
          onClick={() => setIsSidebarOpen(false)}
        >
          <div 
            className="absolute left-0 w-96 h-full bg-white shadow-2xl animate-in slide-in-from-left duration-300 flex flex-col"
            style={{ top: '65px' }} 
            onClick={e => e.stopPropagation()}
          >
            <div className="flex items-center justify-between px-8 py-6 bg-white border-b border-gray-100">
              <h2 className="text-xl font-black text-gray-800 tracking-tight">Menu</h2>
              <button 
                onClick={() => setIsSidebarOpen(false)} 
                className="p-2 hover:bg-gray-100 rounded-full transition-colors outline-none"
              >
                <X className="w-6 h-6 text-gray-400 hover:text-gray-900 stroke-[2.5px]" /> 
              </button>
            </div>
            
            <div className="flex-1 overflow-y-auto px-8 pt-10 pb-24 flex flex-col gap-6">
              {Array.from({ length: 9 }, (_, i) => {
                const lineId = (i + 1).toString();
                const isLine3 = lineId === "3";
                const isActive = currentLine === lineId;
                const lineColors: Record<string, string> = {
                  "1": "#0052A4", "2": "#00A84D", "3": "#EF7C1C", "4": "#00A5DE",
                  "5": "#996CAC", "6": "#CD7C2F", "7": "#747F00", "8": "#E6186C", "9": "#BB8336",
                };
                const currentLineColor = lineColors[lineId] || "#cbd5e1";

                return (
                  <button
                    key={lineId}
                    disabled={!isLine3}
                    onClick={() => {
                      if (isLine3) {
                        setCurrentLine(lineId);
                        setIsSidebarOpen(false);
                      }
                    }}
                    className={`flex items-center gap-6 py-4 px-6 rounded-3xl font-black transition-all border outline-none ${
                      isLine3 
                        ? (isActive 
                            ? 'bg-blue-600 text-white shadow-xl scale-[1.02] border-transparent' 
                            : 'bg-white text-gray-700 hover:bg-gray-50 border-gray-100')
                        : 'bg-gray-50/50 text-gray-300 cursor-not-allowed opacity-60 border-transparent'
                    }`}
                  >
                    <div 
                      className={`w-5 h-5 rounded-full border-2 shrink-0 ${
                        isActive && isLine3 ? 'border-white' : 'border-transparent'
                      }`}
                      style={{ backgroundColor: isActive && isLine3 ? '#ffffff' : currentLineColor }}
                    />
                    <span className="text-base tracking-tight">{lineId}호선</span>
                    {!isLine3 && (
                      <span className="ml-auto text-[10px] bg-gray-200/60 text-gray-500 px-3 py-1 rounded-full font-bold">
                        준비중
                      </span>
                    )}
                  </button>
                );
              })}
            </div>

            <div className="p-8 bg-white border-t border-gray-50 mb-[65px]">
              <p className="text-[12px] text-gray-300 font-bold text-center italic tracking-[0.2em]">
                HISUBTORY
              </p>
            </div>
          </div>
        </div>,
        document.body
      )}

      {currentScreen === "main" && (
        <MainScreen
          key={`${mainKey}-${currentLine}`}
          user={user}
          currentLine={currentLine}
          onMenuClick={() => setIsSidebarOpen(true)}
          onLoginClick={() => setIsLoginModalOpen(true)}
          onLogout={handleLogout}
          onStationClick={handleStationClick}
          onRandomStation={handleRandomStation}
          onGoToMyPage={handleGoToMyPage}
        />
      )}

      {currentScreen === "story" && (
        <StoryScreen
          key={`story-${selectedEpisodeId}`}
          user={user}
          stationId={selectedStationId}
          episodeId={selectedEpisodeId}
          onBack={handleBackToMain}
          onNextEpisode={(newId) => setSelectedEpisodeId(newId)}
        />
      )}

      {currentScreen === "mypage" && (
        <MyPage user={user} onBack={handleBackToMain} onEpisodeClick={handleEpisodeClick} />
      )}

      <LoginModal
        isOpen={isLoginModalOpen}
        onClose={() => setIsLoginModalOpen(false)}
        onLogin={handleLogin}
      />
      <Toaster position="top-center" richColors />
    </div>
  );
}