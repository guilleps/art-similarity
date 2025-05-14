// API
export { uploadImage } from './api/upload'
export type { UploadResponse, Similarity } from './schemas/upload.schema'

// Hooks
export { useUploadHandler } from './hooks/useUploadHandler' 

// Components
export { default as UploadArea } from './components/UploadArea'
export { default as ScanningAnimation } from './components/ScanningAnimation'
export { default as ResultsCard } from './components/ResultsCard'