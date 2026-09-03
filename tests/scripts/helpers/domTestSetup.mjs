import { afterEach, beforeEach } from 'node:test';

import {
   installDocument,
   installTestWindow,
   teardownDocument,
} from './domMock.mjs';

export function installDomTestHooks({
   before: beforeHook,
   after: afterHook,
} = {}) {
   beforeEach(() => {
      installTestWindow();
      installDocument();
      beforeHook?.();
   });

   afterEach(() => {
      afterHook?.();
      teardownDocument();
      delete globalThis.window;
   });
}
