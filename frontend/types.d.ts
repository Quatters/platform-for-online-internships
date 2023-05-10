import { isParenthesizedTypeNode } from 'typescript';
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
