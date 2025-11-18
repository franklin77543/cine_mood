import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/layout';
import { HomePage, MovieDetailPage } from './pages';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/movie/:id" element={<MovieDetailPage />} />
          {/* TODO: 加入更多路由 */}
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
