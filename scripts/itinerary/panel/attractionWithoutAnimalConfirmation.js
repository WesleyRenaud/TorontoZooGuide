import { showItineraryConfirmPopup } from './components/confirmPopup.js';
import { getItineraryOverlayMountEl } from './components/popup.js';
import {
   formatClockTime,
   normalizeText,
} from './format.js';
import { APP_STRINGS } from '../../strings.js';

const ATTRACTION_WITHOUT_ANIMAL_ISSUE = 'attractionWithoutAnimal';

export function hasAttractionWithoutAnimalIssue(issues = []) {
   return issues.some(
      (issue) => issue?.type === ATTRACTION_WITHOUT_ANIMAL_ISSUE
   );
}

export function getAttractionNamesFromWithoutAnimalIssues(issues = []) {
   return getAttractionsFromWithoutAnimalIssues(issues)
      .map((attraction) => attraction.attractionName);
}

export function getAttractionsFromWithoutAnimalIssues(issues = []) {
   const attractionsByName = new Map();

   issues
      .filter((issue) => issue?.type === ATTRACTION_WITHOUT_ANIMAL_ISSUE)
      .flatMap((issue) => issue.items ?? [])
      .forEach((item) => {
         const attractionName = normalizeText(item?.name);

         if (!attractionName) {
            return;
         }

         const attractionTime = formatClockTime(item?.start_time);

         attractionsByName.set(
            attractionName,
            attractionTime
               ? { attractionName, attractionTime }
               : { attractionName }
         );
      });

   return [...attractionsByName.values()];
}

export function getPrimaryAttractionFromWithoutAnimalIssues(issues = []) {
   const [attraction] = getAttractionsFromWithoutAnimalIssues(issues);

   return attraction ?? null;
}

export function attractionWithoutAnimalMessage(
   attraction,
   {
      includeConfirmPrompt = false,
      strings = APP_STRINGS.itinerary.confirmation,
   } = {}
) {
   const attractionName = normalizeText(attraction.attractionName);
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

export function showAttractionWithoutAnimalConfirmation({
   issues = [],
   onConfirm,
   onCancel,
   mountEl = getItineraryOverlayMountEl() ?? document.body,
} = {}) {
   const strings = APP_STRINGS.itinerary.confirmation;
   const attractions = getAttractionsFromWithoutAnimalIssues(issues);

   // Multi-item without-animal warnings use showItineraryBuildWarningsConfirmation.
   if (attractions.length !== 1) {
      return;
   }

   const [attraction] = attractions;

   showItineraryConfirmPopup({
      title: strings.attractionWithoutAnimalTitle,
      message: attractionWithoutAnimalMessage(attraction, {
         includeConfirmPrompt: true,
         strings,
      }),
      confirmText: strings.saveIssuesButton,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      mountEl,
      onConfirm,
      onCancel,
   });
}
