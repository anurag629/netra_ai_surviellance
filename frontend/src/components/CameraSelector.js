import React, { useState, useEffect } from 'react';
import { getCameras, addCamera, deleteCamera } from '../services/cameraService'; // Assume deleteCamera is added to cameraService



const CameraSelector = ({ onSelectCamera }) => {
  const [cameras, setCameras] = useState([]);
  const [newCamera, setNewCamera] = useState({ name: '', url: '' });
  const [showModal, setShowModal] = useState(false);


  useEffect(() => {
    const fetchCameras = async () => {
      const data = await getCameras();
      setCameras(data);
    };
    fetchCameras();
  }, []);

  const handleAddCamera = async () => {
    const addedCamera = await addCamera(newCamera);
    setCameras([...cameras, addedCamera]);
    setNewCamera({ name: '', url: '' });
    setShowModal(false);
  };

  const handleDeleteCamera = async (id) => {
    const isConfirmed = window.confirm('Are you sure you want to delete this camera?');
    if (isConfirmed) {
      await deleteCamera(id); // This function needs to be implemented in your cameraService
      setCameras(cameras.filter(camera => camera.id !== id));
    }
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4">Camera Selector</h2>
      <div className="flex mb-4 items-center">
        <button onClick={() => setShowModal(true)} className="bg-blue-500 text-white p-2 rounded-md">Add Camera</button>
        {showModal && (
          <div className="fixed top-0 left-0 w-full h-full bg-gray-900 bg-opacity-50 flex items-center justify-center">
            <div className="bg-white p-4 rounded-lg shadow-md w-1/2">
              <h2 className="bg-red-500 text-xl font-bold mb-4 text-center">Add Camera</h2>
              <input
                type="text"
                placeholder="Name"
                value={newCamera.name}
                onChange={(e) => setNewCamera({ ...newCamera, name: e.target.value })}
                className="border p-2 m-2"
              />
              <input
                type="text"
                placeholder="URL"
                value={newCamera.url}
                onChange={(e) => setNewCamera({ ...newCamera, url: e.target.value })}
                className="border p-2 m-2"
              />
              <button onClick={handleAddCamera} className="bg-blue-500 text-white p-2 rounded-md">Add</button>
              <button onClick={() => setShowModal(false)} className="bg-red-500 text-white p-2 rounded-md ml-2">Cancel</button>
            </div>
          </div>
        )}
      </div>
      <div>
        {cameras.map(camera => (
          <div key={camera.id} className="p-2 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <div>{camera.name}</div>
              <button onClick={(e) => { e.stopPropagation(); handleDeleteCamera(camera.id); }} className="text-red-500">Delete</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CameraSelector;
