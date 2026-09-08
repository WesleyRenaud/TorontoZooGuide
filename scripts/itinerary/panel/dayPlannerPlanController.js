import { DayPlannerPlanActionsHelper } from './dayPlannerPlanActionsHelper.js';
export class DayPlannerPlanController {
   static hasScheduledItineraryItems(itinerary = {}) {
      return DayPlannerPlanActionsHelper.collectionHasScheduledItems(itinerary.animals)
         || DayPlannerPlanActionsHelper.collectionHasScheduledItems(itinerary.attractions)
         || DayPlannerPlanActionsHelper.collectionHasScheduledItems(itinerary.guardiansTalks)
         || DayPlannerPlanActionsHelper.collectionHasScheduledItems(itinerary.wildEncounters)
         || DayPlannerPlanActionsHelper.collectionHasScheduledItems(itinerary.transportations)
         || DayPlannerPlanActionsHelper.collectionHasScheduledItems(itinerary.events);
   }
}
