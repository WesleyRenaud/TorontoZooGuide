import { DayPlannerActionFeedback } from '../dayPlannerActionFeedback.js';
import { DayPlannerActionFeedbackBanner } from './dayPlannerActionFeedbackBanner.js';
import { ItineraryPanelDom } from '../itineraryPanelDom.js';
import { ItineraryPanelSectionBuilder } from './itineraryPanelSectionBuilder.js';
import { ScheduleItemButton } from './scheduleItemButton.js';
import { SectionConfigs } from '../sectionConfigs.js';

export class DayPlannerPreviewBuilder {
   static resolveSectionShowEditButton(
      sectionKey,
      {
         showEditButton = true,
         editButtonSectionKeys = null,
      } = {}
   ) {
      if (editButtonSectionKeys) {
         return editButtonSectionKeys.includes(sectionKey);
      }

      return showEditButton;
   }

   static makeItemsListSection(
      itinerary = {},
      sectionTitle = '',
      {
         showEditButton = true,
         editButtonSectionKeys = null,
         onUnscheduleItem = null,
         onScheduleItem = null,
         onRemoveItem = null,
         sectionKeys = SectionConfigs.SCHEDULED_DAY_PLANNER_SECTION_KEYS,
         splitTransportationSequences = false,
      } = {}
   ) {
      const sectionConfigs = SectionConfigs.buildSectionConfigs(itinerary, {
         keys: sectionKeys,
         onUnscheduleItem,
         onScheduleItem,
         onRemoveItem,
         splitTransportationSequences,
      });

      if (sectionConfigs.length === 0) {
         return null;
      }

      const wrapper = ItineraryPanelDom.el('section', 'itinerary-day-items-sections');
      const title = ItineraryPanelDom.el('h4', 'itinerary-day-items-title', sectionTitle);

      wrapper.appendChild(title);
      sectionConfigs.forEach((sectionConfig) => {
         wrapper.appendChild(ItineraryPanelSectionBuilder.makeSection({
            ...sectionConfig,
            showEditButton: DayPlannerPreviewBuilder.resolveSectionShowEditButton(sectionConfig.key, {
               showEditButton,
               editButtonSectionKeys,
            }),
         }));
      });

      return wrapper;
   }

   static appendScheduleActionButtons(
      container,
      {
         onScheduleItemClick = null,
         onRebuildScheduleClick = null,
         onUnscheduleAllItemsClick = null,
         strings = {},
      } = {}
   ) {
      const buttons = [];
      const feedback = DayPlannerActionFeedback.consumePendingDayPlannerActionFeedback();

      if (typeof onScheduleItemClick === 'function') {
         buttons.push(
            ScheduleItemButton.makeScheduleItemButton({
               label: strings.scheduleItemButton,
               onClick: onScheduleItemClick,
            })
         );
      }

      if (typeof onRebuildScheduleClick === 'function') {
         const rebuildScheduleButton = ScheduleItemButton.makeScheduleItemButton({
            label: strings.rebuildScheduleButton,
            variant: 'secondary',
         });

         rebuildScheduleButton.addEventListener('click', () => {
            void ScheduleItemButton.runScheduleItemButtonAction(
               rebuildScheduleButton,
               onRebuildScheduleClick,
               strings.rebuildScheduleButtonBusy
            );
         });

         buttons.push(rebuildScheduleButton);
      }

      if (typeof onUnscheduleAllItemsClick === 'function') {
         const unscheduleAllButton = ScheduleItemButton.makeScheduleItemButton({
            label: strings.unscheduleAllButton,
            variant: 'destructive',
         });

         unscheduleAllButton.addEventListener('click', () => {
            void ScheduleItemButton.runScheduleItemButtonAction(
               unscheduleAllButton,
               onUnscheduleAllItemsClick,
               strings.unscheduleAllButtonBusy
            );
         });

         buttons.push(unscheduleAllButton);
      }

      if (buttons.length > 0) {
         container.appendChild(ScheduleItemButton.makeScheduleActionsBar(buttons));

         const feedbackSlot = DayPlannerActionFeedbackBanner.appendDayPlannerActionFeedbackSlot(container);

         if (feedback) {
            DayPlannerActionFeedbackBanner.appendDayPlannerActionFeedbackBanner(feedbackSlot, feedback);
         }
      }
   }

   static buildTimelinePointPillMarkers({
      earlyAdmissionMinutes,
      openMinutes,
      lastAdmissionMinutes,
      closeMinutes,
      itineraryTimeMarkers = [],
   } = {}) {
      return [
         earlyAdmissionMinutes,
         openMinutes,
         lastAdmissionMinutes,
         closeMinutes,
         ...itineraryTimeMarkers.map((marker) => marker.startMinutes),
      ]
         .filter((startMinutes) => Number.isFinite(startMinutes))
         .map((startMinutes) => ({ startMinutes }));
   }

   static buildTimelineSlotStarts(halfHourSlotStarts, closeMinutes) {
      const slotStarts = [...halfHourSlotStarts];

      if (Number.isFinite(closeMinutes) && !slotStarts.includes(closeMinutes)) {
         slotStarts.push(closeMinutes);
         slotStarts.sort((left, right) => left - right);
      }

      return slotStarts;
   }
}
