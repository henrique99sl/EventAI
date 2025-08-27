import { CanActivateFn, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

export const roleGuard: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
) => {
  const requiredRole = route.data?.['role'];
  if (!requiredRole) return false;
  let userRoles: string[] = [];
  try {
    userRoles = JSON.parse(localStorage.getItem('user_roles') || '[]');
    if (!Array.isArray(userRoles)) userRoles = [];
  } catch {
    userRoles = [];
  }
  return userRoles.includes(requiredRole);
};