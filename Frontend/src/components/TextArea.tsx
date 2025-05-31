import React, { useState, FormEvent, useRef, useEffect } from "react"; // Import useRef and useEffect
import { IoMdSend } from "react-icons/io";
import { LiaLinkSolid } from "react-icons/lia";
import { useChat } from "../context/ChatContext";

const TextArea: React.FC = () => {
  const [message, setMessage] = useState<string>("");
  const { sendMessage, loading } = useChat();
  const inputRef = useRef<HTMLInputElement>(null);
  const handleSubmit = (e: FormEvent<HTMLFormElement>): void => {
    e.preventDefault();

    if (message.trim() && !loading) {
      sendMessage(message);
      setMessage("");
      if (inputRef.current) {
        inputRef.current.focus();
      }
    }
  };

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  return (
    <div className="fixed bottom-0 w-full shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1),0_-2px_4px_-2px_rgba(0,0,0,0.1)] min-h-14 max-h-20 px-3.5 py-1 flex justify-center items-center z-50 bg-base-200">
      <form
        onSubmit={handleSubmit}
        className="w-full flex gap-x-2.5 h-full justify-center items-center"
      >
        <div className="w-fit">
          <button
            type="button"
            className="text-gray-500 hover:text-blue-600 text-xl"
          >
            <LiaLinkSolid />
          </button>
        </div>
        <div className="w-full">
          <input
            ref={inputRef}
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type a message..."
            className="w-full h-10 rounded-2xl px-4 ring-1 ring-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
            autoComplete="off"
          />
        </div>
        <div className="w-fit">
          <button
            type="submit"
            className={`text-2xl ${
              message.trim() && !loading
                ? "text-blue-600"
                : "text-gray-400 cursor-not-allowed"
            }`}
            disabled={!message.trim() || loading}
          >
            <IoMdSend />
          </button>
        </div>
      </form>
    </div>
  );
};

export default TextArea;
