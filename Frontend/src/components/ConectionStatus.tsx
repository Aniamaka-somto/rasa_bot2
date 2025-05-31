// src/context/ConnectionContext.tsx
import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { rasaService } from "../services/rasaService"; // Make sure this path is correct

interface ConnectionContextType {
  isOnline: boolean | null;
  isLoadingConnection: boolean; // Renamed from 'loading' to avoid confusion with chat loading
}

const ConnectionContext = createContext<ConnectionContextType | undefined>(
  undefined
);

export const useConnectionStatus = () => {
  const context = useContext(ConnectionContext);
  if (context === undefined) {
    throw new Error(
      "useConnectionStatus must be used within a ConnectionProvider"
    );
  }
  return context;
};

interface ConnectionProviderProps {
  children: ReactNode;
}

export const ConnectionProvider: React.FC<ConnectionProviderProps> = ({
  children,
}) => {
  const [isOnline, setIsOnline] = useState<boolean | null>(null);
  const [isLoadingConnection, setIsLoadingConnection] = useState<boolean>(true);

  useEffect(() => {
    const checkConnection = async () => {
      try {
        setIsLoadingConnection(true); // Start loading
        const status = await rasaService.checkStatus();
        setIsOnline(status.status !== "offline");
      } catch (error) {
        console.error("Error checking Rasa connection:", error);
        setIsOnline(false);
      } finally {
        setIsLoadingConnection(false); // End loading
      }
    };

    checkConnection(); // Initial check

    // Check connection every 30 seconds
    const interval = setInterval(checkConnection, 30000);

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  return (
    <ConnectionContext.Provider value={{ isOnline, isLoadingConnection }}>
      {children}
    </ConnectionContext.Provider>
  );
};
