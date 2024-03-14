
import { useState } from "react";
import useToken from "./Token";

const LogOutPopUp = (props) => {
    const { setToken, getToken, setName, setIsMaster } = useToken();
    const [errorMessage, setErrorMessage] = useState('');

    const handleLogout = async (e) => {
        try {
            const result = await fetch("http://127.0.0.1:5000/logout", {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                }
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
                setToken(null);
                setName(null);
                setIsMaster(false);
                props.onClose();
                if (e.target && e.target.form) {
                    e.target.form.reset();
                }
            }

        } catch (error) {
            console.error('Error during fetch:', error);
        }
    };


    return (
        <div className="popup">
            <button className="close" onClick={props.onClose}>Close</button>
            <div className="logout">
                <p>Log Out?</p>
                <button className="green-button" onClick={handleLogout}> Log Out </button>
                <button className="cancel-button" onClick={props.onClose}> Cancel </button>
                {errorMessage && <p className="error-message">{errorMessage}</p>}
            </div>
        </div >
    )
}

export default LogOutPopUp