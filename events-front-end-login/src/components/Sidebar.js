
import '@fortawesome/fontawesome-free/css/all.css';
import { useState, useEffect } from "react";
import useToken from "./Token";

const Sidebar = (props) => {
    const { getToken, getName, getIsMaster } = useToken();
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [isMaster, setIsMaster] = useState(false);
    const users_name = getName()

    function setMaster() {
        if (getIsMaster()) {
            setIsMaster(true);
        } else {
            setIsMaster(false);
        }
    }

    useEffect(() => {
        const token = getToken();
        setIsLoggedIn(!!token); // Set isLoggedIn to true if token exists, otherwise false
        setMaster();
    }, [getToken]);

    useEffect(() => {
        props.onLoggedInChange(isLoggedIn);
    }, [isLoggedIn]);

    return (
        <div className="sidebar">
            <div className="sidebar-inner">
                {isLoggedIn ? (
                    <div>
                        <div className="sidebar-top">
                            <div><p>Welcome</p>
                                <p>{users_name}!</p></div>
                            <div id="close-sidebar"><button onClick={props.onClose}>X</button></div>
                        </div>
                        <div className="sidebar-buttons">
                            <div className="sidebar-buttons-wrapper">
                                <button> <i class="fa-solid fa-magnifying-glass"></i> Search Event </button>
                                <button ><i class="fa-solid fa-plus"></i> Add Event </button>
                                <button ><i class="fa-solid fa-calendar-days"></i> My Events </button>
                            </div>
                            <div className="sidebar-buttons-wrapper">
                                <button><i class="fa-solid fa-pen-to-square"></i> My Registrations </button>
                                <button><i class="fa-solid fa-gift"></i> Attended Events </button>
                            </div>
                            <div className="sidebar-buttons-wrapper">
                                <button><i class="fa-solid fa-user"></i> My Profile </button>
                                <button onClick={() => { props.onLogOut(); props.onClose(); }}><i class="fa-solid fa-arrow-right-from-bracket"></i> Log Out </button>
                            </div>
                            {isMaster ? (
                                <div className='sidebar-buttons-wrapper'>
                                    <button ><i class="fa-solid fa-globe"></i> Show All Events </button>
                                    <button> <i class="fa-solid fa-list-check"></i> Category Managment </button>
                                    <button><i class="fa-solid fa-people-roof"></i> Users Managment </button>
                                    <button><i class="fa-solid fa-user-shield"></i> Admins Managment </button>
                                </div>
                            ) : (null)}
                        </div>
                    </div>
                ) : (
                    <div>
                        <div className="sidebar-top">
                            <div><p>Hello Guest!</p></div>
                            <div id="close-sidebar"><button onClick={props.onClose}>X</button></div>
                        </div>
                        <div className="sidebar-buttons">
                            <div className="sidebar-buttons-wrapper">
                                <button> <i class="fa-solid fa-magnifying-glass"></i> Search Event </button>
                            </div>
                            <div className="sidebar-buttons-wrapper">
                                <button onClick={() => { props.onLogIn(); props.onClose(); }}> <i class="fa-solid fa-right-to-bracket"></i> Log In </button>
                                <button onClick={() => { props.onSignUp(); props.onClose(); }}> <i class="fa-solid fa-user-plus"></i> Sign Up </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div >
    )
}

export default Sidebar