import React from 'react';
import PersonList from '../components/PersonList';
import CameraSelector from '../components/CameraSelector';

const Manage = () => {
  return (
    <div className="p-4 flex">
      <div className="w-1/2 p-4">
        <h2 className="text-xl font-bold mb-4">Manage Persons</h2>
        <PersonList />
      </div>
      <div className="w-1/2 p-4">
        <h2 className="text-xl font-bold mb-4">Manage Cameras</h2>
        <CameraSelector />
      </div>
    </div>
  );
};

export default Manage;
