// src/utils/rasaUtils.ts

// Environment variable types
interface RasaConfig {
  API_URL: string;
  WEBHOOK_ENDPOINT: string;
  STATUS_ENDPOINT: string;
  DOMAIN_ENDPOINT: string;
  DEFAULT_TIMEOUT: number;
}

import config from "../config";

// Set up configuration
export const RASA_CONFIG: RasaConfig = {
  API_URL: config.RASA_URL,
  WEBHOOK_ENDPOINT: config.RASA_WEBHOOK_PATH,
  STATUS_ENDPOINT: config.RASA_STATUS_PATH,
  DOMAIN_ENDPOINT: config.RASA_DOMAIN_PATH,
  DEFAULT_TIMEOUT: config.API_TIMEOUT,
};

// Error types
export enum RasaErrorType {
  CONNECTION = "connection",
  TIMEOUT = "timeout",
  SERVER = "server",
  UNKNOWN = "unknown",
}

// Error class for Rasa API
export class RasaAPIError extends Error {
  type: RasaErrorType;
  statusCode?: number;

  constructor(message: string, type: RasaErrorType, statusCode?: number) {
    super(message);
    this.name = "RasaAPIError";
    this.type = type;
    this.statusCode = statusCode;
  }
}

// Helper function to handle API timeouts
export const withTimeout = <T>(promise: Promise<T>, ms: number): Promise<T> => {
  const timeout = new Promise<never>((_, reject) => {
    setTimeout(() => {
      reject(new RasaAPIError("Request timed out", RasaErrorType.TIMEOUT));
    }, ms);
  });

  return Promise.race([promise, timeout]);
};

// Helper to create the full API URL
export const getApiUrl = (endpoint: string): string => {
  return `${RASA_CONFIG.API_URL}${endpoint}`;
};
