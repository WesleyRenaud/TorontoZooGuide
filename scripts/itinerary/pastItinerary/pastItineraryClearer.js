import { RenderView } from '../panel/renderView.js';

export class PastItineraryClearer {
   static async clearPastItinerary(deps = {}) {
      const { clearItinerary = RenderView.clearStoredItinerary } = deps;

      await clearItinerary(deps);
   }
}
