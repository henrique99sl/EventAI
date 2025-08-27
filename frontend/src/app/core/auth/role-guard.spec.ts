import { roleGuard } from './role-guard';
import { ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

function mockRoute(data: any): ActivatedRouteSnapshot {
  return { data } as ActivatedRouteSnapshot;
}

describe('roleGuard', () => {
  beforeEach(() => {
    localStorage.removeItem('user_roles');
  });

  it('should allow access if user has required role', () => {
    localStorage.setItem('user_roles', JSON.stringify(['admin', 'user']));
    const route = mockRoute({ role: 'admin' });
    expect(roleGuard(route, {} as RouterStateSnapshot)).toBeTrue();
  });

  it('should block access if user does not have required role', () => {
    localStorage.setItem('user_roles', JSON.stringify(['user']));
    const route = mockRoute({ role: 'admin' });
    expect(roleGuard(route, {} as RouterStateSnapshot)).toBeFalse();
  });

  it('should block access if user_roles is not set', () => {
    const route = mockRoute({ role: 'admin' });
    expect(roleGuard(route, {} as RouterStateSnapshot)).toBeFalse();
  });

  it('should block access if requiredRole is missing', () => {
    const route = mockRoute({});
    expect(roleGuard(route, {} as RouterStateSnapshot)).toBeFalse();
  });
});