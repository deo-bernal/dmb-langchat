import { useEffect, useMemo, useRef, useState } from "react";
import { useMutation, useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import type { Id } from "../../convex/_generated/dataModel";
import { getSessionId } from "./session";
import RoboCopWidget from "./RoboCopWidget";

const configuredApi = (import.meta.env.VITE_API_URL as string | undefined)?.trim() || "";
// Production uses same-origin /langchat/api (Vercel rewrite → live Render host) to avoid CORS
// and the suspended dmb-langchat-api.onrender.com hostname.
const API_URL = import.meta.env.DEV
  ? configuredApi || "http://localhost:8080"
  : `${import.meta.env.BASE_URL}api`;
const SITE = "https://www.dmbwebsolutions.com";
const logoSrc = `${import.meta.env.BASE_URL}dmb-web-solutions-logo.png`;

export default function App() {
  const sessionId = useMemo(() => getSessionId(), []);
  const threads = useQuery(api.threads.listBySession, { sessionId });
  const createThread = useMutation(api.threads.create);

  const [threadId, setThreadId] = useState<Id<"threads"> | null>(null);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  const messages = useQuery(
    api.messages.listByThread,
    threadId ? { threadId } : "skip"
  );

  useEffect(() => {
    if (!threadId && threads && threads.length > 0) {
      setThreadId(threads[0]._id);
    }
  }, [threads, threadId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, busy]);

  async function onNewChat() {
    setError(null);
    const id = await createThread({ sessionId, title: "New chat" });
    setThreadId(id);
  }

  async function onSend() {
    const text = draft.trim();
    if (!text || busy) return;
    setBusy(true);
    setError(null);
    setDraft("");
    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sessionId,
          threadId: threadId ?? undefined,
          message: text,
        }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : `Chat failed (${res.status})`
        );
      }
      if (data.threadId && data.threadId !== threadId) {
        setThreadId(data.threadId as Id<"threads">);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
      setDraft(text);
    } finally {
      setBusy(false);
    }
  }

  const activeTitle =
    threads?.find((t: { _id: Id<"threads">; title: string }) => t._id === threadId)?.title ||
    "Conversation";

  return (
    <div className="app-frame">
      <div className="app-body">
        <div className="shell">
          <aside className="nav">
            <a className="brand-wrap" href={`${SITE}/ai-automation`}>
              <span className="brand">
                <img src={logoSrc} alt="" width={48} height={48} />
                <span className="brand-name">
                  LangChat
                  <span className="brand-sub">LangChain memory on Convex</span>
                </span>
              </span>
            </a>

            <button className="secondary" type="button" onClick={() => void onNewChat()}>
              New chat
            </button>

            <div className="nav-stack">
              <div className="nav-label">Threads</div>
              <ul className="thread-list">
                {(threads ?? []).map((t: { _id: Id<"threads">; title: string }) => (
                  <li key={t._id}>
                    <button
                      type="button"
                      className={t._id === threadId ? "active" : ""}
                      onClick={() => setThreadId(t._id)}
                    >
                      {t.title}
                    </button>
                  </li>
                ))}
              </ul>

              <div className="nav-label">Workspace</div>
              <a href={`${SITE}/crm`}>CRM</a>
              <a href={`${SITE}/lms`}>LMS</a>
              <a href={`${SITE}/commerce`}>Commerce</a>
              <a href={`${SITE}/agent`}>Agent</a>
              <a href={`${SITE}/accent-sidebar/portfolio`}>Portfolio</a>
              <a href={SITE}>Website</a>
            </div>

            <a className="nav-also" href={`${SITE}/profiles#lots`}>
              Also: lots in Pampanga
            </a>
          </aside>

          <main className="main">
            <div className="main-panel">
              <div className="toolbar">
                <div>
                  <h1>{activeTitle}</h1>
                  <p>Messages persist in Convex. Refresh the page — your thread is still here.</p>
                </div>
              </div>

              <div className="messages">
                {!threadId && (
                  <div className="empty">
                    <strong>Start a thread</strong>
                    Ask anything. History is stored permanently (unlike the lab RAM list).
                  </div>
                )}
                {(messages ?? []).map((m: { _id: string; role: string; content: string }) => (
                  <div key={m._id} className={`bubble ${m.role === "human" ? "human" : "ai"}`}>
                    {m.content}
                  </div>
                ))}
                {busy && <div className="bubble ai">Thinking…</div>}
                <div ref={bottomRef} />
              </div>

              {error ? <div className="error">{error}</div> : null}

              <div className="composer">
                <textarea
                  value={draft}
                  placeholder="Message LangChat…"
                  onChange={(e) => setDraft(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault();
                      void onSend();
                    }
                  }}
                />
                <button type="button" disabled={busy || !draft.trim()} onClick={() => void onSend()}>
                  Send
                </button>
              </div>
            </div>
          </main>
        </div>
      </div>

      <footer className="site-footer">
        © {new Date().getFullYear()} DMB Web Solutions ·{" "}
        <a href={SITE}>dmbwebsolutions.com</a>
      </footer>

      <RoboCopWidget />
    </div>
  );
}
