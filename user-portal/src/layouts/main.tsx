import { motion } from "framer-motion";
import MIcon from "@assets/logo/icon.png";
import React, { useState, useContext } from "react";

import HLogo from "@assets/logo/logo_horizontal_white.svg";
import { HanburgerIcon } from "@components/Icons";

import styles from "./main.module.css";
import { AppStateContext } from "App";

const MainLayout = ({
  children,
  menu,
  header,
  title,
}: {
  children: React.ReactNode;
  menu?: React.ReactNode;
  header?: React.ReactNode;
  title: string;
}) => {
  const AppStateContextConsumer = useContext(AppStateContext);


  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(
    AppStateContextConsumer.isSideBarOpen
  );

  const variants = {
    open: { width: `240px` },
    close: { width: `4rem` },
  };

  const setSideBarGlobalState = (state: boolean) =>
    (AppStateContextConsumer.isSideBarOpen = state);

  const hamburgerOnClickHandler = () => {
    const newIsSidebarOpen = !isSidebarOpen;
    setSideBarGlobalState(newIsSidebarOpen);
    setIsSidebarOpen(newIsSidebarOpen);
  };

  return (
    <div className={`${AppStateContextConsumer.theme} console-root`}>
      <div className={`min-h-screen ${styles.container}`}>
        <motion.aside
          variants={variants}
          initial={isSidebarOpen ? "open" : "close"}
          animate={isSidebarOpen ? "open" : "close"}
          className={`text-white flex flex-col items-stretch ${styles.sidebar} sidebar relative`}
        >
          <div className="logo flex items-center w-[240px]">
            <div className="relative">
              <img src={MIcon} className="h-16 w-16 p-3" />
              <div className="logo-shadow absolute w-10 h-10 left-3 top-3"></div>
            </div>
            {title}
          </div>
          <div
            className="w-16 py-2 flex justify-center cursor-pointer"
            onClick={hamburgerOnClickHandler}
          >
            <HanburgerIcon />
          </div>
          <nav className="flex-1 flex flex-col w-[240px]">{menu}</nav>
          <div
            className={`${styles.edition} bg-primary-gradient text-white pl-6 pr-10 py-2 flex flex-row items-center text-sm`}
            style={{ width: `calc(240px + 20px)` }}
          >
            <div className="flex-1 text-sm">Open-source</div>
            <img src={HLogo} className="h-3 inline-block" />
          </div>
        </motion.aside>
        <div
          className={`main-container ${styles.main} relative z-10 grid`}
          style={{ gridTemplateRows: `auto 1fr` }}
        >
          {header}
          <main className={`rounded-tl-3xl shadow-xl p-6 overflow-x-hidden`}>
            {children}
          </main>
        </div>
      </div>
    </div>
  );
};

export default MainLayout;
