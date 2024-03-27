
import { useState } from "react";
import { useToken } from '../../Token';
import Spinner from "../../Loading";
import '../../../style/Pop-Up.css';

const CancelRegistration = (props) => {
    const { storedToken } = useToken();
    const [isSuccess, setIsSuccess] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [loading, setLoading] = useState(false);

    const handleCancel = async (e) => {
        e.preventDefault();
        setLoading(true)
        try {
            const result = await fetch(`http://127.0.0.1:5000/cancel_registeration/${props.event_id}`, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    token: storedToken
                })
            });

            if (!result.ok) {
                const data = await result.json();

                if (data.error) {
                    console.error('Error from backend:', data.error);
                    setErrorMessage(data.error);

                } else {
                    throw new Error(`HTTP error! Status: ${result.status}`);
                }

            } else {
                setIsSuccess(true);
                setTimeout(() => {
                    props.onClose();
                }, 5000);
            }

        } catch (error) {
            console.error('Error during fetch:', error);

        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="popup">
            <div className="popup-inner">
                <div className="close"><button onClick={props.onClose}>X</button></div>
                <div className="cancel-registration">
                    <p>Cancel Registration To {props.event_title}?</p>
                    <button className="red-button" onClick={handleCancel}> Cancel Registration </button>
                    <button className="cancel-button" onClick={props.onClose}> Exit </button>
                    {loading && <div className="events-loading">
                        <Spinner />
                    </div>}
                    {isSuccess &&
                        <div className="sucsess-message">
                            <p> Registration Canceled </p>
                        </div>}
                    {errorMessage && <p className="error-message">{errorMessage}</p>}
                </div>
            </div>
        </div >
    )

}

export default CancelRegistration