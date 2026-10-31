const chatForm = document.getElementById("chat-form");
const questionInput = document.getElementById("question");
const chatBox = document.getElementById("chat-box");
const sendButton = document.getElementById("send-button");


function addMessage(message, sender) {
    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message", sender);
    messageDiv.textContent = message;

    chatBox.appendChild(messageDiv);

    // Automatically scroll to the latest message
    chatBox.scrollTop = chatBox.scrollHeight;
}


function formatResponse(data) {
    const result = data.result;

    switch (data.intent) {

        case "total_revenue":
            return `Total Revenue: ₹${result.toLocaleString("en-IN")}`;

        case "top_product":
            return `Highest Revenue Product: ${result.product}
Revenue: ₹${result.revenue.toLocaleString("en-IN")}`;

        case "top_region":
            return `Best Performing Region: ${result.region}
Revenue: ₹${result.revenue.toLocaleString("en-IN")}`;

        case "monthly_revenue":
            return result.map(item =>
                `${item.month}: ₹${item.revenue.toLocaleString("en-IN")}`
            ).join("\n");

        case "compare_months":
            const difference = result.difference;

            const comparison = difference >= 0
                ? `${result.month2} performed better`
                : `${result.month1} performed better`;

            return `Revenue Comparison:

${result.month1}: ₹${result.revenue1.toLocaleString("en-IN")}
${result.month2}: ₹${result.revenue2.toLocaleString("en-IN")}

Difference: ₹${Math.abs(difference).toLocaleString("en-IN")}
${comparison}`;

        default:
            return "I couldn't process that question.";
    }
}


chatForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    const question = questionInput.value.trim();

    if (!question) return;

    addMessage(question, "user");

    questionInput.value = "";
    sendButton.disabled = true;
    sendButton.textContent = "Thinking...";

    try {

        const response = await fetch("/ask", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong.");
        }

        const answer = formatResponse(data);

        addMessage(answer, "bot");

    } catch (error) {

        addMessage(
            "Sorry, I couldn't process your question. " + error.message,
            "bot"
        );

    } finally {

        sendButton.disabled = false;
        sendButton.textContent = "Send";
        questionInput.focus();

    }
});

