import App, { AppStateContext } from "App";
import { useState } from "react";
import { BrowserRouter } from "react-router-dom";

const AppContainer = () => {
  const [selectedThemeState, setSelectedThemeState] = useState(
    localStorage.getItem("SelectedTheme") ?? "healthtag"
  );

  const setTheme = (themeKey: string) => {
    setSelectedThemeState(themeKey);
    localStorage.setItem("SelectedTheme", themeKey);
  };

  return (
    <AppStateContext.Provider
      value={{
        isSideBarOpen: window.matchMedia("(min-width: 768px)").matches,
        theme: selectedThemeState,
        switchTheme: (themeKey: string) => setTheme(themeKey),
      }}
    >
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </AppStateContext.Provider>
  );
};

export default AppContainer;
