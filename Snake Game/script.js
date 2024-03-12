const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const gridSize = 20;
const tileCountX = canvas.width / gridSize;
const tileCountY = canvas.height / gridSize;

let snake = [{ x: 10, y: 10 }];
let food = { x: 15, y: 15 };
let dx = 0;
let dy = 0;
let score = 0;
let speed = 8;
let isPaused = false;
let isGameOver = false;

function drawSnake() {
    ctx.fillStyle = "#2ecc71";
    snake.forEach(segment => {
        ctx.fillRect(segment.x * gridSize, segment.y * gridSize, gridSize, gridSize);
    });
}

function drawFood() {
    ctx.fillStyle = "#e74c3c";
    ctx.fillRect(food.x * gridSize, food.y * gridSize, gridSize, gridSize);
}

function moveSnake() {
    const head = { x: snake[0].x + dx, y: snake[0].y + dy };
    snake.unshift(head);

    if (head.x === food.x && head.y === food.y) {
        score++;
        generateFood();
        if (score % 5 === 0 && speed > 1) {
            speed--;
        }
    } else {
        snake.pop();
    }

    if (head.x < 0 || head.x >= tileCountX || head.y < 0 || head.y >= tileCountY || checkCollision()) {
        gameOver();
    }
}

function generateFood() {
    food.x = Math.floor(Math.random() * tileCountX);
    food.y = Math.floor(Math.random() * tileCountY);
}

function checkCollision() {
    const head = snake[0];
    for (let i = 1; i < snake.length; i++) {
        if (head.x === snake[i].x && head.y === snake[i].y) {
            return true;
        }
    }
    return false;
}

function drawScore() {
    ctx.fillStyle = "#333";
    ctx.font = "20px Arial";
    ctx.fillText("Score: " + score, 10, 30);
}

function drawPaused() {
    ctx.fillStyle = "#333";
    ctx.font = "30px Arial";
    ctx.fillText("Paused", canvas.width / 2 - 50, canvas.height / 2);
}

function drawGameOver() {
    ctx.fillStyle = "#333";
    ctx.font = "30px Arial";
    ctx.fillText("Game Over", canvas.width / 2 - 100, canvas.height / 2);
}

function gameOver() {
    isGameOver = true;
    clearInterval(game);
    drawGameOver();
}

function gameLoop() {
    if (!isPaused && !isGameOver) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        drawSnake();
        drawFood();
        drawScore();

        moveSnake();
    }
}

document.addEventListener("keydown", event => {
    if (event.key === "ArrowUp" && dy === 0) {
        dx = 0;
        dy = -1;
    } else if (event.key === "ArrowDown" && dy === 0) {
        dx = 0;
        dy = 1;
    } else if (event.key === "ArrowLeft" && dx === 0) {
        dx = -1;
        dy = 0;
    } else if (event.key === "ArrowRight" && dx === 0) {
        dx = 1;
        dy = 0;
    } else if (event.key === " ") {
        isPaused = !isPaused;
        if (isPaused) {
            drawPaused();
        }
    }
});

generateFood();
let game = setInterval(gameLoop, 1000 / speed);
