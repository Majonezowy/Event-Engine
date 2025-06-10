document.getElementById('loginForm').onsubmit = async function(e) {
    e.preventDefault();
    const email = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    try {
        const res = await axios.post('http://127.0.0.1:8000/user/login', { email, password });
        console.log(res.data);
    } catch (err) {
        document.getElementById('message').innerText = 'Login failed';
    }
};