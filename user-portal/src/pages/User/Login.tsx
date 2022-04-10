import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import Input from "@components/Input";
import Button from "@components/Button";
import SmallCenterDialogLayout from "@layouts/smallCenterDialogLayout";
import { KeyIcon } from "@components/Icons";
import { Message } from "@components/Message";

const LoginPage = () => {
  const navigate = useNavigate();

  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [isValid, setIsValid] = useState<boolean>();
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isDisplayErrorMessage, setIsDisplayErrorMessage] =
    useState<boolean>(false);

  useEffect(() => {
    setIsValid(username !== "" && password !== "");
  }, [username, password]);

  const onSubmitHandler = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setIsDisplayErrorMessage(false);
    await getUserInfo();
  };

  const getUserInfo = async () => {
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_KONG_URL}/admin-api/consumers/${username}`,
        {
          auth: {
            username: username,
            password: password,
          },
        }
      );
      setIsLoading(false);
      sessionStorage.setItem("username", username);
      sessionStorage.setItem("password", password);
      sessionStorage.setItem("hn", response.data.custom_id);
      navigate("/user/console/medications");
    } catch (error) {
      setIsLoading(false);
      setIsDisplayErrorMessage(true);
    }
  };

  return (
    <SmallCenterDialogLayout>
      {isDisplayErrorMessage && (
        <Message type="error" title="เข้าสู่ระบบผิดพลาด">
          Username หรือ Password ไม่ถูกต้อง
        </Message>
      )}
      <div className="flex flex-col gap-6 min-w-[360px]">
        <h3 className="text-gray-700">เข้าสู่ระบบ</h3>
        <form onSubmit={onSubmitHandler} className="flex flex-col gap-6">
          <Input
            label="ชื่อผู้ใช้"
            required
            placeholder="ชื่อผู้ใช้"
            value={username}
            setValue={setUsername}
          />
          <Input
            label="รหัสผ่าน"
            required
            placeholder="รหัสผ่าน"
            type="password"
            value={password}
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
        </form>
      </div>
    </SmallCenterDialogLayout>
  );
};
export default LoginPage;
