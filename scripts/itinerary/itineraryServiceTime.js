import { ItineraryApi } from '../api/itineraryApi.js';
import { ItineraryServiceTimeRunner } from './itineraryServiceTimeRunner.js';

export class ItineraryServiceTime {
   static async setItineraryArrivalTime(arrivalTime) {
      return ItineraryServiceTimeRunner.setItineraryTimeAndDispatch(
         ItineraryApi.setItineraryArrivalTimeRequest,
         arrivalTime
      );
   }

   static async setItineraryDepartureTime(departureTime) {
      return ItineraryServiceTimeRunner.setItineraryTimeAndDispatch(
         ItineraryApi.setItineraryDepartureTimeRequest,
         departureTime
      );
   }
}
