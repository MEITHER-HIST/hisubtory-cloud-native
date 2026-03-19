import { useState } from "react";
import { X } from "lucide-react";
import type { User } from "../App"; // App.tsx에서 export한 User 타입 사용

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
  onLogin: (user: User) => void; // ✅ username string → User 객체로 변경
}

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

  const text = await res.text();
  let data: any = null;
  try {
    data = JSON.parse(text);
  } catch {
    data = null;
  }
  return { res, data, text };
}

function prettyErrors(errors: any): string {
  if (!errors) return "요청에 실패했습니다.";
  // Django form.errors는 {field: ["msg",...]} 형태가 많음
  try {
    const lines: string[] = [];
    for (const [k, v] of Object.entries(errors)) {
      if (Array.isArray(v)) lines.push(`${k}: ${v.join(", ")}`);
      else lines.push(`${k}: ${String(v)}`);
    }
    return lines.join("\n");
  } catch {
    return "입력값을 확인해 주세요.";
  }
}

export function LoginModal({ isOpen, onClose, onLogin }: LoginModalProps) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [activeTab, setActiveTab] = useState<"login" | "signup">("login");

  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  if (!isOpen) return null;

  const fetchMeAndLogin = async () => {
    const meRes = await fetch("/api/accounts/me/", { credentials: "include" });
    const meText = await meRes.text();
    let me: any = null;
    try {
      me = JSON.parse(meText);
    } catch {
      me = null;
    }

    if (!meRes.ok || !me?.success) {
      throw new Error("me_failed");
    }

    const u: User = {
      id: me.id,
      username: me.username,
      email: me.email ?? "",
      name: me.username, // UI에서 name 쓰는 곳 대비
    };
    onLogin(u);
  };

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);

    if (!email.trim() || !password.trim()) {
      setErr("이메일과 비밀번호를 입력해 주세요.");
      return;
    }

    setLoading(true);
    try {
      const { res, data, text } = await postForm("/api/accounts/login/", {
        email: email.trim(),
        password,
      });

      if (!res.ok || !data?.success) {
        setErr(data?.message ?? text ?? "로그인 실패");
        return;
      }

      await fetchMeAndLogin();
      setPassword("");
    } catch (e) {
      setErr("네트워크 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  const handleSignupSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);

    if (!username.trim() || !email.trim() || !password.trim() || !confirmPassword.trim()) {
      setErr("모든 항목을 입력해 주세요.");
      return;
    }
    if (password !== confirmPassword) {
      setErr("비밀번호가 일치하지 않습니다.");
      return;
    }

    setLoading(true);
    try {
      // ✅ Django SignupForm(UserCreationForm)이면 password1/password2가 정석
      const { res, data, text } = await postForm("/api/accounts/signup/", {
        username: username.trim(),
        email: email.trim(),
        password1: password,
        password2: confirmPassword,
      });

      if (!res.ok || !data?.success) {
        if (data?.errors) setErr(prettyErrors(data.errors));
        else setErr(data?.message ?? text ?? "회원가입 실패");
        return;
      }

      // ✅ 회원가입 직후 자동 로그인(세션 생성)
      const loginTry = await postForm("/api/accounts/login/", {
        email: email.trim(),
        password,
      });
      if (!loginTry.res.ok || !loginTry.data?.success) {
        setActiveTab("login");
        setErr("회원가입은 완료됐지만 로그인에 실패했어요. 로그인 탭에서 다시 시도해 주세요.");
        return;
      }

      await fetchMeAndLogin();

      setUsername("");
      setPassword("");
      setConfirmPassword("");
    } catch {
      setErr("네트워크 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 relative">
        <button
          onClick={() => {
            setErr(null);
            onClose();
          }}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
          aria-label="close"
        >
          <X className="w-6 h-6" />
        </button>

        <h2 className="text-gray-900 mb-6">환영합니다!</h2>

        <div className="flex gap-2 mb-6 bg-gray-100 p-1 rounded-lg">
          <button
            type="button"
            onClick={() => {
              setErr(null);
              setActiveTab("login");
            }}
            className={`flex-1 py-2 rounded-md transition-all ${
              activeTab === "login" ? "bg-white text-blue-600 shadow-sm" : "text-gray-600 hover:text-gray-900"
            }`}
          >
            로그인
          </button>
          <button
            type="button"
            onClick={() => {
              setErr(null);
              setActiveTab("signup");
            }}
            className={`flex-1 py-2 rounded-md transition-all ${
              activeTab === "signup" ? "bg-white text-blue-600 shadow-sm" : "text-gray-600 hover:text-gray-900"
            }`}
          >
            회원가입
          </button>
        </div>

        {err && (
          <div className="mb-4 p-3 rounded-lg bg-red-50 text-red-700 text-sm border border-red-100 whitespace-pre-wrap">
            {err}
          </div>
        )}

        {activeTab === "login" && (
          <form onSubmit={handleLoginSubmit}>
            <div className="mb-4">
              <label htmlFor="login-email" className="block text-gray-700 mb-2">
                이메일
              </label>
              <input
                type="email"
                id="login-email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                placeholder="example@email.com"
                autoFocus
                autoComplete="email"
              />
            </div>

            <div className="mb-6">
              <label htmlFor="login-password" className="block text-gray-700 mb-2">
                비밀번호
              </label>
              <input
                type="password"
                id="login-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                placeholder="비밀번호를 입력하세요"
                autoComplete="current-password"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className={`w-full py-3 rounded-lg transition-colors ${
                loading ? "bg-blue-300 text-white cursor-not-allowed" : "bg-blue-600 text-white hover:bg-blue-700"
              }`}
            >
              {loading ? "처리 중..." : "로그인"}
            </button>
          </form>
        )}

        {activeTab === "signup" && (
          <form onSubmit={handleSignupSubmit}>
            <div className="mb-4">
              <label htmlFor="signup-username" className="block text-gray-700 mb-2">
                사용자 이름
              </label>
              <input
                type="text"
                id="signup-username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                placeholder="이름을 입력하세요"
                autoFocus
                autoComplete="username"
              />
            </div>

            <div className="mb-4">
              <label htmlFor="signup-email" className="block text-gray-700 mb-2">
                이메일
              </label>
              <input
                type="email"
                id="signup-email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                placeholder="example@email.com"
                autoComplete="email"
              />
            </div>

            <div className="mb-4">
              <label htmlFor="signup-password" className="block text-gray-700 mb-2">
                비밀번호
              </label>
              <input
                type="password"
                id="signup-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                placeholder="비밀번호를 입력하세요"
                autoComplete="new-password"
              />
            </div>

            <div className="mb-6">
              <label htmlFor="signup-confirm-password" className="block text-gray-700 mb-2">
                비밀번호 확인
              </label>
              <input
                type="password"
                id="signup-confirm-password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                placeholder="비밀번호를 다시 입력하세요"
                autoComplete="new-password"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className={`w-full py-3 rounded-lg transition-colors ${
                loading ? "bg-blue-300 text-white cursor-not-allowed" : "bg-blue-600 text-white hover:bg-blue-700"
              }`}
            >
              {loading ? "처리 중..." : "회원가입"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
