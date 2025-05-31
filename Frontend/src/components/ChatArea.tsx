import React, { useRef, useEffect } from "react";
import { ChatEnd, ChatStart, ChatLoading, TypingEffect } from "./ChatBubble"; // Import TypingEffect
import { useChat, ChatMessage } from "../context/ChatContext";

const ChatArea: React.FC = () => {
  const { messages, isBotTyping, currentTypingText } = useChat(); // Get isBotTyping and currentTypingText
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isBotTyping, currentTypingText]); // Scroll when anything changes that affects chat height

  return (
    <div className="px-5 py-10 mt-10 pb-20 overflow-y-auto max-h-[calc(100vh-80px)]">
      {messages.length === 0 && !isBotTyping && !currentTypingText ? ( // Only show "Start conversation" if truly empty
        <div className="flex justify-center items-center h-64 text-gray-400">
          Start a conversation with the chatbot
        </div>
      ) : (
        messages.map((message: ChatMessage, index: number) =>
          message.sender === "user" ? (
            <ChatEnd key={index} text={message.text} />
          ) : (
            <ChatStart
              key={index}
              text={message.text}
              buttons={message.buttons}
              image={message.image}
              isError={message.isError}
            />
          )
        )
      )}

      {/* Conditionally render TypingEffect if bot is currently typing a message */}
      {isBotTyping && currentTypingText && (
        <ChatStart // Re-use ChatStart's structure
          text={currentTypingText}
          buttons={undefined} // No buttons during typing
          image={undefined}
          isError={false}
        />
      )}

      {/* Conditionally render ChatLoading when bot is processing or waiting to type next message */}
      {isBotTyping &&
        !currentTypingText &&
        messages.length > 0 &&
        messages[messages.length - 1].sender === "bot" && <ChatLoading />}
      {/* Also show ChatLoading at the very start if bot is typing the first message */}
      {isBotTyping && !currentTypingText && messages.length === 0 && (
        <ChatLoading />
      )}

      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatArea;
