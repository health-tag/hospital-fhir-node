import { pageAnimationVariants } from "@animations/variants";
import { HospitalIcon, UserAddIcon, UserGroupIcon } from "@components/Icons";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

const PersonManagerPage = () => {
  const navigate = useNavigate();
  return (
    <motion.div
      variants={pageAnimationVariants}
      initial="initial"
      animate="animate"
      exit="exit"
    >
      <h3 className="page-h">
        <UserGroupIcon className="h-8 w-8 inline-block mr-3" />
        จัดการผู้ใช้งาน
      </h3>
      <div
        className="card flex items-center cursor-pointer hover:text-secondary transition-all hover:bg-secondary-light-5.5"
        onClick={() => navigate("register")}
      >
        <UserAddIcon className="w-12 h-12 ml-6" />
        <div className="p-6 flex-1">
          <h4>ลงทะเบียนผู้รับบริการ</h4>
          <p>เพิ่มผู้รับบริการรายใหม่</p>
        </div>
      </div>
    </motion.div>
  );
};
export default PersonManagerPage;
