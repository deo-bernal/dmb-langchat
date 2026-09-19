import { useEffect, useRef, useState } from "react";
import { streamSiteChat, type SiteChatMessage } from "./roboCopChat";

const SITE = "https://www.dmbwebsolutions.com";
const ASSISTANT_ICON = `${import.meta.env.BASE_URL}images/icons/dmb-assistant.jpg`;

const WELCOME: SiteChatMessage = {
  role: "assistant",
  content:
    "Hi. I am DMB Assistant (Robocop). Ask about AI automation, free portfolio pages, or how LangChat works. I run on free-tier Groq and Gemini.",
};

export default function RoboCopWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<SiteChatMessage[]>([WELCOME]);
  const [inputText, setInputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [streamingText, setStreamingText] = useState("");
  const [showHint, setShowHint] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamingText, isLoading, isOpen]);

  useEffect(() => {
    if (isOpen) return;
    const t = window.setTimeout(() => setShowHint(true), 2500);
    return () => window.clearTimeout(t);
  }, [isOpen]);

  async function send(text: string) {
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;
    const nextMessages: SiteChatMessage[] = [...messages, { role: "user", content: trimmed }];
    setMessages(nextMessages);
    setInputText("");
    setIsLoading(true);
    setStreamingText("");
    try {
      const reply = await streamSiteChat(nextMessages, setStreamingText);
      setMessages([...nextMessages, { role: "assistant", content: reply || "(empty reply)" }]);
    } catch (err) {
      setMessages([
        ...nextMessages,
        {
          role: "assistant",
          content: err instanceof Error ? err.message : "Chat failed.",
        },
      ]);
    } finally {
      setStreamingText("");
      setIsLoading(false);
    }
  }

  return (
    <div className="robocop">
      {!isOpen && (
        <div className="robocop-launcher-wrap">
          {showHint && (
            <button
              type="button"
              className="robocop-hint"
              onClick={() => {
                setIsOpen(true);
                setShowHint(false);
              }}
            >
              Agentic AI · Robocop
            </button>
          )}
          <button
            type="button"
            className="robocop-launcher"
            aria-label="Open Agentic AI Robocop chat"
            onClick={() => {
              setIsOpen(true);
              setShowHint(false);
            }}
          >
            <img src={ASSISTANT_ICON} alt="" width={88} height={88} />
          </button>
        </div>
      )}

      {isOpen && (
        <div className="robocop-panel" role="dialog" aria-label="DMB Assistant">
          <header className="robocop-header">
            <div className="robocop-header-brand">
              <img src={ASSISTANT_ICON} alt="" width={44} height={44} />
              <div>
                <strong>DMB Assistant</strong>
                <span>{isLoading ? "Typing..." : "Agentic AI · Robocop"}</span>
              </div>
            </div>
            <div className="robocop-header-actions">
              <a href={`${SITE}/accent-sidebar/agent`} title="Open Agentic AI">
                ✦
              </a>
              <button type="button" aria-label="Close chat" onClick={() => setIsOpen(false)}>
                ×
              </button>
            </div>
          </header>

          <div className="robocop-messages">
            {messages.map((message, index) => (
              <div
                key={`${message.role}-${index}`}
                className={`robocop-bubble ${message.role === "user" ? "user" : "assistant"}`}
              >
                {message.content}
              </div>
            ))}
            {streamingText ? (
              <div className="robocop-bubble assistant">
                {streamingText}
                <span className="robocop-cursor" />
              </div>
            ) : null}
            {isLoading && !streamingText ? (
              <div className="robocop-bubble assistant robocop-typing">
                <span />
                <span />
                <span />
              </div>
            ) : null}
            <div ref={endRef} />
          </div>

          <footer className="robocop-composer">
            <input
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  void send(inputText);
                }
              }}
              placeholder="Type a message..."
              disabled={isLoading}
            />
            <button
              type="button"
              disabled={!inputText.trim() || isLoading}
              onClick={() => void send(inputText)}
            >
              Send
            </button>
            <p>Free-tier AI — rate limits apply. Same assistant as the main site.</p>
          </footer>
        </div>
      )}
    </div>
  );
}
