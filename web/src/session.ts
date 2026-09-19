const SESSION_KEY = "dmb_langchat_session";

export function getSessionId(): string {
  let id = localStorage.getItem(SESSION_KEY);
  if (id && id.length >= 8) return id;
  id =
    typeof crypto !== "undefined" && "randomUUID" in crypto
      ? crypto.randomUUID()
      : `sess_${Date.now()}_${Math.random().toString(36).slice(2)}`;
  localStorage.setItem(SESSION_KEY, id);
  return id;
}
