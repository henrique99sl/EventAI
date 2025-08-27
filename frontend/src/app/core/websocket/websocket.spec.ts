import { WebSocketService } from './websocket';

describe('WebSocketService', () => {
  let service: WebSocketService;
  let mockSocket: any;

  beforeEach(() => {
    service = new WebSocketService();
    mockSocket = {
      readyState: 1,
      send: jasmine.createSpy('send'),
      close: jasmine.createSpy('close'),
      onmessage: null
    };
    // @ts-ignore
    service['socket'] = mockSocket;
  });

  it('should send data if socket is open', () => {
    service.send('hello');
    expect(mockSocket.send).toHaveBeenCalledWith('hello');
  });

  it('should not send data if socket is not open', () => {
    mockSocket.readyState = 0; // connecting
    service.send('hello');
    expect(mockSocket.send).not.toHaveBeenCalledWith('hello');
  });

  it('should close socket', () => {
    service.close();
    expect(mockSocket.close).toHaveBeenCalled();
    // @ts-ignore
    expect(service['socket']).toBeNull();
  });

  it('should call onMessage callback', () => {
    const cb = jasmine.createSpy('callback');
    service.onMessage(cb);
    const event = { data: 'test' };
    mockSocket.onmessage(event);
    expect(cb).toHaveBeenCalledWith('test');
  });

  it('should return isConnected true if socket is open', () => {
    expect(service.isConnected()).toBeTrue();
  });

  it('should return isConnected false if socket is null', () => {
    // @ts-ignore
    service['socket'] = null;
    expect(service.isConnected()).toBeFalse();
  });
});