import { SearchService } from '@/shared/api';
import { makeAutoObservable, runInAction } from 'mobx';

class SearchSuggestionsModel {
  public suggestions = [];

  public constructor() {
    makeAutoObservable(this);
  }

  public async fetchSuggestions(query: string) {
    const { data } = await SearchService.fetchSuggestions(query);

    runInAction(() => {
      this.suggestions = data;
    });
  }
}

export const searchSuggestionsModel = new SearchSuggestionsModel();
