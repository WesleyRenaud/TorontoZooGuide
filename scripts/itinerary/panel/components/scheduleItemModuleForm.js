import { el } from '../dom.js';
import { makeScheduleItemTimeFields } from './scheduleItemTimeFields.js';
import { buildScheduleItemTypeOptions } from '../scheduleItemTypes.js';
import {
   buildAnimalImageSrc,
   getAnimalEnclosureName,
   getAnimalSpecies,
   getAnimalSubtitle,
   getAnimalTitleLine,
} from '../../selectors/animalSelector/model.js';
import {
   buildAttractionImageSrc,
   getAttractionInfoLink,
   getAttractionSubtitle,
   getAttractionTitle,
} from '../../selectors/attractionSelector/model.js';
import { createDefaultSelectorRowLeftRenderer } from '../../selectors/base/resultRenderer.js';
import {
   buildGuardiansTalkImageSrc,
   getGuardiansTalkName,
   getGuardiansTalkSubtitle,
   getGuardiansTalkTitleSuffix,
} from '../../selectors/guardiansTalkSelector/model.js';
import {
   buildWildEncounterImageSrc,
   getWildEncounterLink,
   getWildEncounterName,
   getWildEncounterSubtitle,
   getWildEncounterTitleSuffix,
} from '../../selectors/wildEncounterSelector/model.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';

function createFieldLabel(text) {
   return el('label', 'schedule-item-field-label', text);
}

function createOnlyItineraryItemsCheckbox(labelText) {
   const wrap = el('div', 'schedule-item-only-itinerary-wrap');
   const label = el('label', 'schedule-item-only-itinerary-row');
   const checkbox = document.createElement('input');

   checkbox.type = 'checkbox';
   checkbox.className = 'schedule-item-only-itinerary-checkbox';
   checkbox.checked = false;

   const text = el('span', 'schedule-item-only-itinerary-label', labelText);
   label.append(checkbox, text);
   wrap.appendChild(label);

   return { wrap, checkbox };
}

function createSelectField({
   label,
   options = [],
   getOptionValue = (option) => option,
   getOptionLabel = (option) => String(option),
} = {}) {
   const field = el('div', 'schedule-item-field');
   const select = document.createElement('select');
   select.className = 'schedule-item-select';

   field.appendChild(createFieldLabel(label));
   field.appendChild(select);

   options.forEach((option) => {
      const optionEl = document.createElement('option');
      const value = getOptionValue(option);

      optionEl.value = value;
      optionEl.textContent = getOptionLabel(option);
      optionEl.selected = Boolean(option.selected);
      select.appendChild(optionEl);
   });

   return {
      field,
      select,
   };
}

export function buildSearchRowRenderer(moduleType) {
   if (moduleType === ScheduleItemKind.ANIMAL.itemType) {
      return createDefaultSelectorRowLeftRenderer({
         getTitle: getAnimalTitleLine,
         getTitleParts: (row) => ({
            species: getAnimalSpecies(row),
            enclosureName: getAnimalEnclosureName(row),
         }),
         getSubtitle: getAnimalSubtitle,
         getImageSrc: buildAnimalImageSrc,
         getInfoLink: () => null,
      });
   }

   if (moduleType === ScheduleItemKind.GUARDIANS_TALK.itemType) {
      return createDefaultSelectorRowLeftRenderer({
         getTitle: getGuardiansTalkName,
         getTitleSuffix: getGuardiansTalkTitleSuffix,
         getSubtitle: getGuardiansTalkSubtitle,
         getImageSrc: buildGuardiansTalkImageSrc,
         getInfoLink: () => null,
      });
   }

   if (moduleType === ScheduleItemKind.WILD_ENCOUNTER.itemType) {
      return createDefaultSelectorRowLeftRenderer({
         getTitle: getWildEncounterName,
         getTitleSuffix: getWildEncounterTitleSuffix,
         getSubtitle: getWildEncounterSubtitle,
         getImageSrc: buildWildEncounterImageSrc,
         getInfoLink: getWildEncounterLink,
      });
   }

   return createDefaultSelectorRowLeftRenderer({
      getTitle: getAttractionTitle,
      getSubtitle: getAttractionSubtitle,
      getImageSrc: buildAttractionImageSrc,
      getInfoLink: () => null,
      onTitleClick: (row) => {
         const link = getAttractionInfoLink(row);

         if (link) {
            window.open(link, '_blank');
         }
      },
      shouldEnableTitleClick: (row) => Boolean(getAttractionInfoLink(row)),
   });
}

export function buildScheduleItemModuleBody(strings, eventTypes = []) {
   const body = el('div', 'schedule-item-module-body');

   const typeField = createSelectField({
      label: strings.typeLabel,
      options: buildScheduleItemTypeOptions(eventTypes, strings),
      getOptionValue: (option) => option.value,
      getOptionLabel: (option) => option.label,
   });

   const searchField = el('div', 'schedule-item-field schedule-item-search-field');
   const searchLabelEl = createFieldLabel(strings.searchLabel);
   const searchInput = document.createElement('input');
   searchInput.className = 'schedule-item-search-input';
   searchInput.type = 'text';
   searchInput.placeholder = strings.searchPlaceholder;
   searchInput.autocomplete = 'off';

   const onlyItineraryItemsField = createOnlyItineraryItemsCheckbox(
      strings.onlyItineraryItemsLabel
   );

   searchField.append(searchLabelEl, searchInput);

   const resultsEl = el('div', 'itin-results schedule-item-results');
   resultsEl.setAttribute('aria-live', 'polite');
   const scheduleTimeFields = makeScheduleItemTimeFields(strings);

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
