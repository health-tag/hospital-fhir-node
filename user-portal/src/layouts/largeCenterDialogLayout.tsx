import { ReactComponent as HLogo } from "@assets/logo/logo_horizontal.svg";
import {  motion } from "framer-motion";
import { dialogAnimationVariants } from "@animations/variants";

const LargeCenterDialogLayout = ({
  children,
  controls,
  className = "",
  limitHeightToScreen = false,
}: {
  children: React.ReactNode;
  controls?: React.ReactNode;
  limitHeightToScreen?: boolean;
  className?: string;
}) => {
  return (
    <div
      className={`${
        limitHeightToScreen ? "h-screen" : "min-h-screen"
      } w-screen bg-primary-gradient-light-5.5`}
    >
      <div
        className={`${className} p-6 md:p-12 ${
          limitHeightToScreen ? "h-screen" : "min-h-screen"
        } relative z-10 flex flex-col items-center justify-center`}
      >
        <motion.div
          variants={dialogAnimationVariants}
          initial="initial"
          animate="animate"
          exit="exit"
          className="overflow-hidden bg-white rounded-lg shadow-xl max-w-7xl mx-auto flex flex-col"
        >
          <div className="bg-primary-gradient-light-4.5 p-3">
            <HLogo className="h-8" />
          </div>
          <section className="p-6 flex-1 overflow-y-auto">{children}</section>
          {controls}
        </motion.div>
      </div>
    </div>
  );
};
export default LargeCenterDialogLayout;
