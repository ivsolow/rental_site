
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



//
// import React from 'react';
// import './App.css';
// import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
// import EquipmentList from './EquipmentList';
// import EquipmentDetail from './EquipmentDetail';

// function App() {
//   return (
// <Router>
//   <Route exact path="/" component={EquipmentList} />
//   <Route path="/equipment/:id" component={EquipmentDetail} />
// </Router>

//   );
// }

// export default App;



//
// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;


