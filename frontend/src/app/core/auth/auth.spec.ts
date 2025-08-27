import { AuthService } from './auth';

describe('AuthService', () => {
  let service: AuthService;

  beforeEach(() => {
    service = new AuthService();
    localStorage.clear();
  });

  it('should set, get and remove token', () => {
    service.setToken('abc123');
    expect(service.getToken()).toBe('abc123');
    service.removeToken();
    expect(service.getToken()).toBeNull();
  });

  it('should authenticate when token is set', () => {
    service.setToken('token');
    expect(service.isAuthenticated()).toBeTrue();
  });

  it('should not authenticate when token is missing', () => {
    service.removeToken();
    expect(service.isAuthenticated()).toBeFalse();
  });
});