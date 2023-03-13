import { SearchService } from '@/shared/api';
import { makeAutoObservable, runInAction, toJS } from 'mobx';
import { ChangeEvent } from 'react';

interface IData {
  id: number;
  doc_id: number;
  text: string;
  title: string;
  views_count: number;
}

type PropType<TObj, TProp extends keyof TObj> = TObj[TProp];

class SearchModel {
  public query = '';
  public loading = false;

  public pagination = {
    pageSize: 50,
    currentPage: 1,
    count: null,
    previousPage: null,
    nextPage: null,
  };

  public data: IData[];

  public constructor() {
    makeAutoObservable(this);
  }

  public async search() {
    this.loading = true;
    const { data } = await SearchService.search(
      this.query,
      this.pagination.currentPage,
      this.pagination.pageSize
    );

    runInAction(() => {
      this.pagination = {
        ...this.pagination,
        count: data.count,
        previousPage: data.previous_page,
        nextPage: data.next_page,
      };

      this.data = data.results;
      this.loading = false;
    });
  }

  public handleQueryChange = (newValue: string) => {
    this.query = newValue;

    this.changeCurrentPage(1);
  };

  public get pagesCount() {
    return Math.ceil(this.pagination.count / this.pagination.pageSize);
  }

  public changeCurrentPage = (newPage: number) => {
    this.pagination.currentPage = newPage;
  };
}

export const searchModel = new SearchModel();
