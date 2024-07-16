import Link from 'next/link';
import Menu from '../../data-types/menu';

interface MenuBarProps {
  menu: Menu[];
}

const MenuBar: React.FC<MenuBarProps> = ({ menu }) => {
  return (
    <div className="w-full h-24 flex justify-center items-center">
      <div className="w-full max-w-[1420px] flex justify-between">
        <div>logo</div>
        <div className="flex gap-2">
          {menu.map(m => (
            <Link href={m.href} key={m.name}>
              {m.name}
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MenuBar;
