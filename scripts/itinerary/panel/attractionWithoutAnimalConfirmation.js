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
   return issues
      .filter((issue) => issue?.type === ATTRACTION_WITHOUT_ANIMAL_ISSUE)
      .flatMap((issue) => (issue.items ?? [])
         .map((item) => (item?.name ?? '').trim())
         .filter(Boolean));
}

export function getPrimaryAttractionFromWithoutAnimalIssues(issues = []) {
   const [attractionName] = getAttractionNamesFromWithoutAnimalIssues(issues);

   if (!attractionName) {
      return null;
   }

   const attractionItem = issues
      .filter((issue) => issue?.type === ATTRACTION_WITHOUT_ANIMAL_ISSUE)
      .flatMap((issue) => issue.items ?? [])
      .find((item) => (item?.name ?? '').trim() === attractionName);

   const attractionTime = formatClockTime(
      attractionItem?.start_time ?? attractionItem?.startTime
   );

   if (!attractionTime) {
      return { attractionName };
   }

   return { attractionName, attractionTime };
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
   const attraction = getPrimaryAttractionFromWithoutAnimalIssues(issues);

   if (!attraction?.attractionName) {
      return;
   }

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
