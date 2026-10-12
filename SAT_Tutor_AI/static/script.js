
const questionBox = document.getElementById("question");
const askButton = document.getElementById("askButton");
const resultBox = document.getElementById("result");
const answerBox = document.getElementById("answer");
const tabs = document.querySelectorAll(".tab");
const exampleButtons = document.querySelectorAll(".example");

let selectedSection = "Math";

// Switch between SAT sections
tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    tabs.forEach((item) => item.classList.remove("active"));
    tab.classList.add("active");
    selectedSection = tab.dataset.section;
  });
});

// Fill the question box with an example
exampleButtons.forEach((button) => {
  button.addEventListener("click", () => {
    questionBox.value = button.dataset.question;
    questionBox.focus();
  });
});

// Send the question to Flask
askButton.addEventListener("click", async () => {
  const question = questionBox.value.trim();

  if (!question) {
    questionBox.focus();
    answerBox.textContent = "Please enter an SAT question first.";
    resultBox.hidden = false;
    return;
  }

  askButton.disabled = true;
  askButton.textContent = "Solving your question...";
  answerBox.textContent = "Your AI tutor is working through the problem. Please wait...";
  resultBox.hidden = false;

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: question,
        section: selectedSection,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || `Request failed (${response.status})`);
    }

    answerBox.textContent = data.answer || "No answer was returned. Please try again.";
  } catch (error) {
    answerBox.textContent =
      "Something went wrong: " + error.message +
      "\n\nCheck the VS Code terminal for more details.";
    console.error("SAT Tutor error:", error);
  } finally {
    askButton.disabled = false;
    askButton.innerHTML = 'Explain my answer <span>→</span>';
  }
});

console.log("SAT Tutor JavaScript loaded successfully.");

