import React from "react";
import { FaRobot } from "react-icons/fa";
import { FaUser } from "react-icons/fa";
import { useChat, Button } from "../context/ChatContext";

// Props for the ChatEnd component
interface ChatEndProps {
  text: string;
}

// Props for the ChatStart component
interface ChatStartProps {
  text: string;
  buttons?: Button[];
  image?: string | null;
  isError?: boolean;
}

export const TypingDots: React.FC = () => {
  return (
    <div className="loading-dots">
      <span className="dot"></span>
      <span className="dot"></span>
      <span className="dot"></span>
    </div>
  );
};

export const ChatLoading: React.FC = () => {
  return (
    <div className="chat chat-start">
      <div className="chat-image avatar">
        <div className="lg:w-10 w-7 rounded-full flex justify-center items-center p-2">
          <FaRobot className="w-full h-auto" />
        </div>
      </div>
      <div className="chat-header">Chatbot</div>
      <div className="chat-bubble text-sm min-h-8 flex items-center justify-center py-4">
        <TypingDots />
      </div>
    </div>
  );
};

// Bot message bubble (start-aligned)
export const ChatStart: React.FC<ChatStartProps> = ({
  text,
  buttons,
  image,
  isError,
}) => {
  const { sendMessage, isBotTyping, currentTypingText } = useChat(); // Use currentTypingText to decide if parsing

  // Handle button click from Rasa's quick replies
  const handleButtonClick = (payload: string): void => {
    if (payload) {
      sendMessage(payload);
    }
  };

  // Function to parse text for bold formatting (apply only to full messages)
  const parseTextForBold = (inputText: string) => {
    // Regex to find text surrounded by **
    const parts = inputText.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, index) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        // Remove the asterisks and wrap in <strong>
        return <strong key={index}>{part.slice(2, -2)}</strong>;
      }
      return <span key={index}>{part}</span>;
    });
  };

  // Determine if this bubble is currently the one being typed out
  const isThisBubbleTyping = isBotTyping && text === currentTypingText;

  return (
    <div className="chat chat-start">
      <div className="chat-image avatar">
        <div className="lg:w-10 w-7 rounded-full flex justify-center items-center p-2">
          <FaRobot className="w-full h-auto" />
        </div>
      </div>
      <div className="chat-header">Chatbot</div>
      <div
        className={`chat-bubble text-sm ${
          isError ? "bg-red-100 text-red-800" : ""
        }`}
      >
        {/* Display message text, applying bold parsing only if not currently typing */}
        <p className="break-words">
          {isThisBubbleTyping ? text : parseTextForBold(text)}
        </p>

        {/* Display image if available, only after typing is complete */}
        {!isThisBubbleTyping && image && (
          <div className="mt-2">
            <img
              src={image}
              alt="Bot attachment"
              className="max-w-full rounded-md"
              onError={(e: React.SyntheticEvent<HTMLImageElement>) => {
                const target = e.target as HTMLImageElement;
                target.onerror = null;
                target.src = "/api/placeholder/200/150"; // Fallback image
                target.alt = "Image failed to load";
              }}
            />
          </div>
        )}

        {/* Display buttons if available, only after typing is complete */}
        {!isThisBubbleTyping && buttons && buttons.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-2">
            {buttons.map((button: Button, idx: number) => (
              <button
                key={idx}
                onClick={() => handleButtonClick(button.payload)}
                className="bg-white border border-blue-500 text-blue-500 px-3 py-1 rounded-full text-sm hover:bg-blue-50 transition-colors"
              >
                {button.title}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// User message bubble (end-aligned)
export const ChatEnd: React.FC<ChatEndProps> = ({ text }) => {
  return (
    <div className="chat chat-end">
      <div className="chat-image avatar">
        <div className="lg:w-10 w-7 rounded-full flex justify-center items-center p-2 bg-gray-300 dark:bg-gray-200">
          <FaUser className="w-full h-auto" />
        </div>
      </div>
      <div className="chat-header">User</div>
      <div className="chat-bubble bg-blue-600 text-white">
        <p className="break-words">{text}</p>
      </div>
    </div>
  );
};
