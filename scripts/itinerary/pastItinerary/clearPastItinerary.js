import { clearStoredItinerary } from '../panel/renderPanel.js';

export class ClearPastItinerary {
   static async clearPastItinerary(deps = {}) {
      const { clearItinerary = clearStoredItinerary } = deps;

      await clearItinerary(deps);
   }
}
