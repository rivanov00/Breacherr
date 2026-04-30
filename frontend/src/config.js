// ⚙️ КОНФИГУРАЦИЯ НА IP АДРЕС
export const BACKEND_IP = "192.168.1.3"; // ТУК ВЪВЕДЕТЕ ВАШИЯТ IP ADDRESS за мобилното приложение
export const BACKEND_PORT = "8000";

export const getApiBase = () => {
  // Проверяваме дали сме на компютъра (localhost или 127.0.0.1)
  const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  
  if (isLocal) {
    return `http://127.0.0.1:${BACKEND_PORT}`;
  }
  
  // За мобилното приложение използваме IP адреса
  return `http://${BACKEND_IP}:${BACKEND_PORT}`;
};
