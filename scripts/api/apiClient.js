function buildJsonRequestOptions(data = {}) {
   return {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json',
         'Accept': 'application/json',
      },
      body: JSON.stringify(data),
   };
}

function parseJsonText(text = '') {
   const trimmedText = text.trim();

   if (!trimmedText) {
      return {};
   }

   return JSON.parse(trimmedText);
}

function buildHttpError(response, payload, url) {
   const message = typeof payload?.error === 'string' && payload.error.trim()
      ? payload.error.trim()
      : `Request failed: ${response.status} ${response.statusText}`.trim();

   const error = new Error(`${message} (${url})`);
   error.name = 'ApiClientError';
   error.status = response.status;
   error.statusText = response.statusText;
   error.url = url;
   error.payload = payload;

   return error;
}

async function readJsonResponse(response, url) {
   const text = await response.text();

   try {
      return parseJsonText(text);
   } catch {
      throw new Error(`Invalid JSON response from ${url}`);
   }
}

export class ApiClient {
   static async postJson(url, data = {}) {
      const response = await fetch(url, buildJsonRequestOptions(data));
      const payload = await readJsonResponse(response, url);

      if (!response.ok) {
         throw buildHttpError(response, payload, url);
      }

      return payload;
   }
}
