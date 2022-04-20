import { useEffect, useState } from "react";
import { useNavigate, NavLink } from "react-router-dom";
import axios from "axios";

import Input from "@components/Input";
import Button from "@components/Button";

import {
  AcceptIcon,
  ChevronIcon,
  PasswordResetIcon,
  UserAddIcon,
  UserGroupIcon,
} from "@components/Icons";
import { pageAnimationVariants } from "@animations/variants";
import { motion } from "framer-motion";
import { Modal } from "@components/Modal";
import { Form } from "@components/Form";

type RegisterData = { hospitalNumber: ""; pinCode: ""; pinCodeVerify: "" };

const AdminResetPinPage = () => {
  const navigate = useNavigate();
  const [alertModalData, setAlertModalData] = useState<{
    hospitalNumber: string;
  } | null>();
  const [errorModalData, setErrorModalData] = useState<{
    errorMessage: any;
  } | null>();

  const [isValid, setIsValid] = useState<boolean>(false);

  const [registerData, _setRegisterData] = useState<RegisterData>({
    hospitalNumber: "",
    pinCode: "",
    pinCodeVerify: "",
  });
  const setHospitalNumber = (value) =>
    _setRegisterData({ ...registerData, hospitalNumber: value });
  const setPinCode = (value) =>
    _setRegisterData({ ...registerData, pinCode: value });
  const setPinCodeVerify = (value) =>
    _setRegisterData({ ...registerData, pinCodeVerify: value });

  const [isWorking, setIsWorking] = useState<boolean>(false);

  const onSubmitHandler = async () => {
    await registerPatient();
  };

  const registerPatient = async () => {
    setIsWorking(true);
    const adminUsername = sessionStorage.getItem("admin_username")!;
    const adminPassword = sessionStorage.getItem("admin_password")!;
    if (isValid) {
      try {
        // Get user information
        const setPasswordData = {
          password: registerData.pinCode,
        };
        var response = await axios.get(
          `${process.env.REACT_APP_KONG_URL}/admin-api/consumers/${registerData.hospitalNumber}/basic-auth`,
          {
            auth: {
              username: adminUsername,
              password: adminPassword,
            },
          }
        );
        
        // Set user password
        await axios.put(
          `${process.env.REACT_APP_KONG_URL}/admin-api/consumers/${registerData.hospitalNumber}/basic-auth/${registerData.hospitalNumber}`,
          setPasswordData,
          {
            auth: {
              username: adminUsername,
              password: adminPassword,
            },
          }
        );
        setIsWorking(false);
        setAlertModalData({ hospitalNumber: registerData.hospitalNumber });
      } catch (error: any) {
        console.log({ error });
        setIsWorking(false);
        if (error.response.status === 409) {
          setErrorModalData({
            errorMessage: "มีหมายเลขประจำตัวผู้ป่วย (HN) นี้อยู่แล้วในระบบ",
          });
        } else {
          setErrorModalData({ errorMessage: error.message });
        }
      }
    }
  };
  const [escapeHatch, setEscapeHatch] = useState<number>();
  useEffect(() => {
    setEscapeHatch(Date.now);
  }, [registerData.pinCode, registerData.pinCodeVerify]);

  const pinValidator = (val: string) => {
    const result = /\d{6}/.test(val);
    return { result: result, message: "PIN ต้องเป็นตัวเลข 6 หลักเท่านั้น" };
  };

  const pinVerifyValidator = (val: string) => {
    return { result: val === registerData.pinCode, message: "PIN ไม่ตรงกัน" };
  };

  return (
    <motion.div
      variants={pageAnimationVariants}
      initial="initial"
      animate="animate"
      exit="exit"
    >
      <h3 className="page-h mb-0">
        <NavLink to="./../">
          <UserGroupIcon className="h-8 w-8 inline-block mr-3" />
          จัดการผู้ใช้งาน
        </NavLink>
        <ChevronIcon side="right" className="h-8 w-8 inline-block" />
        <PasswordResetIcon className="h-8 w-8 inline-block mr-3 " />
        รีเซ็ท PIN ของผู้ใช้งาน
      </h3>
      <Form
        className="card p-6"
        onValidSubmit={onSubmitHandler}
        onValidityChange={setIsValid}
      >
        <Input
          type="text"
          name="hospitalNumber"
          value={registerData.hospitalNumber}
          setValue={(val: string) => setHospitalNumber(val.trim())}
          required
          label="หมายเลขประจำตัวผู้ป่วย"
          placeholder="HN"
          className="mb-6"
        />
        <Input
          type="password"
          name="pinCode"
          value={registerData.pinCode}
          setValue={(val: string) => setPinCode(val.trim().replace(/\D/, ""))}
          required
          validator={pinValidator}
          label="ตั้งรหัสตัวเลข (PIN) ใหม่ สำหรับผู้รับบริการเข้าสู่ระบบ"
          inputMode="numeric"
          placeholder="PIN 6 หลัก"
          maxLength={6}
          minLength={6}
          className="mb-6"
        />
        <Input
          forceRevalidate={escapeHatch}
          type="password"
          name="pinCodeVerify"
          value={registerData.pinCodeVerify}
          setValue={(val: string) =>
            setPinCodeVerify(val.trim().replace(/\D/, ""))
          }
          validator={pinVerifyValidator}
          label="ยืนยันรหัสตัวเลข (PIN) ใหม่ สำหรับผู้รับบริการเข้าสู่ระบบ"
          required
          inputMode="numeric"
          placeholder="ใส่ PIN 6 หลัก อีกครั้ง"
          maxLength={6}
          minLength={6}
          className="mb-6"
        />
        <Button
          type="submit"
          mode="primary"
          disabled={!isValid || isWorking}
          isLoading={isWorking}
        >
          <AcceptIcon />
          ยืนยัน
        </Button>
      </Form>
      {alertModalData && (
        <Modal
          buttons={
            <>
              <Button mode="primary" onClick={() => navigate("./../")}>
                <AcceptIcon />
                เสร็จสิ้น
              </Button>
              <Button
                className=" whitespace-nowrap"
                mode="secondary"
                onClick={() => setAlertModalData(null)}
              >
                <UserAddIcon />
                รีเซ็ท PIN คนอื่นต่อ
              </Button>
            </>
          }
          title="สำเร็จ"
        >
          <p>
            ทำการรีเซ็ท PIN ของ {alertModalData.hospitalNumber} เรียบร้อยแล้ว
          </p>
        </Modal>
      )}
      {errorModalData && (
        <Modal
          buttons={
            <>
              <Button mode="secondary" onClick={() => setErrorModalData(null)}>
                <AcceptIcon />
                ปิด
              </Button>
            </>
          }
          title="เกิดข้อผิดพลาด"
        >
          <p>{errorModalData.errorMessage}</p>
        </Modal>
      )}
    </motion.div>
  );
};
export default AdminResetPinPage;
