// src/config.ts

// interface AppConfig {
//   RASA_URL: string;
//   RASA_WEBHOOK_PATH: string;
//   RASA_STATUS_PATH: string;
//   RASA_DOMAIN_PATH: string;
//   API_TIMEOUT: number;
//   BOT_NAME: string;
// }

// const config: AppConfig = {
//   RASA_URL: process.env.REACT_APP_RASA_URL || "http://localhost:5005",
//   RASA_WEBHOOK_PATH: "/webhooks/rest/webhook",
//   RASA_STATUS_PATH: "/status",
//   RASA_DOMAIN_PATH: "/domain",
//   API_TIMEOUT: 10000,
//   BOT_NAME: process.env.REACT_APP_BOT_NAME || "Rasa Assistant",
// };

// export default config;
interface AppConfig {
  RASA_URL: string;
  RASA_WEBHOOK_PATH: string;
  RASA_STATUS_PATH: string;
  RASA_DOMAIN_PATH: string;
  API_TIMEOUT: number;
  BOT_NAME: string;
}

const config: AppConfig = {
  RASA_URL: import.meta.env.VITE_RASA_URL || "http://localhost:5005",
  RASA_WEBHOOK_PATH: "/webhooks/rest/webhook",
  RASA_STATUS_PATH: "/status",
  RASA_DOMAIN_PATH: "/domain",
  API_TIMEOUT: 10000,
  BOT_NAME: import.meta.env.VITE_BOT_NAME || "Rasa Assistant",
};

export default config;
