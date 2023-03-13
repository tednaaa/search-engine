import clsx from 'clsx';
import React, { FC } from 'react';
import styles from './Loader.module.scss';

interface Props {
  className?: string;
}

export const Loader: FC<Props> = ({ className }) => {
  return <div className={clsx(styles.loader, className)} />;
};
