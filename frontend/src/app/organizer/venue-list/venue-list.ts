import { Component, OnInit } from '@angular/core';
import { VenueService, Venue } from '../../core/api/venue.service';

@Component({
  selector: 'app-venue-list',
  templateUrl: './venue-list.html',
  styleUrls: ['./venue-list.scss']
})
export class VenueListComponent implements OnInit {
  venues: Venue[] = [];
  loading = false;
  error: string = '';

  constructor(private venueService: VenueService) {}

  ngOnInit() {
    this.loadVenues();
  }

  loadVenues() {
    this.loading = true;
    this.venueService.getVenues().subscribe(
      (data) => {
        this.venues = data;
        this.loading = false;
      },
      (error) => {
        this.error = 'Erro ao carregar venues';
        this.loading = false;
      }
    );
  }

  deleteVenue(id: number) {
    if (!confirm('Tens a certeza que queres apagar esta venue?')) return;
    this.venueService.deleteVenue(id).subscribe(
      () => {
        this.venues = this.venues.filter(v => v.id !== id);
      },
      (error) => {
        this.error = 'Erro ao apagar venue';
      }
    );
  }
}