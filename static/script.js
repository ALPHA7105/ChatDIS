async function askQuestion() {
    const input = document.getElementById("question");
    const chat = document.getElementById("chat");

    const question = input.value.trim();
    if (!question) return;

    // 1. Clear input
    input.value = "";

    // 2. Add User Message Bubble
    chat.innerHTML += `
        <div class="message user-message">
            ${question}
        </div>
    `;

    // Scroll to bottom
    chat.scrollTop = chat.scrollHeight;

    // 3. Fetch from Backend
    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        // 4. Add Bot Message Bubble
        chat.innerHTML += `
            <div class="message bot-message">
                ${data.answer}
            </div>
        `;
    } catch (error) {
        chat.innerHTML += `
            <div class="message bot-message">
                Sorry, I'm having trouble connecting right now.
            </div>
        `;
    }

    // Scroll to bottom again
    chat.scrollTop = chat.scrollHeight;
}

// Allow pressing "Enter" to send
document.getElementById("question").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        askQuestion();
    }
});
