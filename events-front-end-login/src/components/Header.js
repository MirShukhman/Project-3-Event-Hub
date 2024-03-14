
import { useEffect, useState } from 'react';
import logo from '../images/logo.png'
import useToken from './Token';

const Header = (props) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const { flag, getToken } = useToken
    const token = getToken

    useEffect(() => {
        if (token != null) {
            setIsLoggedIn(true)
        }
        else {
            setIsLoggedIn(false)
        }
    }, [flag, token]);

    return (
        <div className="header">
            <div id='logo'>
                <img src={logo} />
            </div>
            <div className='header-elements'>
                <div className="header-buttons" id='open-sidebar'><button onClick={props.openSidebar}><i class="fa-solid fa-bars"></i> Menu </button></div>
                {isLoggedIn ? (
                    <div className="header-buttons">
                        <button className="header-button" id='log-out-header' onClick={props.onLogOut}> Log Out </button>
                    </div>
                ) : (
                    <div className="header-buttons">
                        <button className="header-button" id='sign-up-header' onClick={props.onSignUp}> Sign Up </button>
                        <button className="header-button" id='log-in-header' onClick={props.onLogIn}> Login <i class="fa-solid fa-right-to-bracket"></i></button>
                    </div>
                )}

            </div>
        </div>
    )
}

export default Header