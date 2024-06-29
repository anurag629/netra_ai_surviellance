import React, { useState, useEffect } from 'react';
import { getPersons, addPerson, uploadPersonImage, deletePerson } from '../services/personService';

const PersonList = ({ onSelectPerson }) => {
  const [persons, setPersons] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [newPerson, setNewPerson] = useState({ name: '', age: '', city: '', country: '', dob: '' });
  const [selectedFile, setSelectedFile] = useState(null);
  

  useEffect(() => {
    const fetchPersons = async () => {
      const data = await getPersons();
      setPersons(data);
    };
    fetchPersons();
  }, []);

  const handleAddPerson = async () => {
    const addedPerson = await addPerson(newPerson);
    setPersons([...persons, addedPerson]);
    setNewPerson({ name: '', age: '', city: '', country: '', dob: '' });

    if (selectedFile) {
      await uploadPersonImage(addedPerson.id, selectedFile);
      setSelectedFile(null);
    }
    setShowModal(false);
  };

  const handleDeletePerson = async (id) => {
    const isConfirmed = window.confirm('Are you sure you want to delete this person?');
    if (isConfirmed) {
      await deletePerson(id);
      setPersons(persons.filter(person => person.id !== id));
    }
  }


  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4">Person List</h2>
      <div className="flex mb-4 items-center">
      <button onClick={() => setShowModal(true)} className="bg-blue-500 text-white p-2 rounded-md">Add Person</button>
      {showModal && (
        <div className="fixed top-0 left-0 w-full h-full bg-gray-900 bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-4 rounded-lg shadow-md w-1/2">
            <h2 className="bg-red-500 text-xl font-bold mb-4 text-center">Add Person</h2>
            <input type="text" placeholder="Name" value={newPerson.name} onChange={(e) => setNewPerson({ ...newPerson, name: e.target.value })} className="border p-2 m-2" />
            <input type="text" placeholder="Age" value={newPerson.age} onChange={(e) => setNewPerson({ ...newPerson, age: e.target.value })} className="border p-2 m-2" />
            <input type="text" placeholder="City" value={newPerson.city} onChange={(e) => setNewPerson({ ...newPerson, city: e.target.value })} className="border p-2 m-2" />
            <input type="text" placeholder="Country" value={newPerson.country} onChange={(e) => setNewPerson({ ...newPerson, country: e.target.value })} className="border p-2 m-2" />
            <input type="date" placeholder="DOB" value={newPerson.dob} onChange={(e) => setNewPerson({ ...newPerson, dob: e.target.value })} className="border p-2 m-2" />
            <input type="file" onChange={(e) => setSelectedFile(e.target.files[0])} className="border p-2 m-2" />
            <button onClick={handleAddPerson} className="bg-blue-500 text-white p-2 rounded-md">Add</button>
            <button onClick={() => setShowModal(false)} className="bg-red-500 text-white p-2 rounded-md ml-2">Cancel</button>
          </div>
        </div>
      )}

      </div>
      <div className="grid grid-cols-3 gap-4">
        {persons.map(person => (
          <div key={person.id} className="bg-gray-100 p-4 rounded-lg shadow-md flex flex-col items-center justify-center">
            <img src={person.image} alt={person.name} className="w-24 h-24 rounded-full" />
            <div className="text-lg font-bold mt-2">{person.name}</div>
            <div className="text-sm text-gray-500">{person.city}, {person.country}</div>
            <div className="mt-4">
              <button onClick={() => handleDeletePerson(person.id)} className="bg-red-500 text-white p-2 rounded-md ml-2">Delete</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default PersonList;
