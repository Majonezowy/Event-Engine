document.getElementById('registerForm').onsubmit = async function(e) {
    e.preventDefault();

    const imie = document.getElementById('imie').value;
    const nazwisko = document.getElementById('nazwisko').value;
    const klasa = document.getElementById('klasa').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    try {
        const res = await axios.post('http://127.0.0.1:8000/user/register', {email, password, imie, nazwisko, klasa });
        document.getElementById('message').innerText = res.data.detail || res.data.message;
    } catch (err) {
        document.getElementById('message').innerText = err.response?.data?.detail || 'Registration failed';
    }
};