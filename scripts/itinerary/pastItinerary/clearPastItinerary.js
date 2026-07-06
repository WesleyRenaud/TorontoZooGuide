import { clearStoredItinerary } from '../panel/renderPanel.js';

export async function clearPastItinerary(deps = {}) {
   const { clearItinerary = clearStoredItinerary } = deps;

   await clearItinerary(deps);
}
