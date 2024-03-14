
import { useRef } from "react";
import { useState } from "react";
import useToken from "./Token";

const LoginPopUp = (props) => {
    const username = useRef();
    const password = useRef();
    const { setToken, setName, setIsMaster } = useToken();
    const [errorMessage, setErrorMessage] = useState('');

    function openSignUp() {
        props.onClickSignUp()
        props.onClose()
    }

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const result = await fetch("http://127.0.0.1:5000/login", {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username.current.value,
                    password: password.current.value
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
                const data = await result.json();
                const receivedToken = data.front_end_token;
                const receivedName = data.users_name;
                const recevedMasterPrem = data.is_master;
                setToken(receivedToken);
                setName(receivedName);
                setIsMaster(recevedMasterPrem);
                props.onClose();
                e.target.reset();
            }

        } catch (error) {
            console.error('Error during fetch:', error);
        }
    };

    return (
        <div className="popup">
            <div className="popup-inner">
                <div className="login">
                    <form className="login-form" onSubmit={handleLogin}>
                        <p>Login</p>
                        <label htmlFor="username">Username:</label>
                        <input type="text" id="username" ref={username} required />
                        <label htmlFor="password">Password:</label>
                        <input type="password" id="password" ref={password} required />

                        <button className="green-button" type="submit"> Log In </button>
                    </form>
                    {errorMessage && <p className="error-message">{errorMessage}</p>}
                </div>
                <div className="signup">
                    <p>New to EventHub?</p>
                    <button className="go-to-signup-button" onClick={openSignUp}> Sign Up !</button>
                </div>
                <div className="close"><button onClick={props.onClose}>X</button></div>
            </div>
        </div >
    )
}

export default LoginPopUp