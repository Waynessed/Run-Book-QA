import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({plugins:[react()], server:{proxy:{'/v1':'http://api:8081','/readyz':'http://api:8081'}}});
