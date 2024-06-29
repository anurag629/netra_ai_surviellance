import React from 'react';
import CameraFeed from '../components/CameraFeed';
import LocationMap from '../components/LocationMap';

const HomePage = () => {
  return (
    <div className="p-4">
      <div className="grid grid-cols-1 gap-4">
        <div>
          <CameraFeed />
        </div>
        <div>
          <LocationMap />
        </div>
      </div>
    </div>
  );
};

export default HomePage;
