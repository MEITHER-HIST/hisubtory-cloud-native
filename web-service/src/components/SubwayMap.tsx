import { useState } from "react";
import { line3Stations } from "../data/stations";

// 데이터 구조 정의
type StationDTO = { 
  id: number; 
  name: string; 
  clickable: boolean; 
  color: "green" | "gray"; 
  is_viewed: boolean; 
};

interface SubwayMapProps {
  stationByName: Map<string | number, StationDTO>;
  onPickEpisode: (stationId: number) => void;
  isLoggedIn: boolean; // 로그인 상태 추가
}

export function SubwayMap({ stationByName, onPickEpisode, isLoggedIn }: SubwayMapProps) {
  const [hoveredStation, setHoveredStation] = useState<{name: string, dto: StationDTO | undefined} | null>(null);
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });

  const getStationPosition = (index: number) => {
    if (index <= 15) return { x: 100 + index * 70, y: 100 };
    if (index <= 30) return { x: 100 + (30 - index) * 70, y: 250 };
    return { x: 100 + (index - 30) * 70, y: 400 };
  };

  return (
    <div className="relative w-full bg-white rounded-2xl p-4 overflow-x-auto scrollbar-hide">
      <svg width="1200" height="550" className="mx-auto">
        {/* 지하철 노선 배경 */}
        <g stroke="#EF7C1C" strokeWidth="6" fill="none" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="100,100 1150,100 1150,250 100,250 100,400 1010,400" />
        </g>

        {line3Stations.map((stationName, index) => {
          const pos = getStationPosition(index);
          const cleanName = stationName.trim().replace(/역$/, "");
          const dto = stationByName.get(cleanName) || stationByName.get(stationName.trim());
          
          const isViewed = dto?.color === "green";
          // 클릭 가능 여부: 서버에서 로그인 여부를 판단하여 내려준 clickable 값 사용
          const canClick = dto?.clickable === true;

          return (
            <g key={index} 
               className={canClick ? "cursor-pointer" : "cursor-default"} 
               onClick={() => canClick && onPickEpisode(dto!.id)}>
              {/* 역 점(Dot) */}
              <circle
                cx={pos.x} cy={pos.y} r={hoveredStation?.name === stationName ? 13 : 10}
                fill={isViewed ? "#22c55e" : "#9ca3af"}
                stroke="white" strokeWidth="3"
                className="transition-all duration-200"
                onMouseEnter={(e) => {
                  const rect = e.currentTarget.getBoundingClientRect();
                  setHoveredStation({ name: stationName, dto });
                  setTooltipPosition({ 
                    x: rect.left + window.scrollX + rect.width / 2, 
                    y: rect.top + window.scrollY - 10 
                  });
                }}
                onMouseLeave={() => setHoveredStation(null)}
              />
              {/* ✅ [수정] 역 이름 위치: y값을 pos.y - 20으로 변경하여 라인 위로 배치 */}
              <text x={pos.x} y={pos.y - 20} textAnchor="middle" 
                    className={`text-[11px] font-bold pointer-events-none transition-colors ${isViewed ? "fill-green-600" : "fill-gray-400"}`}>
                {stationName}
              </text>
            </g>
          );
        })}
      </svg>

      {/* 동적 툴팁 */}
      {hoveredStation && (
        <div 
          className="fixed bg-white border border-gray-100 p-3 rounded-xl shadow-2xl z-[10000] transform -translate-x-1/2 -translate-y-full pointer-events-none min-w-[140px]"
          style={{ left: tooltipPosition.x, top: tooltipPosition.y }}
        >
          <div className="flex items-center gap-2 mb-1">
            <div className={`w-2 h-2 rounded-full ${hoveredStation.dto?.color === "green" ? "bg-green-500" : "bg-gray-300"}`} />
            <span className="font-bold text-sm text-gray-800">{hoveredStation.name}</span>
          </div>
          <p className="text-[11px] text-gray-500 whitespace-nowrap">
            {hoveredStation.dto?.color === "green" 
              ? "✅ 다시보기 가능" 
              : (isLoggedIn ? "🔒 미방문 역" : "🔒 로그인 후 이용 가능")}
          </p>
        </div>
      )}
    </div>
  );
}