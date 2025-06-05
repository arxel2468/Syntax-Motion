import React from 'react';
import { Toast } from './ToastContext';

interface ToastContainerProps {
  toasts: Toast[];
  onClose: (id: string) => void;
}

const ToastContainer: React.FC<ToastContainerProps> = ({ toasts, onClose }) => {
  if (toasts.length === 0) {
    return null;
  }

  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col space-y-2">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={`px-4 py-3 rounded-md shadow-md flex items-center justify-between max-w-md transition-all duration-300 ease-in-out ${getToastColorClasses(
            toast.type
          )}`}
        >
          <p className="text-white">{toast.message}</p>
          <button
            onClick={() => onClose(toast.id)}
            className="ml-4 text-white focus:outline-none"
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  );
};

const getToastColorClasses = (type: Toast['type']): string => {
  switch (type) {
    case 'success':
      return 'bg-green-500';
    case 'error':
      return 'bg-red-500';
    case 'warning':
      return 'bg-yellow-500';
    case 'info':
    default:
      return 'bg-blue-500';
  }
};

export default ToastContainer;
