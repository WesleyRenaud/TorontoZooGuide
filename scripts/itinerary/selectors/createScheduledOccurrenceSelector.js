import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { StoredSelection } from './base/storedSelection.js';
import { CreateSelectorController } from './createSelectorController.js';
import { ItinerarySearchContext } from '../itinerarySearchContext.js';
import { ScheduledOccurrencePresentation } from '../scheduledOccurrencePresentation.js';
import { ScheduledOccurrenceSelectorFactory } from './scheduledOccurrenceSelectorFactory.js';
import { ScheduledOccurrenceSort } from '../scheduledOccurrenceSort.js';
import { ScheduledOccurrenceTimeRange } from '../scheduledOccurrenceTimeRange.js';
import { Strings } from '../../strings.js';

export class CreateScheduledOccurrenceSelector {
   static createScheduledOccurrenceMigration({
   emptyStoredFields,
   buildImageSrc,
   includeLink = false,
   readStoredFields,
   getId,
} = {}) {
      return (items) => StoredSelection.migrateStoredSelectionItems(items, {
         fromString: (item) => ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromString(item, {
            emptyStoredFields,
            buildImageSrc,
         }),
         fromObject: (item) => ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromObject(item, {
            buildImageSrc,
            includeLink,
            readStoredFields,
            getId,
         }),
      });
   }

   static createScheduledOccurrenceSelectorController({
   mountEl,
   onNext,
   onPrev,
   onFinish,
   onClose,
   hideNextButton = false,
   storageKey,
   responseKey,
   searchFlag,
   imageDirectory,
   defaultTitle,
   heading,
   subtitle,
   emptyText,
   getName = ScheduledOccurrenceSelectorFactory.getOccurrenceName,
   getId = getName,
   getPrimaryValue,
   getTimeOfDay = (row) => ValueNormalizer.asTrimmedString(row?.start_time),
   getLink = null,
   emptyStoredFields = {},
   readStoredFields,
   buildSelectionFields,
} = {}) {
      const buildImageSrc = (name) => (
         ScheduledOccurrencePresentation.buildOccurrenceDetailImageSrc(imageDirectory, name)
      );

      const migrateSelected = CreateScheduledOccurrenceSelector.createScheduledOccurrenceMigration({
         emptyStoredFields,
         buildImageSrc,
         includeLink: typeof getLink === 'function',
         readStoredFields,
         getId,
      });

      const makeSelection = (row) => ScheduledOccurrenceSelectorFactory.createOccurrenceSelection(row, {
         getId,
         getLink,
         getName,
         getTimeOfDay,
         buildImageSrc,
         buildSelectionFields,
      });

      return CreateSelectorController.createItinerarySelectorController({
         mountEl,
         onPrev,
         onNext,
         onFinish,
         onClose,
         hideNextButton,

         storageKey,
         migrateSelected,

         getContext: ItinerarySearchContext.getItineraryDateSearchContext,

         buildSearchPayload: (query) => ({
            query,
            [searchFlag]: true,
         }),

         extractRows: (response) => ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime(
            response[responseKey],
            getTimeOfDay),

         getId,
         getTitle: (row) => getName(row) || defaultTitle,
         getSubtitle: (row) => ScheduledOccurrencePresentation.buildOccurrenceSubtitle({
            primaryValue: getPrimaryValue(row),
            timeRange: ScheduledOccurrenceTimeRange.buildScheduledOccurrenceTimeRange(row),
         }),
         getImageSrc: (row) => buildImageSrc(getName(row)),
         getInfoLink: () => null,
         onTitleClick: typeof getLink === 'function'
            ? (row) => {
               const link = getLink(row);

               if (link) {
                  window.open(link, '_blank');
               }
            }
            : null,
         makeSelection,

         topTitle: Strings.itinerary.selectors.builderTitle,
         h1: heading,
         subtitle,
         emptyText,
      });
   }
}
