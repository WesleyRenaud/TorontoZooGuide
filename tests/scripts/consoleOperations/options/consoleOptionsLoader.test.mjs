import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../scripts/api/consoleOperationsClient.js';
import { ConsoleOptionsLoader } from '../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleOptionsLoaderHelper } from '../../../../scripts/consoleOperations/options/consoleOptionsLoaderHelper.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';


async function _withCachedLoader(run) {
   const original = ConsoleOptionsLoaderHelper.loadCachedOptions;
   const cached = ['ok'];
   let captured;

   ConsoleOptionsLoaderHelper.loadCachedOptions = async (args) => {
      captured = args;
      return cached;
   };

   try {
      await run({ cached, getCaptured: () => captured });
   } finally {
      ConsoleOptionsLoaderHelper.loadCachedOptions = original;
   }
}


test('Test_LoadSpecies_TestDelegation_ExpectCachedLoaderArgs', async () => {
   await _withCachedLoader(async ({ cached, getCaptured }) => {
      const options = await ConsoleOptionsLoader.loadSpecies();

      assert.equal(options, cached);
      assert.equal(getCaptured().cacheKey, 'species');
      assert.equal(getCaptured().fetchOptions, ConsoleOperationsClient.getSpeciesOptions);
      assert.equal(getCaptured().resultKey, 'species');
   });
});


test('Test_LoadExhibits_TestDelegation_ExpectCachedLoaderArgs', async () => {
   await _withCachedLoader(async ({ cached, getCaptured }) => {
      const options = await ConsoleOptionsLoader.loadExhibits();

      assert.equal(options, cached);
      assert.equal(getCaptured().cacheKey, 'exhibits');
      assert.equal(getCaptured().fetchOptions, ConsoleOperationsClient.getExhibitOptions);
      assert.equal(getCaptured().resultKey, 'exhibits');
   });
});


test('Test_LoadRestaurants_TestDelegation_ExpectCachedLoaderArgs', async () => {
   await _withCachedLoader(async ({ cached, getCaptured }) => {
      const options = await ConsoleOptionsLoader.loadRestaurants();

      assert.equal(options, cached);
      assert.equal(getCaptured().cacheKey, 'restaurants');
      assert.equal(getCaptured().fetchOptions, ConsoleOperationsClient.getRestaurantNameOptions);
      assert.equal(getCaptured().resultKey, 'restaurants');
   });
});


test('Test_LoadRestrooms_TestDelegation_ExpectCachedLoaderArgs', async () => {
   await _withCachedLoader(async ({ cached, getCaptured }) => {
      const options = await ConsoleOptionsLoader.loadRestrooms();

      assert.equal(options, cached);
      assert.equal(getCaptured().cacheKey, 'restrooms');
      assert.equal(getCaptured().fetchOptions, ConsoleOperationsClient.getRestroomNameOptions);
      assert.equal(getCaptured().resultKey, 'restrooms');
   });
});


test('Test_LoadGiftShops_TestDelegation_ExpectCachedLoaderArgs', async () => {
   await _withCachedLoader(async ({ cached, getCaptured }) => {
      const options = await ConsoleOptionsLoader.loadGiftShops();

      assert.equal(options, cached);
      assert.equal(getCaptured().cacheKey, 'giftShops');
      assert.equal(getCaptured().fetchOptions, ConsoleOperationsClient.getGiftShopNameOptions);
      assert.equal(getCaptured().resultKey, 'gift_shops');
   });
});


test('Test_LoadAttractions_TestDelegation_ExpectCachedLoaderArgs', async () => {
   await _withCachedLoader(async ({ cached, getCaptured }) => {
      const options = await ConsoleOptionsLoader.loadAttractions();

      assert.equal(options, cached);
      assert.equal(getCaptured().cacheKey, 'attractions');
      assert.equal(getCaptured().fetchOptions, ConsoleOperationsClient.getAttractionNameOptions);
      assert.equal(getCaptured().resultKey, ScheduleItemKind.ATTRACTION.itemType);
   });
});


test('Test_LoadTransportationStations_TestDelegation_ExpectCachedLoaderArgs', async () => {
   await _withCachedLoader(async ({ cached, getCaptured }) => {
      const options = await ConsoleOptionsLoader.loadTransportationStations();

      assert.equal(options, cached);
      assert.equal(getCaptured().cacheKey, 'transportationStations');
      assert.equal(getCaptured().fetchOptions, ConsoleOperationsClient.getTransportationStationNameOptions);
      assert.equal(getCaptured().resultKey, 'transportation_stations');
   });
});


test('Test_LoadGuardiansTalks_TestDelegation_ExpectCachedLoaderArgs', async () => {
   await _withCachedLoader(async ({ cached, getCaptured }) => {
      const options = await ConsoleOptionsLoader.loadGuardiansTalks();

      assert.equal(options, cached);
      assert.equal(getCaptured().cacheKey, 'guardiansTalks');
      assert.equal(getCaptured().fetchOptions, ConsoleOperationsClient.getGuardiansTalkNameOptions);
      assert.equal(getCaptured().resultKey, ScheduleItemKind.GUARDIANS_TALK.itemType);
   });
});


test('Test_LoadWildEncounters_TestDelegation_ExpectCachedLoaderArgs', async () => {
   await _withCachedLoader(async ({ cached, getCaptured }) => {
      const options = await ConsoleOptionsLoader.loadWildEncounters();

      assert.equal(options, cached);
      assert.equal(getCaptured().cacheKey, 'wildEncounters');
      assert.equal(getCaptured().fetchOptions, ConsoleOperationsClient.getWildEncounterNameOptions);
      assert.equal(getCaptured().resultKey, ScheduleItemKind.WILD_ENCOUNTER.itemType);
   });
});


test('Test_LoadClosedExhibits_TestClientResult_ExpectExhibits', async () => {
   const exhibits = ['Canadian Domain', 'Kids Zoo'];
   const originalGet = ConsoleOperationsClient.getClosedExhibitOptions;
   ConsoleOperationsClient.getClosedExhibitOptions = async () => ({ exhibits });

   try {
      const loaded = await ConsoleOptionsLoader.loadClosedExhibits();

      assert.deepEqual(loaded, exhibits);
   } finally {
      ConsoleOperationsClient.getClosedExhibitOptions = originalGet;
   }
});


test('Test_LoadClosedRestrooms_TestClientResult_ExpectRestrooms', async () => {
   const restrooms = ['Entrance Restroom', 'Africa Restaurant Restroom'];
   const originalGet = ConsoleOperationsClient.getClosedRestroomOptions;
   ConsoleOperationsClient.getClosedRestroomOptions = async () => ({ restrooms });

   try {
      const loaded = await ConsoleOptionsLoader.loadClosedRestrooms();

      assert.deepEqual(loaded, restrooms);
   } finally {
      ConsoleOperationsClient.getClosedRestroomOptions = originalGet;
   }
});


test('Test_LoadAlertRestrooms_TestClientResult_ExpectRestrooms', async () => {
   const restrooms = ['Entrance Restroom', 'Splash Island Restroom'];
   const originalGet = ConsoleOperationsClient.getRestroomAlertOptions;
   ConsoleOperationsClient.getRestroomAlertOptions = async () => ({ restrooms });

   try {
      const loaded = await ConsoleOptionsLoader.loadAlertRestrooms();

      assert.deepEqual(loaded, restrooms);
   } finally {
      ConsoleOperationsClient.getRestroomAlertOptions = originalGet;
   }
});


test('Test_LoadClosedTransportationStations_TestClientResult_ExpectStations', async () => {
   const stations = ['Africa Zoomobile Station', 'Main Zoomobile Station'];
   const originalGet = ConsoleOperationsClient.getClosedTransportationStationOptions;
   ConsoleOperationsClient.getClosedTransportationStationOptions = async () => ({
      transportation_stations: stations,
   });

   try {
      const loaded = await ConsoleOptionsLoader.loadClosedTransportationStations();

      assert.deepEqual(loaded, stations);
   } finally {
      ConsoleOperationsClient.getClosedTransportationStationOptions = originalGet;
   }
});


test('Test_LoadOffDisplayExhibits_TestNoSpecies_ExpectExhibits', async () => {
   const exhibits = ['Africa Savanna', 'Eurasia Wilds'];
   const originalGet = ConsoleOperationsClient.getOffDisplayExhibitOptions;
   const payloads = [];
   ConsoleOperationsClient.getOffDisplayExhibitOptions = async (payload) => {
      payloads.push(payload);
      return { exhibits };
   };

   try {
      const loaded = await ConsoleOptionsLoader.loadOffDisplayExhibits();

      assert.deepEqual(loaded, exhibits);
      assert.deepEqual(payloads, [{}]);
   } finally {
      ConsoleOperationsClient.getOffDisplayExhibitOptions = originalGet;
   }
});


test('Test_LoadOffDisplayExhibits_TestSpecies_ExpectExhibits', async () => {
   const species = 'African Lion';
   const exhibits = ['Africa Savanna', 'Eurasia Wilds'];
   const originalGet = ConsoleOperationsClient.getOffDisplayExhibitOptions;
   const payloads = [];
   ConsoleOperationsClient.getOffDisplayExhibitOptions = async (payload) => {
      payloads.push(payload);
      return { exhibits };
   };

   try {
      const loaded = await ConsoleOptionsLoader.loadOffDisplayExhibits(species);

      assert.deepEqual(loaded, exhibits);
      assert.deepEqual(payloads, [{ species }]);
   } finally {
      ConsoleOperationsClient.getOffDisplayExhibitOptions = originalGet;
   }
});


test('Test_LoadOffDisplayViewingScopes_TestClientResult_ExpectScopes', async () => {
   const species = 'Sumatran Orangutan';
   const exhibit = 'Indo-Malaya Pavilion';
   const viewingScopes = [
      { enclosureName: 'Indoor', label: 'Indoor' },
      { enclosureName: 'Outdoor', label: 'Outdoor' },
   ];
   const originalGet = ConsoleOperationsClient.getOffDisplayViewingScopeOptions;
   const payloads = [];
   ConsoleOperationsClient.getOffDisplayViewingScopeOptions = async (payload) => {
      payloads.push(payload);
      return { viewingScopes };
   };

   try {
      const loaded = await ConsoleOptionsLoader.loadOffDisplayViewingScopes({ species, exhibit });

      assert.deepEqual(loaded, viewingScopes);
      assert.deepEqual(payloads, [{ species, exhibit }]);
   } finally {
      ConsoleOperationsClient.getOffDisplayViewingScopeOptions = originalGet;
   }
});


test('Test_LoadVisibilityScheduleExhibits_TestNoSpecies_ExpectExhibits', async () => {
   const exhibits = ['Africa Savanna', 'Eurasia Wilds'];
   const originalGet = ConsoleOperationsClient.getAnimalVisibilityScheduleExhibitOptions;
   const payloads = [];
   ConsoleOperationsClient.getAnimalVisibilityScheduleExhibitOptions = async (payload) => {
      payloads.push(payload);
      return { exhibits };
   };

   try {
      const loaded = await ConsoleOptionsLoader.loadVisibilityScheduleExhibits();

      assert.deepEqual(loaded, exhibits);
      assert.deepEqual(payloads, [{}]);
   } finally {
      ConsoleOperationsClient.getAnimalVisibilityScheduleExhibitOptions = originalGet;
   }
});


test('Test_LoadVisibilityScheduleExhibits_TestSpecies_ExpectExhibits', async () => {
   const species = 'African Lion';
   const exhibits = ['Africa Savanna', 'Eurasia Wilds'];
   const originalGet = ConsoleOperationsClient.getAnimalVisibilityScheduleExhibitOptions;
   const payloads = [];
   ConsoleOperationsClient.getAnimalVisibilityScheduleExhibitOptions = async (payload) => {
      payloads.push(payload);
      return { exhibits };
   };

   try {
      const loaded = await ConsoleOptionsLoader.loadVisibilityScheduleExhibits(species);

      assert.deepEqual(loaded, exhibits);
      assert.deepEqual(payloads, [{ species }]);
   } finally {
      ConsoleOperationsClient.getAnimalVisibilityScheduleExhibitOptions = originalGet;
   }
});


test('Test_LoadScheduledWildEncounters_TestClientResult_ExpectEncounters', async () => {
   const encounters = ['Giraffe Encounter', 'Kangaroo Encounter'];
   const originalGet = ConsoleOperationsClient.getWildEncounterScheduleOptions;
   ConsoleOperationsClient.getWildEncounterScheduleOptions = async () => ({
      wild_encounters: encounters,
   });

   try {
      const loaded = await ConsoleOptionsLoader.loadScheduledWildEncounters();

      assert.deepEqual(loaded, encounters);
   } finally {
      ConsoleOperationsClient.getWildEncounterScheduleOptions = originalGet;
   }
});


test('Test_LoadViewingAlertExhibits_TestNoSpecies_ExpectExhibits', async () => {
   const exhibits = ['Africa Savanna', 'Eurasia Wilds'];
   const originalGet = ConsoleOperationsClient.getAnimalViewingAlertExhibitOptions;
   const payloads = [];
   ConsoleOperationsClient.getAnimalViewingAlertExhibitOptions = async (payload) => {
      payloads.push(payload);
      return { exhibits };
   };

   try {
      const loaded = await ConsoleOptionsLoader.loadViewingAlertExhibits();

      assert.deepEqual(loaded, exhibits);
      assert.deepEqual(payloads, [{}]);
   } finally {
      ConsoleOperationsClient.getAnimalViewingAlertExhibitOptions = originalGet;
   }
});


test('Test_LoadViewingAlertExhibits_TestSpecies_ExpectExhibits', async () => {
   const species = 'African Lion';
   const exhibits = ['Africa Savanna', 'Eurasia Wilds'];
   const originalGet = ConsoleOperationsClient.getAnimalViewingAlertExhibitOptions;
   const payloads = [];
   ConsoleOperationsClient.getAnimalViewingAlertExhibitOptions = async (payload) => {
      payloads.push(payload);
      return { exhibits };
   };

   try {
      const loaded = await ConsoleOptionsLoader.loadViewingAlertExhibits(species);

      assert.deepEqual(loaded, exhibits);
      assert.deepEqual(payloads, [{ species }]);
   } finally {
      ConsoleOperationsClient.getAnimalViewingAlertExhibitOptions = originalGet;
   }
});


test('Test_LoadExhibitsForSpecies_TestClientResult_ExpectExhibits', async () => {
   const species = 'African Lion';
   const exhibits = ['Africa Savanna'];
   const originalGet = ConsoleOperationsClient.getExhibitsForSpecies;
   ConsoleOperationsClient.getExhibitsForSpecies = async (payload) => {
      assert.deepEqual(payload, { species });
      return { exhibits };
   };

   try {
      const loaded = await ConsoleOptionsLoader.loadExhibitsForSpecies(species);

      assert.deepEqual(loaded, exhibits);
   } finally {
      ConsoleOperationsClient.getExhibitsForSpecies = originalGet;
   }
});
