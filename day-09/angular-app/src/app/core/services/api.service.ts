import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import {
  Facility,
  Inspection,
  Complaint,
  Paginated
} from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = '/api';

  facilities(): Observable<Paginated<Facility>> {
    return this.http.get<Paginated<Facility>>(
      `${this.baseUrl}/facilities`
    );
  }

  facility(id: number | string): Observable<Facility> {
    return this.http.get<Facility>(
      `${this.baseUrl}/facilities/${id}`
    );
  }

  createFacility(
    facility: Partial<Facility>
  ): Observable<Facility> {
    return this.http.post<Facility>(
      `${this.baseUrl}/facilities`,
      facility
    );
  }

  updateFacility(
    id: number | string,
    facility: Partial<Facility>
  ): Observable<Facility> {
    return this.http.put<Facility>(
      `${this.baseUrl}/facilities/${id}`,
      facility
    );
  }

  deleteFacility(id: number | string): Observable<void> {
    return this.http.delete<void>(
      `${this.baseUrl}/facilities/${id}`
    );
  }

  inspections(
    facilityId?: number | string
  ): Observable<Paginated<Inspection> | Inspection[]> {
    const url = facilityId
      ? `${this.baseUrl}/facilities/${facilityId}/inspections`
      : `${this.baseUrl}/inspections`;

    return this.http.get<Paginated<Inspection> | Inspection[]>(url);
  }

  inspection(id: number | string): Observable<Inspection> {
    return this.http.get<Inspection>(
      `${this.baseUrl}/inspections/${id}`
    );
  }

  createInspection(
    inspection: Partial<Inspection>
  ): Observable<Inspection> {
    return this.http.post<Inspection>(
      `${this.baseUrl}/inspections`,
      inspection
    );
  }

  complaints(): Observable<Paginated<Complaint> | Complaint[]> {
    return this.http.get<Paginated<Complaint> | Complaint[]>(
      `${this.baseUrl}/complaints`
    );
  }
}
