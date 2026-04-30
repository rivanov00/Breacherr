// ⚙️ КОНФИГУРАЦИЯ НА IP АДРЕС
export const BACKEND_IP = "192.168.1.3"; 
export const BACKEND_PORT = "8000";

export const getApiBase = () => {
  const host = window.location.hostname;
  
  // Ако сме на компютъра (localhost или 127.0.0.1)
  if (host === 'localhost' || host === '127.0.0.1') {
    // Използваме ТОЧНО същия хост, който е в браузъра, за да няма CORS конфликти
    return `http://${host}:${BACKEND_PORT}`;
  }
  
  // За мобилното приложение
  return `http://${BACKEND_IP}:${BACKEND_PORT}`;
};
