import { ConfirmPopup } from './components/confirmPopup.js';
import { Popup } from './components/popup.js';
import { Format } from './format.js';
import { Strings } from '../../strings.js';

const ATTRACTION_WITHOUT_ANIMAL_ISSUE = 'attractionWithoutAnimal';

export class AttractionWithoutAnimalConfirmation {
   static hasAttractionWithoutAnimalIssue(issues = []) {
      return issues.some(
         (issue) => issue?.type === ATTRACTION_WITHOUT_ANIMAL_ISSUE
      );

   }

   static getAttractionNamesFromWithoutAnimalIssues(issues = []) {
      return AttractionWithoutAnimalConfirmation.getAttractionsFromWithoutAnimalIssues(issues)
         .map((attraction) => attraction.attractionName);

   }

   static getAttractionsFromWithoutAnimalIssues(issues = []) {
      const attractionsByName = new Map();

      issues
         .filter((issue) => issue?.type === ATTRACTION_WITHOUT_ANIMAL_ISSUE)
         .flatMap((issue) => issue.items ?? [])
         .forEach((item) => {
            const attractionName = Format.normalizeText(item?.name);

            if (!attractionName) {
               return;
            }

            const attractionTime = Format.formatClockTime(item?.start_time);

            attractionsByName.set(
               attractionName,
               attractionTime
                  ? { attractionName, attractionTime }
                  : { attractionName }
            );
         });

      return [...attractionsByName.values()];

   }

   static getPrimaryAttractionFromWithoutAnimalIssues(issues = []) {
      const [attraction] = AttractionWithoutAnimalConfirmation.getAttractionsFromWithoutAnimalIssues(issues);

      return attraction ?? null;

   }

   static attractionWithoutAnimalMessage(
      attraction,
      {
      includeConfirmPrompt = false,
      strings = Strings.itinerary.confirmation,
      } = {}
   ) {
      const attractionName = Format.normalizeText(attraction.attractionName);
      const body = attraction.attractionTime
         ? strings.attractionWithoutAnimalBody(
            attractionName,
            attraction.attractionTime
         )
         : strings.attractionWithoutAnimalBodyWithoutTime(attractionName);

      if (!includeConfirmPrompt) {
         return body;
      }

      return `${body}${strings.attractionWithoutAnimalConfirmPrompt}`;

   }

   static showAttractionWithoutAnimalConfirmation({
      issues = [],
      onConfirm,
      onCancel,
      mountEl = Popup.getItineraryOverlayMountEl() ?? document.body,
   } = {}) {
      const strings = Strings.itinerary.confirmation;
      const attractions = AttractionWithoutAnimalConfirmation.getAttractionsFromWithoutAnimalIssues(issues);

      // Multi-item without-animal warnings use showItineraryBuildWarningsConfirmation.
      if (attractions.length !== 1) {
         return;
      }

      const [attraction] = attractions;

      ConfirmPopup.showItineraryConfirmPopup({
         title: strings.attractionWithoutAnimalTitle,
         message: AttractionWithoutAnimalConfirmation.attractionWithoutAnimalMessage(attraction, {
            includeConfirmPrompt: true,
            strings,
         }),
         confirmText: strings.saveIssuesButton,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl,
         onConfirm,
         onCancel,
      });
   }
}
