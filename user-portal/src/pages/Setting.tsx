import { pageAnimationVariants } from "@animations/variants";
import {
  CogIcon,
  HanburgerIcon,
  HomeIcon,
  LibraryIcon,
} from "@components/Icons";
import { AppStateContext } from "App";
import { motion } from "framer-motion";
import { ReactComponent as Logo } from "@assets/logo/icon.svg";
import { useContext } from "react";

const SettingPage = () => {
  const AppStateContextConsumer = useContext(AppStateContext);

  return (
    <motion.div
      variants={pageAnimationVariants}
      initial="initial"
      animate="animate"
      exit="exit"
    >
      <h3 className="page-h">
        <CogIcon className="h-8 w-8 inline-block mr-3" />
        ตั้งค่า
      </h3>
      <h4 className="page-h">ธีม</h4>
      <div
        className="card p-3 flex gap-3 flex-wrap"
        onChange={(e: any) =>
          AppStateContextConsumer.switchTheme(e.target.value)
        }
      >
        <div className="flex-1">
          <input
            id="healthtag-theme"
            type="radio"
            value="healthtag"
            name="theme"
            checked={AppStateContextConsumer.theme === "healthtag"}
          />
          <label className="ml-3" htmlFor="healthtag-theme">
            HealthTag
          </label>
          <label className="block" htmlFor="healthtag-theme">
            <div className="console-root healthtag">
              <div className="flex w-full">
                <div className="sidebar">
                  <div className="logo flex items-center text-white">
                    <div className="relative">
                      <Logo className="h-16 w-16 p-3" />
                      <div className="logo-shadow absolute w-10 h-10 left-3 top-3"></div>
                    </div>
                    HealthTag Theme
                  </div>
                  <div className="w-16 py-2 flex justify-center cursor-pointer text-white">
                    <HanburgerIcon />
                  </div>
                  <nav>
                    <a className="active">
                      <HomeIcon />
                      Home
                    </a>
                    <hr />
                    <a>
                      <LibraryIcon />
                      Menu
                    </a>
                  </nav>
                </div>
                <div className="main-container h-96 flex-1 flex flex-col">
                  <header className="h-16 flex justify-end"></header>
                  <main className="flex-1 rounded-tl-3xl shadow-xl p-6">
                    <h3>Modern-style theme</h3>
                    <p>Content</p>
                  </main>
                </div>
              </div>
            </div>
          </label>
        </div>
        <div className="flex-1">
          <input
            id="notebook-theme"
            type="radio"
            value="notebook"
            name="theme"
            checked={AppStateContextConsumer.theme === "notebook"}
          />
          <label className="ml-3" htmlFor="notebook-theme">
            Notebook
          </label>
          <label className="block" htmlFor="notebook-theme">
            <div className="console-root notebook">
              <div className="flex">
                <div className="sidebar">
                  <div className="logo flex items-center text-white">
                    <div className="relative">
                      <Logo className="h-16 w-16 p-3" />
                      <div className="logo-shadow absolute w-10 h-10 left-3 top-3"></div>
                    </div>
                    Notebook Theme
                  </div>
                  <div className="w-16 py-2 flex justify-center cursor-pointer text-white">
                    <HanburgerIcon />
                  </div>
                  <nav>
                    <a className="active">
                      <HomeIcon />
                      Home
                    </a>
                    <hr />
                    <a>
                      <LibraryIcon />
                      Menu
                    </a>
                  </nav>
                </div>
                <div className="main-container h-96 flex-1 flex flex-col">
                  <header className="h-16 flex justify-end"></header>
                  <main className="flex-1 rounded-tl-3xl shadow-xl p-6">
                    <h3>Old-style theme</h3>
                    <p>Content</p>
                  </main>
                </div>
              </div>
            </div>
          </label>
        </div>
      </div>
    </motion.div>
  );
};
export default SettingPage;
