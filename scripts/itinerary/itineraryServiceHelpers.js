import { ItineraryApi } from '../api/itineraryApi.js';
import { DraftStorage } from './draftStorage.js';

export class ItineraryServiceHelpers {
   static async fetchSavedItineraryVisitDate() {
      const { date } = await ItineraryApi.getItineraryDateRequest();

      if (date) {
         DraftStorage.setStoredItineraryDate(date);
      }

      return date;
   }
}
