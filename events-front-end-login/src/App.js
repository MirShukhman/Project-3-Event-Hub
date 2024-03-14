
import { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';
import Footer from './components/Footer';
import Sidebar from './components/Sidebar'
import LoginPopUp from './components/LogIn';
import SignUpPopUp from './components/SignUp';
import LogOutPopUp from './components/LogOut';

function App() {
  const [headerRefreshTrigger, setHeaderRefreshTrigger] = useState(false);
  const [sidebarIsOpen, setSIdebarIsOpen] = useState(false);
  const [loginPopUpIsOpen, setloginPopUpIsOpen] = useState(false);
  const [signUpPopUpIsOpen, setsignUpPopUpIsOpen] = useState(false);
  const [logOutIsOpen, setLogOutIsOpen] = useState(false);

  function hadleHeaderRefresh(isLoggedIn) {
    if (isLoggedIn) {
      setHeaderRefreshTrigger(true);
    } else {
      setHeaderRefreshTrigger(false);
    }
  }

  function openSidebar() {
    setSIdebarIsOpen(true);
  }

  function closeSidebar() {
    setSIdebarIsOpen(false);
  }

  function openLogin() {
    setloginPopUpIsOpen(true);
  }

  function closeLogin() {
    setloginPopUpIsOpen(false);
  }

  function openSignUp() {
    setsignUpPopUpIsOpen(true);
  }

  function closeSignUp() {
    setsignUpPopUpIsOpen(false);
  }

  function openLogOut() {
    setLogOutIsOpen(true);
  }

  function closeLogOut() {
    setLogOutIsOpen(false);
  }

  return (
    <div className="App">
      <Header refreshTrigger={headerRefreshTrigger} onLogOut={openLogOut} onSignUp={openSignUp} onLogIn={openLogin} openSidebar={openSidebar} />
      {sidebarIsOpen && <Sidebar onLoggedInChange={hadleHeaderRefresh} onClose={closeSidebar} onLogOut={openLogOut} onSignUp={openSignUp} onLogIn={openLogin} />}
      {signUpPopUpIsOpen && <SignUpPopUp onClose={closeSignUp} onOpenLogin={openLogin} />}
      {loginPopUpIsOpen && <LoginPopUp onClose={closeLogin} onClickSignUp={openSignUp} />}
      {logOutIsOpen && <LogOutPopUp onClose={closeLogOut} />}
      <Footer />
    </div>
  );
}

export default App;
