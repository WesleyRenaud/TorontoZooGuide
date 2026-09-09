import { ScheduleItemWithoutAnimalFragment } from './scheduleItemWithoutAnimalFragment.js';
import { ItineraryErrorType } from '../../shared/enums/itineraryErrorType.js';
import { Strings } from '../../strings.js';

export class AttractionWithoutAnimalFragment {
   static ATTRACTION_WITHOUT_ANIMAL_CONFIG = Object.freeze({
      issueType: ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
      nameKey: 'attractionName',
      timeKey: 'attractionTime',
      getTitle: () => Strings.itinerary.confirmation.attractionWithoutAnimalTitle,
      getMessage: (name, time) => {
         const strings = Strings.itinerary.confirmation;

         return `${strings.attractionWithoutAnimalBody(name, time)}${strings.attractionWithoutAnimalConfirmPrompt}`;
      },
      getMessageWithoutTime: (name) => {
         const strings = Strings.itinerary.confirmation;

         return `${strings.attractionWithoutAnimalBodyWithoutTime(name)}${strings.attractionWithoutAnimalConfirmPrompt}`;
      },
      getBodyMessage: (name, time, strings) => strings.attractionWithoutAnimalBody(name, time),
      getBodyMessageWithoutTime: (name, strings) => strings.attractionWithoutAnimalBodyWithoutTime(name),
      getConfirmPrompt: (strings) => strings.attractionWithoutAnimalConfirmPrompt,
   });

   static hasAttractionWithoutAnimalIssue(issues = []) {
      return ScheduleItemWithoutAnimalFragment.hasWithoutAnimalIssue(
         issues,
         AttractionWithoutAnimalFragment.ATTRACTION_WITHOUT_ANIMAL_CONFIG
      );

   }

   static getAttractionNamesFromWithoutAnimalIssues(issues = []) {
      return ScheduleItemWithoutAnimalFragment.getNamesFromWithoutAnimalIssues(
         issues,
         AttractionWithoutAnimalFragment.ATTRACTION_WITHOUT_ANIMAL_CONFIG
      );

   }

   static getAttractionsFromWithoutAnimalIssues(issues = []) {
      return ScheduleItemWithoutAnimalFragment.getItemsFromWithoutAnimalIssues(
         issues,
         AttractionWithoutAnimalFragment.ATTRACTION_WITHOUT_ANIMAL_CONFIG
      );

   }

   static getPrimaryAttractionFromWithoutAnimalIssues(issues = []) {
      return ScheduleItemWithoutAnimalFragment.getPrimaryFromWithoutAnimalIssues(
         issues,
         AttractionWithoutAnimalFragment.ATTRACTION_WITHOUT_ANIMAL_CONFIG
      );

   }

   static attractionWithoutAnimalMessage(
      attraction,
      {
      includeConfirmPrompt = false,
      strings = Strings.itinerary.confirmation,
      } = {}
   ) {
      return ScheduleItemWithoutAnimalFragment.withoutAnimalMessage(
         attraction,
         AttractionWithoutAnimalFragment.ATTRACTION_WITHOUT_ANIMAL_CONFIG,
         {
            includeConfirmPrompt,
            strings,
         }
      );

   }

   static showAttractionWithoutAnimalConfirmation(options = {}) {
      ScheduleItemWithoutAnimalFragment.showWithoutAnimalConfirmation(
         options,
         AttractionWithoutAnimalFragment.ATTRACTION_WITHOUT_ANIMAL_CONFIG
      );
   }
}
