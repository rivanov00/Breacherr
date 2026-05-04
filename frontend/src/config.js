export const BACKEND_IP = "192.168.1.3"; //// променете тук вашият IP адрес!
export const BACKEND_PORT = "8000";

export const getApiBase = () => {
  const host = window.location.hostname;

  if (host === 'localhost' || host === '127.0.0.1') {
    return `http://${host}:${BACKEND_PORT}`;
  }

  return `http://${BACKEND_IP}:${BACKEND_PORT}`;
};

