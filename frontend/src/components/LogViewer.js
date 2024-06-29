import React, { useEffect, useState } from 'react';
import api from '../services/api';

const LogViewer = () => {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const fetchLogs = async () => {
      const response = await api.get('/logs');
      setLogs(response.data);
    };
    fetchLogs();
  }, []);

  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4">Log Viewer</h2>
      <div>
        {logs.map((log) => (
          <div key={log.id} className="p-2 border-b border-gray-200">
            {log.message} - {new Date(log.timestamp).toLocaleString()}
          </div>
        ))}
      </div>
    </div>
  );
};

export default LogViewer;
