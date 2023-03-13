import React, {
  ChangeEvent,
  FormEvent,
  MouseEvent as ReactMouseEvent,
  useEffect,
  useRef,
  useState,
} from 'react';
import { Button, Container, Input, Loader } from '@/shared/ui';

import styles from './home.module.scss';
import { observer } from 'mobx-react-lite';
import { searchModel, searchSuggestionsModel } from '@/entities/search';
import { Pagination } from './pagination';

export const HomePage = observer(() => {
  const [showDropdown, setShowDropdown] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (!ref.current.contains(event.target)) {
        setShowDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);

    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [ref]);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (searchModel.query) searchModel.search();
  };

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { value } = event.currentTarget;

    searchModel.handleQueryChange(value);

    if (value.trim()) {
      searchSuggestionsModel.fetchSuggestions(value);
      setShowDropdown(true);
    }
  };

  const handleSuggestionClick = (event: ReactMouseEvent<HTMLButtonElement>) => {
    const { textContent } = event.currentTarget;

    searchModel.handleQueryChange(textContent);

    if (textContent.trim()) {
      searchModel.search();
      setShowDropdown(false);
    }
  };

  return (
    <div className={styles.wrapper}>
      <Container>
        <h1 className={styles.title}>
          🍓 Search engine based on React.js and Django.py 🕵️
        </h1>
        <form onSubmit={handleSubmit} className={styles.form}>
          <div ref={ref} className={styles.inputWrapper}>
            <Input
              onFocus={() => setShowDropdown(true)}
              className={styles.input}
              value={searchModel.query}
              onChange={handleChange}
              placeholder="search ..."
              type="text"
            />
            {showDropdown && (
              <ul className={styles.dropdown}>
                {searchSuggestionsModel.suggestions.map((suggestion) => {
                  return (
                    <li className={styles.dropdownItem} key={suggestion}>
                      <button onClick={handleSuggestionClick}>
                        {suggestion}
                      </button>
                    </li>
                  );
                })}
              </ul>
            )}
          </div>

          <Button className={styles.searchButton} type="submit" />
        </form>

        {searchModel.data?.length &&
          !searchModel.loading &&
          searchModel.query && <Pagination />}
        {searchModel.loading ? (
          <Loader className={styles.loader} />
        ) : (
          <ul className={styles.list}>
            {searchModel.data?.map(({ doc_id, title, text, views_count }) => {
              return (
                <li className={styles.listItem} key={doc_id}>
                  <h3 className={styles.postTitle}>
                    <a
                      target="_blank"
                      href={`https://bitcoin.stackexchange.com/questions/${doc_id}`}
                    >
                      {title}
                    </a>
                  </h3>
                  <div
                    className={styles.postText}
                    dangerouslySetInnerHTML={{ __html: text }}
                  />
                  <div className={styles.postViews}>{views_count} views</div>
                </li>
              );
            })}
          </ul>
        )}
      </Container>
    </div>
  );
});
