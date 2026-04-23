const STREAM_URL = '/ask/stream';
const FALLBACK_URL = '/ask';

async function askQuestion() {
    const input = document.getElementById("question");
    const chat = document.getElementById("chat");

    const question = input.value.trim();
    if (!question) return;

    input.value = "";

    const userMsg = document.createElement("div");
    userMsg.className = "message user-message";
    userMsg.textContent = question;
    chat.appendChild(userMsg);

    const thinkingId = "think-" + Date.now();

    chat.innerHTML += `
    <div id="${thinkingId}" class="message bot-message thinking">
        Thinking
        <span class="dots">
            <span></span>
            <span></span>
            <span></span>
        </span>
    </div>
    `;

    chat.scrollTop = chat.scrollHeight;

    const bubble = document.getElementById(thinkingId);

    try {
        const res = await fetch(STREAM_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });

        if (!res.ok || !res.body) throw new Error("Stream unavailable");

        bubble.classList.remove("thinking");
        bubble.innerHTML = "";

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let accumulated = "";
        let buffer = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split("\n");
            buffer = lines.pop();

            for (const line of lines) {
                if (!line.startsWith("data: ")) continue;
                const payload = line.slice(6);
                if (payload.trim() === "[DONE]") {
                    bubble.innerHTML = marked.parse(accumulated);
                    chat.scrollTop = chat.scrollHeight;
                    return;
                }
                try {
                    const parsed = JSON.parse(payload);
                    if (parsed.error) {
                        bubble.textContent = parsed.error;
                        return;
                    }
                    if (parsed.token) {
                        accumulated += parsed.token;
                        bubble.innerHTML = marked.parse(accumulated);
                        chat.scrollTop = chat.scrollHeight;
                    }
                } catch {}
            }
        }

        if (accumulated) {
            bubble.innerHTML = marked.parse(accumulated);
        } else {
            bubble.textContent = "No response received.";
        }
    } catch {
        try {
            const res = await fetch(FALLBACK_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question })
            });
            const data = await res.json();
            bubble.classList.remove("thinking");
            bubble.innerHTML = marked.parse(data.answer);
        } catch {
            bubble.classList.remove("thinking");
            bubble.innerHTML = "Sorry, I'm having trouble connecting right now.";
        }
    }

    chat.scrollTop = chat.scrollHeight;
}

document.getElementById("question").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        askQuestion();
    }
});

function quickAsk(text) {
    document.getElementById("question").value = text;
    askQuestion();
}
