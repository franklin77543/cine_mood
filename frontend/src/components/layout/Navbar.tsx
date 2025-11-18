import { Link } from 'react-router-dom';

export function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-hero border-b border-slate-700">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <span className="text-3xl">🎬</span>
            <span className="text-2xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
              CineMood
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            <Link to="/" className="hover:text-primary transition">
              首頁
            </Link>
            <Link to="/explore" className="hover:text-primary transition">
              探索
            </Link>
            <Link to="/my-list" className="hover:text-primary transition">
              我的片單
            </Link>
          </div>

          {/* Actions */}
          <div className="flex items-center space-x-4">
            <button className="p-2 hover:bg-slate-800 rounded-lg transition">
              🔍
            </button>
            <button className="px-4 py-2 bg-primary hover:bg-indigo-600 rounded-lg transition">
              登入
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
