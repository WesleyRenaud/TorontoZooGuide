import {
   buildHalfHourSlotStarts,
   formatMinutesAsClockTime,
   parseClockTimeMinutes,
} from '../dayPlannerSchedule.js';
import { el } from '../dom.js';
import {
   formatClockTime,
   formatISODateFull,
} from '../format.js';
import {
   buildGuardiansRows,
   buildWildRows,
} from '../rows.js';
import { makeSection } from './section.js';
import { buildSectionConfigs } from '../sectionConfigs.js';
import { APP_STRINGS } from '../../../strings.js';

export const ITINERARY_PANEL_VIEWS = {
   list: 'list',
   dayPlanner: 'dayPlanner',
};

function makeToggleButton({ label, view, activeView, onSelect }) {
   const button = el('button', 'itin-panel-view-toggle-button', label);
   button.type = 'button';
   button.dataset.view = view;
   button.setAttribute('aria-pressed', view === activeView ? 'true' : 'false');
   button.addEventListener('click', () => onSelect(view));
   return button;
}

function setViewVisibility(root, selectedView) {
   root.querySelectorAll('.itin-panel-view-toggle-button').forEach((button) => {
      const isSelected = button.dataset.view === selectedView;
      button.classList.toggle('itin-panel-view-toggle-button-active', isSelected);
      button.setAttribute('aria-pressed', isSelected ? 'true' : 'false');
   });

   root.querySelectorAll('.itin-panel-view').forEach((view) => {
      view.hidden = view.dataset.view !== selectedView;
   });
}

function makeTimelineRow(timeLabel, pillLabel) {
   const gridLine = el('div', 'itinerary-day-grid-line');

   if (pillLabel) {
      gridLine.appendChild(el('span', 'itinerary-day-open-pill', pillLabel));
   }

   return [
      el('div', 'itinerary-day-time', timeLabel),
      gridLine,
   ];
}

function makeUnavailableMessage(message) {
   return el('div', 'itinerary-day-unavailable', message);
}

function getScheduledMaximumDuration(item) {
   const maximumDuration = Number(item?.maximum_duration);
   return Number.isFinite(maximumDuration) && maximumDuration > 0 ? maximumDuration : null;
}

function makeScheduledItemBlock(itemRow, maximumDuration) {
   const block = el('div', 'itinerary-day-event');
   const slotSpan = maximumDuration / 30;

   block.style.setProperty('--itinerary-event-slot-span', slotSpan);
   itemRow.classList.add('itinerary-day-event-card');
   block.appendChild(itemRow);

   return block;
}

function buildScheduledItemRows(items, buildRows) {
   return items.map((item, index) => {
      const [row] = buildRows([item]);
      const maximumDuration = getScheduledMaximumDuration(item);
      return {
         index,
         item,
         row,
         startMinutes: parseClockTimeMinutes(item?.start_time),
         maximumDuration,
      };
   }).filter((scheduledItem) => (
      scheduledItem.row
      && Number.isFinite(scheduledItem.startMinutes)
      && Number.isFinite(scheduledItem.maximumDuration)
   ));
}

function buildScheduledItemRowsContext(
   {
      guardiansTalks = [],
      wildEncounters = [],
   } = {},
   slotStarts = []
) {
   const slotStartSet = new Set(slotStarts);
   const guardiansTalkRows = buildScheduledItemRows(guardiansTalks, buildGuardiansRows)
      .filter((scheduledItem) => slotStartSet.has(scheduledItem.startMinutes));
   const wildEncounterRows = buildScheduledItemRows(wildEncounters, buildWildRows)
      .filter((scheduledItem) => slotStartSet.has(scheduledItem.startMinutes));
   const scheduledItems = [
      ...guardiansTalkRows,
      ...wildEncounterRows,
   ];
   const itemsByStart = scheduledItems.reduce((itemsByStartMap, scheduledItem) => {
      const items = itemsByStartMap.get(scheduledItem.startMinutes) ?? [];
      items.push(scheduledItem);
      itemsByStartMap.set(scheduledItem.startMinutes, items);
      return itemsByStartMap;
   }, new Map());

   return {
      itemsByStart,
      scheduledGuardiansTalkIndexes: new Set(
         guardiansTalkRows.map((scheduledItem) => scheduledItem.index)
      ),
      scheduledWildEncounterIndexes: new Set(
         wildEncounterRows.map((scheduledItem) => scheduledItem.index)
      ),
   };
}

function buildUnscheduledItinerary(
   itinerary = {},
   {
      scheduledGuardiansTalkIndexes = new Set(),
      scheduledWildEncounterIndexes = new Set(),
   } = {}
) {
   return {
      ...itinerary,
      guardiansTalks: (itinerary.guardiansTalks ?? []).filter((_, index) => (
         !scheduledGuardiansTalkIndexes.has(index)
      )),
      wildEncounters: (itinerary.wildEncounters ?? []).filter((_, index) => (
         !scheduledWildEncounterIndexes.has(index)
      )),
   };
}

function appendScheduledItems(gridLine, scheduledItems = []) {
   scheduledItems.forEach((scheduledItem) => {
      gridLine.appendChild(
         makeScheduledItemBlock(scheduledItem.row, scheduledItem.maximumDuration)
      );
   });
}

function makeUnscheduledSections(itinerary = {}, scheduledRowsContext = {}) {
   const sectionConfigs = buildSectionConfigs(
      buildUnscheduledItinerary(itinerary, scheduledRowsContext)
   );

   if (sectionConfigs.length === 0) {
      return null;
   }

   const wrapper = el('section', 'itinerary-day-unscheduled-sections');
   const title = el('h4', 'itinerary-day-unscheduled-title', (
      APP_STRINGS.itinerary.dayPlanner.unscheduledTitle
   ));

   wrapper.appendChild(title);
   sectionConfigs.forEach((sectionConfig) => {
      wrapper.appendChild(makeSection(sectionConfig));
   });

   return wrapper;
}

export function makeItineraryPanelViews({
   activeView = ITINERARY_PANEL_VIEWS.list,
   onViewChange = null,
} = {}) {
   const root = el('div', 'itin-panel-view-shell');
   const toggle = el('div', 'itin-panel-view-toggle');
   const sharedHeader = el('div', 'itin-panel-shared-header');
   const listView = el('div', 'itin-panel-view itin-panel-list-view');
   const dayPlannerView = el('div', 'itin-panel-view itin-panel-day-planner-view');

   listView.dataset.view = ITINERARY_PANEL_VIEWS.list;
   dayPlannerView.dataset.view = ITINERARY_PANEL_VIEWS.dayPlanner;

   const selectView = (view) => {
      onViewChange?.(view);
      setViewVisibility(root, view);
   };

   toggle.appendChild(
      makeToggleButton({
         label: APP_STRINGS.itinerary.dayPlanner.listViewLabel,
         view: ITINERARY_PANEL_VIEWS.list,
         activeView,
         onSelect: selectView,
      })
   );
   toggle.appendChild(
      makeToggleButton({
         label: APP_STRINGS.itinerary.dayPlanner.dayPlannerLabel,
         view: ITINERARY_PANEL_VIEWS.dayPlanner,
         activeView,
         onSelect: selectView,
      })
   );

   root.appendChild(sharedHeader);
   root.appendChild(toggle);
   root.appendChild(listView);
   root.appendChild(dayPlannerView);
   setViewVisibility(root, activeView);

   return {
      root,
      sharedHeader,
      listView,
      dayPlannerView,
   };
}

export function makeDayPlannerPreview(zooHours = null, itinerary = {}) {
   const strings = APP_STRINGS.itinerary.dayPlanner;
   const hours = zooHours && typeof zooHours === 'object'
      ? zooHours
      : {};
   const closeTime = formatClockTime(hours.closeTime, strings.thirdSlot);
   const root = el('div', 'itinerary-day-planner-content');
   const section = el('section', 'itinerary-day-module');
   const header = el('div', 'itinerary-day-module-header');
   const titleWrap = el('div');
   const title = el('h3', '', strings.title);
   const date = el('span', 'itinerary-day-module-date', formatISODateFull(hours.date, strings.date));
   const timeline = el('div', 'itinerary-day-timeline');

   section.setAttribute('aria-label', strings.aria);
   timeline.setAttribute('aria-hidden', 'true');

   titleWrap.appendChild(title);
   header.appendChild(titleWrap);
   header.appendChild(date);

   const earlyAdmissionMinutes = parseClockTimeMinutes(hours.earlyAdmissionTime);
   const openMinutes = parseClockTimeMinutes(hours.openTime);
   const lastAdmissionMinutes = parseClockTimeMinutes(hours.lastAdmissionTime);
   const closeMinutes = parseClockTimeMinutes(hours.closeTime);
   const timelineStartMinutes = Number.isFinite(earlyAdmissionMinutes)
      ? earlyAdmissionMinutes
      : openMinutes;
   const halfHourSlotStarts = buildHalfHourSlotStarts(timelineStartMinutes, closeMinutes);
   const scheduledRowsContext = buildScheduledItemRowsContext(
      itinerary,
      halfHourSlotStarts
   );

   if (halfHourSlotStarts.length === 0) {
      section.appendChild(header);
      section.appendChild(makeUnavailableMessage(strings.hoursUnavailable));
      root.appendChild(section);
      return root;
   }

   halfHourSlotStarts.forEach((slotStart) => {
      let pillLabel = null;

      if (slotStart === earlyAdmissionMinutes) {
         pillLabel = strings.earlyAdmissionLabel;
      } else if (slotStart === openMinutes) {
         pillLabel = strings.openLabel;
      } else if (slotStart === lastAdmissionMinutes) {
         pillLabel = strings.lastAdmissionLabel;
      }

      const [timeCell, gridLine] = makeTimelineRow(
         formatMinutesAsClockTime(slotStart),
         pillLabel
      );

      appendScheduledItems(gridLine, scheduledRowsContext.itemsByStart.get(slotStart));
      timeline.appendChild(timeCell);
      timeline.appendChild(gridLine);
   });

   timeline.append(...makeTimelineRow(closeTime, strings.closeLabel));

   section.appendChild(header);
   section.appendChild(timeline);
   root.appendChild(section);

   const unscheduledSection = makeUnscheduledSections(itinerary, scheduledRowsContext);

   if (unscheduledSection) {
      root.appendChild(unscheduledSection);
   }

   return root;
}
