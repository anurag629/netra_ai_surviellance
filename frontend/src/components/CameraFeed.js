import React, { useEffect, useState } from 'react';
import { getCameras } from '../services/cameraService';

const CameraFeed = () => {
  const [cameras, setCameras] = useState([]);

  useEffect(() => {
    const fetchCameras = async () => {
      const data = await getCameras();
      setCameras(data);
    };
    fetchCameras();
  }, []);

  return (
    <div className="grid grid-cols-2 gap-4">
      {cameras.map((camera) => (
        <div key={camera.id} className="bg-white p-4 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">{camera.name}</h2>
          <img 
            src={`http://localhost:8000/cameras/${camera.id}/stream_objects`} 
            alt={`Camera ${camera.id}`} 
            className="w-full h-64 object-cover"
          />
        </div>
      ))}
    </div>
  );
};

export default CameraFeed;
