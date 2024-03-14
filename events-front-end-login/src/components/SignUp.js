
import { useRef } from "react";
import { useState } from "react";

const SignUpPopUp = (props) => {
    const username = useRef();
    const password = useRef();
    const repeatPassword = useRef();
    const email = useRef();
    const name = useRef();
    const description = useRef();
    const [passwordsMatch, setPasswordsMatch] = useState(true);
    const [errorMessage, setErrorMessage] = useState('');
    const [sucsess, setSucsess] = useState(false);

    function goToLogin() {
        props.onClose();
        props.onOpenLogin();
    }

    const handleSignUp = async (e) => {
        e.preventDefault();

        if (password.current.value !== repeatPassword.current.value) {
            setPasswordsMatch(false);
            return;
        }

        try {
            const result = await fetch("http://127.0.0.1:5000/signup", {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username.current.value,
                    password: password.current.value,
                    email: email.current.value,
                    name: name.current.value,
                    description: description.current.value
                })
            });

            if (!result.ok) {
                const data = await result.json();

                if (data.error) {
                    console.error('Error from backend:', data.error);
                    setErrorMessage(data.error);
                }
                else {
                    throw new Error(`HTTP error! Status: ${result.status}`);
                }
            }
            else {
                e.target.reset();
                setSucsess(true);
            }

        } catch (error) {
            console.error('Error during fetch:', error);
        }
    };

    return (
        <div className="popup">
            <button className="close" onClick={props.onClose}>Close</button>
            <p>Sign Up</p>
            <form className="signup-form" onSubmit={handleSignUp}>
                <label htmlFor="username">Username:</label>
                <input type="text" id="username" ref={username} pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,50}" required /><br />
                <p>Username must include: number, upper and lowercase letters</p>
                <label htmlFor="password">Password:</label>
                <input type="password" id="password" ref={password} pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,50}" required /><br />
                <p>Password must include: number, upper and lowercase letters</p>
                <label htmlFor="repeat-password">Repeat Password:</label>
                <input type="password" id="repeat-password" ref={repeatPassword} pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,50}" required /><br />
                {!passwordsMatch && <p className="error-message">Passwords do not match</p>}
                <label htmlFor="email">Email:</label>
                <input type="email" id="email" ref={email} maxLength="50" required /><br />
                <label htmlFor="name">Full Name:</label>
                <input type="text" id="name" ref={name} maxLength="100" required /><br />
                <label htmlFor="description">About Yourself:</label><br />
                <textarea type="text" id="description" ref={description} maxLength="1000" /><br />

                <button className="green-button" type="submit"> Sign Up</button>
            </form>
            {errorMessage && <p className="error-message">{errorMessage}</p>}
            {sucsess &&
                <div className="signup-sucsess">
                    <p>Welcome to EventHub!</p>
                    <p>Your Sign Up has been sucsessful. Please proceed to Log In:</p>
                    <button className="green-button" onClick={goToLogin}> Log In </button>
                </div>}
        </div >
    )
}

export default SignUpPopUp