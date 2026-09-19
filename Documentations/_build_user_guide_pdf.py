from pathlib import Path

from _pdf_kit import new_doc, write_pdf

OUT = Path(__file__).resolve().parent / "DMB-LangChat-User-Guide.pdf"


def build():
    pdf = new_doc(
        "DMB LangChat  |  User guide",
        "How to use durable LangChain chat",
    )
    pdf.cover(
        "DMB LANGCHAT",
        "User guide",
        "How the product runs, with live test scenarios",
        "User documentation  |  19 September 2026",
    )

    pdf.business(
        headline=(
            "Use LangChat to prove memory: say your name, refresh, ask again. If it remembers, "
            "Convex did its job."
        ),
        problem="People do not trust AI demos that forget them after F5.",
        customer="Anyone with the deployed URL on the same browser session.",
        money="Demo for custom AI work — not a paid SKU yet.",
        flow=[
            [("New chat", "dark")],
            ["Tell it your name"],
            ["Refresh the page"],
            [("Ask 'what is my name?' — it answers", "ok")],
        ],
        flow_caption="Figure B1. The one scenario that matters.",
        loop_rows=[
            ["Open", "Load the web app.", "Session id is created automatically."],
            ["Talk", "Send 2-3 messages.", "Bubbles appear; AI replies."],
            ["Prove", "Hard refresh.", "Same thread still listed and filled."],
            ["Isolate", "Open a private window.", "Empty threads — different session."],
        ],
        kpis=[
            "Memory survives refresh.",
            "Private window does not see your threads.",
            "/health shows convexConfigured and modelConfigured true.",
        ],
    )

    pdf.h1("1. How to use this guide")
    pdf.p(
        "Run these on the deployed LangChat URL (or local Vite + API). First Render request after "
        "sleep can take ~30-60s."
    )

    pdf.h1("2. Modules")
    pdf.table(
        ["UI", "Why"],
        [
            ["New chat", "Start a fresh Convex thread."],
            ["Thread list", "Switch among saved conversations for this browser session."],
            ["Composer", "Sends to Python LangChain; reply is stored then streamed via Convex query."],
        ],
        [48, 130],
    )

    pdf.scenario(
        1,
        "Durable memory smoke test",
        ["LangChat web open; API healthy."],
        [
            "Click New chat.",
            "Send: My name is Alice and I love pizza.",
            "Wait for the AI reply.",
            "Hard refresh the browser (Ctrl+F5).",
            "Open the same thread. Send: What is my name and what do I like?",
        ],
        [
            "After refresh the first messages are still visible.",
            "The AI answer mentions Alice and pizza (or equivalent).",
        ],
    )

    pdf.scenario(
        2,
        "Session isolation",
        ["Scenario 1 done in a normal window."],
        [
            "Open a private/incognito window to the same LangChat URL.",
            "Confirm the thread list does not show Alice's chat.",
            "Create a new chat and send Hi from private.",
        ],
        ["Private session has its own threads. Normal window still has Alice."],
    )

    pdf.scenario(
        3,
        "API health",
        ["API base URL known (Render)."],
        [
            "GET {API}/health",
            "Confirm ok true, convexConfigured true, modelConfigured true.",
        ],
        ["If modelConfigured is false, set GOOGLE_API_KEY on Render and redeploy."],
    )

    pdf.h1("3. What you should not expect yet")
    pdf.bullet("Google / Facebook login (Phase 2).")
    pdf.bullet("Document upload / RAG.")
    pdf.bullet("Shared threads across devices without copying sessionId.")

    pdf.end_note("End of document. Architecture and Auth PDFs live in the same Documentations folder.")
    write_pdf(pdf, OUT)


if __name__ == "__main__":
    build()
