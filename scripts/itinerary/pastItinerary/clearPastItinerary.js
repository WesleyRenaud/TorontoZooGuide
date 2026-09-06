import { RenderPanel } from '../panel/renderPanel.js';

export class ClearPastItinerary {
   static async clearPastItinerary(deps = {}) {
      const { clearItinerary = RenderPanel.clearStoredItinerary } = deps;

      await clearItinerary(deps);
   }
}
