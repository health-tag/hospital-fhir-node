import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import axios from 'axios';

import Input from './../../components/Input';
import Button from './../../components/Button';

import Logo from './../../assets/logo-main.png';

const LoginPage = () => {
  const navigate = useNavigate();

  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isDisplayErrorMessage, setIsDisplayErrorMessage] = useState<boolean>(false);

  const onClickLogin = async () => {
    setIsLoading(true);
    setIsDisplayErrorMessage(false);
    getUserInfo()
  };

  const getUserInfo = async () => {
    axios.get(`${process.env.REACT_APP_KONG_URL}/admin-api/consumers/${username}`,{
      auth: {
        username: username,
        password: password
      }
    })
    .then((response) => {
      setIsLoading(false);
      sessionStorage.setItem('username', username)
      sessionStorage.setItem('password', password)
      sessionStorage.setItem('hn', response.data.custom_id)
      navigate('/prescription', { replace: true });
    })
    .catch((error) => {
      setIsLoading(false);
      setIsDisplayErrorMessage(true);
    })
  }

  return (
    <div className="w-full h-screen flex flex-col items-center justify-center p-8 bg-blue-200">
      <div className="w-2/3 flex flex-col items-center">
        <img width="200" src={Logo} alt="" />
        

        {isDisplayErrorMessage && (
          <div className="mb-8 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative flex" role="alert">
            <strong className="font-bold">เข้าสู่ระบบผิดพลาด</strong>
            <span className="block sm:inline"> Username หรือ Password ไม่ถูกต้อง</span>
            <span onClick={() => setIsDisplayErrorMessage(false)}>
              <svg className="fill-current h-6 w-6 text-red-500" role="button" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><title>Close</title><path d="M14.348 14.849a1.2 1.2 0 0 1-1.697 0L10 11.819l-2.651 3.029a1.2 1.2 0 1 1-1.697-1.697l2.758-3.15-2.759-3.152a1.2 1.2 0 1 1 1.697-1.697L10 8.183l2.651-3.031a1.2 1.2 0 1 1 1.697 1.697l-2.758 3.152 2.758 3.15a1.2 1.2 0 0 1 0 1.698z"/></svg>
            </span>
          </div>
        )}
        <div className="bg-sky-400 shadow-md rounded px-8 pt-6 pb-8 mb-4 flex flex-col items-center">
          <h3 className="text-gray-700 text-2xl mb-4">ตรวจสอบข้อมูลยา</h3>
          <div className="mb-4">
            <Input
              placeholder="Username"
              value={username}
              setValue={setUsername}
              extraClass="mb-6"
            />
            <Input
              placeholder="Password"
              type="password"
              value={password}
              setValue={setPassword}
              extraClass="mb-6"
            />
          </div>
          <div className="flex items-center justify-between">
            <Button
              text="เข้าสู่ระบบ"
              isLoading={isLoading}
              onClick={onClickLogin}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
export default LoginPage;
