import Button from "@components/Button";
import { ChevronIcon } from "@components/Icons";
import { motion } from "framer-motion";
import { useState } from "react";

const menus = [
    {
        name:"Test"
    }
]

export const Navbar = () => {
  const [selectItem, setSelectedItem] = useState<number | null>(null);
  return (
    <nav>
      <div
        className="relative p-3 hover:cursor-pointer flex items-center text-white gap-6"
        style={{ background: `rgba(255,255,255,0.1 )` }}
      >
        Test <ChevronIcon />
        <motion.div className="absolute top-full right-0 rounded-lg bg-glass w-full p-3">
          <Button mode="secondary">Logout</Button>
        </motion.div>
      </div>
    </nav>
  );
};
