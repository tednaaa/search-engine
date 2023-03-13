import { routeNames } from '@/shared/router';
import { ComponentType } from 'react';
import { HomePage } from './home/home';

interface IRoute {
  path: string;
  Component: ComponentType;
}

export const publicRoutes: IRoute[] = [
  {
    path: routeNames.HOME,
    Component: HomePage,
  },
];
