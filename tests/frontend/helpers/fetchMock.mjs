export function mockJsonResponse(payload) {
   return {
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify(payload),
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
