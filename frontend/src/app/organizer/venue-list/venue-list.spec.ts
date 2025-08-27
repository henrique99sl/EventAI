import { ComponentFixture, TestBed } from '@angular/core/testing';
import { VenueListComponent } from './venue-list';
import { VenueService } from '../../core/api/venue.service';
import { of } from 'rxjs';

describe('VenueListComponent', () => {
  let component: VenueListComponent;
  let fixture: ComponentFixture<VenueListComponent>;
  let mockVenueService: jasmine.SpyObj<VenueService>;

  beforeEach(async () => {
    mockVenueService = jasmine.createSpyObj('VenueService', ['getVenues', 'deleteVenue']);
    await TestBed.configureTestingModule({
      declarations: [VenueListComponent],
      providers: [{ provide: VenueService, useValue: mockVenueService }]
    }).compileComponents();

    fixture = TestBed.createComponent(VenueListComponent);
    component = fixture.componentInstance;
  });

  it('carrega venues ao iniciar', () => {
    mockVenueService.getVenues.and.returnValue(of([{ id: 1, name: 'Auditório' }]));
    component.ngOnInit();
    expect(component.venues.length).toBe(1);
    expect(component.venues[0].name).toBe('Auditório');
  });

  it('apaga venue corretamente', () => {
    component.venues = [{ id: 1, name: 'A' }, { id: 2, name: 'B' }];
    spyOn(window, 'confirm').and.returnValue(true);
    mockVenueService.deleteVenue.and.returnValue(of({}));
    component.deleteVenue(1);
    expect(component.venues.length).toBe(1);
    expect(component.venues[0].name).toBe('B');
  });
});