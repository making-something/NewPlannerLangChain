export interface HealthResponse {
  status: string;
  message: string;
}

export interface ModelItem {
  id: string;
  name: string;
}

export interface ProviderInfo {
  provider: string;
  name: string;
  models: ModelItem[];
}

export interface ModelsResponse {
  providers: ProviderInfo[];
}

export interface ItineraryRequest {
  description: string;
  provider?: string;
  model?: string;
}

export interface RefinementRequest {
  session_id: string;
  feedback: string;
}

export interface FollowUpQuestion {
  question: string;
  order: number;
}

export interface ItineraryResponse {
  session_id: string;
  itinerary: string;
  follow_up_questions: FollowUpQuestion[];
  provider: string;
  model: string;
}

export interface SaveItineraryRequest {
  session_id: string;
  filename?: string;
}

export interface SaveItineraryResponse {
  success: boolean;
  filename: string;
  message: string;
}

export interface ErrorResponse {
  error: string;
  detail?: string;
}
