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

const LoginPage = () => {
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
      const response = await axios.get(
        `${process.env.REACT_APP_KONG_URL}/admin-api/consumers/${loginData.username}`,
        {
          auth: {
            username: loginData.username,
            password: loginData.password,
          },
        }
      );
      setIsLoading(false);
      sessionStorage.setItem("username", loginData.username);
      sessionStorage.setItem("password", loginData.password);
      sessionStorage.setItem("hn", response.data.custom_id);
      navigate("/user/console/medications");
    } catch (error) {
      setIsLoading(false);
      setIsDisplayErrorMessage(true);
    }
  };

  const pinValidator = (val: string) => {
    const result = /\d{6}/.test(val);
    return { result: result, message: "PIN ต้องเป็นตัวเลข 6 หลักเท่านั้น" };
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
            label="รหัสตัวเลข"
            required
            placeholder="รหัสตัวเลข 6 หลัก"
            maxLength={6}
            type="password"
            inputMode="numeric"
            name={nameof<LoginData>("password")}
            value={loginData.password}
            validator={pinValidator}
            setValue={(val: string) => setPassword(val.trim().replace(/\D/, ""))}
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
export default LoginPage;
