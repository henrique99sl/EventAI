import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Venue {
  id?: number;
  name: string;
  location?: string;
  // Adiciona outros campos conforme necessário
}

@Injectable({
  providedIn: 'root'
})
export class VenueService {
  private apiUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  // Obter todas as venues
  getVenues(): Observable<Venue[]> {
    return this.http.get<Venue[]>(`${this.apiUrl}/venues`);
  }

  // Obter uma venue por ID
  getVenue(id: number): Observable<Venue> {
    return this.http.get<Venue>(`${this.apiUrl}/venues/${id}`);
  }

  // Criar nova venue
  createVenue(venue: Venue): Observable<Venue> {
    return this.http.post<Venue>(`${this.apiUrl}/venues`, venue);
  }

  // Editar venue existente (PUT ou PATCH)
  updateVenue(id: number, venue: Venue): Observable<Venue> {
    return this.http.put<Venue>(`${this.apiUrl}/venues/${id}`, venue);
    // Se preferires PATCH: return this.http.patch<Venue>(`${this.apiUrl}/venues/${id}`, venue);
  }

  // Apagar venue
  deleteVenue(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/venues/${id}`);
  }
}