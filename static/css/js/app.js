const task = document.getElementById("task");
const inputText = document.getElementById("inputText");
const submitBtn = document.getElementById("submitBtn");

const quizOptions = document.getElementById("quizOptions");
const learningOptions = document.getElementById("learningOptions");

const difficulty = document.getElementById("difficulty");
const questionCount = document.getElementById("questionCount");

const level = document.getElementById("level");
const weeks = document.getElementById("weeks");

const result = document.getElementById("result");
const loading = document.getElementById("loading");

const copyBtn = document.getElementById("copyBtn");
const clearBtn = document.getElementById("clearBtn");


function updateOptions() {
    quizOptions.classList.add("hidden");
    learningOptions.classList.add("hidden");

    if (task.value === "quiz") {
        quizOptions.classList.remove("hidden");
    }

    if (task.value === "learn") {
        learningOptions.classList.remove("hidden");
    }
}


task.addEventListener("change", updateOptions);


async function generateAnswer() {

    const selectedTask = task.value;
    const text = inputText.value.trim();

    if (!text) {
        result.innerHTML = `
            <p class="error">
                Please enter a question or topic.
            </p>
        `;
        return;
    }

    loading.classList.remove("hidden");
    result.innerHTML = "";

    try {

        let url = "";
        let body = {};

        if (selectedTask === "qa") {

            url = "/qa";

            body = {
                text: text
            };

        } else if (selectedTask === "explain") {

            url = "/explain";

            body = {
                text: text
            };

        } else if (selectedTask === "summarize") {

            url = "/summarize";

            body = {
                text: text
            };

        } else if (selectedTask === "quiz") {

            url = "/quiz";

            body = {
                topic: text,
                difficulty: difficulty.value,
                count: Number(questionCount.value)
            };

        } else if (selectedTask === "learn") {

            url = "/learn/recommendations";

            body = {
                topic: text,
                level: level.value,
                weeks: Number(weeks.value)
            };
        }


        const response = await fetch(url, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(body)

        });


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Something went wrong."
            );

        }


        displayResult(selectedTask, data);


    } catch (error) {

        result.innerHTML = `
            <div class="error">

                <h3>❌ Error</h3>

                <p>
                    ${escapeHtml(error.message)}
                </p>

            </div>
        `;

    } finally {

        loading.classList.add("hidden");

    }
}


function displayResult(type, data) {

    if (type === "qa") {

        result.innerHTML = `
            <div class="answer">

                <h3>Answer</h3>

                <p>
                    ${formatText(data.answer)}
                </p>

            </div>
        `;

        return;
    }


    if (type === "explain") {

        result.innerHTML = `
            <div class="answer">

                <h3>Explanation</h3>

                <p>
                    ${formatText(data.explanation)}
                </p>

            </div>
        `;

        return;
    }


    if (type === "summarize") {

        result.innerHTML = `
            <div class="answer">

                <h3>Summary</h3>

                <p>
                    ${formatText(data.summary)}
                </p>

            </div>
        `;

        return;
    }


    if (type === "quiz") {

        displayQuiz(data);

        return;
    }


    if (type === "learn") {

        result.innerHTML = `
            <div class="answer">

                <h3>Learning Path</h3>

                <p>
                    ${formatText(data.recommendations)}
                </p>

            </div>
        `;

        return;
    }
}


/* =========================
   QUIZ
========================= */

function displayQuiz(data) {

    let quiz = data.quiz;


    /*
       Backend may return:
       1. quiz as string
       2. quiz as object
    */


    if (typeof quiz === "string") {

        try {

            quiz = quiz
                .replace(/```json/g, "")
                .replace(/```/g, "")
                .trim();

            quiz = JSON.parse(quiz);

        } catch (error) {

            result.innerHTML = `
                <div class="error">

                    <h3>❌ Quiz Error</h3>

                    <p>
                        Could not read quiz data.
                    </p>

                </div>
            `;

            return;
        }
    }


    /*
       Find question array
    */

    let questions = [];


    if (quiz && Array.isArray(quiz.quiz)) {

        questions = quiz.quiz;

    } else if (quiz && Array.isArray(quiz.questions)) {

        questions = quiz.questions;

    } else if (Array.isArray(quiz)) {

        questions = quiz;

    }


    if (data.error) {
    result.innerHTML = `
        <div class="error">
            <h3>⚠️ Quiz Temporarily Unavailable</h3>
            <p>${escapeHtml(data.error)}</p>
        </div>
    `;
    return;
}if (questions.length === 0) {

        result.innerHTML = `
            <div class="error">

                <h3>❌ No Questions Found</h3>

                <p>
                    The AI returned quiz data, but no questions were found.
                </p>

            </div>
        `;

        return;
    }


    let html = `

        <div class="answer">

            <h3>📝 Python Quiz</h3>

    `;


    questions.forEach((question, index) => {

        html += `

            <div class="quiz-question">

                <h4>

                    ${index + 1}.
                    ${escapeHtml(question.question)}

                </h4>

                <div class="quiz-options">

        `;


        if (Array.isArray(question.options)) {

            question.options.forEach((option, optionIndex) => {

                html += `

                    <label class="quiz-option">

                        <input

                            type="radio"

                            name="question-${index}"

                            value="${optionIndex}"

                        >

                        ${escapeHtml(option)}

                    </label>

                `;

            });
        }


        html += `

                </div>

                <button

                    class="check-answer"

                    onclick="checkAnswer(${index})"

                >

                    Check Answer

                </button>


                <div

                    id="feedback-${index}"

                    class="quiz-feedback"

                ></div>


                <div

                    id="correct-${index}"

                    style="display:none"

                >

                    ${escapeHtml(question.correct_answer || "")}

                </div>


                <div

                    id="explanation-${index}"

                    style="display:none"

                >

                    ${escapeHtml(question.explanation || "")}

                </div>

            </div>

        `;

    });


    html += `

        </div>

    `;


    result.innerHTML = html;


    /*
       Save questions for answer checking
    */

    window.currentQuiz = questions;
}


/* =========================
   CHECK ANSWER
========================= */

function checkAnswer(index) {

    const selected = document.querySelector(
        `input[name="question-${index}"]:checked`
    );


    const feedback = document.getElementById(
        `feedback-${index}`
    );


    if (!selected) {

        feedback.innerHTML = `

            <div class="wrong-answer">

                ⚠️ Please select an answer.

            </div>

        `;

        return;
    }


    const question = window.currentQuiz[index];


    const selectedOption =
        question.options[Number(selected.value)];


    const correctAnswer =
        question.correct_answer;


    if (selectedOption === correctAnswer) {

        feedback.innerHTML = `

            <div class="correct-answer">

                <strong>✅ Correct!</strong>

                <p>

                    ${escapeHtml(
                        question.explanation || ""
                    )}

                </p>

            </div>

        `;

    } else {

        feedback.innerHTML = `

            <div class="wrong-answer">

                <strong>❌ Wrong Answer</strong>

                <p>

                    <strong>Correct answer:</strong>

                    ${escapeHtml(correctAnswer)}

                </p>

                <p>

                    ${escapeHtml(
                        question.explanation || ""
                    )}

                </p>

            </div>

        `;
    }
}


/* =========================
   FORMAT TEXT
========================= */

function formatText(text) {

    if (text === null || text === undefined) {

        return "";

    }


    if (typeof text === "object") {

        text = JSON.stringify(
            text,
            null,
            2
        );

    }


    return escapeHtml(
        String(text)
    ).replace(/\n/g, "<br>");
}


/* =========================
   ESCAPE HTML
========================= */

function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


/* =========================
   BUTTONS
========================= */

submitBtn.addEventListener(
    "click",
    generateAnswer
);


clearBtn.addEventListener(
    "click",
    () => {

        inputText.value = "";

        result.innerHTML = "";

    }
);


copyBtn.addEventListener(
    "click",
    async () => {

        const text =
            result.innerText.trim();


        if (!text) {

            return;

        }


        try {

            await navigator.clipboard.writeText(
                text
            );


            copyBtn.textContent =
                "Copied!";


            setTimeout(() => {

                copyBtn.textContent =
                    "Copy";

            }, 1500);


        } catch (error) {

            console.error(
                "Copy failed:",
                error
            );

        }

    }
);


updateOptions();