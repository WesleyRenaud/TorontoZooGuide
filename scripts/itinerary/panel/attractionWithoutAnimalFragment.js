import { ConfirmFragment } from './components/confirmFragment.js';
import { ItineraryPanelFragment } from './components/itineraryPanelFragment.js';
import { ItineraryItemFormatter } from './itineraryItemFormatter.js';
import { Strings } from '../../strings.js';

export class AttractionWithoutAnimalFragment {
   static ATTRACTION_WITHOUT_ANIMAL_ISSUE = 'attractionWithoutAnimal';

   static hasAttractionWithoutAnimalIssue(issues = []) {
      return issues.some(
         (issue) => issue?.type === AttractionWithoutAnimalFragment.ATTRACTION_WITHOUT_ANIMAL_ISSUE
      );

   }

   static getAttractionNamesFromWithoutAnimalIssues(issues = []) {
      return AttractionWithoutAnimalFragment.getAttractionsFromWithoutAnimalIssues(issues)
         .map((attraction) => attraction.attractionName);

   }

   static getAttractionsFromWithoutAnimalIssues(issues = []) {
      const attractionsByName = new Map();

      issues
         .filter((issue) => issue?.type === AttractionWithoutAnimalFragment.ATTRACTION_WITHOUT_ANIMAL_ISSUE)
         .flatMap((issue) => issue.items ?? [])
         .forEach((item) => {
            const attractionName = ItineraryItemFormatter.normalizeText(item?.name);

            if (!attractionName) {
               return;
            }

            const attractionTime = ItineraryItemFormatter.formatClockTime(item?.start_time);

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
      const [attraction] = AttractionWithoutAnimalFragment.getAttractionsFromWithoutAnimalIssues(issues);

      return attraction ?? null;

   }

   static attractionWithoutAnimalMessage(
      attraction,
      {
      includeConfirmPrompt = false,
      strings = Strings.itinerary.confirmation,
      } = {}
   ) {
      const attractionName = ItineraryItemFormatter.normalizeText(attraction.attractionName);
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
      mountEl = ItineraryPanelFragment.getItineraryOverlayMountEl() ?? document.body,
   } = {}) {
      const attractions = AttractionWithoutAnimalFragment.getAttractionsFromWithoutAnimalIssues(issues);

      // Multi-item without-animal warnings use showItineraryBuildWarningsConfirmation.
      if (attractions.length !== 1) {
         return;
      }

      const [attraction] = attractions;

      ConfirmFragment.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.attractionWithoutAnimalTitle,
         message: AttractionWithoutAnimalFragment.attractionWithoutAnimalMessage(attraction, {
            includeConfirmPrompt: true,
            strings: Strings.itinerary.confirmation,
         }),
         confirmText: Strings.itinerary.confirmation.saveIssuesButton,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl,
         onConfirm,
         onCancel,
      });
   }
}
