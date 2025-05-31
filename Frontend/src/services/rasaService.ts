// src/services/rasaService.ts
// Additional utility functions for Rasa API interaction
interface RasaStatus {
  status: string;
  version?: string;
  [key: string]: any;
}

interface RasaDomain {
  intents: string[];
  entities: string[];
  actions: string[];
  responses: Record<string, any>;
  [key: string]: any;
}

export const rasaService = {
  // Function to check if Rasa server is online
  checkStatus: async (): Promise<RasaStatus> => {
    try {
      const response = await fetch("http://localhost:5005/status");
      return await response.json();
    } catch (error) {
      console.error("Rasa server status check failed:", error);
      return { status: "offline" };
    }
  },

  // Function to get Rasa domain info (available intents, actions, etc.)
  getDomainInfo: async (): Promise<RasaDomain | null> => {
    try {
      const response = await fetch("http://localhost:5005/domain");
      return await response.json();
    } catch (error) {
      console.error("Failed to fetch Rasa domain info:", error);
      return null;
    }
  },
};
