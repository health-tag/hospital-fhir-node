import { motion } from "framer-motion";
import { useIsScreenLg } from "@hooks/useMediaQuery";
import HLogo from "@assets/logo/logo_horizontal_white.svg";
import style from "./login.module.css";
import Bg from "@assets/images/login-bg.svg";
import { loginAnimationVariants } from "@animations/variants";


const SmallCenterDialogLayout = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const isScreenLg = useIsScreenLg();
  return (
    <div className="w-screen min-h-screen bg-primary-gradient-light-5.5">
      <img className="absolute w-full h-full object-cover" src={Bg} />
      <div className="min-h-screen flex flex-col items-center justify-center p-6 md:p-12 relative z-10">
        <motion.main
          custom={isScreenLg}
          variants={loginAnimationVariants}
          initial="initial"
          animate="animate"
          exit="exit"
          className="bg-glass shadow-xl rounded-lg overflow-hidden"
        >
          <div className={style.container}>
            <div
              className={`${style.logo} bg-primary-gradient-light-4.5 flex items-center justify-center lg:w-96`}
            >
              <div>
              </div>
            </div>
            <div className={style.body}>
              <section>
                <div className="px-8 pt-6 pb-8 mb-4">{children}</div>
              </section>
            </div>
            <div
              className={`${style.edition} text-white text-sm flex items-center`}
            >
              <div className="flex-1">Open-source</div>
              <div className={`${style.logo}`}>
                <img src={HLogo} className="h-3" />
              </div>
            </div>
          </div>
        </motion.main>
      </div>
    </div>
  );
};
export default SmallCenterDialogLayout;
