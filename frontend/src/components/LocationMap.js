import React, { useEffect, useState } from 'react';
import { getLocations } from '../services/locationService';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const LocationMap = () => {
  const [locations, setLocations] = useState([]);

  useEffect(() => {
    const fetchLocations = async () => {
      const data = await getLocations();
      setLocations(data);
    };
    fetchLocations();
  }, []);

  return (
    <MapContainer center={[20, 77]} zoom={5} style={{ height: "600px", width: "100%" }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {locations.map(location => (
        <CircleMarker
          key={location.id}
          center={[location.latitude, location.longitude]}
          color="red"
          radius={10}
        >
          <Popup>
            <div>
              <p><strong>Culprit Details:</strong></p>
              <p><strong>Address:</strong> {location.address}</p>
              <p><strong>Timestamp:</strong> {new Date(location.timestamp).toLocaleString()}</p>
              <img src={location.screenshot} alt="Screenshot" style={{ width: '100%' }} />
            </div>
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
};

export default LocationMap;
