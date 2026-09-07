import { ApiClientHttp } from './apiClientHttp.js';

export class ApiClient {
   static async postJson(url, data = {}) {
      const response = await fetch(url, ApiClientHttp.buildJsonRequestOptions(data));
      const payload = await ApiClientHttp.readJsonResponse(response, url);

      if (!response.ok) {
         throw ApiClientHttp.buildHttpError(response, payload, url);
      }

      return payload;
   }
}
