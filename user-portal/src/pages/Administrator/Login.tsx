import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import Input from "@components/Input";
import Button from "@components/Button";
import SmallCenterDialogLayout from "@layouts/smallCenterDialogLayout";
import { KeyIcon } from "@components/Icons";
import { Message } from "@components/Message";
import { Form } from "@components/Form";
import { nameof } from "@utilities/ts";

type LoginData = { username: ""; password: "" };

const AdminLoginPage = () => {
  const navigate = useNavigate();
  const [loginData, _setLoginData] = useState<LoginData>({
    username: "",
    password: "",
  });
  const setUserName = (value) =>
    _setLoginData({ ...loginData, username: value });
  const setPassword = (value) =>
    _setLoginData({ ...loginData, password: value });
  const [isValid, setIsValid] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isDisplayErrorMessage, setIsDisplayErrorMessage] =
    useState<boolean>(false);

  const handleOnValidSubmit = async () => {
    setIsLoading(true);
    setIsDisplayErrorMessage(false);
    await getUserInfo();
  };

  const getUserInfo = async () => {
    try {
      await axios.get(
        `${process.env.REACT_APP_KONG_URL}/admin-api/consumers/`,
        {
          auth: {
            username: loginData.username,
            password: loginData.password,
          },
        }
      );
      setIsLoading(false);
      sessionStorage.setItem("admin_username", loginData.username);
      sessionStorage.setItem("admin_password", loginData.password);
      navigate("/admin/console/manage-people");
    } catch (error) {
      setIsLoading(false);
      setIsDisplayErrorMessage(true);
    }
  };

  return (
    <SmallCenterDialogLayout>
      {isDisplayErrorMessage && (
        <Message
          type="error"
          title="เข้าสู่ระบบผิดพลาด"
          onClose={() => setIsDisplayErrorMessage(false)}
        >
          Username หรือ Password ไม่ถูกต้อง
        </Message>
      )}
      <div className="flex flex-col gap-6 min-w-[360px]">
        <h3 className="text-gray-700">เข้าสู่ระบบ</h3>
        <h4 className="text-gray-700">ผู้ดูแลระบบ</h4>
        <Form
          onValidSubmit={handleOnValidSubmit}
          onValidityChange={setIsValid}
          className="flex flex-col gap-6"
        >
          <Input
            label="ชื่อผู้ใช้"
            required
            placeholder="ชื่อผู้ใช้"
            name={nameof<LoginData>("username")}
            value={loginData.username}
            setValue={setUserName}
          />
          <Input
            label="รหัสผ่าน"
            required
            placeholder="รหัสผ่าน"
            type="password"
            name={nameof<LoginData>("password")}
            value={loginData.password}
            setValue={setPassword}
          />
          <Button
            mode="primary"
            type="submit"
            disabled={isLoading || !isValid}
            isLoading={isLoading}
          >
            <KeyIcon />
            เข้าสู่ระบบ
          </Button>
        </Form>
      </div>
    </SmallCenterDialogLayout>
  );
};
export default AdminLoginPage;
