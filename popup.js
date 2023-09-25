document.addEventListener('DOMContentLoaded', function () {
    var checkButton = document.getElementById('checkButton');
    var contentInput = document.getElementById('content');
    var resultElement = document.getElementById('result');

    checkButton.addEventListener('click', function () {
        var content = contentInput.value;
        var data = { content: content };

        fetch('http://localhost:5000/check-spam', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.spam) {
                resultElement.textContent = 'SPAM';
            } else {
                resultElement.textContent = 'NOT SPAM';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});