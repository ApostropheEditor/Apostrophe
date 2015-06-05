
import * as dom from './../../../../dom.js';
import {WalkontableOverlay} from './_base.js';

/**
 * A overlay that renders ALL available rows & columns positioned on top of the original Walkontable instance and all other overlays.
 * Used for debugging purposes to see if the other overlays (that render only part of the rows & columns) are positioned correctly
 *
 * @class WalkontableDebugOverlay
 */
class WalkontableDebugOverlay extends WalkontableOverlay {
  /**
   * @param {Walkontable} wotInstance
   */
  constructor(wotInstance) {
    super(wotInstance);

    this.clone = this.makeClone(WalkontableOverlay.CLONE_DEBUG);
    this.clone.wtTable.holder.style.opacity = 0.4;
    this.clone.wtTable.holder.style.textShadow = '0 0 2px #ff0000';

    dom.addClass(this.clone.wtTable.holder.parentNode, 'wtDebugVisible');
  }
}

export {WalkontableDebugOverlay};

window.WalkontableDebugOverlay = WalkontableDebugOverlay;
