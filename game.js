// ========================
//   INIZIALIZZAZIONE TELEGRAM WEBAPP
// ========================
let tg = window.Telegram.WebApp;
tg.expand();  // Espande la WebApp a schermo intero su Telegram
console.log("Telegram WebApp inizializzata");

// ========================
//   CONFIGURAZIONE CANVAS
// ========================
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();

// ========================
//   GIOCO & MOVIMENTO
// ========================
const player = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    size: 20,
    speed: 2,
    dx: 0,
    dy: 0
};

// ========================
//   GESTIONE JOYSTICK
// ========================
let movementJoystick = { dx: 0, dy: 0 };

canvas.addEventListener("touchstart", (e) => {
    const touch = e.touches[0];
    if (touch.clientX < canvas.width / 2) { // Joystick sinistro
        movementJoystick.x = touch.clientX;
        movementJoystick.y = touch.clientY;
    }
});

canvas.addEventListener("touchmove", (e) => {
    const touch = e.touches[0];
    if (touch.clientX < canvas.width / 2) { // Joystick sinistro
        let dx = touch.clientX - movementJoystick.x;
        let dy = touch.clientY - movementJoystick.y;

        movementJoystick.dx = dx * 0.05;
        movementJoystick.dy = dy * 0.05;

        player.dx = movementJoystick.dx;
        player.dy = movementJoystick.dy;
    }
});

canvas.addEventListener("touchend", () => {
    movementJoystick.dx = 0;
    movementJoystick.dy = 0;
    player.dx = 0;
    player.dy = 0;
});

// ========================
//   LOGICA DEL GIOCO
// ========================
function updatePlayerMovement() {
    player.x += player.dx;
    player.y += player.dy;

    // Evita che il giocatore esca dallo schermo
    if (player.x < 0) player.x = 0;
    if (player.x + player.size > canvas.width) player.x = canvas.width - player.size;
    if (player.y < 0) player.y = 0;
    if (player.y + player.size > canvas.height) player.y = canvas.height - player.size;
}

function drawPlayer() {
    ctx.fillStyle = 'blue';
    ctx.fillRect(player.x, player.y, player.size, player.size);
}

function drawGame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawPlayer();
}

function gameLoop() {
    updatePlayerMovement();
    drawGame();
    requestAnimationFrame(gameLoop);
}

console.log("Gioco avviato!");
gameLoop();
