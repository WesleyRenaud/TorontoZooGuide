import { ItineraryPanelDom } from '../itineraryPanelDom.js';
import { ScheduleItemModuleFormBuilder } from './scheduleItemModuleFormBuilder.js';
import { ScheduleItemTimeFields } from './scheduleItemTimeFields.js';
import { ScheduleItemTypes } from '../scheduleItemTypes.js';
import { AnimalSelectorModel } from '../../selectors/animalSelector/animalSelectorModel.js';
import { AttractionSelectorModel } from '../../selectors/attractionSelector/attractionSelectorModel.js';
import { ResultRenderer } from '../../selectors/base/resultRenderer.js';
import { GuardiansTalkSelectorModel } from '../../selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { TransportationSelectorModel } from '../../selectors/transportationSelector/transportationSelectorModel.js';
import { WildEncounterSelectorModel } from '../../selectors/wildEncounterSelector/wildEncounterSelectorModel.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';

export class ScheduleItemModuleForm {
   static buildSearchRowRenderer(moduleType) {
      if (moduleType === ScheduleItemKind.ANIMAL.itemType) {
         return ResultRenderer.createDefaultSelectorRowLeftRenderer({
            getTitle: AnimalSelectorModel.getAnimalTitleLine,
            getTitleParts: (row) => ({
               species: AnimalSelectorModel.getAnimalSpecies(row),
               enclosureName: AnimalSelectorModel.getAnimalEnclosureName(row),
            }),
            getSubtitle: AnimalSelectorModel.getAnimalSubtitle,
            getImageSrc: AnimalSelectorModel.buildAnimalImageSrc,
            getInfoLink: () => null,
         });
      }

      if (moduleType === ScheduleItemKind.GUARDIANS_TALK.itemType) {
         return ResultRenderer.createDefaultSelectorRowLeftRenderer({
            getTitle: GuardiansTalkSelectorModel.getGuardiansTalkName,
            getTitleSuffix: GuardiansTalkSelectorModel.getGuardiansTalkTitleSuffix,
            getSubtitle: GuardiansTalkSelectorModel.getGuardiansTalkSubtitle,
            getImageSrc: GuardiansTalkSelectorModel.buildGuardiansTalkImageSrc,
            getInfoLink: () => null,
         });
      }

      if (moduleType === ScheduleItemKind.WILD_ENCOUNTER.itemType) {
         return ResultRenderer.createDefaultSelectorRowLeftRenderer({
            getTitle: WildEncounterSelectorModel.getWildEncounterName,
            getTitleSuffix: WildEncounterSelectorModel.getWildEncounterTitleSuffix,
            getSubtitle: WildEncounterSelectorModel.getWildEncounterSubtitle,
            getImageSrc: WildEncounterSelectorModel.buildWildEncounterImageSrc,
            getInfoLink: WildEncounterSelectorModel.getWildEncounterLink,
         });
      }

      if (moduleType === ScheduleItemKind.TRANSPORTATION.itemType) {
         return ResultRenderer.createDefaultSelectorRowLeftRenderer({
            getTitle: TransportationSelectorModel.getTransportationName,
            getSubtitle: TransportationSelectorModel.buildTransportationStationsLine,
            getImageSrc: TransportationSelectorModel.buildTransportationImageSrc,
            getInfoLink: () => null,
            onTitleClick: (row) => {
               const link = TransportationSelectorModel.getTransportationInfoLink(row);

               if (link) {
                  window.open(link, '_blank');
               }
            },
            shouldEnableTitleClick: (row) => Boolean(TransportationSelectorModel.getTransportationInfoLink(row)),
         });
      }

      return ResultRenderer.createDefaultSelectorRowLeftRenderer({
         getTitle: AttractionSelectorModel.getAttractionTitle,
         getSubtitle: AttractionSelectorModel.getAttractionSubtitle,
         getImageSrc: AttractionSelectorModel.buildAttractionImageSrc,
         getInfoLink: () => null,
         onTitleClick: (row) => {
            const link = AttractionSelectorModel.getAttractionInfoLink(row);

            if (link) {
               window.open(link, '_blank');
            }
         },
         shouldEnableTitleClick: (row) => Boolean(AttractionSelectorModel.getAttractionInfoLink(row)),
      });

   }

   static buildScheduleItemModuleBody(strings, eventTypes = []) {
      const body = ItineraryPanelDom.el('div', 'schedule-item-module-body');

      const typeField = ScheduleItemModuleFormBuilder.createSelectField({
         label: strings.typeLabel,
         options: ScheduleItemTypes.buildScheduleItemTypeOptions(eventTypes, strings),
         getOptionValue: (option) => option.value,
         getOptionLabel: (option) => option.label,
      });

      const searchField = ItineraryPanelDom.el('div', 'schedule-item-field schedule-item-search-field');
      const searchLabelEl = ScheduleItemModuleFormBuilder.createFieldLabel(strings.searchLabel);
      const searchInput = document.createElement('input');
      searchInput.className = 'schedule-item-search-input';
      searchInput.type = 'text';
      searchInput.placeholder = strings.searchPlaceholder;
      searchInput.autocomplete = 'off';

      const onlyItineraryItemsField = ScheduleItemModuleFormBuilder.createOnlyItineraryItemsCheckbox(
         strings.onlyItineraryItemsLabel
      );

      searchField.append(searchLabelEl, searchInput);

      const resultsEl = ItineraryPanelDom.el('div', 'itin-results schedule-item-results');
      resultsEl.setAttribute('aria-live', 'polite');
      const scheduleTimeFields = ScheduleItemTimeFields.makeScheduleItemTimeFields(strings);

      body.append(
         typeField.field,
         searchField,
         onlyItineraryItemsField.wrap,
         ...scheduleTimeFields.fields,
         resultsEl
      );

      return {
         body,
         typeSelect: typeField.select,
         searchInput,
         onlyItineraryItemsCheckbox: onlyItineraryItemsField.checkbox,
         resultsEl,
         scheduleTimeFields,
      };
   }
}
