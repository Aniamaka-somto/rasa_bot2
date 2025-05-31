import { FaRobot } from "react-icons/fa";
import ThemeButton from "./ThemeButton";

const Navbar = () => {
  return (
    <div className="h-16 w-full bg-green-700 flex justify-between items-center px-7 text-white fixed top-0 z-50">
      <div className="flex items-center gap-x-2">
        <div className="rounded-full bg-green-500 p-1 flex justify-center items-center">
          <FaRobot className="text-2xl" />
        </div>
        <div className="">
          <h3 className="text-sm font-bold">Chatbot</h3>
          <p className="text-xs">online</p>
        </div>
      </div>
      <ThemeButton />
    </div>
  );
};

export default Navbar;
