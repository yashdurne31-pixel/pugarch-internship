export interface Facility {
  id: number;
  name?: string;
  facility_name?: string;
  location?: string;
  city?: string;
  cleanliness_score?: number | null;
  status?: string;
  operational_status?: string;
  description?: string | null;
  [key: string]: unknown;
}

export interface Inspection {
  id: number;
  facility_id?: number;
  facility?: Facility;
  inspection_date?: string;
  date?: string;
  status?: string;
  rating?: number | string | null;
  cleanliness_score?: number | null;
  notes?: string | null;
  inspector_name?: string | null;
  [key: string]: unknown;
}

export interface Complaint {
  id: number;
  facility_id?: number;
  facility?: Facility;
  title?: string;
  description?: string;
  status?: string;
  created_at?: string;
  [key: string]: unknown;
}

export interface Paginated<T> {
  data: T[];
  current_page: number;
  last_page: number;
  total: number;
}

