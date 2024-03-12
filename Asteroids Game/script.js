// Constants
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const shipWidth = 20;
const shipHeight = 20;
const bulletRadius = 3;
const asteroidColors = ["#bdc3c7", "#95a5a6", "#7f8c8d"];

// Player ship
const ship = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    radius: shipWidth / 2,
    angle: -Math.PI / 2,
    rotationSpeed: Math.PI / 60,
    speed: 0.2,
    isThrusting: false,
    isDestroyed: false,
    blinkTimer: 0
};

// Bullets
const bullets = [];

// Asteroids
const asteroids = [];

// Initialize game
function init() {
    createAsteroids(3);
}

// Create asteroids
function createAsteroids(num) {
    for (let i = 0; i < num; i++) {
        let asteroid = {
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 30 + 15,
            speedX: Math.random() * 2 - 1,
            speedY: Math.random() * 2 - 1,
            rotation: Math.random() * Math.PI * 2,
            vertices: Math.floor(Math.random() * 7) + 5
        };
        asteroids.push(asteroid);
    }
}

// Draw ship
function drawShip() {
    ctx.save();
    ctx.translate(ship.x, ship.y);
    ctx.rotate(ship.angle);
    ctx.strokeStyle = "#fff";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, -shipHeight / 2);
    ctx.lineTo(shipWidth / 2, shipHeight / 2);
    ctx.lineTo(-shipWidth / 2, shipHeight / 2);
    ctx.closePath();
    ctx.stroke();
    ctx.restore();
}

// Draw bullet
function drawBullet(bullet) {
    ctx.fillStyle = "#fff";
    ctx.beginPath();
    ctx.arc(bullet.x, bullet.y, bulletRadius, 0, Math.PI * 2);
    ctx.fill();
}

// Draw asteroid
function drawAsteroid(asteroid) {
    ctx.strokeStyle = "#fff";
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (let i = 0; i < asteroid.vertices; i++) {
        let angle = i / asteroid.vertices * Math.PI * 2;
        let x = asteroid.x + asteroid.radius * Math.cos(angle + asteroid.rotation);
        let y = asteroid.y + asteroid.radius * Math.sin(angle + asteroid.rotation);
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    }
    ctx.closePath();
    ctx.stroke();
}

// Draw score
function drawScore(score) {
    ctx.fillStyle = "#fff";
    ctx.font = "20px Arial";
    ctx.fillText("Score: " + score, 20, 30);
}

// Check collision between two objects
function checkCollision(obj1, obj2) {
    let dx = obj1.x - obj2.x;
    let dy = obj1.y - obj2.y;
    let distance = Math.sqrt(dx * dx + dy * dy);
    return distance < obj1.radius + obj2.radius;
}

// Update game objects
function update() {
    // Update ship
    if (ship.isThrusting && !ship.isDestroyed) {
        ship.x += ship.speed * Math.cos(ship.angle);
        ship.y += ship.speed * Math.sin(ship.angle);
    }

    // Update bullets
    bullets.forEach(bullet => {
        bullet.x += bullet.speedX;
        bullet.y += bullet.speedY;
    });

    // Update asteroids
    asteroids.forEach(asteroid => {
        asteroid.x += asteroid.speedX;
        asteroid.y += asteroid.speedY;

        // Wrap asteroids around the screen
        if (asteroid.x < -asteroid.radius) {
            asteroid.x = canvas.width + asteroid.radius;
        }
        if (asteroid.x > canvas.width + asteroid.radius) {
            asteroid.x = -asteroid.radius;
        }
        if (asteroid.y < -asteroid.radius) {
            asteroid.y = canvas.height + asteroid.radius;
        }
        if (asteroid.y > canvas.height + asteroid.radius) {
            asteroid.y = -asteroid.radius;
        }

        // Check collision with ship
        if (!ship.isDestroyed && checkCollision(ship, asteroid)) {
            ship.isDestroyed = true;
        }

        // Check collision with bullets
        bullets.forEach(bullet => {
            if (checkCollision(bullet, asteroid)) {
                asteroid.radius -= 10;
                if (asteroid.radius < 10) {
                    asteroids.splice(asteroids.indexOf(asteroid), 1);
                    bullets.splice(bullets.indexOf(bullet), 1);
                    createAsteroids(1);
                }
                bullets.splice(bullets.indexOf(bullet), 1);
            }
        });
    });
}

// Draw game objects
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    drawShip();
    bullets.forEach(drawBullet);
    asteroids.forEach(drawAsteroid);

    if (ship.isDestroyed) {
        ctx.fillStyle = "#fff";
        ctx.font = "40px Arial";
        ctx.fillText("Game Over", canvas.width / 2 - 100, canvas.height / 2);
    }
}

// Game loop
function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

// Keydown event listener
document.addEventListener("keydown", event => {
    if (event.key === "ArrowUp" && !ship.isDestroyed) {
        ship.isThrusting = true;
    }
    if (event.key === "ArrowLeft" && !ship.isDestroyed) {
        ship.angle -= ship.rotationSpeed;
    }
    if (event.key === "ArrowRight" && !ship.isDestroyed) {
        ship.angle += ship.rotationSpeed;
    }
    if (event.key === " ") {
        if (!ship.isDestroyed) {
            bullets.push({
                x: ship.x + ship.radius * Math.cos(ship.angle),
                y: ship.y + ship.radius * Math.sin(ship.angle),
                speedX: 4 * Math.cos(ship.angle),
                speedY: 4 * Math.sin(ship.angle)
            });
        }
    }
});

// Keyup event listener
document.addEventListener("keyup", event => {
    if (event.key === "ArrowUp" && !ship.isDestroyed) {
        ship.isThrusting = false;
    }
});

// Initialize game
init();
gameLoop();
