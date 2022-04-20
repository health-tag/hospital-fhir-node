import {
  useLocation,
  Routes,
  Route,
  NavLink,
  useNavigate,
  Navigate
} from "react-router-dom";

import MainLayout from "@layouts/main";
import { AnimatePresence, motion } from "framer-motion";
import {
  dropDownMenuAnimationVariant,
  menuHeaderAnimationVariants,
} from "@animations/variants";
import {
  BookOpenIcon,
  ChevronIcon,
  CogIcon,
  KeyIcon,
  MedicationIcon,
  SupportIcon,
} from "@components/Icons";
import SettingPage from "@pages/Setting";
import { useEffect, useRef, useState } from "react";
import MedicationsPage from "./Medications";
import axios from "axios";
import { Placeholder } from "@components/Placeholder";

const UserConsolePage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const profileDropDownRef = useRef<HTMLDivElement>(null);
  const [isProfileOpen, setIsProfileOpen] = useState<boolean>();
  const [profileData, setProfileData] = useState<{
    name: string;
    surname: string;
  }>();

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
    (async () => {
      const username = sessionStorage.getItem("username")!;
      const password = sessionStorage.getItem("password")!;
      const hn = sessionStorage.getItem("hn");
      const nameRegex = /(ชื่อ|)\s+(?<name>\S+)\s+(?<surname>.+)/;
      if (!hn) {
        navigate("/");
      }

      const patientResponse = await axios.get(
        `${process.env.REACT_APP_KONG_URL}/fhir-api/Patient?identifier=https%3A%2F%2Fsil-th.org%2FCSOP%2Fhn%7C${hn}`,
        {
          auth: {
            username: username,
            password: password,
          },
        }
      );

      const patientInfo = patientResponse.data.entry[0].resource;
      const patientID = patientInfo.id;
      // Temporary workaround for the name data which is still included "ชื่อ"
      const nameRegexResult = nameRegex.exec(patientInfo.name[0].text.trim());
      const name = nameRegexResult?.groups?.name ?? "";
      const surname = nameRegexResult?.groups?.surname ?? "";
      setProfileData({ name: name, surname: surname });
    })();
  }, []);

  const logout = () => {
    sessionStorage.removeItem("username");
    sessionStorage.removeItem("password");
    sessionStorage.removeItem("hn");
    navigate("/user/login");
  };

  return (
    <MainLayout
      title="ข้อมูลสุขภาพ"
      menu={
        <>
          <hr />
          <motion.h5 variants={menuHeaderAnimationVariants}>ข้อมูล</motion.h5>
          <NavLink to="medications">
            <MedicationIcon className="h-6" />
            ยา
          </NavLink>
          <hr />
          <motion.h5 variants={menuHeaderAnimationVariants}>
            การสนับสนุน
          </motion.h5>
          <a>
            <BookOpenIcon />
            คู่มือการใช้งาน
          </a>
          <a>
            <SupportIcon />
            ขอรับความช่วยเหลือ
          </a>
          <hr />
          <motion.h5 variants={menuHeaderAnimationVariants}>
            การตั้งค่า
          </motion.h5>
          <NavLink to="setting">
            <CogIcon />
            ตั้งค่าระบบ
          </NavLink>
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
              <div>
                <div>
                  {profileData ? (
                    <>
                      {profileData?.name} {profileData?.surname}
                    </>
                  ) : (
                    <Placeholder />
                  )}
                </div>
                <div>{sessionStorage.getItem("hn")}</div>
              </div>
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
          <Route path="" element={<Navigate to="medications" replace />} />
          <Route path="medications" element={<MedicationsPage />} />
          <Route path="setting" element={<SettingPage />} />
        </Routes>
      </AnimatePresence>
    </MainLayout>
  );
};

export default UserConsolePage;
