// src/api/auth.ts

function getCookie(name: string) {
  const v = `; ${document.cookie}`;
  const parts = v.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()!.split(";").shift() ?? null;
  return null;
}

async function ensureCsrf() {
  // CSRF 쿠키 발급
  await fetch("/api/accounts/csrf/", {
    method: "GET",
    credentials: "include",
  });
}

/**
 * 전송 방식을 JSON으로 변경하여 장고의 DRF(request.data)와 호환성을 높였습니다.
 */
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

  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.message || "request_failed");
  return data;
}

export const authApi = {
  login: (email: string, password: string) =>
    postForm("/api/accounts/login/", { email, password }),

  logout: () => postForm("/api/accounts/logout/", {}),

  me: async () => {
    const res = await fetch("/api/accounts/me/", { credentials: "include" });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data?.message || "not_logged_in");
    return data;
  },
};