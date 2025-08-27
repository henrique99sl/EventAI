const fs = require('fs');
const path = require('path');
const axios = require('axios');

// 1. Lista de rotas do backend (coloca igual ao do teu test-backend-routes.js)
const backendRoutes = [
  '/assistant',
  '/events/cached',
  '/events/1/cancel',
  '/users/change-password',
  '/events',
  '/users',
  '/venues',
  '/events/1',
  '/users/1',
  '/venues/1',
  '/events/1/image',
  '/events/calendar',
  '/feedback',
  '/me',
  '/users/me',
  '/recommendations',
  '/metrics',
  '/health',
  '/liveness',
  '/login',
  '/events/1/participate',
  '/readiness',
  '/users/recover-password',
  '/auth/refresh',
  '/users/reset-password',
  '/',
  '/recommendations/update',
  '/events/1/upload'
  // Adiciona todas as rotas relevantes
];

// 2. Função para extrair endpoints do frontend
function findEndpointsInFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  // Regex para apanhar endpoints (adapta se usares /api/)
  const regex = /(http:\/\/localhost:5000|\/api)?(\/[a-zA-Z0-9_\/-]+)/g;
  let endpoints = [];
  let match;
  while ((match = regex.exec(content)) !== null) {
    endpoints.push(match[2]);
  }
  return endpoints;
}

function getAllFrontendEndpoints(dir) {
  let endpoints = new Set();
  function traverse(currentDir) {
    fs.readdirSync(currentDir).forEach(file => {
      const fullPath = path.join(currentDir, file);
      if (fs.statSync(fullPath).isDirectory()) {
        traverse(fullPath);
      } else if (fullPath.endsWith('.ts') || fullPath.endsWith('.js')) {
        findEndpointsInFile(fullPath).forEach(ep => endpoints.add(ep));
      }
    });
  }
  traverse(dir);
  return Array.from(endpoints);
}

// 3. Comparar rotas do backend com usadas no frontend
function compareRoutes(backendRoutes, frontendEndpoints) {
  const used = [];
  const unused = [];
  backendRoutes.forEach(route => {
    if (frontendEndpoints.some(ep => ep.startsWith(route.replace(/\/1$/, '')))) {
      used.push(route);
    } else {
      unused.push(route);
    }
  });
  return { used, unused };
}

// 4. Teste real de comunicação (opcional)
async function testEndpoints(endpoints) {
  for (const ep of endpoints) {
    try {
      const url = `http://localhost:5000${ep.replace(/\/1$/, '/1')}`;
      const res = await axios.get(url, { validateStatus: () => true });
      console.log(`GET ${url}: ${res.status}`);
    } catch (err) {
      console.log(`GET ${url}: FAILED`);
    }
  }
}

// 5. Executa tudo
function main() {
  const frontendDir = './frontend/src'; // Ajusta para o teu projeto
  console.log('A analisar endpoints usados pelo frontend...');
  const frontendEndpoints = getAllFrontendEndpoints(frontendDir);
  fs.writeFileSync('frontend_endpoints.json', JSON.stringify(frontendEndpoints, null, 2));
  console.log(`Encontrados ${frontendEndpoints.length} endpoints no frontend.`);

  const { used, unused } = compareRoutes(backendRoutes, frontendEndpoints);

  console.log('\nRotas do backend USADAS no frontend:');
  used.forEach(r => console.log('✅', r));

  console.log('\nRotas do backend NÃO usadas no frontend:');
  unused.forEach(r => console.log('❌', r));

  // Opcional: testar as rotas usadas
  // testEndpoints(used);
}

main();