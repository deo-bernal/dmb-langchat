from pathlib import Path

from _pdf_kit import new_doc, write_pdf

OUT = Path(__file__).resolve().parent / "DMB-LangChat-SSO-Implementation.pdf"


def build():
    pdf = new_doc(
        "DMB LangChat  |  Auth / SSO",
        "Session threads  ·  Convex Free",
    )
    pdf.cover(
        "DMB LANGCHAT",
        "SSO / Auth implementation",
        "Phase 1 session identity (not marketing OAuth hub)",
        "Technical documentation  |  19 September 2026  |  Web + Python API + Convex",
    )

    pdf.business(
        headline=(
            "LangChat is a durable-memory assistant. Phase 1 auth is a browser session id so "
            "history sticks without forcing Google login. That lowers the barrier to try the product."
        ),
        problem=(
            "The Python lab stored chat in RAM. Refresh meant amnesia. Marketing SSO is a shared "
            "OAuth hub for three products — too heavy for a first LangChain demo."
        ),
        customer=(
            "You (Deo) and anyone you send the LangChat URL to. They are not CRM contacts or LMS parents."
        ),
        money=(
            "This MVP does not bill. Value is proof that LangChain + Convex memory works on free tiers "
            "so you can sell custom AI chat with permanent history."
        ),
        flow=[
            [("Visitor opens LangChat", "dark")],
            ["Browser creates sessionId in localStorage"],
            ["Threads scoped to that session in Convex"],
            [("Refresh keeps the conversation", "ok")],
        ],
        flow_caption="Figure B1. Phase 1 identity is a session cookie-equivalent, not Google OAuth.",
        loop_rows=[
            ["Arrive", "Open the web app.", "getSessionId() writes localStorage."],
            ["Chat", "Send a message.", "API checks thread.sessionId matches."],
            ["Return", "Same browser later.", "Same sessionId -> same threads."],
            ["Later SSO", "Optional Google via Convex Auth.", "Documented as Phase 2 — not required for MVP."],
        ],
        kpis=[
            "Refresh does not wipe threads for the same browser.",
            "Another browser/session cannot read your threadIds (403 on mismatch).",
            "No Render wake page or marketing /auth/callback involved.",
        ],
        note="Do not register LangChat callbacks on the shared www Facebook/LinkedIn hub until Phase 2.",
    )

    pdf.h1("1. Purpose")
    pdf.p(
        "This document describes how DMB LangChat identifies users in Phase 1 and how that differs "
        "from DMB Web Solutions / CRM / LMS OAuth SSO. Secrets are never stored here."
    )

    pdf.h1("2. Phase 1 design")
    pdf.bullet("Client generates a UUID sessionId and stores it in localStorage (dmb_langchat_session).")
    pdf.bullet("Convex threads.sessionId scopes the thread list.")
    pdf.bullet("POST /chat requires sessionId; API rejects thread access if sessionId mismatches.")
    pdf.bullet("No JWT, no ExternalLogin table, no Vercel auth-external proxy.")
    pdf.flowchart(
        [
            [("localStorage sessionId", "dark")],
            ["threads:create / listBySession"],
            ["POST /chat with sessionId + threadId"],
            [("messages append in Convex", "ok")],
        ],
        caption="Figure 1. Auth surface for MVP.",
    )

    pdf.h1("3. Why not the marketing SSO hub")
    pdf.p(
        "Marketing, CRM, and LMS share Google/Facebook/LinkedIn apps with state prefixes crm. / lms. "
        "LangChat is a fourth product. Wiring it into that hub before the chat loop works would slow delivery "
        "and burn Hobby serverless capacity on the marketing site."
    )

    pdf.h1("4. Phase 2 (planned)")
    pdf.bullet("Convex Auth with Google (or Clerk) issuing a user id.")
    pdf.bullet("Replace sessionId with authenticated subject; migrate threads.")
    pdf.bullet("Optional link from www.dmbwebsolutions.com/langchat via real navigation.")

    pdf.h1("5. Environment (names only)")
    pdf.table(
        ["Name", "Where", "Role"],
        [
            ["CONVEX_URL", "Render api", "Deployment URL for convex-py"],
            ["VITE_CONVEX_URL", "Vercel web", "Same deployment for ConvexReactClient"],
            ["GOOGLE_API_KEY", "Render api", "Gemini for LangChain"],
            ["VITE_API_URL", "Vercel web", "Public URL of the Python API"],
        ],
        [40, 36, 102],
    )

    pdf.h1("6. Security notes")
    pdf.bullet("sessionId is bearer-like in the browser — anyone with the id can use that session.")
    pdf.bullet("Do not log full message bodies with PII in Render logs.")
    pdf.bullet("CORS_ORIGINS must list the production web origin.")

    pdf.end_note(
        "End of document. Pair with DMB-LangChat-System-Architecture.pdf and DMB-LangChat-User-Guide.pdf."
    )
    write_pdf(pdf, OUT)


if __name__ == "__main__":
    build()
