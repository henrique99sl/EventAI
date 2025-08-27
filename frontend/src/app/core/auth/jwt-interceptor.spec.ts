import { JwtInterceptor } from './jwt-interceptor';
import { AuthService } from './auth';
import { HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable, of } from 'rxjs';

describe('JwtInterceptor', () => {
  let interceptor: JwtInterceptor;
  let authService: AuthService;
  let next: jasmine.SpyObj<HttpHandler>;

  beforeEach(() => {
    authService = new AuthService();
    interceptor = new JwtInterceptor(authService);
    next = jasmine.createSpyObj('HttpHandler', ['handle']);
    next.handle.and.returnValue(of({} as HttpEvent<any>));
  });

  it('should add Authorization header if token exists', () => {
    spyOn(authService, 'getToken').and.returnValue('test-token');
    const req = new HttpRequest('GET', '/api/test');
    interceptor.intercept(req, next).subscribe();
    expect(next.handle).toHaveBeenCalled();
    const clonedReq = next.handle.calls.mostRecent().args[0];
    expect(clonedReq.headers.get('Authorization')).toBe('Bearer test-token');
  });

  it('should not add Authorization header if token does not exist', () => {
    spyOn(authService, 'getToken').and.returnValue(null);
    const req = new HttpRequest('GET', '/api/test');
    interceptor.intercept(req, next).subscribe();
    expect(next.handle).toHaveBeenCalled();
    const handledReq = next.handle.calls.mostRecent().args[0];
    expect(handledReq.headers.get('Authorization')).toBeNull();
  });
});