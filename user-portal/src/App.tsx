import React from "react";
import { Routes, Route, useLocation, Navigate } from "react-router-dom";

import { AnimatePresence } from "framer-motion";
import AdminLoginPage from "@pages/Administrator/Login";
import AdminConsolePage from "@pages/Administrator/Console/Layout";
import LoginPage from "@pages/User/Login";
import MedicationsPage from "@pages/User/Console/Medications";

export const AppStateContext = React.createContext({
  isSideBarOpen: window.matchMedia("(min-width: 768px)").matches,
  theme: localStorage.getItem("SelectedTheme") ?? "healthtag",
  switchTheme: (themeKey: string) => {},
});

function App() {
  const location = useLocation();

  return (
    <>
      <Routes>
        <Route path="/" element={<MedicationsPage />} />
      </Routes>
    </>
  );
}

export default App;
