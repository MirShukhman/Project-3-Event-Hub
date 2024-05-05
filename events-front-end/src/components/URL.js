import React, { createContext, useContext } from 'react';

const URLContext = createContext();

const URLProvider = ({ children }) => {
    const storedURL = 'http://20.253.72.112:5000';

    return (
        <URLContext.Provider
            value={{
                storedURL
            }}
        >
            {children}
        </URLContext.Provider>
    );
};

const useURL = () => useContext(URLContext);

export { URLProvider, useURL };
