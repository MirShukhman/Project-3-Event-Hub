
import SearchForAdmin from "./SearchForAdmin";
import { useState } from "react";
import { useToken } from '../../Token';
import { useURL } from "../../URL";
import Spinner from "../../Loading";
import '../../../style/Window.css';

const AddAdmin = (props) => {
    const { storedToken } = useToken();
    const { storedURL } = useURL();
    const [searched, setSearched] = useState(false)
    const [errorMessage, setErrorMessage] = useState('');
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(false);
    const [sucsess, setSucsess] = useState(false);

    const makeAdmin = async (user) => {
        setLoading(true)
        try {
            const result = await fetch(`${storedURL}/make_admin/${user.user_id}`, {
                method: 'PUT',
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
                setSucsess(user)
                setLoading(false)
            }

        } catch (error) {
            console.error('Error during fetch:', error);
        }
    }

    return (
        <div className="window">
            <div className="window-inner">

                <div className='add-admin-window'>
                    <div className="add-admin-search">
                        <SearchForAdmin setUsers={setUsers}
                            setErrorMessage={setErrorMessage}
                            setSearched={setSearched}
                            setLoading={setLoading} />
                        {sucsess &&
                            <div className="sucsess-message">
                                <p>User {sucsess.name}, ID {sucsess.user_id} Made Admin</p>
                            </div>
                        }
                        {errorMessage && <p>{errorMessage}</p>}
                        {loading && <Spinner />}
                    </div>
                    {searched && users &&
                        <div className="users-display">
                            <table>
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Username</th>
                                        <th>Email</th>
                                        <th>Full Name</th>
                                        <th>Created At</th>
                                        <th>Status</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {users.map(user => (
                                        <tr key={user.user_id} className="table">
                                            <td>{user.user_id}</td>
                                            <td>{user.username}</td>
                                            <td >{user.email}</td>
                                            <td>{user.name}</td>
                                            <td>{user.created}</td>
                                            <td>{user.is_active}</td>
                                            <td>{user.is_active === 'Active' ?
                                                (<button id='make-admin' onClick={() => makeAdmin(user)}> Make Admin</button>) :
                                                (<button id='make-admin' disabled> Make Admin </button>)}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>}

                    {searched && !users &&
                        <div className="none-user-found">
                            No Users Meeting Search Found</div>}
                </div>

                <div className="close"><button onClick={props.onClose}>X</button></div>
            </div >
        </div>
    )
}
export default AddAdmin