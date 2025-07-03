import React from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import PokerTable from "./components/PokerTable"; // NEW

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <PokerTable />
  </React.StrictMode>
);
