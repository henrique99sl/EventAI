import { TestBed } from '@angular/core/testing';
import { ApiService } from './api';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

describe('ApiService', () => {
  let service: ApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ApiService]
    });

    service = TestBed.inject(ApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should GET data', () => {
    service.get('/test/url').subscribe(res => {
      expect(res).toEqual({ foo: 'bar' });
    });

    const req = httpMock.expectOne('/test/url');
    expect(req.request.method).toBe('GET');
    req.flush({ foo: 'bar' });
  });

  it('should POST data', () => {
    service.post('/test/url', { baz: 'qux' }).subscribe(res => {
      expect(res).toEqual({ ok: true });
    });

    const req = httpMock.expectOne('/test/url');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ baz: 'qux' });
    req.flush({ ok: true });
  });

  it('should PUT data', () => {
    service.put('/test/url', { baz: 'qux' }).subscribe(res => {
      expect(res).toEqual({ updated: true });
    });

    const req = httpMock.expectOne('/test/url');
    expect(req.request.method).toBe('PUT');
    expect(req.request.body).toEqual({ baz: 'qux' });
    req.flush({ updated: true });
  });

  it('should DELETE data', () => {
    service.delete('/test/url').subscribe(res => {
      expect(res).toEqual({ deleted: true });
    });

    const req = httpMock.expectOne('/test/url');
    expect(req.request.method).toBe('DELETE');
    req.flush({ deleted: true });
  });
});