async function askQuestion() {
    const input = document.getElementById("question");
    const chat = document.getElementById("chat");

    const question = input.value.trim();
    if (!question) return;

    input.value = "";

    chat.innerHTML += `
        <div class="message user-message">
            ${question}
        </div>
    `;

    const thinkingId = "think-" + Date.now();
    
    chat.innerHTML += `
        <div id="${thinkingId}" class="message bot-message thinking">
            ChatDIS is thinking...
        </div>
    `;

    chat.scrollTop = chat.scrollHeight;

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        const thinkingBubble = document.getElementById(thinkingId);
        
        thinkingBubble.classList.remove("thinking");
        
        thinkingBubble.innerHTML = marked.parse(data.answer);

    } catch (error) {
        const thinkingBubble = document.getElementById(thinkingId);
        if (thinkingBubble) {
            thinkingBubble.classList.remove("thinking");
            thinkingBubble.innerHTML = "Sorry, I'm having trouble connecting right now.";
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
