import { searchModel } from '@/entities/search';
import { observer } from 'mobx-react-lite';
import React from 'react';
import styles from './pagination.module.scss';

export const Pagination = observer(() => {
  return (
    <div className={styles.pagination}>
      <button
        className={styles.previousButton}
        disabled={!searchModel.pagination.previousPage}
        onClick={() => {
          searchModel.changeCurrentPage(searchModel.pagination.previousPage);
          searchModel.search();
        }}
      />
      <span>{searchModel.pagination.currentPage}</span>
      <button
        className={styles.nextButton}
        disabled={!searchModel.pagination.nextPage}
        onClick={() => {
          searchModel.changeCurrentPage(searchModel.pagination.nextPage);
          searchModel.search();
        }}
      />
    </div>
  );
});
