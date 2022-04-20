import {
  useLocation,
  Routes,
  Route,
  NavLink,
  Navigate,
  useNavigate,
} from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";

import MainLayout from "@layouts/main";
import {
  ChevronIcon,
  CogIcon,
  KeyIcon,
  PremiumIcon,
  SupportIcon,
  UserGroupIcon,
} from "@components/Icons";
import {
  dropDownMenuAnimationVariant,
  menuHeaderAnimationVariants,
} from "@animations/variants";
import SettingPage from "@pages/Setting";
import { useEffect, useRef, useState } from "react";
import PersonManagerPage from "./PersonManager";
import AdminRegisterPage from "./PersonManager/Register";
import AdminResetPinPage from "./PersonManager/ResetPin";

const AdminConsolePage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const profileDropDownRef = useRef<HTMLDivElement>(null);
  const [isProfileOpen, setIsProfileOpen] = useState<boolean>();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        profileDropDownRef.current &&
        !profileDropDownRef.current.contains(event.target)
      ) {
        setIsProfileOpen(false);
      }
    };
    document.addEventListener("click", handleClickOutside, true);
    return () => {
      document.removeEventListener("click", handleClickOutside, true);
    };
  });

  useEffect(() => {
    if (!sessionStorage.getItem("admin_username")) {
      navigate("/admin/login");
    }
  }, []);

  const logout = () => {
    sessionStorage.removeItem("admin_username");
    sessionStorage.removeItem("admin_password");
    navigate("/admin/login");
  };

  return (
    <MainLayout
      title="ศูนย์จัดการระบบ"
      menu={
        <>
          <hr />
          <motion.h5 variants={menuHeaderAnimationVariants}>
            การจัดการ
          </motion.h5>
          <NavLink to="manage-people">
            <UserGroupIcon />
            จัดการผู้ใช้งาน
          </NavLink>

          <hr />
          <motion.h5 variants={menuHeaderAnimationVariants}>
            การสนับสนุน
          </motion.h5>
          <a href="https://healthtag.io/support">
            <SupportIcon />
            คู่มือ + การช่วยเหลือ
          </a>
          <hr />
          <motion.h5 variants={menuHeaderAnimationVariants}>
            การตั้งค่า
          </motion.h5>
          <NavLink to="setting">
            <CogIcon />
            ตั้งค่าระบบ
          </NavLink>
          <a className="premium" href="https://healthtag.io/upgrade">
            <PremiumIcon />
            อัพเกรด
          </a>
        </>
      }
      header={
        <header className="h-16 flex justify-end">
          <div
            ref={profileDropDownRef}
            className="relative flex"
            style={{ background: `rgba(255,255,255,0.1 )` }}
          >
            <div
              className="p-3 hover:cursor-pointer flex items-center text-white gap-6"
              onClick={() => setIsProfileOpen(!isProfileOpen)}
            >
              {sessionStorage.getItem("admin_username")}{" "}
              <ChevronIcon side={isProfileOpen ? "up" : "down"} />
            </div>
            <AnimatePresence>
              {isProfileOpen ? (
                <motion.nav
                  variants={dropDownMenuAnimationVariant}
                  initial="initial"
                  animate="animate"
                  exit="exit"
                  key="profile-dropdown"
                  className={`dropdown flex flex-col gap-3`}
                >
                  <a onClick={logout}>
                    <KeyIcon /> ออกจากระบบ
                  </a>
                </motion.nav>
              ) : (
                <></>
              )}
            </AnimatePresence>
          </div>
        </header>
      }
    >
      <AnimatePresence exitBeforeEnter>
        <Routes location={location} key={location.pathname}>
          <Route path="" element={<Navigate to="manage-people" replace />} />
          <Route path="manage-people" element={<PersonManagerPage />} />
          <Route
            path="manage-people/register"
            element={<AdminRegisterPage />}
          />{" "}
          <Route
            path="manage-people/reset-pin"
            element={<AdminResetPinPage />}
          />
          <Route path="setting" element={<SettingPage />} />
        </Routes>
      </AnimatePresence>
    </MainLayout>
  );
};

export default AdminConsolePage;
