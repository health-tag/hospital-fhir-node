import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import axios from "axios";

import Input from "@components/Input";
import Button from "@components/Button";

import Logo from "@assets/logo/logo-main.png";
import { AcceptIcon } from "@components/Icons";

const AdminRegisterPage = () => {
  const navigate = useNavigate();

  const [HN, setHN] = useState<string>("");
  const [pinCode, setPinCode] = useState<string>("");
  const [pinCodeVerify, setPinCodeVerify] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isDisplayErrorMessage, setIsDisplayErrorMessage] =
    useState<boolean>(false);
  const [isDisplaySuccessMessage, setIsDisplaySuccessMessage] =
    useState<boolean>(false);

  const onClickSubmit = async () => {
    setIsLoading(true);
    setIsDisplaySuccessMessage(false);
    setIsDisplayErrorMessage(false);
    registerPatient();
  };

  const registerPatient = async () => {
    const adminUsername = sessionStorage.getItem("admin_username")!;
    const adminPassword = sessionStorage.getItem("admin_password")!;
    if (pinCode == pinCodeVerify) {
      const consumerData = {
        username: HN,
        custom_id: HN,
      };
      axios
        .post(
          `${process.env.REACT_APP_KONG_URL}/admin-api/consumers/`,
          consumerData,
          {
            auth: {
              username: adminUsername,
              password: adminPassword,
            },
          }
        )
        .then((response) => {
          const setPasswordData = {
            username: HN,
            password: pinCode,
          };
          axios
            .post(
              `${process.env.REACT_APP_KONG_URL}/admin-api/consumers/${HN}/basic-auth`,
              setPasswordData,
              {
                auth: {
                  username: adminUsername,
                  password: adminPassword,
                },
              }
            )
            .then((response) => {
              setIsLoading(false);
              setHN("");
              setPinCode("");
              setPinCodeVerify("");
              setIsDisplaySuccessMessage(true);
            })
            .catch((error) => {
              setIsLoading(false);
              setIsDisplayErrorMessage(true);
            });
        })
        .catch((error) => {
          setIsLoading(false);
          setIsDisplayErrorMessage(true);
        });
    } else {
      setIsLoading(false);
      setIsDisplayErrorMessage(true);
    }
  };

  return (
    <div className="w-full h-screen flex flex-col items-center justify-center p-8 bg-blue-200">
      <div className="w-2/3 flex flex-col items-center">
        <img width="200" src={Logo} alt="" />

        {isDisplayErrorMessage && (
          <div
            className="mb-8 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative flex"
            role="alert"
          >
            <strong className="font-bold">PinCode ไม่ตรงกัน</strong>
            <span onClick={() => setIsDisplayErrorMessage(false)}>
              <svg
                className="fill-current h-6 w-6 text-red-500"
                role="button"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
              >
                <title>Close</title>
                <path d="M14.348 14.849a1.2 1.2 0 0 1-1.697 0L10 11.819l-2.651 3.029a1.2 1.2 0 1 1-1.697-1.697l2.758-3.15-2.759-3.152a1.2 1.2 0 1 1 1.697-1.697L10 8.183l2.651-3.031a1.2 1.2 0 1 1 1.697 1.697l-2.758 3.152 2.758 3.15a1.2 1.2 0 0 1 0 1.698z" />
              </svg>
            </span>
          </div>
        )}
        {isDisplaySuccessMessage && (
          <div
            className="mb-8 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative flex"
            role="alert"
          >
            <strong className="font-bold">ลงทะเบียนสำเร็จ</strong>
            <span onClick={() => setIsDisplayErrorMessage(false)}>
              <svg
                className="fill-current h-6 w-6 text-green-500"
                role="button"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
              >
                <title>Close</title>
                <path d="M14.348 14.849a1.2 1.2 0 0 1-1.697 0L10 11.819l-2.651 3.029a1.2 1.2 0 1 1-1.697-1.697l2.758-3.15-2.759-3.152a1.2 1.2 0 1 1 1.697-1.697L10 8.183l2.651-3.031a1.2 1.2 0 1 1 1.697 1.697l-2.758 3.152 2.758 3.15a1.2 1.2 0 0 1 0 1.698z" />
              </svg>
            </span>
          </div>
        )}

        <div className="bg-sky-400 shadow-md rounded px-8 pt-6 pb-8 mb-4 flex flex-col items-center">
          <h3 className="text-gray-700 text-2xl mb-4">
            เข้าสู่ระบบสร้าง Username ผู้ป่วย
          </h3>
          <div className="mb-4">
            <Input
              placeholder="HN"
              value={HN}
              required
              setValue={setHN}
              extraClass="mb-6"
            />
            <Input
              placeholder="Pincode"
              type="password"
              required
              inputMode="numeric"
              value={pinCode}
              setValue={setPinCode}
              extraClass="mb-6"
            />
            <Input
              placeholder="Pincode Verify"
              type="password"
              required
              inputMode="numeric"
              value={pinCodeVerify}
              setValue={setPinCodeVerify}
              extraClass="mb-6"
            />
          </div>
          <div className="flex items-center justify-between">
            <Button
              disabled={isLoading}
              isLoading={isLoading}
              onClick={onClickSubmit}
            >
              <AcceptIcon />
              ลงทะเบียนผู้ป่วย
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};
export default AdminRegisterPage;
