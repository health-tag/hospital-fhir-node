import React from "react";
import { Routes, Route, useLocation, Navigate } from "react-router-dom";

import { AnimatePresence } from "framer-motion";
import AdminLoginPage from "@pages/Administrator/Login";
import AdminConsolePage from "@pages/Administrator/Console/Layout";
import LoginPage from "@pages/User/Login";
import UserConsolePage from "@pages/User/Console/Layout";

export const AppStateContext = React.createContext({
  isSideBarOpen: window.matchMedia("(min-width: 768px)").matches,
  theme: localStorage.getItem("SelectedTheme") ?? "healthtag",
  switchTheme: (themeKey: string) => {},
});

function App() {
  const location = useLocation();

  return (
    <>
      <AnimatePresence exitBeforeEnter>
        <Routes location={location} key={location.pathname}>
          <Route path="/" element={<Navigate to="/user/login" replace />} />
          <Route path="/admin/login" element={<AdminLoginPage />} />
          <Route path="/user/login" element={<LoginPage />} />
        </Routes>
      </AnimatePresence>
      <Routes>
        <Route path="/admin/console/*" element={<AdminConsolePage />} />
        <Route path="/user/console/*" element={<UserConsolePage />} />
      </Routes>
    </>
  );
}

export default App;
