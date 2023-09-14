
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import EquipmentList from './EquipmentList';
import EquipmentDetail from './EquipmentDetail';
import Cart from './CartList';
import Login from './Login';
import Logout from './LogOut';
import EquipmentByDates from './EquipmentByDates';
import Home from './NavLink';

function App() {
  return (
    <Router>
      <Routes>
      <Route path="/" element={<Home />} />
        <Route path="/equipment" element={<EquipmentList />} />
        <Route path="/equipment/:id" element={<EquipmentDetail />} />
        <Route path="/cart" element={<Cart />} /> 
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/equipment-dates" element={<EquipmentByDates />} />
      </Routes>
    </Router>
  );
}

export default App;

