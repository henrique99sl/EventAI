import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NotificationsAdminComponent } from './notifications-admin';
import { By } from '@angular/platform-browser';

describe('NotificationsAdminComponent', () => {
  let component: NotificationsAdminComponent;
  let fixture: ComponentFixture<NotificationsAdminComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [NotificationsAdminComponent]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NotificationsAdminComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should mark notification as read', () => {
    const notification = { id: 99, message: 'Teste', read: false, createdAt: new Date() };
    component.notifications = [notification];
    component.markAsRead(notification);
    expect(notification.read).toBeTrue();
  });

  it('should remove notification', () => {
    const n1 = { id: 1, message: 'Um', read: false, createdAt: new Date() };
    const n2 = { id: 2, message: 'Dois', read: false, createdAt: new Date() };
    component.notifications = [n1, n2];
    component.removeNotification(n1);
    expect(component.notifications.length).toBe(1);
    expect(component.notifications[0].id).toBe(2);
  });

  it('should show empty message when no notifications', () => {
    component.notifications = [];
    fixture.detectChanges();
    const emptyEl = fixture.debugElement.query(By.css('.empty'));
    expect(emptyEl).toBeTruthy();
    expect(emptyEl.nativeElement.textContent).toContain('Nenhuma notificação');
  });
});