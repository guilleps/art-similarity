import { BrowserRouter, Routes, Route } from 'react-router-dom'
import IndexPage from '@/pages/Index'
import AnalysisPage from '@/pages/Analysis'
import NotFoundPage from '@/pages/NotFound'

const AppRouter = () => {
  return (
    <BrowserRouter future={{
      v7_startTransition: true,
      v7_relativeSplatPath: true
    }} >
      <Routes>
        <Route path="/" element={<IndexPage />} />
        <Route path="/analysis" element={<AnalysisPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default AppRouter
