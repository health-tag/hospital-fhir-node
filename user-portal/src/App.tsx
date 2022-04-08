import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import LoginPage from './pages/Login';
import PrescriptionPage from "./pages/Prescription";
import AdminLoginPage from './pages/AdminLogin';
import AdminRegisterPage from './pages/Register';

import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          
          <Route path="/admin" element={<AdminLoginPage />} />
          <Route path="/admin/register" element={<AdminRegisterPage />} />
          <Route path="/prescription" element={<PrescriptionPage />} />
          <Route path="/" element={<LoginPage />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
