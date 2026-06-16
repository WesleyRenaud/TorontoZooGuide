export function mockJsonResponse(
   payload,
   { ok = true, status = 200, statusText = 'OK' } = {}
) {
   return {
      ok,
      status,
      statusText,
      text: async () => JSON.stringify(payload),
   };
}

export function mockFetchJsonResponse(body) {
   return {
      async json() {
         return body;
      },
   };
}

export function createFetchMock(routes = {}) {
   return async (url, options = {}) => {
      const handler = routes[url];

      if (typeof handler === 'function') {
         return mockJsonResponse(await handler(url, options));
      }

      if (handler !== undefined) {
         return mockJsonResponse(handler);
      }

      throw new Error(`Unexpected fetch url: ${url}`);
   };
}

export function mockRegionSelectorFetch({
   regions = [{ name: 'Africa', exhibits: ['Africa Savanna'] }],
   animals = [],
} = {}) {
   globalThis.fetch = createFetchMock({
      '/get-exhibits-by-region': { regions },
      '/get-animals-by-exhibit': { animals },
   });

   return globalThis.fetch;
}
