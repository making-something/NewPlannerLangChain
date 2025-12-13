import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { 
  ItineraryRequest, 
  ItineraryResponse, 
  ModelsResponse, 
  RefinementRequest, 
  SaveItineraryRequest, 
  SaveItineraryResponse 
} from '../models/planner.models';

@Injectable({
  providedIn: 'root'
})
export class PlannerService {
  private apiUrl = 'http://localhost:8000/api/v1/planner';

  constructor(private http: HttpClient) { }

  getModels(): Observable<ModelsResponse> {
    return this.http.get<ModelsResponse>(`${this.apiUrl}/models`);
  }

  generateItinerary(request: ItineraryRequest): Observable<ItineraryResponse> {
    return this.http.post<ItineraryResponse>(`${this.apiUrl}/generate`, request);
  }

  refineItinerary(request: RefinementRequest): Observable<ItineraryResponse> {
    return this.http.post<ItineraryResponse>(`${this.apiUrl}/refine`, request);
  }

  saveItinerary(request: SaveItineraryRequest): Observable<SaveItineraryResponse> {
    return this.http.post<SaveItineraryResponse>(`${this.apiUrl}/save`, request);
  }

  getSession(sessionId: string): Observable<ItineraryResponse> {
    return this.http.get<ItineraryResponse>(`${this.apiUrl}/sessions/${sessionId}`);
  }

  deleteSession(sessionId: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/sessions/${sessionId}`);
  }
}
