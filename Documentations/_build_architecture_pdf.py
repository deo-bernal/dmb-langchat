from pathlib import Path

from _pdf_kit import new_doc, write_pdf

OUT = Path(__file__).resolve().parent / "DMB-LangChat-System-Architecture.pdf"


def build():
    pdf = new_doc(
        "DMB LangChat  |  System architecture",
        "LangChain  ·  Python  ·  Convex Free",
    )
    pdf.cover(
        "DMB LANGCHAT",
        "System architecture",
        "Business and technical design, end to end",
        "Technical + business documentation  |  19 September 2026",
    )

    pdf.business(
        headline=(
            "LangChat proves the YouTube LangChain diagram: chatbot + knowledge + chat history in a "
            "real DATABASE. Convex Free is that database. Python LangChain is the brain."
        ),
        problem=(
            "Lab memory died on process exit. Buyers of custom AI chat ask 'will it remember me?' "
            "Without durable storage the answer is no."
        ),
        customer=(
            "DMB uses this as a demo product. End users are visitors chatting in a browser session."
        ),
        money=(
            "Not SaaS-billed yet. Demo value: show permanent memory on $0 Convex + Render + Vercel free tiers."
        ),
        flow=[
            [("User message in UI", "dark")],
            ["Python LangChain loads Convex history"],
            ["Gemini reply"],
            [("Human + AI rows saved in Convex", "ok")],
        ],
        flow_caption="Figure B1. Durable memory loop.",
        loop_rows=[
            ["Capture", "User types a message.", "Web POST /chat"],
            ["Recall", "API loads last N messages.", "messages:listByThread"],
            ["Think", "LangChain invokes Gemini.", "ChatGoogleGenerativeAI"],
            ["Remember", "Append human + AI.", "messages:append + thread title"],
            ["Show", "UI updates live.", "Convex useQuery subscription"],
        ],
        kpis=[
            "Refresh keeps history.",
            "Free-tier Convex stays under 1M calls / 0.5 GB for demo traffic.",
            "Cold Render wake still returns a reply (visitor may wait once).",
        ],
    )

    pdf.h1("1. What this product is")
    pdf.p(
        "DMB LangChat is a standalone sibling of dmbportfolio, CRM, and LMS. It is not tutoring and "
        "not a sales CRM. It is a LangChain chat with Convex-backed threads."
    )

    pdf.h1("2. Live system map")
    pdf.stack(
        [
            ("Browser  LangChat web (Vercel)", "dark"),
            ("Convex Cloud Free  threads + messages realtime", "accent"),
            ("Render Free  FastAPI + LangChain + convex-py", "default"),
            ("Google Gemini  (API key on Render only)", "ok"),
        ],
        caption="Figure 1. Three free hosts. Marketing site is not in the path.",
    )

    pdf.h1("3. Data model")
    pdf.table(
        ["Table", "Fields", "Indexes"],
        [
            ["threads", "sessionId, title, updatedAt", "by_session"],
            ["messages", "threadId, role, content, createdAt", "by_thread"],
        ],
        [40, 80, 58],
    )
    pdf.p("Roles: system | human | ai. First human message can rename title from 'New chat'.")

    pdf.h1("4. API surface")
    pdf.table(
        ["Method", "Path", "Purpose"],
        [
            ["GET", "/health", "Convex + model config flags"],
            ["POST", "/threads", "Create thread for sessionId"],
            ["POST", "/chat", "Append human, invoke model, append AI"],
        ],
        [28, 40, 110],
    )

    pdf.h1("5. Key files")
    pdf.table(
        ["Area", "Path"],
        [
            ["Schema", "convex/schema.ts"],
            ["Threads / messages", "convex/threads.ts, convex/messages.ts"],
            ["API", "api/main.py"],
            ["UI", "web/src/App.tsx"],
            ["Docs kit", "Documentations/_pdf_kit.py"],
        ],
        [48, 130],
    )

    pdf.h1("6. Free-tier limits to watch")
    pdf.bullet("Convex Free: hard caps (function calls, storage).")
    pdf.bullet("Render Free: sleeps; first chat after idle is slower.")
    pdf.bullet("Vercel Hobby: fine for a static/Vite SPA.")
    pdf.bullet("Never put GOOGLE_API_KEY in the web bundle.")

    pdf.h1("7. Out of scope")
    pdf.bullet("RAG / vector search, agent tools, payments, marketing SSO hub merge.")

    pdf.end_note("End of document. See also SSO/Auth and User Guide PDFs in this folder.")
    write_pdf(pdf, OUT)


if __name__ == "__main__":
    build()
