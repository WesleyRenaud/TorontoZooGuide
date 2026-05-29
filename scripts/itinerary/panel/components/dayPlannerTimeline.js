import { appendTimelinePill } from './dayPlannerTimelinePills.js';
import { el } from '../dom.js';

export function makeTimelineRow(timeLabel, pillLabel) {
   const gridLine = el('div', 'itinerary-day-grid-line');

   appendTimelinePill(gridLine, pillLabel);

   return [
      el('div', 'itinerary-day-time', timeLabel),
      gridLine,
   ];
}

export function makeUnavailableMessage(message) {
   return el('div', 'itinerary-day-unavailable', message);
}

function makeScheduledItemBlock(itemRow, maximumDuration) {
   const block = el('div', 'itinerary-day-event');
   const slotSpan = maximumDuration / 30;

   block.style.setProperty('--itinerary-event-slot-span', slotSpan);
   itemRow.classList.add('itinerary-day-event-card');
   block.appendChild(itemRow);

   return block;
}

export function appendScheduledItems(gridLine, scheduledItems = []) {
   scheduledItems.forEach((scheduledItem) => {
      gridLine.appendChild(
         makeScheduledItemBlock(scheduledItem.row, scheduledItem.maximumDuration)
      );
   });
}
