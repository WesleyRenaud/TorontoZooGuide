import { Dom } from '../dom.js';
import { ItineraryPillMenu } from './itineraryPillMenu.js';
import { OpenTimelinePill } from './openTimelinePill.js';
import { ScheduledPillPresentation } from '../scheduledPillPresentation.js';
import { Constants } from '../../../shared/constants.js';
import { RegionColors } from '../../../shared/regionColors.js';
import { Strings } from '../../../strings.js';

function applyScheduledPillRegionColors(pill, item = null) {
   RegionColors.applyRegionColorsToElement(
      pill,
      RegionColors.resolveRegionColorSlugForScheduledItem(item)
   );
}

function applyScheduledPillDuration(
   pill,
   durationMinutes,
   slotSpanMinutes = Constants.TIMELINE_SLOT_MINUTES
) {
   const slotSpan = Number.isFinite(slotSpanMinutes) && slotSpanMinutes > 0
      ? slotSpanMinutes
      : Constants.TIMELINE_SLOT_MINUTES;
   const durationFraction = durationMinutes / slotSpan;

   pill.style.setProperty(
      '--itinerary-scheduled-pill-duration-fraction',
      String(durationFraction)
   );
   pill.setAttribute('data-duration-fraction', String(durationFraction));
}

function makeScheduledPillArrowButton(label, direction) {
   const button = document.createElement('button');

   button.type = 'button';
   button.className = `itinerary-day-scheduled-pill-toggle itinerary-day-scheduled-pill-toggle--${direction}`;
   button.setAttribute('aria-label', label);
   button.textContent = direction === 'previous' ? '‹' : '›';

   return button;
}

function replaceGroupedScheduledPillLabel(
   labelMount,
   {
      label = '',
      item = null,
      suffixCount = 0,
      onLabelClick = null,
   } = {}
) {
   const labelNode = OpenTimelinePill.createPillLabelNode(
      label,
      'itinerary-day-scheduled-pill-label itinerary-day-scheduled-pill-label-name',
      onLabelClick,
      item
   );

   while (labelMount.children.length > 0) {
      labelMount.removeChild(labelMount.children[0]);
   }

   labelMount.textContent = '';
   labelMount.appendChild(labelNode);

   if (suffixCount > 0) {
      labelMount.appendChild(
         Dom.el(
            'span',
            'itinerary-day-scheduled-pill-count',
            Strings.itinerary.dayPlanner.scheduledPillMoreCount(suffixCount)
         )
      );
   }
}

function resolveWrappedGroupIndex(index, groupSize) {
   if (groupSize <= 0) {
      return 0;
   }

   return ((index % groupSize) + groupSize) % groupSize;
}

function buildGroupedScheduledPill(
   groupItems,
   durationMinutes,
   {
      menuAriaLabel,
   }
) {
   let activeIndex = 0;
   const groupSize = groupItems.length;
   const suffixCount = groupSize - 1;
   const longestLabelLength = Math.max(
      ...groupItems.map((groupItem) => (groupItem.label ?? '').length)
   );
   const hasMenuItems = groupItems.some((groupItem) => (
      (groupItem.menuItems ?? []).length > 0
   ));
   const pill = Dom.el('div', 'itinerary-day-scheduled-pill itinerary-day-scheduled-pill--with-menu itinerary-day-scheduled-pill--grouped');
   const header = Dom.el('div', 'itinerary-day-scheduled-pill-header itinerary-day-scheduled-pill-header--grouped');
   const previousButton = makeScheduledPillArrowButton(
      Strings.itinerary.dayPlanner.previousScheduledItem,
      'previous'
   );
   const nextButton = makeScheduledPillArrowButton(
      Strings.itinerary.dayPlanner.nextScheduledItem,
      'next'
   );
   const labelMount = Dom.el('div', 'itinerary-day-scheduled-pill-label-mount');
   const menuNodes = hasMenuItems
      ? ItineraryPillMenu.buildPillMenuNodes(menuAriaLabel, groupItems[0]?.menuItems ?? [])
      : null;

   if (ScheduledPillPresentation.isExtendedScheduledPill(durationMinutes)) {
      pill.classList.add('itinerary-day-scheduled-pill--extended');
   }

   pill.style.setProperty(
      '--itinerary-scheduled-pill-group-label-chars',
      String(longestLabelLength)
   );

   function getActiveItem() {
      return groupItems[activeIndex] ?? groupItems[0];
   }

   function syncActiveItem() {
      const activeItem = getActiveItem();

      replaceGroupedScheduledPillLabel(
         labelMount,
         {
            label: activeItem.label,
            item: activeItem.item,
            suffixCount,
            onLabelClick: activeItem.onLabelClick,
         }
      );
      pill.setAttribute('data-active-group-index', String(activeIndex));
   }

   previousButton.addEventListener('click', (event) => {
      event.stopPropagation();
      activeIndex = resolveWrappedGroupIndex(activeIndex - 1, groupSize);
      syncActiveItem();
   });
   nextButton.addEventListener('click', (event) => {
      event.stopPropagation();
      activeIndex = resolveWrappedGroupIndex(activeIndex + 1, groupSize);
      syncActiveItem();
   });

   const trailingControls = Dom.el('div', 'itinerary-day-scheduled-pill-trailing-controls');

   header.appendChild(previousButton);
   header.appendChild(labelMount);
   trailingControls.appendChild(nextButton);

   if (menuNodes) {
      trailingControls.appendChild(menuNodes.menu);
   }

   header.appendChild(trailingControls);

   pill.appendChild(header);
   pill.setAttribute('data-group-size', String(groupSize));
   syncActiveItem();

   if (menuNodes) {
      ItineraryPillMenu.bindPillMenu(pill, {
         menuButton: menuNodes.menuButton,
         menuPanel: menuNodes.menuPanel,
         getMenuItems: () => getActiveItem()?.menuItems ?? [],
         menuOpenClass: 'itinerary-day-scheduled-pill--menu-open',
      });
   }

   return pill;
}

function buildScheduledPillWithMenu(
   label,
   durationMinutes,
   {
      startTime,
      endTime,
      menuItems = [],
      menuAriaLabel,
      onLabelClick = null,
      item = null,
   }
) {
   const pill = Dom.el('div', 'itinerary-day-scheduled-pill itinerary-day-scheduled-pill--with-menu');
   const header = Dom.el('div', 'itinerary-day-scheduled-pill-header');
   const labelNode = OpenTimelinePill.createPillLabelNode(
      label,
      'itinerary-day-scheduled-pill-label',
      onLabelClick,
      item
   );
   const { menu, menuButton, menuPanel } = ItineraryPillMenu.buildPillMenuNodes(
      menuAriaLabel,
      menuItems
   );

   if (ScheduledPillPresentation.isExtendedScheduledPill(durationMinutes)) {
      pill.classList.add('itinerary-day-scheduled-pill--extended');
   }

   header.appendChild(labelNode);
   header.appendChild(menu);
   pill.appendChild(header);
   ItineraryPillMenu.bindPillMenu(pill, {
      menuButton,
      menuPanel,
      menuItems,
      menuOpenClass: 'itinerary-day-scheduled-pill--menu-open',
   });

   return pill;
}

function buildScheduledPillWithoutMenu(
   label,
   durationMinutes,
   {
      startTime,
      endTime,
      onLabelClick = null,
      item = null,
   }
) {
   if (!ScheduledPillPresentation.isExtendedScheduledPill(durationMinutes)) {
      const pill = Dom.el('span', 'itinerary-day-scheduled-pill');
      pill.appendChild(
         OpenTimelinePill.createPillLabelNode(
            label,
            'itinerary-day-scheduled-pill-label',
            onLabelClick,
            item
         )
      );
      return pill;
   }

   const pill = Dom.el('div', 'itinerary-day-scheduled-pill itinerary-day-scheduled-pill--extended');
   const header = Dom.el('div', 'itinerary-day-scheduled-pill-header');

   header.appendChild(
      OpenTimelinePill.createPillLabelNode(
         label,
         'itinerary-day-scheduled-pill-label',
         onLabelClick,
         item
      )
   );
   pill.appendChild(header);

   return pill;
}

export class ScheduledTimelinePill {
   static makeScheduledPill(
      label,
      durationMinutes,
      {
      startTime,
      endTime,
      groupItems = [],
      menuItems = [],
      menuAriaLabel = '',
      onLabelClick = null,
      item = null,
      slotSpanMinutes = Constants.TIMELINE_SLOT_MINUTES,
      displayDurationMinutes = durationMinutes,
      } = {}
   ) {
      if (!label || !Number.isFinite(durationMinutes) || durationMinutes <= 0) {
         return null;
      }

      let pill;

      if (groupItems.length > 1) {
         pill = buildGroupedScheduledPill(groupItems, durationMinutes, {
            menuAriaLabel,
         });
      }
      else if (menuItems.length > 0) {
         pill = buildScheduledPillWithMenu(label, durationMinutes, {
            startTime,
            endTime,
            menuItems,
            menuAriaLabel,
            onLabelClick,
            item,
         });
      }
      else {
         pill = buildScheduledPillWithoutMenu(label, durationMinutes, {
            startTime,
            endTime,
            onLabelClick,
            item,
         });
      }

      applyScheduledPillDuration(pill, displayDurationMinutes, slotSpanMinutes);
      applyScheduledPillRegionColors(pill, item);

      return pill;
   }
}
