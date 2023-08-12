const $startDisplay = $("#start-display");
const $startButton = $("#start");
const $userGuess = $("#user-guess");
const $guessForm = $("#guess-form");
const $userMessage = $("#user-message");
const $boggleBoard = $("#board-display");
const $foundWords = $("#correct-guess");
const $scoreBoard = $("#score-board");
const $submit = $("#guess-submit");
const $timer = $("#timer");

// create functionality of a game
class GameUtilities {
    constructor() {
        this.time = 60;
        this.score = 0;
        this.usedWords = [];
        this.timer();
        this.countdown;
        $scoreBoard.text(this.score);
    }

    updateScore(word) {
        this.score += word.length;
        $scoreBoard.text(this.score);
    }
    postWord(word) {
        this.usedWords.push(`${word}`);
        $foundWords.append(`<li>${word}</li>`);
    }
    timer() {
        this.time--;
        $timer.text(this.time);
        if (this.time <= 0) {
            clearInterval(this.countdown);
            $userGuess.remove();
            $submit.replaceWith("<div>Time is up! Great job!</div>");
            endGame();
        }
    }
}

let game = new GameUtilities();

function gameStart() {
    $timer.text(game.time);
    $startDisplay.addClass("hidden");
    $boggleBoard.removeClass("hidden");
    game.countdown = setInterval(function () {
        game.timer();
    }, 1000);
}

$startButton.click(gameStart);

async function guess(userGuess) {
    if (!userGuess) {
        return;
    }
    const res = await axios.get("/guess", { params: { word: userGuess } });
    let userMessage = "";
    if (game.usedWords.includes(userGuess)) {
        userMessage = "Word already found!";
    } else if (res.data.result == "not-word") {
        userMessage = "Word not in our dictionary";
    } else if (res.data.result == "not-on-board") {
        userMessage = "Word not found on the board";
    } else {
        userMessage = "Great find!";
        game.updateScore(userGuess);
        game.postWord(userGuess);
    }
    $userMessage.text(userMessage);
    $userGuess.val("");
}

$guessForm.submit(function (evt) {
    evt.preventDefault();
    const userGuess = $("#user-guess").val();
    guess(userGuess);
});

async function endGame() {
    $userMessage.hide();
    const res = await axios.post("/stats", { score: game.score });
    if (res.data.new_record === false) {
        $guessForm.append("<p>NEW HIGH SCORE!</p>");
    }
}
