import { ItineraryPanelHelper } from '../itineraryPanelHelper.js';
import { ItineraryPillView } from './itineraryPillView.js';
import { OpenTimelineView } from './openTimelineView.js';
import { ScheduledPillPresenter } from '../scheduledPillPresenter.js';
import { RegionColors } from '../../../shared/regionColors.js';
import { TimelineLayoutConstants } from '../../../shared/timelineLayoutConstants.js';
import { Strings } from '../../../strings.js';

export class ScheduledTimelinePillBuilder {
   static applyScheduledPillRegionColors(pill, item = null) {
      RegionColors.applyRegionColorsToElement(
         pill,
         RegionColors.resolveRegionColorSlugForScheduledItem(item)
      );
   }

   static applyScheduledPillDuration(
      pill,
      durationMinutes,
      slotSpanMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES
   ) {
      const slotSpan = Number.isFinite(slotSpanMinutes) && slotSpanMinutes > 0
         ? slotSpanMinutes
         : TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
      const durationFraction = durationMinutes / slotSpan;

      pill.style.setProperty(
         '--itinerary-scheduled-pill-duration-fraction',
         String(durationFraction)
      );
      pill.setAttribute('data-duration-fraction', String(durationFraction));
   }

   static makeScheduledPillArrowButton(label, direction) {
      const button = document.createElement('button');

      button.type = 'button';
      button.className = `itinerary-day-scheduled-pill-toggle itinerary-day-scheduled-pill-toggle--${direction}`;
      button.setAttribute('aria-label', label);
      button.textContent = direction === 'previous' ? '‹' : '›';

      return button;
   }

   static replaceGroupedScheduledPillLabel(
      labelMount,
      {
         label = '',
         item = null,
         suffixCount = 0,
         onLabelClick = null,
      } = {}
   ) {
      const labelNode = OpenTimelineView.createPillLabelNode(
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
            ItineraryPanelHelper.el(
               'span',
               'itinerary-day-scheduled-pill-count',
               Strings.itinerary.dayPlanner.scheduledPillMoreCount(suffixCount)
            )
         );
      }
   }

   static resolveWrappedGroupIndex(index, groupSize) {
      if (groupSize <= 0) {
         return 0;
      }

      return ((index % groupSize) + groupSize) % groupSize;
   }

   static buildGroupedScheduledPill(
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
      const pill = ItineraryPanelHelper.el('div', 'itinerary-day-scheduled-pill itinerary-day-scheduled-pill--with-menu itinerary-day-scheduled-pill--grouped');
      const header = ItineraryPanelHelper.el('div', 'itinerary-day-scheduled-pill-header itinerary-day-scheduled-pill-header--grouped');
      const previousButton = ScheduledTimelinePillBuilder.makeScheduledPillArrowButton(
         Strings.itinerary.dayPlanner.previousScheduledItem,
         'previous'
      );
      const nextButton = ScheduledTimelinePillBuilder.makeScheduledPillArrowButton(
         Strings.itinerary.dayPlanner.nextScheduledItem,
         'next'
      );
      const labelMount = ItineraryPanelHelper.el('div', 'itinerary-day-scheduled-pill-label-mount');
      const menuNodes = hasMenuItems
         ? ItineraryPillView.buildPillMenuNodes(menuAriaLabel, groupItems[0]?.menuItems ?? [])
         : null;

      if (ScheduledPillPresenter.isExtendedScheduledPill(durationMinutes)) {
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

         ScheduledTimelinePillBuilder.replaceGroupedScheduledPillLabel(
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
         activeIndex = ScheduledTimelinePillBuilder.resolveWrappedGroupIndex(activeIndex - 1, groupSize);
         syncActiveItem();
      });
      nextButton.addEventListener('click', (event) => {
         event.stopPropagation();
         activeIndex = ScheduledTimelinePillBuilder.resolveWrappedGroupIndex(activeIndex + 1, groupSize);
         syncActiveItem();
      });

      const trailingControls = ItineraryPanelHelper.el('div', 'itinerary-day-scheduled-pill-trailing-controls');

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
         ItineraryPillView.bindPillMenu(pill, {
            menuButton: menuNodes.menuButton,
            menuPanel: menuNodes.menuPanel,
            getMenuItems: () => getActiveItem()?.menuItems ?? [],
            menuOpenClass: 'itinerary-day-scheduled-pill--menu-open',
         });
      }

      return pill;
   }

   static buildScheduledPillWithMenu(
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
      const pill = ItineraryPanelHelper.el('div', 'itinerary-day-scheduled-pill itinerary-day-scheduled-pill--with-menu');
      const header = ItineraryPanelHelper.el('div', 'itinerary-day-scheduled-pill-header');
      const labelNode = OpenTimelineView.createPillLabelNode(
         label,
         'itinerary-day-scheduled-pill-label',
         onLabelClick,
         item
      );
      const { menu, menuButton, menuPanel } = ItineraryPillView.buildPillMenuNodes(
         menuAriaLabel,
         menuItems
      );

      if (ScheduledPillPresenter.isExtendedScheduledPill(durationMinutes)) {
         pill.classList.add('itinerary-day-scheduled-pill--extended');
      }

      header.appendChild(labelNode);
      header.appendChild(menu);
      pill.appendChild(header);
      ItineraryPillView.bindPillMenu(pill, {
         menuButton,
         menuPanel,
         menuItems,
         menuOpenClass: 'itinerary-day-scheduled-pill--menu-open',
      });

      return pill;
   }

   static buildScheduledPillWithoutMenu(
      label,
      durationMinutes,
      {
         startTime,
         endTime,
         onLabelClick = null,
         item = null,
      }
   ) {
      if (!ScheduledPillPresenter.isExtendedScheduledPill(durationMinutes)) {
         const pill = ItineraryPanelHelper.el('span', 'itinerary-day-scheduled-pill');
         pill.appendChild(
            OpenTimelineView.createPillLabelNode(
               label,
               'itinerary-day-scheduled-pill-label',
               onLabelClick,
               item
            )
         );
         return pill;
      }

      const pill = ItineraryPanelHelper.el('div', 'itinerary-day-scheduled-pill itinerary-day-scheduled-pill--extended');
      const header = ItineraryPanelHelper.el('div', 'itinerary-day-scheduled-pill-header');

      header.appendChild(
         OpenTimelineView.createPillLabelNode(
            label,
            'itinerary-day-scheduled-pill-label',
            onLabelClick,
            item
         )
      );
      pill.appendChild(header);

      return pill;
   }
}
