import React from "react";
import ChatArea from "./components/ChatArea";
import Navbar from "./components/Navbar";
import TextArea from "./components/TextArea";
import { ChatProvider } from "./context/ChatContext";

const App: React.FC = () => {
  return (
    <ChatProvider>
      <div className="flex flex-col h-screen">
        <Navbar />
        <div className="flex-1 overflow-hidden relative">
          <ChatArea />
          <TextArea />
        </div>
      </div>
    </ChatProvider>
  );
};

export default App;
