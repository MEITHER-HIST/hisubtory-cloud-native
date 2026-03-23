// src/utils/mediaUrl.ts
const CDN_BASE = (import.meta.env.VITE_CDN_BASE_URL || "").replace(/\/$/, "");

// S3 도메인이 섞여서 오는 경우(하드코딩/DB에 저장된 URL 치환용)
// 필요 없으면 빈 배열로 두면 됨.
const S3_HOSTS = [
    "d27nsin45nib0r.cloudfront.net"
];

function isAbsoluteUrl(u: string) {
  return /^https?:\/\//i.test(u);
}

export function mediaUrl(input?: string | null): string {
  if (!input) return "";

  // 이미 CloudFront면 그대로
  if (CDN_BASE && input.startsWith(CDN_BASE)) return input;

  // 절대 URL이면:
  // 1) S3 호스트면 CloudFront로 치환
  if (isAbsoluteUrl(input)) {
    try {
      const url = new URL(input);
      if (CDN_BASE && S3_HOSTS.includes(url.host)) {
        return `${CDN_BASE}${url.pathname}`;
      }
      // S3가 아니면 그냥 그대로 사용(외부 이미지 등)
      return input;
    } catch {
      return input;
    }
  }

  // 상대경로면 CloudFront 붙이기
  // 예: "media/webtoons/..." 또는 "/media/webtoons/..."
  const path = input.startsWith("/") ? input : `/${input}`;
  return CDN_BASE ? `${CDN_BASE}${path}` : path;
}
