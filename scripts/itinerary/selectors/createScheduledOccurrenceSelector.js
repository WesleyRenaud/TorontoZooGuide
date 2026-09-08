import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { StoredSelectionNormalizer } from './base/storedSelectionNormalizer.js';
import { ItinerarySearchContext } from '../itinerarySearchContext.js';
import { ScheduledOccurrencePresenter } from '../scheduledOccurrencePresenter.js';
import { ScheduledOccurrenceSelectorFactory } from './scheduledOccurrenceSelectorFactory.js';
import { ScheduledOccurrenceSorter } from '../scheduledOccurrenceSorter.js';
import { ScheduledOccurrenceTimeModel } from '../scheduledOccurrenceTimeModel.js';
import { SelectorControllerFactory } from './selectorControllerFactory.js';
import { Strings } from '../../strings.js';

export class CreateScheduledOccurrenceSelector {
   static createScheduledOccurrenceMigration({
   emptyStoredFields,
   buildImageSrc,
   includeLink = false,
   readStoredFields,
   getId,
} = {}) {
      return (items) => StoredSelectionNormalizer.migrateStoredSelectionItems(items, {
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
         ScheduledOccurrencePresenter.buildOccurrenceDetailImageSrc(imageDirectory, name)
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

      return SelectorControllerFactory.createItinerarySelectorController({
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

         extractRows: (response) => ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime(
            response[responseKey],
            getTimeOfDay),

         getId,
         getTitle: (row) => getName(row) || defaultTitle,
         getSubtitle: (row) => ScheduledOccurrencePresenter.buildOccurrenceSubtitle({
            primaryValue: getPrimaryValue(row),
            timeRange: ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange(row),
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
