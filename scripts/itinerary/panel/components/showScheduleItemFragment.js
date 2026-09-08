import { ItineraryPanelFragment } from './itineraryPanelFragment.js';
import { ScheduleItemModuleController } from './scheduleItemModuleController.js';
import { ScheduleItemModuleView } from './scheduleItemModuleView.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';
import { ShowScheduleItemModuleHelper } from './showScheduleItemModuleHelper.js';
import { Strings } from '../../../strings.js';

export class ShowScheduleItemFragment {
   static showScheduleItemModule({
      itinerary = {},
      eventTypes = [],
      onScheduled = null,
      preselectedRow = null,
   } = {}) {
      const {
         body: moduleBodyEl,
         scheduleTimeFields,
      } = ScheduleItemModuleView.buildScheduleItemModuleBody(Strings.itinerary.scheduleItem, eventTypes);
      const {
         root,
         overlay,
         buttonEls,
         closeButton,
      } = ItineraryPanelFragment.createItineraryPopupLayout({
         popupClassName: 'schedule-item-module',
         title: Strings.itinerary.scheduleItem.title,
         bodyContent: moduleBodyEl,
         showCloseButton: true,
         actionButtons: [
            {
               key: 'cancel',
               className: 'itin-prev',
               text: Strings.itinerary.actions.cancel,
            },
            {
               key: 'schedule',
               className: 'itin-finish',
               text: Strings.itinerary.scheduleItem.scheduleButton,
            },
         ],
      });

      const body = root.querySelector('.schedule-item-module-body');
      const controller = ScheduleItemModuleController.createScheduleItemModuleController({
         itinerary,
         eventTypes,
         strings: Strings.itinerary.scheduleItem,
         preselectedRow,
         scheduleTimeFields,
         onScheduled,
         renderAnimalRowLeft: ScheduleItemModuleView.buildSearchRowRenderer(ScheduleItemKind.ANIMAL.itemType),
         renderAttractionRowLeft: ScheduleItemModuleView.buildSearchRowRenderer(ScheduleItemKind.ATTRACTION.itemType),
         renderTransportationRowLeft: ScheduleItemModuleView.buildSearchRowRenderer(
            ScheduleItemKind.TRANSPORTATION.itemType
         ),
         renderGuardiansTalkRowLeft: ScheduleItemModuleView.buildSearchRowRenderer(ScheduleItemKind.GUARDIANS_TALK.itemType),
         renderWildEncounterRowLeft: ScheduleItemModuleView.buildSearchRowRenderer(ScheduleItemKind.WILD_ENCOUNTER.itemType),
         refs: {
            typeSelect: body?.querySelector('.schedule-item-select'),
            typeLabelEl: body?.querySelector(
               '.schedule-item-type-field .schedule-item-field-label'
            ),
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

      const typeSelect = body?.querySelector('.schedule-item-select');
      const dialogEl = root.querySelector('.itin-card');

      if (preselectedRow) {
         dialogEl?.setAttribute('tabindex', '-1');
      }

      const popup = ItineraryPanelFragment.mountDismissablePopup({
         mountEl: ItineraryPanelFragment.getItineraryPanelMountEl() ?? document.body,
         root,
         overlay,
         initialFocusEl: preselectedRow ? dialogEl : typeSelect,
         onDismiss: null,
      });

      const scheduleSearch = ShowScheduleItemModuleHelper.debounce(() => {
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
}
