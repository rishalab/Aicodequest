import { Routes, Route } from "react-router-dom";
import Login from "./Pages/Login";
import Home from "./Pages/Home";
import CodeEditor from "./Pages/CodeEditor";
import Rules from "./Pages/Rules";

export default function App() {
  return (
    <>
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/home" element={<Home />} />
      <Route path="/editor" element={<CodeEditor/>} />
      <Route path="/rules" element={<Rules/>} />
    </Routes>
    </>
  );
}
