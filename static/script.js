document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('crypto-form').onsubmit = async function(e) {
        e.preventDefault();
        const form = e.target;
        const data = new FormData(form);
        const action = form.getAttribute('action');
        const response = await fetch(action, {
            method: 'POST',
            body: new URLSearchParams(data)
        });
        document.getElementById('result').innerText = await response.text();
    };
});