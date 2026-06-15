import {
   createItineraryPopupLayout,
   getItineraryPanelMountEl,
   mountDismissablePopup,
} from './popup.js';
import { createScheduleItemModuleController } from './scheduleItemModuleController.js';
import {
   buildScheduleItemModuleBody,
   buildSearchRowRenderer,
} from './scheduleItemModuleForm.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';
import { APP_STRINGS } from '../../../strings.js';

const SEARCH_DEBOUNCE_MS = 250;

function debounce(fn, delay = SEARCH_DEBOUNCE_MS) {
   let timeoutId = null;

   return (...args) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => fn(...args), delay);
   };
}

export function showScheduleItemModule({
   itinerary = {},
   eventTypes = [],
   onScheduled = null,
   preselectedRow = null,
} = {}) {
   const strings = APP_STRINGS.itinerary.scheduleItem;
   const {
      body: moduleBodyEl,
      scheduleTimeFields,
   } = buildScheduleItemModuleBody(strings, eventTypes);
   const {
      root,
      overlay,
      buttonEls,
      closeButton,
   } = createItineraryPopupLayout({
      popupClassName: 'schedule-item-module',
      title: strings.title,
      bodyContent: moduleBodyEl,
      showCloseButton: true,
      actionButtons: [
         {
            key: 'cancel',
            className: 'itin-prev',
            text: APP_STRINGS.itinerary.actions.cancel,
         },
         {
            key: 'schedule',
            className: 'itin-finish',
            text: strings.scheduleButton,
         },
      ],
   });

   const body = root.querySelector('.schedule-item-module-body');
   const controller = createScheduleItemModuleController({
      itinerary,
      eventTypes,
      strings,
      preselectedRow,
      scheduleTimeFields,
      onScheduled,
      renderAnimalRowLeft: buildSearchRowRenderer(ScheduleItemKind.ANIMAL.itemType),
      renderAttractionRowLeft: buildSearchRowRenderer(ScheduleItemKind.ATTRACTION.itemType),
      refs: {
         typeSelect: body?.querySelector('.schedule-item-select'),
         searchInput: body?.querySelector('.schedule-item-search-input'),
         resultsEl: body?.querySelector('.schedule-item-results'),
         searchLabelEl: body?.querySelector(
            '.schedule-item-search-field .schedule-item-field-label'
         ),
         onlyItineraryItemsCheckbox: body?.querySelector(
            '.schedule-item-only-itinerary-checkbox'
         ),
         onlyItineraryItemsWrap: body?.querySelector('.schedule-item-only-itinerary-wrap'),
      },
      scheduleButton: buttonEls.schedule,
   });

   const popup = mountDismissablePopup({
      mountEl: getItineraryPanelMountEl() ?? document.body,
      root,
      overlay,
      initialFocusEl: body?.querySelector('.schedule-item-select'),
      onDismiss: null,
   });

   const scheduleSearch = debounce(() => {
      void controller.runSearch();
   });

   controller.bindEvents({ popup, scheduleSearch });

   buttonEls.cancel?.addEventListener('click', () => {
      popup.dismiss();
   });

   closeButton?.addEventListener('click', () => {
      popup.dismiss();
   });

   controller.initialize();

   return popup;
}
