// src/context/ChatContext.tsx
import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useRef,
  ReactNode,
} from "react";
import config from "../config";

// Define types for our chat messages
export interface Button {
  title: string;
  payload: string;
}

export interface ChatMessage {
  sender: "user" | "bot";
  text: string;
  timestamp: string;
  buttons?: Button[];
  image?: string | null;
  isError?: boolean;
}

// Define the shape of our context
interface ChatContextType {
  messages: ChatMessage[];
  loading: boolean; // For initial network loading
  error: string | null;
  sendMessage: (message: string) => Promise<void>;
  clearChat: () => void;
  isBotTyping: boolean; // Indicates if *any* bot message is currently being typed or is pending
  currentTypingText: string; // The text currently being "typed" out
}

// Create the context with default values
const ChatContext = createContext<ChatContextType>({
  messages: [],
  loading: false,
  error: null,
  sendMessage: async () => {},
  clearChat: () => {},
  isBotTyping: false,
  currentTypingText: "",
});

// Custom hook to use the chat context
export const useChat = () => useContext(ChatContext);

// Props for the provider component
interface ChatProviderProps {
  children: ReactNode;
}

// Chat provider component
export const ChatProvider: React.FC<ChatProviderProps> = ({ children }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState<boolean>(false); // Initial network request loading
  const [error, setError] = useState<string | null>(null);
  const [isBotTyping, setIsBotTyping] = useState<boolean>(false); // Indicates if bot is actively typing a message
  const [currentTypingText, setCurrentTypingText] = useState<string>(""); // The text being typed character by character

  // Ref to hold messages that are pending display
  const pendingBotMessagesRef = useRef<ChatMessage[]>([]);
  // Ref to hold the timeout ID for staggered display or character typing
  const typingTimeoutRef = useRef<number | null>(null);
  const messageIndexRef = useRef<number>(0); // To keep track of characters being typed

  // Function to process and display bot messages one by one
  const processAndDisplayBotMessages = (botResponses: ChatMessage[]) => {
    pendingBotMessagesRef.current = [...botResponses]; // Add all new bot messages to the queue
    setIsBotTyping(true); // Set to true to show the initial typing indicator

    // Clear any existing timeout to avoid conflicts
    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current);
    }
    messageIndexRef.current = 0; // Reset character index for new message

    displayNextBotMessage(); // Start displaying messages
  };

  const displayNextBotMessage = () => {
    // If there are still pending messages, or if we are currently typing a message
    if (
      pendingBotMessagesRef.current.length > 0 ||
      currentTypingText.length > 0
    ) {
      const currentMessage = pendingBotMessagesRef.current[0]; // Peek at the first message

      if (!currentMessage) {
        // This case handles when the queue is emptied between `displayNextBotMessage` calls
        // This should theoretically not be hit if `pendingBotMessagesRef.current.length > 0` above is true.
        setIsBotTyping(false);
        setCurrentTypingText("");
        return;
      }

      // Check if we finished typing the current message
      if (messageIndexRef.current < currentMessage.text.length) {
        // Continue typing character by character
        const nextChar = currentMessage.text.charAt(messageIndexRef.current);
        setCurrentTypingText((prevText) => prevText + nextChar);
        messageIndexRef.current++;

        // Speed up typing animation (e.g., 20ms per character)
        const charTypingDelay = 20;
        typingTimeoutRef.current = window.setTimeout(
          displayNextBotMessage,
          charTypingDelay
        );
      } else {
        // Current message typing is complete, add it to the main messages array
        setMessages((prev) => [...prev, currentMessage]);
        pendingBotMessagesRef.current.shift(); // Remove the now-displayed message from queue

        // Reset for the next message
        setCurrentTypingText("");
        messageIndexRef.current = 0;

        // Short delay before processing the next message (e.g., 500ms between messages)
        const delayBeforeNextMessage = 500;
        if (pendingBotMessagesRef.current.length > 0) {
          typingTimeoutRef.current = window.setTimeout(
            displayNextBotMessage,
            delayBeforeNextMessage
          );
        } else {
          // No more pending messages, stop typing animation
          setIsBotTyping(false);
          typingTimeoutRef.current = null;
        }
      }
    } else {
      // No more messages to display or type
      setIsBotTyping(false);
      setCurrentTypingText("");
      typingTimeoutRef.current = null;
    }
  };

  // Clear any active timeouts when the component unmounts
  useEffect(() => {
    return () => {
      if (typingTimeoutRef.current) {
        clearTimeout(typingTimeoutRef.current);
      }
    };
  }, []);

  // Function to send message to Rasa and get response
  const sendMessage = async (message: string): Promise<void> => {
    try {
      setLoading(true); // Indicate initial network request loading
      setError(null); // Clear any previous errors

      // Add user message to the chat
      const userMessage: ChatMessage = {
        sender: "user",
        text: message,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, userMessage]);

      // Send message to Rasa server
      const response = await fetch(
        `${config.RASA_URL}${config.RASA_WEBHOOK_PATH}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            sender: "user", // You can use a unique user ID here
            message: message,
          }),
        }
      );

      const data = await response.json();

      // Process Rasa responses
      if (data && data.length > 0) {
        const botResponses: ChatMessage[] = data.map((item: any) => ({
          sender: "bot",
          text: item.text,
          timestamp: new Date().toISOString(),
          buttons: item.buttons || [],
          image: item.image || null,
        }));
        processAndDisplayBotMessages(botResponses); // Start staggered display
      } else {
        // Handle empty response
        processAndDisplayBotMessages([
          {
            sender: "bot",
            text: "Sorry, I didn't understand that.",
            timestamp: new Date().toISOString(),
          },
        ]);
      }
    } catch (err) {
      console.error("Error sending message to Rasa:", err);
      setError("Failed to connect to the chatbot. Please try again later.");

      // Add error message to chat directly, without staggering
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Sorry, I'm having trouble connecting. Please try again later.",
          timestamp: new Date().toISOString(),
          isError: true,
        },
      ]);
      setIsBotTyping(false); // Stop typing if error occurs
      setCurrentTypingText(""); // Clear typing text on error
    } finally {
      setLoading(false); // Overall network loading done after initial fetch
    }
  };

  // Clear chat history
  const clearChat = (): void => {
    setMessages([]);
    setIsBotTyping(false);
    setCurrentTypingText("");
    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current);
      typingTimeoutRef.current = null;
    }
    pendingBotMessagesRef.current = [];
    messageIndexRef.current = 0;
  };

  // Values to be provided by context
  const value: ChatContextType = {
    messages,
    loading,
    error,
    sendMessage,
    clearChat,
    isBotTyping,
    currentTypingText, // Provide the new state
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};
