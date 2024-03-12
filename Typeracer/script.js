// script.js
document.addEventListener('DOMContentLoaded', function() {
    let user = null;

    function onSignIn(googleUser) {
        user = googleUser.getBasicProfile();
        document.getElementById('auth-container').innerHTML = `<p>Welcome, ${user.getName()}!</p>`;
        document.getElementById('start-button').removeAttribute('disabled');
    }

    document.getElementById('login-button').addEventListener('click', function() {
        gapi.auth2.getAuthInstance().signIn();
    });

    document.getElementById('start-button').addEventListener('click', function() {
        // Send request to server to start race
        fetch('/start_race', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ userId: user.getId() })
        }).then(response => response.json())
          .then(data => {
              // Handle response (e.g., start race)
          });
    });

    // WebSocket connection for real-time updates
    const socket = new WebSocket('ws://localhost:5000/ws');

    socket.onopen = function(event) {
        console.log('WebSocket connection opened');
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        // Handle real-time updates (e.g., update race status, leaderboard)
    };
});
