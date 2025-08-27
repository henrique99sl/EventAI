export const AppConfig = {
  appName: 'EventAI',
  theme: 'light',
  apiUrl: '/api',
  supportedLanguages: ['en', 'pt'],
  defaultLanguage: 'en',
  logoPath: 'assets/images/logo.png'
  // Adiciona outras configs globais aqui
};

export const environment = {
  production: false,
  apiBaseUrl: 'https://api.seuevento.com', // Atualizar para endpoint real
  websocketUrl: 'wss://ws.seuevento.com',  // Atualizar para endpoint real
  appName: 'SeuEvento',
  version: '1.0.0'
};