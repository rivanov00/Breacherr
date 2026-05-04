export const BACKEND_IP = "192.168.1.3"; //// променете тук вашият IP адрес!
export const BACKEND_PORT = "8000";

export const getApiBase = () => {
  
  return `http://${BACKEND_IP}:${BACKEND_PORT}`;
};

