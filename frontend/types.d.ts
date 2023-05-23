import { isParenthesizedTypeNode } from 'typescript';
import type { RouteLocationRaw, RouteLocationNamedRaw } from 'vue-router';
import { paths } from './openapi';

export type HttpMethod = 'get' | 'post' | 'patch' | 'delete';
export type ContentType = 'application/json' | 'application/x-www-form-urlencoded';
export type SuccessfulResponseCode = 200 | 201 | 204;

export type APIPath = keyof paths;

export type APIMethod<P extends APIPath> = keyof paths[P];

export type APIResponseBody<
    P extends APIPath,
    M extends APIMethod,
> = paths[P][M]['responses'][200]['content']['application/json'];

export type APIRequestBody<
    P extends APIPath,
    M extends APIMethod,
    CT extends ContentType,
> = paths[P][M]['requestBody']['content'][CT];

export interface LoaderArgs {
    limit?: number;
    offset?: number;
}

interface SidebarLinkItem {
    title: string;
    link: RouteLocationRaw;
    separator?: never;
    action?: never;
}

interface SidebarActionItem {
    title: string;
    action: () => void;
    link?: never;
    separator?: never;
}

interface SidebarSeparatorItem {
    separator: boolean;
    title?: never;
    link?: never;
    action?: never;
}

export type SidebarItem = SidebarLinkItem | SidebarActionItem | SidebarSeparatorItem;

export interface FieldProps {
    fieldName: string;
    value: unknown;
}
