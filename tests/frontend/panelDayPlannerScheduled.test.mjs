import assert from 'node:assert/strict';
import { test } from 'node:test';

import { makeDayPlannerPreview } from '../../scripts/itinerary/panel/components/dayPlanner.js';
import { buildSectionConfigs } from '../../scripts/itinerary/panel/sectionConfigs.js';
import {
   buildAnimalRows,
   buildAttractionRows,
} from '../../scripts/itinerary/panel/rows.js';
import {
   EMPTY_ITINERARY,
   TEST_ITINERARY_CONFIG,
   allTextFor,
   boundaryMarkerByLabel,
   boundaryMarkerStripByLabel,
   createNode,
   documentListeners,
   imageSrcFor,
   installPanelRowsTestHooks,
   textFor,
   timelinePillTexts,
   timelineScheduledPillTexts,
} from './helpers/panelRowsTestSetup.mjs';


test.describe('itinerary day planner preview scheduled', () => {
   installPanelRowsTestHooks();

   test('scheduled generic event pill renders on the timeline with remove menu', () => {
      const removeCalls = [];
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            events: [
               {
                  event_type: 'lunch',
                  start_time: '12:00 PM',
                  end_time: '12:40 PM',
               },
            ],
         },
         {},
         {
            scheduleHandlers: {
               onRemoveItineraryItem: (request) => {
                  removeCalls.push(request);
               },
            },
         }
      );
      const lunchPill = [...planner.querySelectorAll('.itinerary-day-scheduled-pill')].find((pill) => (
         allTextFor(pill).includes('Lunch')
      ));
   
      assert.ok(lunchPill);
      assert.ok(lunchPill.classList.contains('itinerary-day-scheduled-pill--with-menu'));
      assert.ok(lunchPill.classList.contains('itinerary-day-scheduled-pill--extended'));
      assert.equal(
         lunchPill.querySelector('.itinerary-day-scheduled-pill-label')?.className.includes('species-link'),
         false
      );
      assert.equal(
         lunchPill.querySelector('.itinerary-day-scheduled-pill-time-range'),
         null
      );
      lunchPill?.querySelector('.itinerary-day-open-pill-menu-item')?.click();
      assert.deepEqual(removeCalls, [{
         itemType: 'lunch',
         key: '',
      }]);
   });
   

   test('scheduled guardians talk renders as timeline event card with remove menu only', () => {
      const unscheduleCalls = [];
      const removeCalls = [];
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            guardiansTalks: [
               {
                  name: 'Amur Tiger',
                  location: 'Eurasia Wilds',
                  start_time: '1:30 PM',
                  end_time: '2:00 PM',
                  maximum_duration: 30,
               },
            ],
         },
         {},
         {
            scheduleHandlers: {
               onUnscheduleItineraryItem: (request) => {
                  unscheduleCalls.push(request);
               },
               onRemoveItineraryItem: (request) => {
                  removeCalls.push(request);
               },
            },
         }
      );
      const tigerEvent = [...planner.querySelectorAll('.itinerary-day-event')].find((event) => (
         allTextFor(event).includes('Amur Tiger')
      ));
      const eventCard = tigerEvent?.querySelector('.itinerary-day-event-card');
      const menuItems = [
         ...(eventCard?.querySelectorAll('.itinerary-day-open-pill-menu-item') ?? []),
      ];

      assert.ok(tigerEvent);
      assert.ok(eventCard?.classList.contains('itinerary-day-event-card--with-menu'));
      assert.match(allTextFor(tigerEvent), /Location: Eurasia Wilds/);
      assert.match(
         imageSrcFor(tigerEvent),
         /images\/details\/guardians-talks\/amur-tiger\.png$/
      );
      assert.equal(tigerEvent.querySelector('.itinerary-day-scheduled-pill--with-menu'), null);
      assert.equal(menuItems.length, 1);
      assert.equal(menuItems[0]?.textContent, 'Remove');

      menuItems[0].click();

      assert.deepEqual(unscheduleCalls, []);
      assert.deepEqual(removeCalls, [{
         itemType: 'guardians_talks',
         key: 'Amur Tiger||1:30 PM||2:00 PM',
      }]);
   });

   test('scheduled wild encounter renders as timeline event card with remove menu only', () => {
      const unscheduleCalls = [];
      const removeCalls = [];
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            wildEncounters: [
               {
                  name: 'Kangaroo',
                  meeting_spot: 'Wild Encounter – Eurasia Meeting Spot',
                  start_time: '3:30 PM',
                  end_time: '4:15 PM',
                  maximum_duration: 45,
               },
            ],
         },
         {},
         {
            scheduleHandlers: {
               onUnscheduleItineraryItem: (request) => {
                  unscheduleCalls.push(request);
               },
               onRemoveItineraryItem: (request) => {
                  removeCalls.push(request);
               },
            },
         }
      );
      const kangarooEvent = [...planner.querySelectorAll('.itinerary-day-event')].find((event) => (
         /Kangaroo\s+Wild Encounter/.test(allTextFor(event))
      ));
      const eventCard = kangarooEvent?.querySelector('.itinerary-day-event-card');
      const menuItems = [
         ...(eventCard?.querySelectorAll('.itinerary-day-open-pill-menu-item') ?? []),
      ];

      assert.ok(kangarooEvent);
      assert.ok(eventCard?.classList.contains('itinerary-day-event-card--with-menu'));
      assert.match(allTextFor(kangarooEvent), /Meeting Spot:/);
      assert.equal(menuItems.length, 1);
      assert.equal(menuItems[0]?.textContent, 'Remove');

      menuItems[0].click();

      assert.deepEqual(unscheduleCalls, []);
      assert.deepEqual(removeCalls, [{
         itemType: 'wild_encounters',
         key: 'Kangaroo||3:30 PM||4:15 PM',
      }]);
   });

   test('scheduled attraction renders as timeline event card with unschedule and remove', () => {
      const unscheduleCalls = [];
      const removeCalls = [];
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            attractions: [
               {
                  name: 'Zoomobile',
                  subtitle: 'Ride the rails',
                  region: 'Front Courtyard',
                  price: 'Free with admission',
                  start_time: '2:30 PM',
                  end_time: '3:00 PM',
               },
            ],
         },
         {},
         {
            scheduleHandlers: {
               onUnscheduleItineraryItem: (request) => {
                  unscheduleCalls.push(request);
               },
               onRemoveItineraryItem: (request) => {
                  removeCalls.push(request);
               },
            },
         }
      );
      const zoomobileEvent = [...planner.querySelectorAll('.itinerary-day-event')].find((event) => (
         allTextFor(event).includes('Zoomobile')
      ));
      const eventCard = zoomobileEvent?.querySelector('.itinerary-day-event-card');
      const menuItems = [
         ...(eventCard?.querySelectorAll('.itinerary-day-open-pill-menu-item') ?? []),
      ];

      assert.ok(zoomobileEvent);
      assert.ok(eventCard?.classList.contains('itinerary-day-event-card--with-menu'));
      assert.match(allTextFor(zoomobileEvent), /Location: Front Courtyard/);
      assert.ok(eventCard?.classList.contains('itinerary-day-scheduled-pill--region-front-courtyard'));
      assert.match(allTextFor(zoomobileEvent), /Price: Free with admission/);
      assert.match(
         imageSrcFor(zoomobileEvent),
         /images\/details\/attractions\/zoomobile\.png$/
      );
      assert.equal(zoomobileEvent.querySelector('.itinerary-day-scheduled-pill'), null);
      assert.equal(menuItems.length, 2);
      assert.equal(menuItems[0]?.textContent, 'Unschedule');
      assert.equal(menuItems[1]?.textContent, 'Remove');

      menuItems[0].click();

      assert.deepEqual(unscheduleCalls, [{
         itemType: 'attractions',
         key: 'Zoomobile',
      }]);
      assert.deepEqual(removeCalls, []);

      menuItems[1].click();

      assert.deepEqual(removeCalls, [{
         itemType: 'attractions',
         key: 'Zoomobile',
      }]);
   });

   test('scheduled transportation renders as timeline event card with stations', () => {
      const unscheduleCalls = [];
      const removeCalls = [];
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            transportations: [
               {
                  name: 'Zoomobile',
                  added_as_attraction: true,
                  start_time: '2:30 PM',
                  end_time: '3:00 PM',
                  legs: [
                     {
                        from_station: 'Main Station',
                        to_station: 'Canadian Domain',
                        start_time: '2:30 PM',
                        end_time: '2:40 PM',
                     },
                     {
                        from_station: 'Canadian Domain',
                        to_station: 'Wildlife Health',
                        start_time: '2:40 PM',
                        end_time: '3:00 PM',
                     },
                  ],
               },
            ],
         },
         {},
         {
            scheduleHandlers: {
               onUnscheduleItineraryItem: (request) => {
                  unscheduleCalls.push(request);
               },
               onRemoveItineraryItem: (request) => {
                  removeCalls.push(request);
               },
            },
         }
      );
      const zoomobileEvent = [...planner.querySelectorAll('.itinerary-day-event')].find((event) => (
         allTextFor(event).includes('Zoomobile')
      ));
      const eventCard = zoomobileEvent?.querySelector('.itinerary-day-event-card');
      const menuItems = [
         ...(eventCard?.querySelectorAll('.itinerary-day-open-pill-menu-item') ?? []),
      ];
      const text = allTextFor(planner);

      assert.ok(zoomobileEvent);
      assert.ok(eventCard?.classList.contains('itinerary-day-event-card--with-menu'));
      assert.match(allTextFor(zoomobileEvent), /Main Station - Wildlife Health/);
      assert.match(text, /Attractions \(1\)/);
      assert.match(
         imageSrcFor(zoomobileEvent),
         /images\/details\/transportations\/zoomobile\.png$/
      );
      assert.equal(menuItems.length, 2);
      assert.equal(menuItems[0]?.textContent, 'Unschedule');
      assert.equal(menuItems[1]?.textContent, 'Remove');

      menuItems[0].click();

      assert.deepEqual(unscheduleCalls, [{
         itemType: 'transportations',
         key: 'Zoomobile',
      }]);

      menuItems[1].click();

      assert.deepEqual(removeCalls, [{
         itemType: 'transportations',
         key: 'Zoomobile',
      }]);
   });


   test('pre-open wild encounter keeps its start slot before zoo open', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-07-06',
            openTime: '09:30',
            lastAdmissionTime: '17:00',
            closeTime: '18:00',
         },
         {
            ...EMPTY_ITINERARY,
            arrivalTime: '8:45 AM',
            wildEncounters: [
               {
                  name: 'Mornings in Malaysia',
                  meeting_spot: 'Wild Encounter - Zoo Front Entrance Gates Meeting Spot',
                  start_time: '8:45 AM',
                  end_time: '9:45 AM',
                  maximum_duration: 60,
               },
            ],
         }
      );
      const timelineText = allTextFor(
         planner.querySelector('.itinerary-day-timeline')
      );
      const malaysiaEvent = [...planner.querySelectorAll('.itinerary-day-event')].find(
         (event) => /Mornings in Malaysia\s+Wild Encounter/.test(allTextFor(event))
      );

      assert.match(timelineText, /8:45 AM/);
      assert.ok(malaysiaEvent);
      assert.match(allTextFor(malaysiaEvent), /8:45 AM/);
      assert.match(allTextFor(malaysiaEvent), /9:45 AM/);
   });
   

   test('scheduled animal pill menu offers unschedule and remove', () => {
      const unscheduleCalls = [];
      const removeCalls = [];
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            animals: [
               {
                  species: 'African Lion',
                  exhibit: 'Africa Savanna',
                  start_time: '1:15 PM',
                  end_time: '1:45 PM',
               },
            ],
         },
         {},
         {
            scheduleHandlers: {
               onUnscheduleItineraryItem: (request) => {
                  unscheduleCalls.push(request);
               },
               onRemoveItineraryItem: (request) => {
                  removeCalls.push(request);
               },
            },
         }
      );
      const lionPill = [...planner.querySelectorAll('.itinerary-day-scheduled-pill')].find((pill) => (
         allTextFor(pill).includes('African Lion')
      ));
      const menuItems = [
         ...(lionPill?.querySelectorAll('.itinerary-day-open-pill-menu-item') ?? []),
      ];
   
      assert.equal(menuItems.length, 2);
      assert.deepEqual(
         menuItems.map((button) => button.textContent),
         ['Unschedule', 'Remove']
      );
   
      menuItems[0].click();
      menuItems[1].click();
   
      assert.deepEqual(unscheduleCalls, [{
         itemType: 'animals',
         key: 'African Lion||Africa Savanna',
      }]);
      assert.deepEqual(removeCalls, [{
         itemType: 'animals',
         key: 'African Lion||Africa Savanna',
      }]);
   });
   

   test('scheduled list rows show unschedule and remove buttons for animals and attractions only', () => {
      const unscheduleCalls = [];
      const removeCalls = [];
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            guardiansTalks: [
               {
                  name: 'Amur Tiger',
                  location: 'Eurasia Wilds',
                  start_time: '1:30 PM',
                  end_time: '2:00 PM',
                  maximum_duration: 30,
               },
            ],
            animals: [
               {
                  species: 'African Lion',
                  exhibit: 'Africa Savanna',
                  start_time: '1:00 PM',
                  end_time: '1:30 PM',
               },
            ],
            attractions: [
               {
                  name: 'Zoomobile',
                  subtitle: 'Ride the rails',
                  start_time: '2:30 PM',
                  end_time: '3:00 PM',
               },
            ],
         },
         {},
         {
            scheduleHandlers: {
               onUnscheduleItineraryItem: (request) => {
                  unscheduleCalls.push(request);
               },
               onRemoveItineraryItem: (request) => {
                  removeCalls.push(request);
               },
            },
         }
      );
      const dayItemsSections = [...planner.querySelectorAll('.itinerary-day-items-sections')];
      const scheduledList = dayItemsSections.find((section) => (
         section.querySelector('.itinerary-day-items-title')?.textContent?.includes('Scheduled Items')
      ));
      const unscheduledList = dayItemsSections.find((section) => (
         section.querySelector('.itinerary-day-items-title')?.textContent?.includes('Unscheduled Items')
      ));
      const scheduledButtons = scheduledList?.querySelectorAll('.itin-panel-item-action-btn') ?? [];
      const tigerRow = [...(scheduledList?.querySelectorAll('.itin-panel-item') ?? [])].find((row) => (
         allTextFor(row).includes('Amur Tiger')
      ));
      const tigerButtons = tigerRow?.querySelectorAll('.itin-panel-item-action-btn') ?? [];
   
      assert.equal(scheduledButtons.length, 5);
      assert.equal(
         scheduledButtons.every((button) => (
            button.textContent === 'Unschedule' || button.textContent === 'Remove'
         )),
         true
      );
      assert.equal(tigerButtons.length, 1);
      assert.equal(tigerButtons[0]?.textContent, 'Remove');
      assert.equal(unscheduledList?.querySelectorAll('.itin-panel-item-action-btn').length ?? 0, 0);
   
      [...scheduledButtons]
         .filter((button) => button.textContent === 'Unschedule')
         .forEach((button) => {
            button.click();
         });
   
      assert.deepEqual(unscheduleCalls, [
         {
            itemType: 'animals',
            key: 'African Lion||Africa Savanna',
         },
         {
            itemType: 'attractions',
            key: 'Zoomobile',
         },
      ]);
      assert.equal(removeCalls.length, 0);
   });
   

   test('day planner stacks zoo hours and arrival markers at the same time', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            arrivalTime: '09:30',
            itineraryConfig: TEST_ITINERARY_CONFIG,
            ...EMPTY_ITINERARY,
         }
      );
      const openTimeCell = [...planner.querySelectorAll('.itinerary-day-time')].find((cell) => (
         cell.querySelector('.itinerary-day-time-label')?.textContent === '9:30 AM'
      ));
      const arrivalStrip = boundaryMarkerStripByLabel(planner, 'Arrival');
      const markers = arrivalStrip?.querySelectorAll('.itinerary-day-boundary-marker') ?? [];
   
      assert.match(allTextFor(openTimeCell), /Zoo Opens/);
      assert.ok(arrivalStrip);
      assert.equal(markers.length, 1);
      assert.equal(arrivalStrip?.querySelector('.itinerary-day-boundary-marker')?.attributes?.['aria-label'], 'Arrival');
   });
   

   test('day planner renders scheduled guardians talks and wild encounters', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            guardiansTalks: [
               {
                  name: 'Amur Tiger',
                  location: 'Eurasia Wilds',
                  start_time: '1:30 PM',
                  end_time: '2:00 PM',
                  maximum_duration: 30,
               },
            ],
            wildEncounters: [
               {
                  name: 'African Rainforest',
                  meeting_spot: 'Wild Encounter - Africa Meeting Spot',
                  start_time: '2:00 PM',
                  end_time: '2:45 PM',
                  maximum_duration: 45,
               },
            ],
            animals: [
               {
                  species: 'African Lion',
                  exhibit: 'Africa Savanna',
                  start_time: '1:00 PM',
                  end_time: '1:30 PM',
               },
               {
                  species: 'Giant Panda',
                  exhibit: 'Eurasia Wilds',
               },
            ],
            attractions: [
               {
                  name: 'Conservation Carousel',
                  subtitle: 'Carousels are timeless and fun for all ages!',
               },
               {
                  name: 'Zoomobile',
                  subtitle: 'Ride the rails',
                  start_time: '2:30 PM',
                  end_time: '3:00 PM',
               },
            ],
         }
      );
      const text = allTextFor(planner);
   
      assert.match(text, /Amur Tiger\s+Meet The Guardians Talk/);
      assert.match(text, /Location: Eurasia Wilds/);
      assert.match(text, /African Rainforest\s+Wild Encounter/);
      assert.match(text, /Meeting Spot: Wild Encounter - Africa Meeting Spot/);
      assert.match(text, /Scheduled Items/);
      assert.match(text, /Meet The Guardians \(1\)/);
      assert.match(text, /Wild Encounters \(1\)/);
      assert.match(text, /Animals \(1\)/);
      assert.match(text, /African Lion/);
      assert.match(text, /Attractions \(1\)/);
      assert.match(text, /Zoomobile/);
      assert.match(text, /Unscheduled Items/);
      assert.match(text, /Animals \(1\)/);
      assert.match(text, /Giant Panda/);
      assert.match(text, /Attractions \(1\)/);
      assert.match(text, /Conservation Carousel/);
      assert.doesNotMatch(text, /Unscheduled Items[\s\S]*Meet The Guardians/);
      assert.doesNotMatch(text, /Unscheduled Items[\s\S]*Wild Encounters/);
      assert.ok(text.indexOf('Scheduled Items') < text.indexOf('Unscheduled Items'));
   
      const timelineEventTexts = timelineScheduledPillTexts(planner);
   
      assert.equal(timelineEventTexts.length, 4);
      assert.ok(timelineEventTexts.some((eventText) => eventText.includes('African Lion')));
      assert.ok(timelineEventTexts.some((eventText) => /Amur Tiger\s+Meet The Guardians Talk/.test(eventText)));
      assert.ok(timelineEventTexts.some((eventText) => /African Rainforest\s+Wild Encounter/.test(eventText)));
      assert.ok(timelineEventTexts.some((eventText) => eventText.includes('Zoomobile')));
   
      const dayItemsSections = [...planner.querySelectorAll('.itinerary-day-items-sections')];
      const scheduledList = dayItemsSections.find((section) => (
         section.querySelector('.itinerary-day-items-title')?.textContent?.includes('Scheduled Items')
      ));
      const unscheduledList = dayItemsSections.find((section) => (
         section.querySelector('.itinerary-day-items-title')?.textContent?.includes('Unscheduled Items')
      ));
   
      assert.equal(
         scheduledList?.querySelectorAll('.itin-panel-section-edit-btn').length,
         2
      );
      assert.ok(
         (unscheduledList?.querySelectorAll('.itin-panel-section-edit-btn').length ?? 0) > 0
      );
   });
   

   test('day planner positions off-slot scheduled items between half-hour lines', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            animals: [
               {
                  species: 'African Lion',
                  exhibit: 'Africa Savanna',
                  start_time: '1:15 PM',
                  end_time: '1:45 PM',
               },
            ],
         }
      );
      const lionPill = [...planner.querySelectorAll('.itinerary-day-scheduled-pill')].find((pill) => (
         allTextFor(pill).includes('African Lion')
      ));
      const lionStrip = lionPill?.parentElement;
   
      assert.ok(lionPill);
      assert.equal(lionStrip?.className, 'itinerary-day-pill-strip');
      assert.equal(lionStrip?.attributes?.['data-offset-fraction'], '0.5');
      assert.equal(lionPill.attributes?.['data-duration-fraction'], '1');
   });
   

   test('day planner renders scheduled duration as a larger pill', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            arrivalTime: '11:35',
            departureTime: '17:15',
            itineraryConfig: TEST_ITINERARY_CONFIG,
            ...EMPTY_ITINERARY,
            animals: [
               {
                  species: 'Polar Bear',
                  exhibit: 'Tundra Trek',
                  start_time: '11:35 AM',
                  end_time: '11:45 AM',
               },
            ],
         }
      );
      const polarPill = [...planner.querySelectorAll('.itinerary-day-scheduled-pill')].find((pill) => (
         allTextFor(pill).includes('Polar Bear')
      ));
      const polarStrip = polarPill?.parentElement;
   
      assert.ok(polarPill);
      assert.equal(polarStrip?.className, 'itinerary-day-pill-strip');
      assert.equal(polarStrip?.attributes?.['data-scheduled-column'], 'true');
      assert.equal(polarPill.attributes?.['data-duration-fraction'], String(10 / 30));
      assert.equal(
         Boolean(boundaryMarkerByLabel(planner, 'Arrival')),
         true
      );
      assert.ok(boundaryMarkerByLabel(planner, 'Departure'));
      assert.equal(
         [...planner.querySelectorAll('.itinerary-day-boundary-marker')].some((marker) => (
            marker.attributes?.['aria-label'] === 'Polar Bear'
         )),
         false
      );
   });
   

   test('day planner keeps short scheduled visits readable', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            animals: [
               {
                  species: 'Ring-Tailed Lemur',
                  exhibit: 'Australasia',
                  start_time: '12:00',
                  end_time: '12:08',
               },
            ],
         },
         {},
         {
            scheduleHandlers: {
               onUnscheduleItineraryItem: () => {},
            },
         }
      );
      const lemurPill = [...planner.querySelectorAll('.itinerary-day-scheduled-pill')].find((pill) => (
         allTextFor(pill).includes('Ring-Tailed Lemur')
      ));
   
      assert.ok(lemurPill?.classList.contains('itinerary-day-scheduled-pill--with-menu'));
      assert.equal(lemurPill.attributes?.['data-duration-fraction'], String(8 / 30));
      assert.match(allTextFor(lemurPill), /Ring-Tailed Lemur/);
   });
   

   test('day planner merges overlapping scheduled pills into carousel groups', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            animals: [
               {
                  species: 'Polar Bear',
                  exhibit: 'Tundra Trek',
                  start_time: '4:30 PM',
                  end_time: '4:32 PM',
               },
               {
                  species: 'African Lion',
                  exhibit: 'Africa Savanna',
                  start_time: '4:32 PM',
                  end_time: '4:34 PM',
               },
            ],
         }
      );
      const groupedPill = [...planner.querySelectorAll('.itinerary-day-scheduled-pill--grouped')].find((pill) => (
         allTextFor(pill).includes('Polar Bear')
         || allTextFor(pill).includes('African Lion')
      ));
   
      assert.ok(groupedPill);
      assert.match(allTextFor(groupedPill), /\+ 1/);
   });
   

   test('day planner keeps scheduled pills within the timeline grid width', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            animals: [
               {
                  species: 'Solomon Island Leaf Frog',
                  exhibit: 'Americas',
                  start_time: '11:00 AM',
                  end_time: '11:30 AM',
               },
            ],
         }
      );
      const pill = planner.querySelector('.itinerary-day-scheduled-pill');
      const strip = pill?.parentElement;
   
      assert.ok(pill);
      assert.equal(strip?.attributes?.['data-scheduled-column'], 'true');
      assert.equal(strip?.attributes?.['data-dynamic-horizontal-offset'], undefined);
   });

});
