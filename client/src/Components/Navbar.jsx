import "../styles/navbar.css";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <header className="navbar">
      <h1 className="logo"><Link to={"/home"}>AICodeQuest</Link></h1>
      <div className="flex">
        <span className="rules-link"><Link to={"/rules"}>How to Play ?</Link></span>
        <span className="research-link"><a href="https://rishalab.in/">RISHA Lab</a></span>
      </div>
    </header>
  );
}
