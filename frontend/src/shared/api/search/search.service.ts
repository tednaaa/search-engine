import { apiInstance } from '../api';

interface SearchResponse {
  id: number;
  doc_id: number;
  text: string;
  title: string;
  views_count: number;
}

export class SearchService {
  public static search(query: string, page: number, pageSize: number) {
    return apiInstance.get('/search', {
      params: { query, page, page_size: pageSize },
    });
  }

  public static fetchSuggestions(query: string) {
    return apiInstance.get('/search/suggestions', { params: { query } });
  }
}
