/*!
 * Handsontable 0.15.0-beta6
 * Handsontable is a JavaScript library for editable tables with basic copy-paste compatibility with Excel and Google Docs
 *
 * Copyright (c) 2012-2014 Marcin Warpechowski
 * Copyright 2015 Handsoncode sp. z o.o. <hello@handsontable.com>
 * Licensed under the MIT license.
 * http://handsontable.com/
 *
 * Date: Fri Jun 05 2015 09:18:04 GMT+0200 (CEST)
 */
/*jslint white: true, browser: true, plusplus: true, indent: 4, maxerr: 50 */

window.Handsontable = {
  version: '0.15.0-beta6',
  buildDate: 'Fri Jun 05 2015 09:18:04 GMT+0200 (CEST)'
};
require=(function outer (modules, cache, entry) {
  // Save the require from previous bundle to this closure if any
  var previousRequire = typeof require == "function" && require;
  var globalNS = JSON.parse('{"jsonpatch":"jsonpatch","zeroclipboard":"ZeroClipboard","copyPaste":"copyPaste","SheetClip":"SheetClip","moment":"moment","numeral":"numeral","autoResize":"autoResize","pikaday":"Pikaday"}') || {};

  function newRequire(name, jumped){
    if(!cache[name]) {

      if(!modules[name]) {
        // if we cannot find the the module within our internal map or
        // cache jump to the current global require ie. the last bundle
        // that was added to the page.
        var currentRequire = typeof require == "function" && require;
        if (!jumped && currentRequire) return currentRequire(name, true);

        // If there are other bundles on this page the require from the
        // previous one is saved to 'previousRequire'. Repeat this as
        // many times as there are bundles until the module is found or
        // we exhaust the require chain.
        if (previousRequire) return previousRequire(name, true);

        // Try find module from global scope
        if (globalNS[name] && typeof window[globalNS[name]] !== 'undefined') {
          return window[globalNS[name]];
        }

        var err = new Error('Cannot find module \'' + name + '\'');
        err.code = 'MODULE_NOT_FOUND';
        throw err;
      }
      var m = cache[name] = {exports:{}};
      modules[name][0].call(m.exports, function(x){
        var id = modules[name][1][x];
        return newRequire(id ? id : x);
      },m,m.exports,outer,modules,cache,entry);
    }
    return cache[name].exports;
  }
  for(var i=0;i<entry.length;i++) newRequire(entry[i]);

  // Override the current require with this new one
  return newRequire;
})
({1:[function(require,module,exports){
"use strict";
if (window.jQuery) {
  (function(window, $, Handsontable) {
    $.fn.handsontable = function(action) {
      var i,
          ilen,
          args,
          output,
          userSettings,
          $this = this.first(),
          instance = $this.data('handsontable');
      if (typeof action !== 'string') {
        userSettings = action || {};
        if (instance) {
          instance.updateSettings(userSettings);
        } else {
          instance = new Handsontable.Core($this[0], userSettings);
          $this.data('handsontable', instance);
          instance.init();
        }
        return $this;
      } else {
        args = [];
        if (arguments.length > 1) {
          for (i = 1, ilen = arguments.length; i < ilen; i++) {
            args.push(arguments[i]);
          }
        }
        if (instance) {
          if (typeof instance[action] !== 'undefined') {
            output = instance[action].apply(instance, args);
            if (action === 'destroy') {
              $this.removeData();
            }
          } else {
            throw new Error('Handsontable do not provide action: ' + action);
          }
        }
        return output;
      }
    };
  })(window, jQuery, Handsontable);
}


//# 
},{}],2:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableBorder: {get: function() {
      return WalkontableBorder;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47__46__46__47_eventManager_46_js__,
    $__cell_47_coords_46_js__;
var dom = ($___46__46__47__46__46__47__46__46__47_dom_46_js__ = require("./../../../dom.js"), $___46__46__47__46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47__46__46__47_dom_46_js__});
var eventManagerObject = ($___46__46__47__46__46__47__46__46__47_eventManager_46_js__ = require("./../../../eventManager.js"), $___46__46__47__46__46__47__46__46__47_eventManager_46_js__ && $___46__46__47__46__46__47__46__46__47_eventManager_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47_eventManager_46_js__ || {default: $___46__46__47__46__46__47__46__46__47_eventManager_46_js__}).eventManager;
var WalkontableCellCoords = ($__cell_47_coords_46_js__ = require("./cell/coords.js"), $__cell_47_coords_46_js__ && $__cell_47_coords_46_js__.__esModule && $__cell_47_coords_46_js__ || {default: $__cell_47_coords_46_js__}).WalkontableCellCoords;
function WalkontableBorder(instance, settings) {
  var style;
  var createMultipleSelectorHandles = function() {
    this.selectionHandles = {
      topLeft: document.createElement('DIV'),
      topLeftHitArea: document.createElement('DIV'),
      bottomRight: document.createElement('DIV'),
      bottomRightHitArea: document.createElement('DIV')
    };
    var width = 10,
        hitAreaWidth = 40;
    this.selectionHandles.topLeft.className = 'topLeftSelectionHandle';
    this.selectionHandles.topLeftHitArea.className = 'topLeftSelectionHandle-HitArea';
    this.selectionHandles.bottomRight.className = 'bottomRightSelectionHandle';
    this.selectionHandles.bottomRightHitArea.className = 'bottomRightSelectionHandle-HitArea';
    this.selectionHandles.styles = {
      topLeft: this.selectionHandles.topLeft.style,
      topLeftHitArea: this.selectionHandles.topLeftHitArea.style,
      bottomRight: this.selectionHandles.bottomRight.style,
      bottomRightHitArea: this.selectionHandles.bottomRightHitArea.style
    };
    var hitAreaStyle = {
      'position': 'absolute',
      'height': hitAreaWidth + 'px',
      'width': hitAreaWidth + 'px',
      'border-radius': parseInt(hitAreaWidth / 1.5, 10) + 'px'
    };
    for (var prop in hitAreaStyle) {
      if (hitAreaStyle.hasOwnProperty(prop)) {
        this.selectionHandles.styles.bottomRightHitArea[prop] = hitAreaStyle[prop];
        this.selectionHandles.styles.topLeftHitArea[prop] = hitAreaStyle[prop];
      }
    }
    var handleStyle = {
      'position': 'absolute',
      'height': width + 'px',
      'width': width + 'px',
      'border-radius': parseInt(width / 1.5, 10) + 'px',
      'background': '#F5F5FF',
      'border': '1px solid #4285c8'
    };
    for (var prop in handleStyle) {
      if (handleStyle.hasOwnProperty(prop)) {
        this.selectionHandles.styles.bottomRight[prop] = handleStyle[prop];
        this.selectionHandles.styles.topLeft[prop] = handleStyle[prop];
      }
    }
    this.main.appendChild(this.selectionHandles.topLeft);
    this.main.appendChild(this.selectionHandles.bottomRight);
    this.main.appendChild(this.selectionHandles.topLeftHitArea);
    this.main.appendChild(this.selectionHandles.bottomRightHitArea);
  };
  if (!settings) {
    return;
  }
  var eventManager = eventManagerObject(instance);
  this.instance = instance;
  this.settings = settings;
  this.main = document.createElement("div");
  style = this.main.style;
  style.position = 'absolute';
  style.top = 0;
  style.left = 0;
  var borderDivs = ['top', 'left', 'bottom', 'right', 'corner'];
  for (var i = 0; i < 5; i++) {
    var position = borderDivs[i];
    var DIV = document.createElement('DIV');
    DIV.className = 'wtBorder ' + (this.settings.className || '');
    if (this.settings[position] && this.settings[position].hide) {
      DIV.className += " hidden";
    }
    style = DIV.style;
    style.backgroundColor = (this.settings[position] && this.settings[position].color) ? this.settings[position].color : settings.border.color;
    style.height = (this.settings[position] && this.settings[position].width) ? this.settings[position].width + 'px' : settings.border.width + 'px';
    style.width = (this.settings[position] && this.settings[position].width) ? this.settings[position].width + 'px' : settings.border.width + 'px';
    this.main.appendChild(DIV);
  }
  this.top = this.main.childNodes[0];
  this.left = this.main.childNodes[1];
  this.bottom = this.main.childNodes[2];
  this.right = this.main.childNodes[3];
  this.topStyle = this.top.style;
  this.leftStyle = this.left.style;
  this.bottomStyle = this.bottom.style;
  this.rightStyle = this.right.style;
  this.cornerDefaultStyle = {
    width: '5px',
    height: '5px',
    borderWidth: '2px',
    borderStyle: 'solid',
    borderColor: '#FFF'
  };
  this.corner = this.main.childNodes[4];
  this.corner.className += ' corner';
  this.cornerStyle = this.corner.style;
  this.cornerStyle.width = this.cornerDefaultStyle.width;
  this.cornerStyle.height = this.cornerDefaultStyle.height;
  this.cornerStyle.border = [this.cornerDefaultStyle.borderWidth, this.cornerDefaultStyle.borderStyle, this.cornerDefaultStyle.borderColor].join(' ');
  if (Handsontable.mobileBrowser) {
    createMultipleSelectorHandles.call(this);
  }
  this.disappear();
  if (!instance.wtTable.bordersHolder) {
    instance.wtTable.bordersHolder = document.createElement('div');
    instance.wtTable.bordersHolder.className = 'htBorders';
    instance.wtTable.spreader.appendChild(instance.wtTable.bordersHolder);
  }
  instance.wtTable.bordersHolder.insertBefore(this.main, instance.wtTable.bordersHolder.firstChild);
  var down = false;
  eventManager.addEventListener(document.body, 'mousedown', function() {
    down = true;
  });
  eventManager.addEventListener(document.body, 'mouseup', function() {
    down = false;
  });
  for (var c = 0,
      len = this.main.childNodes.length; c < len; c++) {
    eventManager.addEventListener(this.main.childNodes[c], 'mouseenter', function(event) {
      if (!down || !instance.getSetting('hideBorderOnMouseDownOver')) {
        return;
      }
      event.preventDefault();
      event.stopImmediatePropagation();
      var bounds = this.getBoundingClientRect();
      this.style.display = 'none';
      var isOutside = function(event) {
        if (event.clientY < Math.floor(bounds.top)) {
          return true;
        }
        if (event.clientY > Math.ceil(bounds.top + bounds.height)) {
          return true;
        }
        if (event.clientX < Math.floor(bounds.left)) {
          return true;
        }
        if (event.clientX > Math.ceil(bounds.left + bounds.width)) {
          return true;
        }
      };
      var handler = function(event) {
        if (isOutside(event)) {
          eventManager.removeEventListener(document.body, 'mousemove', handler);
          this.style.display = 'block';
        }
      };
      eventManager.addEventListener(document.body, 'mousemove', handler);
    });
  }
}
WalkontableBorder.prototype.appear = function(corners) {
  if (this.disabled) {
    return;
  }
  var instance = this.instance;
  var isMultiple,
      fromTD,
      toTD,
      fromOffset,
      toOffset,
      containerOffset,
      top,
      minTop,
      left,
      minLeft,
      height,
      width,
      fromRow,
      fromColumn,
      toRow,
      toColumn,
      i,
      ilen,
      s;
  var isPartRange = function() {
    if (this.instance.selections.area.cellRange) {
      if (toRow != this.instance.selections.area.cellRange.to.row || toColumn != this.instance.selections.area.cellRange.to.col) {
        return true;
      }
    }
    return false;
  };
  var updateMultipleSelectionHandlesPosition = function(top, left, width, height) {
    var handleWidth = parseInt(this.selectionHandles.styles.topLeft.width, 10),
        hitAreaWidth = parseInt(this.selectionHandles.styles.topLeftHitArea.width, 10);
    this.selectionHandles.styles.topLeft.top = parseInt(top - handleWidth, 10) + "px";
    this.selectionHandles.styles.topLeft.left = parseInt(left - handleWidth, 10) + "px";
    this.selectionHandles.styles.topLeftHitArea.top = parseInt(top - (hitAreaWidth / 4) * 3, 10) + "px";
    this.selectionHandles.styles.topLeftHitArea.left = parseInt(left - (hitAreaWidth / 4) * 3, 10) + "px";
    this.selectionHandles.styles.bottomRight.top = parseInt(top + height, 10) + "px";
    this.selectionHandles.styles.bottomRight.left = parseInt(left + width, 10) + "px";
    this.selectionHandles.styles.bottomRightHitArea.top = parseInt(top + height - hitAreaWidth / 4, 10) + "px";
    this.selectionHandles.styles.bottomRightHitArea.left = parseInt(left + width - hitAreaWidth / 4, 10) + "px";
    if (this.settings.border.multipleSelectionHandlesVisible && this.settings.border.multipleSelectionHandlesVisible()) {
      this.selectionHandles.styles.topLeft.display = "block";
      this.selectionHandles.styles.topLeftHitArea.display = "block";
      if (!isPartRange.call(this)) {
        this.selectionHandles.styles.bottomRight.display = "block";
        this.selectionHandles.styles.bottomRightHitArea.display = "block";
      } else {
        this.selectionHandles.styles.bottomRight.display = "none";
        this.selectionHandles.styles.bottomRightHitArea.display = "none";
      }
    } else {
      this.selectionHandles.styles.topLeft.display = "none";
      this.selectionHandles.styles.bottomRight.display = "none";
      this.selectionHandles.styles.topLeftHitArea.display = "none";
      this.selectionHandles.styles.bottomRightHitArea.display = "none";
    }
    if (fromRow == this.instance.wtSettings.getSetting('fixedRowsTop') || fromColumn == this.instance.wtSettings.getSetting('fixedColumnsLeft')) {
      this.selectionHandles.styles.topLeft.zIndex = "9999";
      this.selectionHandles.styles.topLeftHitArea.zIndex = "9999";
    } else {
      this.selectionHandles.styles.topLeft.zIndex = "";
      this.selectionHandles.styles.topLeftHitArea.zIndex = "";
    }
  };
  if (instance.cloneOverlay instanceof WalkontableTopOverlay || instance.cloneOverlay instanceof WalkontableCornerOverlay) {
    ilen = instance.getSetting('fixedRowsTop');
  } else {
    ilen = instance.wtTable.getRenderedRowsCount();
  }
  for (i = 0; i < ilen; i++) {
    s = instance.wtTable.rowFilter.renderedToSource(i);
    if (s >= corners[0] && s <= corners[2]) {
      fromRow = s;
      break;
    }
  }
  for (i = ilen - 1; i >= 0; i--) {
    s = instance.wtTable.rowFilter.renderedToSource(i);
    if (s >= corners[0] && s <= corners[2]) {
      toRow = s;
      break;
    }
  }
  ilen = instance.wtTable.getRenderedColumnsCount();
  for (i = 0; i < ilen; i++) {
    s = instance.wtTable.columnFilter.renderedToSource(i);
    if (s >= corners[1] && s <= corners[3]) {
      fromColumn = s;
      break;
    }
  }
  for (i = ilen - 1; i >= 0; i--) {
    s = instance.wtTable.columnFilter.renderedToSource(i);
    if (s >= corners[1] && s <= corners[3]) {
      toColumn = s;
      break;
    }
  }
  if (fromRow !== void 0 && fromColumn !== void 0) {
    isMultiple = (fromRow !== toRow || fromColumn !== toColumn);
    fromTD = instance.wtTable.getCell(new WalkontableCellCoords(fromRow, fromColumn));
    toTD = isMultiple ? instance.wtTable.getCell(new WalkontableCellCoords(toRow, toColumn)) : fromTD;
    fromOffset = dom.offset(fromTD);
    toOffset = isMultiple ? dom.offset(toTD) : fromOffset;
    containerOffset = dom.offset(instance.wtTable.TABLE);
    minTop = fromOffset.top;
    height = toOffset.top + dom.outerHeight(toTD) - minTop;
    minLeft = fromOffset.left;
    width = toOffset.left + dom.outerWidth(toTD) - minLeft;
    top = minTop - containerOffset.top - 1;
    left = minLeft - containerOffset.left - 1;
    var style = dom.getComputedStyle(fromTD);
    if (parseInt(style.borderTopWidth, 10) > 0) {
      top += 1;
      height = height > 0 ? height - 1 : 0;
    }
    if (parseInt(style.borderLeftWidth, 10) > 0) {
      left += 1;
      width = width > 0 ? width - 1 : 0;
    }
  } else {
    this.disappear();
    return;
  }
  this.topStyle.top = top + 'px';
  this.topStyle.left = left + 'px';
  this.topStyle.width = width + 'px';
  this.topStyle.display = 'block';
  this.leftStyle.top = top + 'px';
  this.leftStyle.left = left + 'px';
  this.leftStyle.height = height + 'px';
  this.leftStyle.display = 'block';
  var delta = Math.floor(this.settings.border.width / 2);
  this.bottomStyle.top = top + height - delta + 'px';
  this.bottomStyle.left = left + 'px';
  this.bottomStyle.width = width + 'px';
  this.bottomStyle.display = 'block';
  this.rightStyle.top = top + 'px';
  this.rightStyle.left = left + width - delta + 'px';
  this.rightStyle.height = height + 1 + 'px';
  this.rightStyle.display = 'block';
  if (Handsontable.mobileBrowser || (!this.hasSetting(this.settings.border.cornerVisible) || isPartRange.call(this))) {
    this.cornerStyle.display = 'none';
  } else {
    this.cornerStyle.top = top + height - 4 + 'px';
    this.cornerStyle.left = left + width - 4 + 'px';
    this.cornerStyle.borderRightWidth = this.cornerDefaultStyle.borderWidth;
    this.cornerStyle.width = this.cornerDefaultStyle.width;
    this.cornerStyle.display = 'block';
    if (toColumn === this.instance.getSetting('totalColumns') - 1) {
      var trimmingContainer = dom.getTrimmingContainer(instance.wtTable.TABLE),
          cornerOverlappingContainer = toTD.offsetLeft + dom.outerWidth(toTD) >= dom.innerWidth(trimmingContainer);
      if (cornerOverlappingContainer) {
        this.cornerStyle.left = Math.floor(left + width - 3 - parseInt(this.cornerDefaultStyle.width) / 2) + "px";
        this.cornerStyle.borderRightWidth = 0;
      }
    }
  }
  if (Handsontable.mobileBrowser) {
    updateMultipleSelectionHandlesPosition.call(this, top, left, width, height);
  }
};
WalkontableBorder.prototype.disappear = function() {
  this.topStyle.display = 'none';
  this.leftStyle.display = 'none';
  this.bottomStyle.display = 'none';
  this.rightStyle.display = 'none';
  this.cornerStyle.display = 'none';
  if (Handsontable.mobileBrowser) {
    this.selectionHandles.styles.topLeft.display = 'none';
    this.selectionHandles.styles.bottomRight.display = 'none';
  }
};
WalkontableBorder.prototype.hasSetting = function(setting) {
  if (typeof setting === 'function') {
    return setting();
  }
  return !!setting;
};
;
window.WalkontableBorder = WalkontableBorder;


//# 
},{"./../../../dom.js":27,"./../../../eventManager.js":41,"./cell/coords.js":5}],3:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableViewportColumnsCalculator: {get: function() {
      return WalkontableViewportColumnsCalculator;
    }},
  __esModule: {value: true}
});
var privatePool = new WeakMap();
var WalkontableViewportColumnsCalculator = function WalkontableViewportColumnsCalculator(viewportWidth, scrollOffset, totalColumns, columnWidthFn, overrideFn, onlyFullyVisible, stretchH) {
  privatePool.set(this, {
    viewportWidth: viewportWidth,
    scrollOffset: scrollOffset,
    totalColumns: totalColumns,
    columnWidthFn: columnWidthFn,
    overrideFn: overrideFn,
    onlyFullyVisible: onlyFullyVisible
  });
  this.count = 0;
  this.startColumn = null;
  this.endColumn = null;
  this.startPosition = null;
  this.stretchAllRatio = 0;
  this.stretchLastWidth = 0;
  this.stretch = stretchH;
  this.totalTargetWidth = 0;
  this.needVerifyLastColumnWidth = true;
  this.stretchAllColumnsWidth = [];
  this.calculate();
};
var $WalkontableViewportColumnsCalculator = WalkontableViewportColumnsCalculator;
($traceurRuntime.createClass)(WalkontableViewportColumnsCalculator, {
  calculate: function() {
    var sum = 0;
    var needReverse = true;
    var startPositions = [];
    var columnWidth;
    var priv = privatePool.get(this);
    var onlyFullyVisible = priv.onlyFullyVisible;
    var overrideFn = priv.overrideFn;
    var scrollOffset = priv.scrollOffset;
    var totalColumns = priv.totalColumns;
    var viewportWidth = priv.viewportWidth;
    for (var i = 0; i < totalColumns; i++) {
      columnWidth = this._getColumnWidth(i);
      if (sum <= scrollOffset && !onlyFullyVisible) {
        this.startColumn = i;
      }
      if (sum >= scrollOffset && sum + columnWidth <= scrollOffset + viewportWidth) {
        if (this.startColumn == null) {
          this.startColumn = i;
        }
        this.endColumn = i;
      }
      startPositions.push(sum);
      sum += columnWidth;
      if (!onlyFullyVisible) {
        this.endColumn = i;
      }
      if (sum >= scrollOffset + viewportWidth) {
        needReverse = false;
        break;
      }
    }
    if (this.endColumn === totalColumns - 1 && needReverse) {
      this.startColumn = this.endColumn;
      while (this.startColumn > 0) {
        var viewportSum = startPositions[this.endColumn] + columnWidth - startPositions[this.startColumn - 1];
        if (viewportSum <= viewportWidth || !onlyFullyVisible) {
          this.startColumn--;
        }
        if (viewportSum > viewportWidth) {
          break;
        }
      }
    }
    if (this.startColumn !== null && overrideFn) {
      overrideFn(this);
    }
    this.startPosition = startPositions[this.startColumn];
    if (this.startPosition == void 0) {
      this.startPosition = null;
    }
    if (this.startColumn !== null) {
      this.count = this.endColumn - this.startColumn + 1;
    }
  },
  refreshStretching: function(totalWidth) {
    if (this.stretch === 'none') {
      return;
    }
    var sumAll = 0;
    var columnWidth;
    var remainingSize;
    var priv = privatePool.get(this);
    var totalColumns = priv.totalColumns;
    for (var i = 0; i < totalColumns; i++) {
      columnWidth = this._getColumnWidth(i);
      sumAll += columnWidth;
    }
    this.totalTargetWidth = totalWidth;
    remainingSize = sumAll - totalWidth;
    if (this.stretch === 'all' && remainingSize < 0) {
      this.stretchAllRatio = totalWidth / sumAll;
      this.stretchAllColumnsWidth = [];
      this.needVerifyLastColumnWidth = true;
    } else if (this.stretch === 'last' && totalWidth !== Infinity) {
      this.stretchLastWidth = -remainingSize + this._getColumnWidth(totalColumns - 1);
    }
  },
  getStretchedColumnWidth: function(column, baseWidth) {
    var result = null;
    if (this.stretch === 'all' && this.stretchAllRatio !== 0) {
      result = this._getStretchedAllColumnWidth(column, baseWidth);
    } else if (this.stretch === 'last' && this.stretchLastWidth !== 0) {
      result = this._getStretchedLastColumnWidth(column);
    }
    return result;
  },
  _getStretchedAllColumnWidth: function(column, baseWidth) {
    var sumRatioWidth = 0;
    var priv = privatePool.get(this);
    var totalColumns = priv.totalColumns;
    if (!this.stretchAllColumnsWidth[column]) {
      this.stretchAllColumnsWidth[column] = Math.round(baseWidth * this.stretchAllRatio);
    }
    if (this.stretchAllColumnsWidth.length === totalColumns && this.needVerifyLastColumnWidth) {
      this.needVerifyLastColumnWidth = false;
      for (var i = 0; i < this.stretchAllColumnsWidth.length; i++) {
        sumRatioWidth += this.stretchAllColumnsWidth[i];
      }
      if (sumRatioWidth !== this.totalTargetWidth) {
        this.stretchAllColumnsWidth[this.stretchAllColumnsWidth.length - 1] += this.totalTargetWidth - sumRatioWidth;
      }
    }
    return this.stretchAllColumnsWidth[column];
  },
  _getStretchedLastColumnWidth: function(column) {
    var priv = privatePool.get(this);
    var totalColumns = priv.totalColumns;
    if (column === totalColumns - 1) {
      return this.stretchLastWidth;
    }
    return null;
  },
  _getColumnWidth: function(column) {
    var width = privatePool.get(this).columnWidthFn(column);
    if (width === undefined) {
      width = $WalkontableViewportColumnsCalculator.DEFAULT_WIDTH;
    }
    return width;
  }
}, {get DEFAULT_WIDTH() {
    return 50;
  }});
;
window.WalkontableViewportColumnsCalculator = WalkontableViewportColumnsCalculator;


//# 
},{}],4:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableViewportRowsCalculator: {get: function() {
      return WalkontableViewportRowsCalculator;
    }},
  __esModule: {value: true}
});
var privatePool = new WeakMap();
var WalkontableViewportRowsCalculator = function WalkontableViewportRowsCalculator(viewportHeight, scrollOffset, totalRows, rowHeightFn, overrideFn, onlyFullyVisible) {
  privatePool.set(this, {
    viewportHeight: viewportHeight,
    scrollOffset: scrollOffset,
    totalRows: totalRows,
    rowHeightFn: rowHeightFn,
    overrideFn: overrideFn,
    onlyFullyVisible: onlyFullyVisible
  });
  this.count = 0;
  this.startRow = null;
  this.endRow = null;
  this.startPosition = null;
  this.calculate();
};
var $WalkontableViewportRowsCalculator = WalkontableViewportRowsCalculator;
($traceurRuntime.createClass)(WalkontableViewportRowsCalculator, {calculate: function() {
    var sum = 0;
    var needReverse = true;
    var startPositions = [];
    var priv = privatePool.get(this);
    var onlyFullyVisible = priv.onlyFullyVisible;
    var overrideFn = priv.overrideFn;
    var rowHeightFn = priv.rowHeightFn;
    var scrollOffset = priv.scrollOffset;
    var totalRows = priv.totalRows;
    var viewportHeight = priv.viewportHeight;
    for (var i = 0; i < totalRows; i++) {
      var rowHeight = rowHeightFn(i);
      if (rowHeight === undefined) {
        rowHeight = $WalkontableViewportRowsCalculator.DEFAULT_HEIGHT;
      }
      if (sum <= scrollOffset && !onlyFullyVisible) {
        this.startRow = i;
      }
      if (sum >= scrollOffset && sum + rowHeight <= scrollOffset + viewportHeight) {
        if (this.startRow === null) {
          this.startRow = i;
        }
        this.endRow = i;
      }
      startPositions.push(sum);
      sum += rowHeight;
      if (!onlyFullyVisible) {
        this.endRow = i;
      }
      if (sum >= scrollOffset + viewportHeight) {
        needReverse = false;
        break;
      }
    }
    if (this.endRow === totalRows - 1 && needReverse) {
      this.startRow = this.endRow;
      while (this.startRow > 0) {
        var viewportSum = startPositions[this.endRow] + rowHeight - startPositions[this.startRow - 1];
        if (viewportSum <= viewportHeight || !onlyFullyVisible) {
          this.startRow--;
        }
        if (viewportSum >= viewportHeight) {
          break;
        }
      }
    }
    if (this.startRow !== null && overrideFn) {
      overrideFn(this);
    }
    this.startPosition = startPositions[this.startRow];
    if (this.startPosition == void 0) {
      this.startPosition = null;
    }
    if (this.startRow !== null) {
      this.count = this.endRow - this.startRow + 1;
    }
  }}, {get DEFAULT_HEIGHT() {
    return 23;
  }});
;
window.WalkontableViewportRowsCalculator = WalkontableViewportRowsCalculator;


//# 
},{}],5:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableCellCoords: {get: function() {
      return WalkontableCellCoords;
    }},
  __esModule: {value: true}
});
var WalkontableCellCoords = function WalkontableCellCoords(row, col) {
  if (typeof row !== 'undefined' && typeof col !== 'undefined') {
    this.row = row;
    this.col = col;
  } else {
    this.row = null;
    this.col = null;
  }
};
($traceurRuntime.createClass)(WalkontableCellCoords, {
  isValid: function(wotInstance) {
    if (this.row < 0 || this.col < 0) {
      return false;
    }
    if (this.row >= wotInstance.getSetting('totalRows') || this.col >= wotInstance.getSetting('totalColumns')) {
      return false;
    }
    return true;
  },
  isEqual: function(cellCoords) {
    if (cellCoords === this) {
      return true;
    }
    return this.row === cellCoords.row && this.col === cellCoords.col;
  },
  isSouthEastOf: function(testedCoords) {
    return this.row >= testedCoords.row && this.col >= testedCoords.col;
  },
  isNorthWestOf: function(testedCoords) {
    return this.row <= testedCoords.row && this.col <= testedCoords.col;
  },
  isSouthWestOf: function(testedCoords) {
    return this.row >= testedCoords.row && this.col <= testedCoords.col;
  },
  isNorthEastOf: function(testedCoords) {
    return this.row <= testedCoords.row && this.col >= testedCoords.col;
  }
}, {});
;
window.WalkontableCellCoords = WalkontableCellCoords;


//# 
},{}],6:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableCellRange: {get: function() {
      return WalkontableCellRange;
    }},
  __esModule: {value: true}
});
var $___46__46__47_cell_47_coords_46_js__;
var WalkontableCellCoords = ($___46__46__47_cell_47_coords_46_js__ = require("./../cell/coords.js"), $___46__46__47_cell_47_coords_46_js__ && $___46__46__47_cell_47_coords_46_js__.__esModule && $___46__46__47_cell_47_coords_46_js__ || {default: $___46__46__47_cell_47_coords_46_js__}).WalkontableCellCoords;
var WalkontableCellRange = function WalkontableCellRange(highlight, from, to) {
  this.highlight = highlight;
  this.from = from;
  this.to = to;
};
var $WalkontableCellRange = WalkontableCellRange;
($traceurRuntime.createClass)(WalkontableCellRange, {
  isValid: function(wotInstance) {
    return this.from.isValid(wotInstance) && this.to.isValid(wotInstance);
  },
  isSingle: function() {
    return this.from.row === this.to.row && this.from.col === this.to.col;
  },
  getHeight: function() {
    return Math.max(this.from.row, this.to.row) - Math.min(this.from.row, this.to.row) + 1;
  },
  getWidth: function() {
    return Math.max(this.from.col, this.to.col) - Math.min(this.from.col, this.to.col) + 1;
  },
  includes: function(cellCoords) {
    var topLeft = this.getTopLeftCorner();
    var bottomRight = this.getBottomRightCorner();
    if (cellCoords.row < 0) {
      cellCoords.row = 0;
    }
    if (cellCoords.col < 0) {
      cellCoords.col = 0;
    }
    return topLeft.row <= cellCoords.row && bottomRight.row >= cellCoords.row && topLeft.col <= cellCoords.col && bottomRight.col >= cellCoords.col;
  },
  includesRange: function(testedRange) {
    return this.includes(testedRange.getTopLeftCorner()) && this.includes(testedRange.getBottomRightCorner());
  },
  isEqual: function(testedRange) {
    return (Math.min(this.from.row, this.to.row) == Math.min(testedRange.from.row, testedRange.to.row)) && (Math.max(this.from.row, this.to.row) == Math.max(testedRange.from.row, testedRange.to.row)) && (Math.min(this.from.col, this.to.col) == Math.min(testedRange.from.col, testedRange.to.col)) && (Math.max(this.from.col, this.to.col) == Math.max(testedRange.from.col, testedRange.to.col));
  },
  overlaps: function(testedRange) {
    return testedRange.isSouthEastOf(this.getTopLeftCorner()) && testedRange.isNorthWestOf(this.getBottomRightCorner());
  },
  isSouthEastOf: function(testedCoords) {
    return this.getTopLeftCorner().isSouthEastOf(testedCoords) || this.getBottomRightCorner().isSouthEastOf(testedCoords);
  },
  isNorthWestOf: function(testedCoords) {
    return this.getTopLeftCorner().isNorthWestOf(testedCoords) || this.getBottomRightCorner().isNorthWestOf(testedCoords);
  },
  expand: function(cellCoords) {
    var topLeft = this.getTopLeftCorner();
    var bottomRight = this.getBottomRightCorner();
    if (cellCoords.row < topLeft.row || cellCoords.col < topLeft.col || cellCoords.row > bottomRight.row || cellCoords.col > bottomRight.col) {
      this.from = new WalkontableCellCoords(Math.min(topLeft.row, cellCoords.row), Math.min(topLeft.col, cellCoords.col));
      this.to = new WalkontableCellCoords(Math.max(bottomRight.row, cellCoords.row), Math.max(bottomRight.col, cellCoords.col));
      return true;
    }
    return false;
  },
  expandByRange: function(expandingRange) {
    if (this.includesRange(expandingRange) || !this.overlaps(expandingRange)) {
      return false;
    }
    var topLeft = this.getTopLeftCorner();
    var bottomRight = this.getBottomRightCorner();
    var topRight = this.getTopRightCorner();
    var bottomLeft = this.getBottomLeftCorner();
    var expandingTopLeft = expandingRange.getTopLeftCorner();
    var expandingBottomRight = expandingRange.getBottomRightCorner();
    var resultTopRow = Math.min(topLeft.row, expandingTopLeft.row);
    var resultTopCol = Math.min(topLeft.col, expandingTopLeft.col);
    var resultBottomRow = Math.max(bottomRight.row, expandingBottomRight.row);
    var resultBottomCol = Math.max(bottomRight.col, expandingBottomRight.col);
    var finalFrom = new WalkontableCellCoords(resultTopRow, resultTopCol),
        finalTo = new WalkontableCellCoords(resultBottomRow, resultBottomCol);
    var isCorner = new $WalkontableCellRange(finalFrom, finalFrom, finalTo).isCorner(this.from, expandingRange),
        onlyMerge = expandingRange.isEqual(new $WalkontableCellRange(finalFrom, finalFrom, finalTo));
    if (isCorner && !onlyMerge) {
      if (this.from.col > finalFrom.col) {
        finalFrom.col = resultBottomCol;
        finalTo.col = resultTopCol;
      }
      if (this.from.row > finalFrom.row) {
        finalFrom.row = resultBottomRow;
        finalTo.row = resultTopRow;
      }
    }
    this.from = finalFrom;
    this.to = finalTo;
    return true;
  },
  getDirection: function() {
    if (this.from.isNorthWestOf(this.to)) {
      return 'NW-SE';
    } else if (this.from.isNorthEastOf(this.to)) {
      return 'NE-SW';
    } else if (this.from.isSouthEastOf(this.to)) {
      return 'SE-NW';
    } else if (this.from.isSouthWestOf(this.to)) {
      return 'SW-NE';
    }
  },
  setDirection: function(direction) {
    switch (direction) {
      case 'NW-SE':
        this.from = this.getTopLeftCorner();
        this.to = this.getBottomRightCorner();
        break;
      case 'NE-SW':
        this.from = this.getTopRightCorner();
        this.to = this.getBottomLeftCorner();
        break;
      case 'SE-NW':
        this.from = this.getBottomRightCorner();
        this.to = this.getTopLeftCorner();
        break;
      case 'SW-NE':
        this.from = this.getBottomLeftCorner();
        this.to = this.getTopRightCorner();
        break;
    }
  },
  getTopLeftCorner: function() {
    return new WalkontableCellCoords(Math.min(this.from.row, this.to.row), Math.min(this.from.col, this.to.col));
  },
  getBottomRightCorner: function() {
    return new WalkontableCellCoords(Math.max(this.from.row, this.to.row), Math.max(this.from.col, this.to.col));
  },
  getTopRightCorner: function() {
    return new WalkontableCellCoords(Math.min(this.from.row, this.to.row), Math.max(this.from.col, this.to.col));
  },
  getBottomLeftCorner: function() {
    return new WalkontableCellCoords(Math.max(this.from.row, this.to.row), Math.min(this.from.col, this.to.col));
  },
  isCorner: function(coords, expandedRange) {
    if (expandedRange) {
      if (expandedRange.includes(coords)) {
        if (this.getTopLeftCorner().isEqual(new WalkontableCellCoords(expandedRange.from.row, expandedRange.from.col)) || this.getTopRightCorner().isEqual(new WalkontableCellCoords(expandedRange.from.row, expandedRange.to.col)) || this.getBottomLeftCorner().isEqual(new WalkontableCellCoords(expandedRange.to.row, expandedRange.from.col)) || this.getBottomRightCorner().isEqual(new WalkontableCellCoords(expandedRange.to.row, expandedRange.to.col))) {
          return true;
        }
      }
    }
    return coords.isEqual(this.getTopLeftCorner()) || coords.isEqual(this.getTopRightCorner()) || coords.isEqual(this.getBottomLeftCorner()) || coords.isEqual(this.getBottomRightCorner());
  },
  getOppositeCorner: function(coords, expandedRange) {
    if (!(coords instanceof WalkontableCellCoords)) {
      return false;
    }
    if (expandedRange) {
      if (expandedRange.includes(coords)) {
        if (this.getTopLeftCorner().isEqual(new WalkontableCellCoords(expandedRange.from.row, expandedRange.from.col))) {
          return this.getBottomRightCorner();
        }
        if (this.getTopRightCorner().isEqual(new WalkontableCellCoords(expandedRange.from.row, expandedRange.to.col))) {
          return this.getBottomLeftCorner();
        }
        if (this.getBottomLeftCorner().isEqual(new WalkontableCellCoords(expandedRange.to.row, expandedRange.from.col))) {
          return this.getTopRightCorner();
        }
        if (this.getBottomRightCorner().isEqual(new WalkontableCellCoords(expandedRange.to.row, expandedRange.to.col))) {
          return this.getTopLeftCorner();
        }
      }
    }
    if (coords.isEqual(this.getBottomRightCorner())) {
      return this.getTopLeftCorner();
    } else if (coords.isEqual(this.getTopLeftCorner())) {
      return this.getBottomRightCorner();
    } else if (coords.isEqual(this.getTopRightCorner())) {
      return this.getBottomLeftCorner();
    } else if (coords.isEqual(this.getBottomLeftCorner())) {
      return this.getTopRightCorner();
    }
  },
  getBordersSharedWith: function(range) {
    if (!this.includesRange(range)) {
      return [];
    }
    var thisBorders = {
      top: Math.min(this.from.row, this.to.row),
      bottom: Math.max(this.from.row, this.to.row),
      left: Math.min(this.from.col, this.to.col),
      right: Math.max(this.from.col, this.to.col)
    };
    var rangeBorders = {
      top: Math.min(range.from.row, range.to.row),
      bottom: Math.max(range.from.row, range.to.row),
      left: Math.min(range.from.col, range.to.col),
      right: Math.max(range.from.col, range.to.col)
    };
    var result = [];
    if (thisBorders.top == rangeBorders.top) {
      result.push('top');
    }
    if (thisBorders.right == rangeBorders.right) {
      result.push('right');
    }
    if (thisBorders.bottom == rangeBorders.bottom) {
      result.push('bottom');
    }
    if (thisBorders.left == rangeBorders.left) {
      result.push('left');
    }
    return result;
  },
  getInner: function() {
    var topLeft = this.getTopLeftCorner();
    var bottomRight = this.getBottomRightCorner();
    var out = [];
    for (var r = topLeft.row; r <= bottomRight.row; r++) {
      for (var c = topLeft.col; c <= bottomRight.col; c++) {
        if (!(this.from.row === r && this.from.col === c) && !(this.to.row === r && this.to.col === c)) {
          out.push(new WalkontableCellCoords(r, c));
        }
      }
    }
    return out;
  },
  getAll: function() {
    var topLeft = this.getTopLeftCorner();
    var bottomRight = this.getBottomRightCorner();
    var out = [];
    for (var r = topLeft.row; r <= bottomRight.row; r++) {
      for (var c = topLeft.col; c <= bottomRight.col; c++) {
        if (topLeft.row === r && topLeft.col === c) {
          out.push(topLeft);
        } else if (bottomRight.row === r && bottomRight.col === c) {
          out.push(bottomRight);
        } else {
          out.push(new WalkontableCellCoords(r, c));
        }
      }
    }
    return out;
  },
  forAll: function(callback) {
    var topLeft = this.getTopLeftCorner();
    var bottomRight = this.getBottomRightCorner();
    for (var r = topLeft.row; r <= bottomRight.row; r++) {
      for (var c = topLeft.col; c <= bottomRight.col; c++) {
        var breakIteration = callback(r, c);
        if (breakIteration === false) {
          return;
        }
      }
    }
  }
}, {});
;
window.WalkontableCellRange = WalkontableCellRange;


//# 
},{"./../cell/coords.js":5}],7:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  Walkontable: {get: function() {
      return Walkontable;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47__46__46__47_helpers_46_js__,
    $__event_46_js__,
    $__overlays_46_js__,
    $__scroll_46_js__,
    $__settings_46_js__,
    $__table_46_js__,
    $__viewport_46_js__;
var dom = ($___46__46__47__46__46__47__46__46__47_dom_46_js__ = require("./../../../dom.js"), $___46__46__47__46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47__46__46__47_dom_46_js__});
var randomString = ($___46__46__47__46__46__47__46__46__47_helpers_46_js__ = require("./../../../helpers.js"), $___46__46__47__46__46__47__46__46__47_helpers_46_js__ && $___46__46__47__46__46__47__46__46__47_helpers_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47_helpers_46_js__ || {default: $___46__46__47__46__46__47__46__46__47_helpers_46_js__}).randomString;
var WalkontableEvent = ($__event_46_js__ = require("./event.js"), $__event_46_js__ && $__event_46_js__.__esModule && $__event_46_js__ || {default: $__event_46_js__}).WalkontableEvent;
var WalkontableOverlays = ($__overlays_46_js__ = require("./overlays.js"), $__overlays_46_js__ && $__overlays_46_js__.__esModule && $__overlays_46_js__ || {default: $__overlays_46_js__}).WalkontableOverlays;
var WalkontableScroll = ($__scroll_46_js__ = require("./scroll.js"), $__scroll_46_js__ && $__scroll_46_js__.__esModule && $__scroll_46_js__ || {default: $__scroll_46_js__}).WalkontableScroll;
var WalkontableSettings = ($__settings_46_js__ = require("./settings.js"), $__settings_46_js__ && $__settings_46_js__.__esModule && $__settings_46_js__ || {default: $__settings_46_js__}).WalkontableSettings;
var WalkontableTable = ($__table_46_js__ = require("./table.js"), $__table_46_js__ && $__table_46_js__.__esModule && $__table_46_js__ || {default: $__table_46_js__}).WalkontableTable;
var WalkontableViewport = ($__viewport_46_js__ = require("./viewport.js"), $__viewport_46_js__ && $__viewport_46_js__.__esModule && $__viewport_46_js__ || {default: $__viewport_46_js__}).WalkontableViewport;
var Walkontable = function Walkontable(settings) {
  var originalHeaders = [];
  this.guid = 'wt_' + randomString();
  if (settings.cloneSource) {
    this.cloneSource = settings.cloneSource;
    this.cloneOverlay = settings.cloneOverlay;
    this.wtSettings = settings.cloneSource.wtSettings;
    this.wtTable = new WalkontableTable(this, settings.table, settings.wtRootElement);
    this.wtScroll = new WalkontableScroll(this);
    this.wtViewport = settings.cloneSource.wtViewport;
    this.wtEvent = new WalkontableEvent(this);
    this.selections = this.cloneSource.selections;
  } else {
    this.wtSettings = new WalkontableSettings(this, settings);
    this.wtTable = new WalkontableTable(this, settings.table);
    this.wtScroll = new WalkontableScroll(this);
    this.wtViewport = new WalkontableViewport(this);
    this.wtEvent = new WalkontableEvent(this);
    this.selections = this.getSetting('selections');
    this.wtOverlays = new WalkontableOverlays(this);
  }
  if (this.wtTable.THEAD.childNodes.length && this.wtTable.THEAD.childNodes[0].childNodes.length) {
    for (var c = 0,
        clen = this.wtTable.THEAD.childNodes[0].childNodes.length; c < clen; c++) {
      originalHeaders.push(this.wtTable.THEAD.childNodes[0].childNodes[c].innerHTML);
    }
    if (!this.getSetting('columnHeaders').length) {
      this.update('columnHeaders', [function(column, TH) {
        dom.fastInnerText(TH, originalHeaders[column]);
      }]);
    }
  }
  this.drawn = false;
  this.drawInterrupted = false;
};
($traceurRuntime.createClass)(Walkontable, {
  draw: function() {
    var fastDraw = arguments[0] !== (void 0) ? arguments[0] : false;
    this.drawInterrupted = false;
    if (!fastDraw && !dom.isVisible(this.wtTable.TABLE)) {
      this.drawInterrupted = true;
    } else {
      this.wtTable.draw(fastDraw);
    }
    return this;
  },
  getCell: function(coords) {
    var topmost = arguments[1] !== (void 0) ? arguments[1] : false;
    if (!topmost) {
      return this.wtTable.getCell(coords);
    }
    var fixedRows = this.wtSettings.getSetting('fixedRowsTop');
    var fixedColumns = this.wtSettings.getSetting('fixedColumnsLeft');
    if (coords.row < fixedRows && coords.col < fixedColumns) {
      return this.wtOverlays.topLeftCornerOverlay.clone.wtTable.getCell(coords);
    } else if (coords.row < fixedRows) {
      return this.wtOverlays.topOverlay.clone.wtTable.getCell(coords);
    } else if (coords.col < fixedColumns) {
      return this.wtOverlays.leftOverlay.clone.wtTable.getCell(coords);
    }
    return this.wtTable.getCell(coords);
  },
  update: function(settings, value) {
    return this.wtSettings.update(settings, value);
  },
  scrollVertical: function(row) {
    this.wtOverlays.topOverlay.scrollTo(row);
    this.getSetting('onScrollVertically');
    return this;
  },
  scrollHorizontal: function(column) {
    this.wtOverlays.leftOverlay.scrollTo(column);
    this.getSetting('onScrollHorizontally');
    return this;
  },
  scrollViewport: function(coords) {
    this.wtScroll.scrollViewport(coords);
    return this;
  },
  getViewport: function() {
    return [this.wtTable.getFirstVisibleRow(), this.wtTable.getFirstVisibleColumn(), this.wtTable.getLastVisibleRow(), this.wtTable.getLastVisibleColumn()];
  },
  getOverlayName: function() {
    return this.cloneOverlay ? this.cloneOverlay.type : 'master';
  },
  getSetting: function(key, param1, param2, param3, param4) {
    return this.wtSettings.getSetting(key, param1, param2, param3, param4);
  },
  hasSetting: function(key) {
    return this.wtSettings.has(key);
  },
  destroy: function() {
    this.wtOverlays.destroy();
    if (this.wtEvent) {
      this.wtEvent.destroy();
    }
  }
}, {});
;
window.Walkontable = Walkontable;


//# 
},{"./../../../dom.js":27,"./../../../helpers.js":42,"./event.js":8,"./overlays.js":16,"./scroll.js":17,"./settings.js":19,"./table.js":20,"./viewport.js":22}],8:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableEvent: {get: function() {
      return WalkontableEvent;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47__46__46__47_eventManager_46_js__;
var dom = ($___46__46__47__46__46__47__46__46__47_dom_46_js__ = require("./../../../dom.js"), $___46__46__47__46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47__46__46__47_dom_46_js__});
var eventManagerObject = ($___46__46__47__46__46__47__46__46__47_eventManager_46_js__ = require("./../../../eventManager.js"), $___46__46__47__46__46__47__46__46__47_eventManager_46_js__ && $___46__46__47__46__46__47__46__46__47_eventManager_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47_eventManager_46_js__ || {default: $___46__46__47__46__46__47__46__46__47_eventManager_46_js__}).eventManager;
function WalkontableEvent(instance) {
  var that = this;
  var eventManager = eventManagerObject(instance);
  this.instance = instance;
  var dblClickOrigin = [null, null];
  this.dblClickTimeout = [null, null];
  var onMouseDown = function(event) {
    var cell = that.parentCell(event.realTarget);
    if (dom.hasClass(event.realTarget, 'corner')) {
      that.instance.getSetting('onCellCornerMouseDown', event, event.realTarget);
    } else if (cell.TD) {
      if (that.instance.hasSetting('onCellMouseDown')) {
        that.instance.getSetting('onCellMouseDown', event, cell.coords, cell.TD, that.instance);
      }
    }
    if (event.button !== 2) {
      if (cell.TD) {
        dblClickOrigin[0] = cell.TD;
        clearTimeout(that.dblClickTimeout[0]);
        that.dblClickTimeout[0] = setTimeout(function() {
          dblClickOrigin[0] = null;
        }, 1000);
      }
    }
  };
  var onTouchMove = function(event) {
    that.instance.touchMoving = true;
  };
  var longTouchTimeout;
  var onTouchStart = function(event) {
    var container = this;
    eventManager.addEventListener(this, 'touchmove', onTouchMove);
    that.checkIfTouchMove = setTimeout(function() {
      if (that.instance.touchMoving === true) {
        that.instance.touchMoving = void 0;
        eventManager.removeEventListener("touchmove", onTouchMove, false);
        return;
      } else {
        onMouseDown(event);
      }
    }, 30);
  };
  var lastMouseOver;
  var onMouseOver = function(event) {
    var table,
        td;
    if (that.instance.hasSetting('onCellMouseOver')) {
      table = that.instance.wtTable.TABLE;
      td = dom.closest(event.realTarget, ['TD', 'TH'], table);
      if (td && td !== lastMouseOver && dom.isChildOf(td, table)) {
        lastMouseOver = td;
        that.instance.getSetting('onCellMouseOver', event, that.instance.wtTable.getCoords(td), td, that.instance);
      }
    }
  };
  var onMouseUp = function(event) {
    if (event.button !== 2) {
      var cell = that.parentCell(event.realTarget);
      if (cell.TD === dblClickOrigin[0] && cell.TD === dblClickOrigin[1]) {
        if (dom.hasClass(event.realTarget, 'corner')) {
          that.instance.getSetting('onCellCornerDblClick', event, cell.coords, cell.TD, that.instance);
        } else {
          that.instance.getSetting('onCellDblClick', event, cell.coords, cell.TD, that.instance);
        }
        dblClickOrigin[0] = null;
        dblClickOrigin[1] = null;
      } else if (cell.TD === dblClickOrigin[0]) {
        dblClickOrigin[1] = cell.TD;
        clearTimeout(that.dblClickTimeout[1]);
        that.dblClickTimeout[1] = setTimeout(function() {
          dblClickOrigin[1] = null;
        }, 500);
      }
    }
  };
  var onTouchEnd = function(event) {
    clearTimeout(longTouchTimeout);
    event.preventDefault();
    onMouseUp(event);
  };
  eventManager.addEventListener(this.instance.wtTable.holder, 'mousedown', onMouseDown);
  eventManager.addEventListener(this.instance.wtTable.TABLE, 'mouseover', onMouseOver);
  eventManager.addEventListener(this.instance.wtTable.holder, 'mouseup', onMouseUp);
  if (this.instance.wtTable.holder.parentNode.parentNode && Handsontable.mobileBrowser && !that.instance.wtTable.isWorkingOnClone()) {
    var classSelector = "." + this.instance.wtTable.holder.parentNode.className.split(" ").join(".");
    eventManager.addEventListener(this.instance.wtTable.holder, 'touchstart', function(event) {
      that.instance.touchApplied = true;
      if (dom.isChildOf(event.target, classSelector)) {
        onTouchStart.call(event.target, event);
      }
    });
    eventManager.addEventListener(this.instance.wtTable.holder, 'touchend', function(event) {
      that.instance.touchApplied = false;
      if (dom.isChildOf(event.target, classSelector)) {
        onTouchEnd.call(event.target, event);
      }
    });
    if (!that.instance.momentumScrolling) {
      that.instance.momentumScrolling = {};
    }
    eventManager.addEventListener(this.instance.wtTable.holder, 'scroll', function(event) {
      clearTimeout(that.instance.momentumScrolling._timeout);
      if (!that.instance.momentumScrolling.ongoing) {
        that.instance.getSetting('onBeforeTouchScroll');
      }
      that.instance.momentumScrolling.ongoing = true;
      that.instance.momentumScrolling._timeout = setTimeout(function() {
        if (!that.instance.touchApplied) {
          that.instance.momentumScrolling.ongoing = false;
          that.instance.getSetting('onAfterMomentumScroll');
        }
      }, 200);
    });
  }
  eventManager.addEventListener(window, 'resize', function() {
    if (that.instance.getSetting('stretchH') !== 'none') {
      that.instance.draw();
    }
  });
  this.destroy = function() {
    clearTimeout(this.dblClickTimeout[0]);
    clearTimeout(this.dblClickTimeout[1]);
    eventManager.clear();
  };
}
WalkontableEvent.prototype.parentCell = function(elem) {
  var cell = {};
  var TABLE = this.instance.wtTable.TABLE;
  var TD = dom.closest(elem, ['TD', 'TH'], TABLE);
  if (TD && dom.isChildOf(TD, TABLE)) {
    cell.coords = this.instance.wtTable.getCoords(TD);
    cell.TD = TD;
  } else if (dom.hasClass(elem, 'wtBorder') && dom.hasClass(elem, 'current')) {
    cell.coords = this.instance.selections.current.cellRange.highlight;
    cell.TD = this.instance.wtTable.getCell(cell.coords);
  } else if (dom.hasClass(elem, 'wtBorder') && dom.hasClass(elem, 'area')) {
    if (this.instance.selections.area.cellRange) {
      cell.coords = this.instance.selections.area.cellRange.to;
      cell.TD = this.instance.wtTable.getCell(cell.coords);
    }
  }
  return cell;
};
;
window.WalkontableEvent = WalkontableEvent;


//# 
},{"./../../../dom.js":27,"./../../../eventManager.js":41}],9:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableColumnFilter: {get: function() {
      return WalkontableColumnFilter;
    }},
  __esModule: {value: true}
});
var WalkontableColumnFilter = function WalkontableColumnFilter(offset, total, countTH) {
  this.offset = offset;
  this.total = total;
  this.countTH = countTH;
};
($traceurRuntime.createClass)(WalkontableColumnFilter, {
  offsetted: function(index) {
    return index + this.offset;
  },
  unOffsetted: function(index) {
    return index - this.offset;
  },
  renderedToSource: function(index) {
    return this.offsetted(index);
  },
  sourceToRendered: function(index) {
    return this.unOffsetted(index);
  },
  offsettedTH: function(index) {
    return index - this.countTH;
  },
  unOffsettedTH: function(index) {
    return index + this.countTH;
  },
  visibleRowHeadedColumnToSourceColumn: function(index) {
    return this.renderedToSource(this.offsettedTH(index));
  },
  sourceColumnToVisibleRowHeadedColumn: function(index) {
    return this.unOffsettedTH(this.sourceToRendered(index));
  }
}, {});
;
window.WalkontableColumnFilter = WalkontableColumnFilter;


//# 
},{}],10:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableRowFilter: {get: function() {
      return WalkontableRowFilter;
    }},
  __esModule: {value: true}
});
var WalkontableRowFilter = function WalkontableRowFilter(offset, total, countTH) {
  this.offset = offset;
  this.total = total;
  this.countTH = countTH;
};
($traceurRuntime.createClass)(WalkontableRowFilter, {
  offsetted: function(index) {
    return index + this.offset;
  },
  unOffsetted: function(index) {
    return index - this.offset;
  },
  renderedToSource: function(index) {
    return this.offsetted(index);
  },
  sourceToRendered: function(index) {
    return this.unOffsetted(index);
  },
  offsettedTH: function(index) {
    return index - this.countTH;
  },
  unOffsettedTH: function(index) {
    return index + this.countTH;
  },
  visibleColHeadedRowToSourceRow: function(index) {
    return this.renderedToSource(this.offsettedTH(index));
  },
  sourceRowToVisibleColHeadedRow: function(index) {
    return this.unOffsettedTH(this.sourceToRendered(index));
  }
}, {});
;
window.WalkontableRowFilter = WalkontableRowFilter;


//# 
},{}],11:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableOverlay: {get: function() {
      return WalkontableOverlay;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47__46__46__47__46__46__47_helpers_46_js__,
    $___46__46__47__46__46__47__46__46__47__46__46__47_eventManager_46_js__;
var dom = ($___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__ = require("./../../../../dom.js"), $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__});
var defineGetter = ($___46__46__47__46__46__47__46__46__47__46__46__47_helpers_46_js__ = require("./../../../../helpers.js"), $___46__46__47__46__46__47__46__46__47__46__46__47_helpers_46_js__ && $___46__46__47__46__46__47__46__46__47__46__46__47_helpers_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47__46__46__47_helpers_46_js__ || {default: $___46__46__47__46__46__47__46__46__47__46__46__47_helpers_46_js__}).defineGetter;
var eventManagerObject = ($___46__46__47__46__46__47__46__46__47__46__46__47_eventManager_46_js__ = require("./../../../../eventManager.js"), $___46__46__47__46__46__47__46__46__47__46__46__47_eventManager_46_js__ && $___46__46__47__46__46__47__46__46__47__46__46__47_eventManager_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47__46__46__47_eventManager_46_js__ || {default: $___46__46__47__46__46__47__46__46__47__46__46__47_eventManager_46_js__}).eventManager;
var WalkontableOverlay = function WalkontableOverlay(wotInstance) {
  defineGetter(this, 'wot', wotInstance, {writable: false});
  this.instance = this.wot;
  this.type = '';
  this.TABLE = this.wot.wtTable.TABLE;
  this.hider = this.wot.wtTable.hider;
  this.spreader = this.wot.wtTable.spreader;
  this.holder = this.wot.wtTable.holder;
  this.wtRootElement = this.wot.wtTable.wtRootElement;
  this.trimmingContainer = dom.getTrimmingContainer(this.hider.parentNode.parentNode);
  this.mainTableScrollableElement = dom.getScrollableElement(this.wot.wtTable.TABLE);
  this.needFullRender = this.shouldBeRendered();
  this.isElementSizesAdjusted = false;
};
var $WalkontableOverlay = WalkontableOverlay;
($traceurRuntime.createClass)(WalkontableOverlay, {
  shouldBeRendered: function() {
    return true;
  },
  makeClone: function(direction) {
    if ($WalkontableOverlay.CLONE_TYPES.indexOf(direction) === -1) {
      throw new Error('Clone type "' + direction + '" is not supported.');
    }
    var clone = document.createElement('DIV');
    var clonedTable = document.createElement('TABLE');
    clone.className = 'ht_clone_' + direction + ' handsontable';
    clone.style.position = 'absolute';
    clone.style.top = 0;
    clone.style.left = 0;
    clone.style.overflow = 'hidden';
    clonedTable.className = this.wot.wtTable.TABLE.className;
    clone.appendChild(clonedTable);
    this.type = direction;
    this.wot.wtTable.wtRootElement.parentNode.appendChild(clone);
    return new Walkontable({
      cloneSource: this.wot,
      cloneOverlay: this,
      table: clonedTable
    });
  },
  refresh: function() {
    var fastDraw = arguments[0] !== (void 0) ? arguments[0] : false;
    var nextCycleRenderFlag = this.shouldBeRendered();
    if (this.clone && (this.needFullRender || nextCycleRenderFlag)) {
      this.clone.draw(fastDraw);
    }
    this.needFullRender = nextCycleRenderFlag;
  },
  destroy: function() {
    eventManagerObject(this.clone).clear();
  }
}, {
  get CLONE_TOP() {
    return 'top';
  },
  get CLONE_LEFT() {
    return 'left';
  },
  get CLONE_CORNER() {
    return 'corner';
  },
  get CLONE_DEBUG() {
    return 'debug';
  },
  get CLONE_TYPES() {
    return [$WalkontableOverlay.CLONE_TOP, $WalkontableOverlay.CLONE_LEFT, $WalkontableOverlay.CLONE_CORNER, $WalkontableOverlay.CLONE_DEBUG];
  }
});
;
window.WalkontableOverlay = WalkontableOverlay;


//# 
},{"./../../../../dom.js":27,"./../../../../eventManager.js":41,"./../../../../helpers.js":42}],12:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableCornerOverlay: {get: function() {
      return WalkontableCornerOverlay;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__,
    $___95_base_46_js__;
var dom = ($___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__ = require("./../../../../dom.js"), $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__});
var WalkontableOverlay = ($___95_base_46_js__ = require("./_base.js"), $___95_base_46_js__ && $___95_base_46_js__.__esModule && $___95_base_46_js__ || {default: $___95_base_46_js__}).WalkontableOverlay;
var WalkontableCornerOverlay = function WalkontableCornerOverlay(wotInstance) {
  $traceurRuntime.superConstructor($WalkontableCornerOverlay).call(this, wotInstance);
  this.clone = this.makeClone(WalkontableOverlay.CLONE_CORNER);
};
var $WalkontableCornerOverlay = WalkontableCornerOverlay;
($traceurRuntime.createClass)(WalkontableCornerOverlay, {
  shouldBeRendered: function() {
    return (this.wot.getSetting('fixedRowsTop') || this.wot.getSetting('columnHeaders').length) && (this.wot.getSetting('fixedColumnsLeft') || this.wot.getSetting('rowHeaders').length) ? true : false;
  },
  resetFixedPosition: function() {
    if (!this.wot.wtTable.holder.parentNode) {
      return;
    }
    var overlayRoot = this.clone.wtTable.holder.parentNode;
    var tableHeight = dom.outerHeight(this.clone.wtTable.TABLE);
    var tableWidth = dom.outerWidth(this.clone.wtTable.TABLE);
    if (this.trimmingContainer === window) {
      var box = this.wot.wtTable.hider.getBoundingClientRect();
      var top = Math.ceil(box.top);
      var left = Math.ceil(box.left);
      var bottom = Math.ceil(box.bottom);
      var right = Math.ceil(box.right);
      var finalLeft;
      var finalTop;
      if (left < 0 && (right - overlayRoot.offsetWidth) > 0) {
        finalLeft = -left + 'px';
      } else {
        finalLeft = '0';
      }
      if (top < 0 && (bottom - overlayRoot.offsetHeight) > 0) {
        finalTop = -top + 'px';
      } else {
        finalTop = '0';
      }
      dom.setOverlayPosition(overlayRoot, finalLeft, finalTop);
    }
    overlayRoot.style.height = (tableHeight === 0 ? tableHeight : tableHeight + 4) + 'px';
    overlayRoot.style.width = (tableWidth === 0 ? tableWidth : tableWidth + 4) + 'px';
  }
}, {}, WalkontableOverlay);
;
window.WalkontableCornerOverlay = WalkontableCornerOverlay;


//# 
},{"./../../../../dom.js":27,"./_base.js":11}],13:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableDebugOverlay: {get: function() {
      return WalkontableDebugOverlay;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__,
    $___95_base_46_js__;
var dom = ($___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__ = require("./../../../../dom.js"), $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__});
var WalkontableOverlay = ($___95_base_46_js__ = require("./_base.js"), $___95_base_46_js__ && $___95_base_46_js__.__esModule && $___95_base_46_js__ || {default: $___95_base_46_js__}).WalkontableOverlay;
var WalkontableDebugOverlay = function WalkontableDebugOverlay(wotInstance) {
  $traceurRuntime.superConstructor($WalkontableDebugOverlay).call(this, wotInstance);
  this.clone = this.makeClone(WalkontableOverlay.CLONE_DEBUG);
  this.clone.wtTable.holder.style.opacity = 0.4;
  this.clone.wtTable.holder.style.textShadow = '0 0 2px #ff0000';
  dom.addClass(this.clone.wtTable.holder.parentNode, 'wtDebugVisible');
};
var $WalkontableDebugOverlay = WalkontableDebugOverlay;
($traceurRuntime.createClass)(WalkontableDebugOverlay, {}, {}, WalkontableOverlay);
;
window.WalkontableDebugOverlay = WalkontableDebugOverlay;


//# 
},{"./../../../../dom.js":27,"./_base.js":11}],14:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableLeftOverlay: {get: function() {
      return WalkontableLeftOverlay;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__,
    $___95_base_46_js__;
var dom = ($___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__ = require("./../../../../dom.js"), $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__});
var WalkontableOverlay = ($___95_base_46_js__ = require("./_base.js"), $___95_base_46_js__ && $___95_base_46_js__.__esModule && $___95_base_46_js__ || {default: $___95_base_46_js__}).WalkontableOverlay;
var WalkontableLeftOverlay = function WalkontableLeftOverlay(wotInstance) {
  $traceurRuntime.superConstructor($WalkontableLeftOverlay).call(this, wotInstance);
  this.clone = this.makeClone(WalkontableOverlay.CLONE_LEFT);
};
var $WalkontableLeftOverlay = WalkontableLeftOverlay;
($traceurRuntime.createClass)(WalkontableLeftOverlay, {
  shouldBeRendered: function() {
    return this.wot.getSetting('fixedColumnsLeft') || this.wot.getSetting('rowHeaders').length ? true : false;
  },
  resetFixedPosition: function() {
    if (!this.needFullRender || !this.wot.wtTable.holder.parentNode) {
      return;
    }
    var overlayRoot = this.clone.wtTable.holder.parentNode;
    var headerPosition = 0;
    if (this.trimmingContainer === window) {
      var box = this.wot.wtTable.hider.getBoundingClientRect();
      var left = Math.ceil(box.left);
      var right = Math.ceil(box.right);
      var finalLeft;
      var finalTop;
      finalTop = this.wot.wtTable.hider.style.top;
      finalTop = finalTop === '' ? 0 : finalTop;
      if (left < 0 && (right - overlayRoot.offsetWidth) > 0) {
        finalLeft = -left;
      } else {
        finalLeft = 0;
      }
      headerPosition = finalLeft;
      finalLeft = finalLeft + 'px';
      dom.setOverlayPosition(overlayRoot, finalLeft, finalTop);
    } else {
      headerPosition = this.getScrollPosition();
    }
    this.adjustHeaderBordersPosition(headerPosition);
  },
  setScrollPosition: function(pos) {
    if (this.mainTableScrollableElement === window) {
      window.scrollTo(pos, dom.getWindowScrollTop());
    } else {
      this.mainTableScrollableElement.scrollLeft = pos;
    }
  },
  onScroll: function() {
    this.wot.getSetting('onScrollHorizontally');
  },
  sumCellSizes: function(from, to) {
    var sum = 0;
    var defaultColumnWidth = this.wot.wtSettings.defaultColumnWidth;
    while (from < to) {
      sum += this.wot.wtTable.getStretchedColumnWidth(from) || defaultColumnWidth;
      from++;
    }
    return sum;
  },
  adjustElementsSize: function() {
    if (this.needFullRender) {
      this.adjustRootElementSize();
      this.adjustRootChildsSize();
      this.isElementSizesAdjusted = true;
    }
  },
  adjustRootElementSize: function() {
    var masterHolder = this.wot.wtTable.holder;
    var scrollbarHeight = masterHolder.clientHeight !== masterHolder.offsetHeight ? dom.getScrollbarWidth() : 0;
    var overlayRoot = this.clone.wtTable.holder.parentNode;
    var overlayRootStyle = overlayRoot.style;
    var tableWidth;
    if (this.trimmingContainer !== window) {
      overlayRootStyle.height = this.wot.wtViewport.getWorkspaceHeight() - scrollbarHeight + 'px';
    }
    this.clone.wtTable.holder.style.height = overlayRootStyle.height;
    tableWidth = dom.outerWidth(this.clone.wtTable.TABLE);
    overlayRootStyle.width = (tableWidth === 0 ? tableWidth : tableWidth + 4) + 'px';
  },
  adjustRootChildsSize: function() {
    var scrollbarWidth = dom.getScrollbarWidth();
    this.clone.wtTable.hider.style.height = this.hider.style.height;
    this.clone.wtTable.holder.style.height = this.clone.wtTable.holder.parentNode.style.height;
    if (scrollbarWidth === 0) {
      scrollbarWidth = 30;
    }
    this.clone.wtTable.holder.style.width = parseInt(this.clone.wtTable.holder.parentNode.style.width, 10) + scrollbarWidth + 'px';
  },
  applyToDOM: function() {
    var total = this.wot.getSetting('totalColumns');
    if (!this.isElementSizesAdjusted) {
      this.adjustElementsSize();
    }
    if (typeof this.wot.wtViewport.columnsRenderCalculator.startPosition === 'number') {
      this.spreader.style.left = this.wot.wtViewport.columnsRenderCalculator.startPosition + 'px';
    } else if (total === 0) {
      this.spreader.style.left = '0';
    } else {
      throw new Error('Incorrect value of the columnsRenderCalculator');
    }
    this.spreader.style.right = '';
    if (this.needFullRender) {
      this.syncOverlayOffset();
    }
  },
  syncOverlayOffset: function() {
    if (typeof this.wot.wtViewport.rowsRenderCalculator.startPosition === 'number') {
      this.clone.wtTable.spreader.style.top = this.wot.wtViewport.rowsRenderCalculator.startPosition + 'px';
    } else {
      this.clone.wtTable.spreader.style.top = '';
    }
  },
  scrollTo: function(sourceCol, beyondRendered) {
    var newX = this.getTableParentOffset();
    var sourceInstance = this.wot.cloneSource ? this.wot.cloneSource : this.wot;
    var mainHolder = sourceInstance.wtTable.holder;
    var scrollbarCompensation = 0;
    if (beyondRendered && mainHolder.offsetWidth !== mainHolder.clientWidth) {
      scrollbarCompensation = dom.getScrollbarWidth();
    }
    if (beyondRendered) {
      newX += this.sumCellSizes(0, sourceCol + 1);
      newX -= this.wot.wtViewport.getViewportWidth();
    } else {
      newX += this.sumCellSizes(this.wot.getSetting('fixedColumnsLeft'), sourceCol);
    }
    newX += scrollbarCompensation;
    this.setScrollPosition(newX);
  },
  getTableParentOffset: function() {
    if (this.trimmingContainer === window) {
      return this.wot.wtTable.holderOffset.left;
    } else {
      return 0;
    }
  },
  getScrollPosition: function() {
    return dom.getScrollLeft(this.mainTableScrollableElement);
  },
  adjustHeaderBordersPosition: function(position) {
    if (this.wot.getSetting('fixedColumnsLeft') === 0 && this.wot.getSetting('rowHeaders').length > 0) {
      var masterParent = this.wot.wtTable.holder.parentNode;
      var previousState = dom.hasClass(masterParent, 'innerBorderLeft');
      if (position) {
        dom.addClass(masterParent, 'innerBorderLeft');
      } else {
        dom.removeClass(masterParent, 'innerBorderLeft');
      }
      if (!previousState && position || previousState && !position) {
        this.wot.wtOverlays.adjustElementsSize();
      }
    }
  }
}, {}, WalkontableOverlay);
;
window.WalkontableLeftOverlay = WalkontableLeftOverlay;


//# 
},{"./../../../../dom.js":27,"./_base.js":11}],15:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableTopOverlay: {get: function() {
      return WalkontableTopOverlay;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__,
    $___95_base_46_js__;
var dom = ($___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__ = require("./../../../../dom.js"), $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47__46__46__47__46__46__47_dom_46_js__});
var WalkontableOverlay = ($___95_base_46_js__ = require("./_base.js"), $___95_base_46_js__ && $___95_base_46_js__.__esModule && $___95_base_46_js__ || {default: $___95_base_46_js__}).WalkontableOverlay;
var WalkontableTopOverlay = function WalkontableTopOverlay(wotInstance) {
  $traceurRuntime.superConstructor($WalkontableTopOverlay).call(this, wotInstance);
  this.clone = this.makeClone(WalkontableOverlay.CLONE_TOP);
};
var $WalkontableTopOverlay = WalkontableTopOverlay;
($traceurRuntime.createClass)(WalkontableTopOverlay, {
  shouldBeRendered: function() {
    return this.wot.getSetting('fixedRowsTop') || this.wot.getSetting('columnHeaders').length ? true : false;
  },
  resetFixedPosition: function() {
    if (!this.needFullRender || !this.wot.wtTable.holder.parentNode) {
      return;
    }
    var overlayRoot = this.clone.wtTable.holder.parentNode;
    var headerPosition = 0;
    if (this.wot.wtOverlays.leftOverlay.trimmingContainer === window) {
      var box = this.wot.wtTable.hider.getBoundingClientRect();
      var top = Math.ceil(box.top);
      var bottom = Math.ceil(box.bottom);
      var finalLeft;
      var finalTop;
      finalLeft = this.wot.wtTable.hider.style.left;
      finalLeft = finalLeft === '' ? 0 : finalLeft;
      if (top < 0 && (bottom - overlayRoot.offsetHeight) > 0) {
        finalTop = -top;
      } else {
        finalTop = 0;
      }
      headerPosition = finalTop;
      finalTop = finalTop + 'px';
      dom.setOverlayPosition(overlayRoot, finalLeft, finalTop);
    } else {
      headerPosition = this.getScrollPosition();
    }
    this.adjustHeaderBordersPosition(headerPosition);
  },
  setScrollPosition: function(pos) {
    if (this.mainTableScrollableElement === window) {
      window.scrollTo(dom.getWindowScrollLeft(), pos);
    } else {
      this.mainTableScrollableElement.scrollTop = pos;
    }
  },
  onScroll: function() {
    this.wot.getSetting('onScrollVertically');
  },
  sumCellSizes: function(from, to) {
    var sum = 0;
    var defaultRowHeight = this.wot.wtSettings.settings.defaultRowHeight;
    while (from < to) {
      sum += this.wot.wtTable.getRowHeight(from) || defaultRowHeight;
      from++;
    }
    return sum;
  },
  adjustElementsSize: function() {
    if (this.needFullRender) {
      this.adjustRootElementSize();
      this.adjustRootChildsSize();
      this.isElementSizesAdjusted = true;
    }
  },
  adjustRootElementSize: function() {
    var masterHolder = this.wot.wtTable.holder;
    var scrollbarWidth = masterHolder.clientWidth !== masterHolder.offsetWidth ? dom.getScrollbarWidth() : 0;
    var overlayRoot = this.clone.wtTable.holder.parentNode;
    var overlayRootStyle = overlayRoot.style;
    var tableHeight;
    if (this.trimmingContainer !== window) {
      overlayRootStyle.width = this.wot.wtViewport.getWorkspaceWidth() - scrollbarWidth + 'px';
    }
    this.clone.wtTable.holder.style.width = overlayRootStyle.width;
    tableHeight = dom.outerHeight(this.clone.wtTable.TABLE);
    overlayRootStyle.height = (tableHeight === 0 ? tableHeight : tableHeight + 4) + 'px';
  },
  adjustRootChildsSize: function() {
    var scrollbarWidth = dom.getScrollbarWidth();
    this.clone.wtTable.hider.style.width = this.hider.style.width;
    this.clone.wtTable.holder.style.width = this.clone.wtTable.holder.parentNode.style.width;
    if (scrollbarWidth === 0) {
      scrollbarWidth = 30;
    }
    this.clone.wtTable.holder.style.height = parseInt(this.clone.wtTable.holder.parentNode.style.height, 10) + scrollbarWidth + 'px';
  },
  applyToDOM: function() {
    var total = this.wot.getSetting('totalRows');
    if (!this.isElementSizesAdjusted) {
      this.adjustElementsSize();
    }
    if (typeof this.wot.wtViewport.rowsRenderCalculator.startPosition === 'number') {
      this.spreader.style.top = this.wot.wtViewport.rowsRenderCalculator.startPosition + 'px';
    } else if (total === 0) {
      this.spreader.style.top = '0';
    } else {
      throw new Error("Incorrect value of the rowsRenderCalculator");
    }
    this.spreader.style.bottom = '';
    if (this.needFullRender) {
      this.syncOverlayOffset();
    }
  },
  syncOverlayOffset: function() {
    if (typeof this.wot.wtViewport.columnsRenderCalculator.startPosition === 'number') {
      this.clone.wtTable.spreader.style.left = this.wot.wtViewport.columnsRenderCalculator.startPosition + 'px';
    } else {
      this.clone.wtTable.spreader.style.left = '';
    }
  },
  scrollTo: function(sourceRow, bottomEdge) {
    var newY = this.getTableParentOffset();
    var sourceInstance = this.wot.cloneSource ? this.wot.cloneSource : this.wot;
    var mainHolder = sourceInstance.wtTable.holder;
    var scrollbarCompensation = 0;
    if (bottomEdge && mainHolder.offsetHeight !== mainHolder.clientHeight) {
      scrollbarCompensation = dom.getScrollbarWidth();
    }
    if (bottomEdge) {
      newY += this.sumCellSizes(0, sourceRow + 1);
      newY -= this.wot.wtViewport.getViewportHeight();
      newY += 1;
    } else {
      newY += this.sumCellSizes(this.wot.getSetting('fixedRowsTop'), sourceRow);
    }
    newY += scrollbarCompensation;
    this.setScrollPosition(newY);
  },
  getTableParentOffset: function() {
    if (this.mainTableScrollableElement === window) {
      return this.wot.wtTable.holderOffset.top;
    } else {
      return 0;
    }
  },
  getScrollPosition: function() {
    return dom.getScrollTop(this.mainTableScrollableElement);
  },
  adjustHeaderBordersPosition: function(position) {
    if (this.wot.getSetting('fixedRowsTop') === 0 && this.wot.getSetting('columnHeaders').length > 0) {
      var masterParent = this.wot.wtTable.holder.parentNode;
      var previousState = dom.hasClass(masterParent, 'innerBorderTop');
      if (position) {
        dom.addClass(masterParent, 'innerBorderTop');
      } else {
        dom.removeClass(masterParent, 'innerBorderTop');
      }
      if (!previousState && position || previousState && !position) {
        this.wot.wtOverlays.adjustElementsSize();
      }
    }
    if (this.wot.getSetting('rowHeaders').length === 0) {
      var secondHeaderCell = this.clone.wtTable.THEAD.querySelector('th:nth-of-type(2)');
      if (secondHeaderCell) {
        secondHeaderCell.style['border-left-width'] = 0;
      }
    }
  }
}, {}, WalkontableOverlay);
;
window.WalkontableTopOverlay = WalkontableTopOverlay;


//# 
},{"./../../../../dom.js":27,"./_base.js":11}],16:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableOverlays: {get: function() {
      return WalkontableOverlays;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47__46__46__47_eventManager_46_js__,
    $__overlay_47_corner_46_js__,
    $__overlay_47_debug_46_js__,
    $__overlay_47_left_46_js__,
    $__overlay_47_top_46_js__;
var dom = ($___46__46__47__46__46__47__46__46__47_dom_46_js__ = require("./../../../dom.js"), $___46__46__47__46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47__46__46__47_dom_46_js__});
var EventManager = ($___46__46__47__46__46__47__46__46__47_eventManager_46_js__ = require("./../../../eventManager.js"), $___46__46__47__46__46__47__46__46__47_eventManager_46_js__ && $___46__46__47__46__46__47__46__46__47_eventManager_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47_eventManager_46_js__ || {default: $___46__46__47__46__46__47__46__46__47_eventManager_46_js__}).EventManager;
var WalkontableCornerOverlay = ($__overlay_47_corner_46_js__ = require("./overlay/corner.js"), $__overlay_47_corner_46_js__ && $__overlay_47_corner_46_js__.__esModule && $__overlay_47_corner_46_js__ || {default: $__overlay_47_corner_46_js__}).WalkontableCornerOverlay;
var WalkontableDebugOverlay = ($__overlay_47_debug_46_js__ = require("./overlay/debug.js"), $__overlay_47_debug_46_js__ && $__overlay_47_debug_46_js__.__esModule && $__overlay_47_debug_46_js__ || {default: $__overlay_47_debug_46_js__}).WalkontableDebugOverlay;
var WalkontableLeftOverlay = ($__overlay_47_left_46_js__ = require("./overlay/left.js"), $__overlay_47_left_46_js__ && $__overlay_47_left_46_js__.__esModule && $__overlay_47_left_46_js__ || {default: $__overlay_47_left_46_js__}).WalkontableLeftOverlay;
var WalkontableTopOverlay = ($__overlay_47_top_46_js__ = require("./overlay/top.js"), $__overlay_47_top_46_js__ && $__overlay_47_top_46_js__.__esModule && $__overlay_47_top_46_js__ || {default: $__overlay_47_top_46_js__}).WalkontableTopOverlay;
var WalkontableOverlays = function WalkontableOverlays(wotInstance) {
  this.wot = wotInstance;
  this.instance = this.wot;
  this.eventManager = new EventManager(this.wot);
  this.wot.update('scrollbarWidth', dom.getScrollbarWidth());
  this.wot.update('scrollbarHeight', dom.getScrollbarWidth());
  this.mainTableScrollableElement = dom.getScrollableElement(this.wot.wtTable.TABLE);
  this.topOverlay = new WalkontableTopOverlay(this.wot);
  this.leftOverlay = new WalkontableLeftOverlay(this.wot);
  if (this.topOverlay.needFullRender && this.leftOverlay.needFullRender) {
    this.topLeftCornerOverlay = new WalkontableCornerOverlay(this.wot);
  }
  if (this.wot.getSetting('debug')) {
    this.debug = new WalkontableDebugOverlay(this.wot);
  }
  this.destroyed = false;
  this.keyPressed = false;
  this.spreaderLastSize = {
    width: null,
    height: null
  };
  this.overlayScrollPositions = {
    'master': {
      top: 0,
      left: 0
    },
    'top': {
      top: null,
      left: 0
    },
    'left': {
      top: 0,
      left: null
    }
  };
  this.registerListeners();
};
($traceurRuntime.createClass)(WalkontableOverlays, {
  refreshAll: function() {
    if (!this.wot.drawn) {
      return;
    }
    if (!this.wot.wtTable.holder.parentNode) {
      this.destroy();
      return;
    }
    this.wot.draw(true);
    this.topOverlay.onScroll();
    this.leftOverlay.onScroll();
  },
  registerListeners: function() {
    var $__5 = this;
    this.eventManager.addEventListener(document.documentElement, 'keydown', (function() {
      return $__5.onKeyDown();
    }));
    this.eventManager.addEventListener(document.documentElement, 'keyup', (function() {
      return $__5.onKeyUp();
    }));
    this.eventManager.addEventListener(this.mainTableScrollableElement, 'scroll', (function(event) {
      return $__5.onTableScroll(event);
    }));
    if (this.topOverlay.needFullRender) {
      this.eventManager.addEventListener(this.topOverlay.clone.wtTable.holder, 'scroll', (function(event) {
        return $__5.onTableScroll(event);
      }));
      this.eventManager.addEventListener(this.topOverlay.clone.wtTable.holder, 'wheel', (function(event) {
        return $__5.onTableScroll(event);
      }));
    }
    if (this.leftOverlay.needFullRender) {
      this.eventManager.addEventListener(this.leftOverlay.clone.wtTable.holder, 'scroll', (function(event) {
        return $__5.onTableScroll(event);
      }));
      this.eventManager.addEventListener(this.leftOverlay.clone.wtTable.holder, 'wheel', (function(event) {
        return $__5.onTableScroll(event);
      }));
    }
    if (this.topOverlay.trimmingContainer !== window && this.leftOverlay.trimmingContainer !== window) {
      this.eventManager.addEventListener(window, 'wheel', (function(event) {
        var overlay;
        var deltaY = event.wheelDeltaY || event.deltaY;
        var deltaX = event.wheelDeltaX || event.deltaX;
        if ($__5.topOverlay.clone.wtTable.holder.contains(event.target)) {
          overlay = 'top';
        } else if ($__5.leftOverlay.clone.wtTable.holder.contains(event.target)) {
          overlay = 'left';
        }
        if (overlay == 'top' && deltaY !== 0) {
          event.preventDefault();
        } else if (overlay == 'left' && deltaX !== 0) {
          event.preventDefault();
        }
      }));
    }
  },
  onTableScroll: function(event) {
    if (Handsontable.mobileBrowser) {
      return;
    }
    if (this.keyPressed && this.mainTableScrollableElement !== window && !event.target.contains(this.mainTableScrollableElement)) {
      return;
    }
    if (event.type === 'scroll') {
      this.syncScrollPositions(event);
    } else {
      this.translateMouseWheelToScroll(event);
    }
  },
  onKeyDown: function() {
    this.keyPressed = true;
  },
  onKeyUp: function() {
    this.keyPressed = false;
  },
  translateMouseWheelToScroll: function(event) {
    var topOverlay = this.topOverlay.clone.wtTable.holder;
    var leftOverlay = this.leftOverlay.clone.wtTable.holder;
    var eventMockup = {type: 'wheel'};
    var tempElem = event.target;
    var deltaY = event.wheelDeltaY || (-1) * event.deltaY;
    var deltaX = event.wheelDeltaX || (-1) * event.deltaX;
    var parentHolder;
    while (tempElem != document && tempElem != null) {
      if (tempElem.className.indexOf('wtHolder') > -1) {
        parentHolder = tempElem;
        break;
      }
      tempElem = tempElem.parentNode;
    }
    eventMockup.target = parentHolder;
    if (parentHolder == topOverlay) {
      this.syncScrollPositions(eventMockup, (-0.2) * deltaY);
    } else if (parentHolder == leftOverlay) {
      this.syncScrollPositions(eventMockup, (-0.2) * deltaX);
    }
    return false;
  },
  syncScrollPositions: function(event) {
    var fakeScrollValue = arguments[1] !== (void 0) ? arguments[1] : null;
    if (this.destroyed) {
      return;
    }
    if (arguments.length === 0) {
      this.syncScrollWithMaster();
      return;
    }
    var master = this.mainTableScrollableElement;
    var target = event.target;
    var tempScrollValue = 0;
    var scrollValueChanged = false;
    var topOverlay;
    var leftOverlay;
    if (this.topOverlay.needFullRender) {
      topOverlay = this.topOverlay.clone.wtTable.holder;
    }
    if (this.leftOverlay.needFullRender) {
      leftOverlay = this.leftOverlay.clone.wtTable.holder;
    }
    if (target === document) {
      target = window;
    }
    if (target === master) {
      tempScrollValue = dom.getScrollLeft(target);
      if (this.overlayScrollPositions.master.left !== tempScrollValue) {
        this.overlayScrollPositions.master.left = tempScrollValue;
        scrollValueChanged = true;
        if (topOverlay) {
          topOverlay.scrollLeft = tempScrollValue;
        }
      }
      tempScrollValue = dom.getScrollTop(target);
      if (this.overlayScrollPositions.master.top !== tempScrollValue) {
        this.overlayScrollPositions.master.top = tempScrollValue;
        scrollValueChanged = true;
        if (leftOverlay) {
          leftOverlay.scrollTop = tempScrollValue;
        }
      }
    } else if (target === topOverlay) {
      tempScrollValue = dom.getScrollLeft(target);
      if (this.overlayScrollPositions.top.left !== tempScrollValue) {
        this.overlayScrollPositions.top.left = tempScrollValue;
        scrollValueChanged = true;
        master.scrollLeft = tempScrollValue;
      }
      if (fakeScrollValue !== null) {
        scrollValueChanged = true;
        master.scrollTop += fakeScrollValue;
      }
    } else if (target === leftOverlay) {
      tempScrollValue = dom.getScrollTop(target);
      if (this.overlayScrollPositions.left.top !== tempScrollValue) {
        this.overlayScrollPositions.left.top = tempScrollValue;
        scrollValueChanged = true;
        master.scrollTop = tempScrollValue;
      }
      if (fakeScrollValue !== null) {
        scrollValueChanged = true;
        master.scrollLeft += fakeScrollValue;
      }
    }
    if (!this.keyPressed && scrollValueChanged && event.type === 'scroll') {
      this.refreshAll();
    }
  },
  syncScrollWithMaster: function() {
    var master = this.topOverlay.mainTableScrollableElement;
    if (this.topOverlay.needFullRender) {
      this.topOverlay.clone.wtTable.holder.scrollLeft = master.scrollLeft;
    }
    if (this.leftOverlay.needFullRender) {
      this.leftOverlay.clone.wtTable.holder.scrollTop = master.scrollTop;
    }
  },
  destroy: function() {
    this.eventManager.clear();
    this.topOverlay.destroy();
    this.leftOverlay.destroy();
    if (this.topLeftCornerOverlay) {
      this.topLeftCornerOverlay.destroy();
    }
    if (this.debug) {
      this.debug.destroy();
    }
    this.destroyed = true;
  },
  refresh: function() {
    var fastDraw = arguments[0] !== (void 0) ? arguments[0] : false;
    if (this.topOverlay.isElementSizesAdjusted && this.leftOverlay.isElementSizesAdjusted) {
      var container = this.wot.wtTable.wtRootElement.parentNode || this.wot.wtTable.wtRootElement;
      var width = container.clientWidth;
      var height = container.clientHeight;
      if (width !== this.spreaderLastSize.width || height !== this.spreaderLastSize.height) {
        this.spreaderLastSize.width = width;
        this.spreaderLastSize.height = height;
        this.adjustElementsSize();
      }
    }
    this.leftOverlay.refresh(fastDraw);
    this.topOverlay.refresh(fastDraw);
    if (this.topLeftCornerOverlay) {
      this.topLeftCornerOverlay.refresh(fastDraw);
    }
    if (this.debug) {
      this.debug.refresh(fastDraw);
    }
  },
  adjustElementsSize: function() {
    var totalColumns = this.wot.getSetting('totalColumns');
    var totalRows = this.wot.getSetting('totalRows');
    var headerRowSize = this.wot.wtViewport.getRowHeaderWidth();
    var headerColumnSize = this.wot.wtViewport.getColumnHeaderHeight();
    var hiderStyle = this.wot.wtTable.hider.style;
    hiderStyle.width = (headerRowSize + this.leftOverlay.sumCellSizes(0, totalColumns)) + 'px';
    hiderStyle.height = (headerColumnSize + this.topOverlay.sumCellSizes(0, totalRows) + 1) + 'px';
    this.topOverlay.adjustElementsSize();
    this.leftOverlay.adjustElementsSize();
  },
  applyToDOM: function() {
    if (!this.topOverlay.isElementSizesAdjusted || !this.leftOverlay.isElementSizesAdjusted) {
      this.adjustElementsSize();
    }
    this.topOverlay.applyToDOM();
    this.leftOverlay.applyToDOM();
  }
}, {});
;
window.WalkontableOverlays = WalkontableOverlays;


//# 
},{"./../../../dom.js":27,"./../../../eventManager.js":41,"./overlay/corner.js":12,"./overlay/debug.js":13,"./overlay/left.js":14,"./overlay/top.js":15}],17:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableScroll: {get: function() {
      return WalkontableScroll;
    }},
  __esModule: {value: true}
});
var WalkontableScroll = function WalkontableScroll(wotInstance) {
  this.wot = wotInstance;
  this.instance = wotInstance;
};
($traceurRuntime.createClass)(WalkontableScroll, {scrollViewport: function(coords) {
    if (!this.wot.drawn) {
      return;
    }
    var totalRows = this.wot.getSetting('totalRows');
    var totalColumns = this.wot.getSetting('totalColumns');
    if (coords.row < 0 || coords.row > totalRows - 1) {
      throw new Error('row ' + coords.row + ' does not exist');
    }
    if (coords.col < 0 || coords.col > totalColumns - 1) {
      throw new Error('column ' + coords.col + ' does not exist');
    }
    if (coords.row > this.instance.wtTable.getLastVisibleRow()) {
      this.wot.wtOverlays.topOverlay.scrollTo(coords.row, true);
    } else if (coords.row >= this.instance.getSetting('fixedRowsTop') && coords.row < this.instance.wtTable.getFirstVisibleRow()) {
      this.wot.wtOverlays.topOverlay.scrollTo(coords.row);
    }
    if (coords.col > this.instance.wtTable.getLastVisibleColumn()) {
      this.wot.wtOverlays.leftOverlay.scrollTo(coords.col, true);
    } else if (coords.col >= this.instance.getSetting('fixedColumnsLeft') && coords.col < this.instance.wtTable.getFirstVisibleColumn()) {
      this.wot.wtOverlays.leftOverlay.scrollTo(coords.col);
    }
  }}, {});
;
window.WalkontableScroll = WalkontableScroll;


//# 
},{}],18:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableSelection: {get: function() {
      return WalkontableSelection;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47__46__46__47_dom_46_js__,
    $__border_46_js__,
    $__cell_47_coords_46_js__,
    $__cell_47_range_46_js__;
var dom = ($___46__46__47__46__46__47__46__46__47_dom_46_js__ = require("./../../../dom.js"), $___46__46__47__46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47__46__46__47_dom_46_js__});
var WalkontableBorder = ($__border_46_js__ = require("./border.js"), $__border_46_js__ && $__border_46_js__.__esModule && $__border_46_js__ || {default: $__border_46_js__}).WalkontableBorder;
var WalkontableCellCoords = ($__cell_47_coords_46_js__ = require("./cell/coords.js"), $__cell_47_coords_46_js__ && $__cell_47_coords_46_js__.__esModule && $__cell_47_coords_46_js__ || {default: $__cell_47_coords_46_js__}).WalkontableCellCoords;
var WalkontableCellRange = ($__cell_47_range_46_js__ = require("./cell/range.js"), $__cell_47_range_46_js__ && $__cell_47_range_46_js__.__esModule && $__cell_47_range_46_js__ || {default: $__cell_47_range_46_js__}).WalkontableCellRange;
var WalkontableSelection = function WalkontableSelection(settings, cellRange) {
  this.settings = settings;
  this.cellRange = cellRange || null;
  this.instanceBorders = {};
};
($traceurRuntime.createClass)(WalkontableSelection, {
  getBorder: function(wotInstance) {
    if (this.instanceBorders[wotInstance.guid]) {
      return this.instanceBorders[wotInstance.guid];
    }
    this.instanceBorders[wotInstance.guid] = new WalkontableBorder(wotInstance, this.settings);
  },
  isEmpty: function() {
    return this.cellRange === null;
  },
  add: function(coords) {
    if (this.isEmpty()) {
      this.cellRange = new WalkontableCellRange(coords, coords, coords);
    } else {
      this.cellRange.expand(coords);
    }
  },
  replace: function(oldCoords, newCoords) {
    if (!this.isEmpty()) {
      if (this.cellRange.from.isEqual(oldCoords)) {
        this.cellRange.from = newCoords;
        return true;
      }
      if (this.cellRange.to.isEqual(oldCoords)) {
        this.cellRange.to = newCoords;
        return true;
      }
    }
    return false;
  },
  clear: function() {
    this.cellRange = null;
  },
  getCorners: function() {
    var topLeft = this.cellRange.getTopLeftCorner();
    var bottomRight = this.cellRange.getBottomRightCorner();
    return [topLeft.row, topLeft.col, bottomRight.row, bottomRight.col];
  },
  addClassAtCoords: function(wotInstance, sourceRow, sourceColumn, className) {
    var TD = wotInstance.wtTable.getCell(new WalkontableCellCoords(sourceRow, sourceColumn));
    if (typeof TD === 'object') {
      dom.addClass(TD, className);
    }
  },
  draw: function(wotInstance) {
    if (this.isEmpty()) {
      if (this.settings.border) {
        var border = this.getBorder(wotInstance);
        if (border) {
          border.disappear();
        }
      }
      return;
    }
    var renderedRows = wotInstance.wtTable.getRenderedRowsCount();
    var renderedColumns = wotInstance.wtTable.getRenderedColumnsCount();
    var corners = this.getCorners();
    var sourceRow,
        sourceCol,
        TH;
    for (var column = 0; column < renderedColumns; column++) {
      sourceCol = wotInstance.wtTable.columnFilter.renderedToSource(column);
      if (sourceCol >= corners[1] && sourceCol <= corners[3]) {
        TH = wotInstance.wtTable.getColumnHeader(sourceCol);
        if (TH && this.settings.highlightColumnClassName) {
          dom.addClass(TH, this.settings.highlightColumnClassName);
        }
      }
    }
    for (var row = 0; row < renderedRows; row++) {
      sourceRow = wotInstance.wtTable.rowFilter.renderedToSource(row);
      if (sourceRow >= corners[0] && sourceRow <= corners[2]) {
        TH = wotInstance.wtTable.getRowHeader(sourceRow);
        if (TH && this.settings.highlightRowClassName) {
          dom.addClass(TH, this.settings.highlightRowClassName);
        }
      }
      for (var column$__4 = 0; column$__4 < renderedColumns; column$__4++) {
        sourceCol = wotInstance.wtTable.columnFilter.renderedToSource(column$__4);
        if (sourceRow >= corners[0] && sourceRow <= corners[2] && sourceCol >= corners[1] && sourceCol <= corners[3]) {
          if (this.settings.className) {
            this.addClassAtCoords(wotInstance, sourceRow, sourceCol, this.settings.className);
          }
        } else if (sourceRow >= corners[0] && sourceRow <= corners[2]) {
          if (this.settings.highlightRowClassName) {
            this.addClassAtCoords(wotInstance, sourceRow, sourceCol, this.settings.highlightRowClassName);
          }
        } else if (sourceCol >= corners[1] && sourceCol <= corners[3]) {
          if (this.settings.highlightColumnClassName) {
            this.addClassAtCoords(wotInstance, sourceRow, sourceCol, this.settings.highlightColumnClassName);
          }
        }
      }
    }
    wotInstance.getSetting('onBeforeDrawBorders', corners, this.settings.className);
    if (this.settings.border) {
      var border$__5 = this.getBorder(wotInstance);
      if (border$__5) {
        border$__5.appear(corners);
      }
    }
  }
}, {});
;
window.WalkontableSelection = WalkontableSelection;


//# 
},{"./../../../dom.js":27,"./border.js":2,"./cell/coords.js":5,"./cell/range.js":6}],19:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableSettings: {get: function() {
      return WalkontableSettings;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47__46__46__47_dom_46_js__;
var dom = ($___46__46__47__46__46__47__46__46__47_dom_46_js__ = require("./../../../dom.js"), $___46__46__47__46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47__46__46__47_dom_46_js__});
var WalkontableSettings = function WalkontableSettings(wotInstance, settings) {
  var $__0 = this;
  this.wot = wotInstance;
  this.instance = wotInstance;
  this.defaults = {
    table: void 0,
    debug: false,
    stretchH: 'none',
    currentRowClassName: null,
    currentColumnClassName: null,
    data: void 0,
    fixedColumnsLeft: 0,
    fixedRowsTop: 0,
    rowHeaders: function() {
      return [];
    },
    columnHeaders: function() {
      return [];
    },
    totalRows: void 0,
    totalColumns: void 0,
    cellRenderer: (function(row, column, TD) {
      var cellData = $__0.getSetting('data', row, column);
      dom.fastInnerText(TD, cellData === void 0 || cellData === null ? '' : cellData);
    }),
    columnWidth: function(col) {
      return;
    },
    rowHeight: function(row) {
      return;
    },
    defaultRowHeight: 23,
    defaultColumnWidth: 50,
    selections: null,
    hideBorderOnMouseDownOver: false,
    viewportRowCalculatorOverride: null,
    viewportColumnCalculatorOverride: null,
    onCellMouseDown: null,
    onCellMouseOver: null,
    onCellDblClick: null,
    onCellCornerMouseDown: null,
    onCellCornerDblClick: null,
    beforeDraw: null,
    onDraw: null,
    onBeforeDrawBorders: null,
    onScrollVertically: null,
    onScrollHorizontally: null,
    onBeforeTouchScroll: null,
    onAfterMomentumScroll: null,
    scrollbarWidth: 10,
    scrollbarHeight: 10,
    renderAllRows: false,
    groups: false
  };
  this.settings = {};
  for (var i in this.defaults) {
    if (this.defaults.hasOwnProperty(i)) {
      if (settings[i] !== void 0) {
        this.settings[i] = settings[i];
      } else if (this.defaults[i] === void 0) {
        throw new Error('A required setting "' + i + '" was not provided');
      } else {
        this.settings[i] = this.defaults[i];
      }
    }
  }
};
($traceurRuntime.createClass)(WalkontableSettings, {
  update: function(settings, value) {
    if (value === void 0) {
      for (var i in settings) {
        if (settings.hasOwnProperty(i)) {
          this.settings[i] = settings[i];
        }
      }
    } else {
      this.settings[settings] = value;
    }
    return this.wot;
  },
  getSetting: function(key, param1, param2, param3, param4) {
    if (typeof this.settings[key] === 'function') {
      return this.settings[key](param1, param2, param3, param4);
    } else if (param1 !== void 0 && Array.isArray(this.settings[key])) {
      return this.settings[key][param1];
    } else {
      return this.settings[key];
    }
  },
  has: function(key) {
    return !!this.settings[key];
  }
}, {});
;
window.WalkontableSettings = WalkontableSettings;


//# 
},{"./../../../dom.js":27}],20:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableTable: {get: function() {
      return WalkontableTable;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47__46__46__47_dom_46_js__,
    $__cell_47_coords_46_js__,
    $__cell_47_range_46_js__,
    $__filter_47_column_46_js__,
    $__overlay_47_corner_46_js__,
    $__overlay_47_debug_46_js__,
    $__overlay_47_left_46_js__,
    $__filter_47_row_46_js__,
    $__tableRenderer_46_js__,
    $__overlay_47_top_46_js__;
var dom = ($___46__46__47__46__46__47__46__46__47_dom_46_js__ = require("./../../../dom.js"), $___46__46__47__46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47__46__46__47_dom_46_js__});
var WalkontableCellCoords = ($__cell_47_coords_46_js__ = require("./cell/coords.js"), $__cell_47_coords_46_js__ && $__cell_47_coords_46_js__.__esModule && $__cell_47_coords_46_js__ || {default: $__cell_47_coords_46_js__}).WalkontableCellCoords;
var WalkontableCellRange = ($__cell_47_range_46_js__ = require("./cell/range.js"), $__cell_47_range_46_js__ && $__cell_47_range_46_js__.__esModule && $__cell_47_range_46_js__ || {default: $__cell_47_range_46_js__}).WalkontableCellRange;
var WalkontableColumnFilter = ($__filter_47_column_46_js__ = require("./filter/column.js"), $__filter_47_column_46_js__ && $__filter_47_column_46_js__.__esModule && $__filter_47_column_46_js__ || {default: $__filter_47_column_46_js__}).WalkontableColumnFilter;
var WalkontableCornerOverlay = ($__overlay_47_corner_46_js__ = require("./overlay/corner.js"), $__overlay_47_corner_46_js__ && $__overlay_47_corner_46_js__.__esModule && $__overlay_47_corner_46_js__ || {default: $__overlay_47_corner_46_js__}).WalkontableCornerOverlay;
var WalkontableDebugOverlay = ($__overlay_47_debug_46_js__ = require("./overlay/debug.js"), $__overlay_47_debug_46_js__ && $__overlay_47_debug_46_js__.__esModule && $__overlay_47_debug_46_js__ || {default: $__overlay_47_debug_46_js__}).WalkontableDebugOverlay;
var WalkontableLeftOverlay = ($__overlay_47_left_46_js__ = require("./overlay/left.js"), $__overlay_47_left_46_js__ && $__overlay_47_left_46_js__.__esModule && $__overlay_47_left_46_js__ || {default: $__overlay_47_left_46_js__}).WalkontableLeftOverlay;
var WalkontableRowFilter = ($__filter_47_row_46_js__ = require("./filter/row.js"), $__filter_47_row_46_js__ && $__filter_47_row_46_js__.__esModule && $__filter_47_row_46_js__ || {default: $__filter_47_row_46_js__}).WalkontableRowFilter;
var WalkontableTableRenderer = ($__tableRenderer_46_js__ = require("./tableRenderer.js"), $__tableRenderer_46_js__ && $__tableRenderer_46_js__.__esModule && $__tableRenderer_46_js__ || {default: $__tableRenderer_46_js__}).WalkontableTableRenderer;
var WalkontableTopOverlay = ($__overlay_47_top_46_js__ = require("./overlay/top.js"), $__overlay_47_top_46_js__ && $__overlay_47_top_46_js__.__esModule && $__overlay_47_top_46_js__ || {default: $__overlay_47_top_46_js__}).WalkontableTopOverlay;
function WalkontableTable(instance, table) {
  this.instance = instance;
  this.TABLE = table;
  dom.removeTextNodes(this.TABLE);
  var parent = this.TABLE.parentNode;
  if (!parent || parent.nodeType !== 1 || !dom.hasClass(parent, 'wtHolder')) {
    var spreader = document.createElement('DIV');
    spreader.className = 'wtSpreader';
    if (parent) {
      parent.insertBefore(spreader, this.TABLE);
    }
    spreader.appendChild(this.TABLE);
  }
  this.spreader = this.TABLE.parentNode;
  this.spreader.style.position = 'relative';
  parent = this.spreader.parentNode;
  if (!parent || parent.nodeType !== 1 || !dom.hasClass(parent, 'wtHolder')) {
    var hider = document.createElement('DIV');
    hider.className = 'wtHider';
    if (parent) {
      parent.insertBefore(hider, this.spreader);
    }
    hider.appendChild(this.spreader);
  }
  this.hider = this.spreader.parentNode;
  parent = this.hider.parentNode;
  if (!parent || parent.nodeType !== 1 || !dom.hasClass(parent, 'wtHolder')) {
    var holder = document.createElement('DIV');
    holder.style.position = 'relative';
    holder.className = 'wtHolder';
    if (parent) {
      parent.insertBefore(holder, this.hider);
    }
    if (!instance.cloneSource) {
      holder.parentNode.className += 'ht_master handsontable';
    }
    holder.appendChild(this.hider);
  }
  this.holder = this.hider.parentNode;
  this.wtRootElement = this.holder.parentNode;
  this.alignOverlaysWithTrimmingContainer();
  this.TBODY = this.TABLE.getElementsByTagName('TBODY')[0];
  if (!this.TBODY) {
    this.TBODY = document.createElement('TBODY');
    this.TABLE.appendChild(this.TBODY);
  }
  this.THEAD = this.TABLE.getElementsByTagName('THEAD')[0];
  if (!this.THEAD) {
    this.THEAD = document.createElement('THEAD');
    this.TABLE.insertBefore(this.THEAD, this.TBODY);
  }
  this.COLGROUP = this.TABLE.getElementsByTagName('COLGROUP')[0];
  if (!this.COLGROUP) {
    this.COLGROUP = document.createElement('COLGROUP');
    this.TABLE.insertBefore(this.COLGROUP, this.THEAD);
  }
  if (this.instance.getSetting('columnHeaders').length) {
    if (!this.THEAD.childNodes.length) {
      var TR = document.createElement('TR');
      this.THEAD.appendChild(TR);
    }
  }
  this.colgroupChildrenLength = this.COLGROUP.childNodes.length;
  this.theadChildrenLength = this.THEAD.firstChild ? this.THEAD.firstChild.childNodes.length : 0;
  this.tbodyChildrenLength = this.TBODY.childNodes.length;
  this.rowFilter = null;
  this.columnFilter = null;
}
WalkontableTable.prototype.alignOverlaysWithTrimmingContainer = function() {
  var trimmingElement = dom.getTrimmingContainer(this.wtRootElement);
  if (!this.isWorkingOnClone()) {
    this.holder.parentNode.style.position = 'relative';
    if (trimmingElement !== window) {
      this.holder.style.width = dom.getStyle(trimmingElement, 'width');
      this.holder.style.height = dom.getStyle(trimmingElement, 'height');
      this.holder.style.overflow = '';
    } else {
      this.holder.style.overflow = 'visible';
      this.wtRootElement.style.overflow = 'visible';
    }
  }
};
WalkontableTable.prototype.isWorkingOnClone = function() {
  return !!this.instance.cloneSource;
};
WalkontableTable.prototype.draw = function(fastDraw) {
  if (!this.isWorkingOnClone()) {
    this.holderOffset = dom.offset(this.holder);
    fastDraw = this.instance.wtViewport.createRenderCalculators(fastDraw);
  }
  if (!fastDraw) {
    if (this.isWorkingOnClone()) {
      this.tableOffset = this.instance.cloneSource.wtTable.tableOffset;
    } else {
      this.tableOffset = dom.offset(this.TABLE);
    }
    var startRow;
    if (this.instance.cloneOverlay instanceof WalkontableDebugOverlay || this.instance.cloneOverlay instanceof WalkontableTopOverlay || this.instance.cloneOverlay instanceof WalkontableCornerOverlay) {
      startRow = 0;
    } else {
      startRow = this.instance.wtViewport.rowsRenderCalculator.startRow;
    }
    var startColumn;
    if (this.instance.cloneOverlay instanceof WalkontableDebugOverlay || this.instance.cloneOverlay instanceof WalkontableLeftOverlay || this.instance.cloneOverlay instanceof WalkontableCornerOverlay) {
      startColumn = 0;
    } else {
      startColumn = this.instance.wtViewport.columnsRenderCalculator.startColumn;
    }
    this.rowFilter = new WalkontableRowFilter(startRow, this.instance.getSetting('totalRows'), this.instance.getSetting('columnHeaders').length);
    this.columnFilter = new WalkontableColumnFilter(startColumn, this.instance.getSetting('totalColumns'), this.instance.getSetting('rowHeaders').length);
    this._doDraw();
    this.alignOverlaysWithTrimmingContainer();
  } else {
    if (!this.isWorkingOnClone()) {
      this.instance.wtViewport.createVisibleCalculators();
    }
    if (this.instance.wtOverlays) {
      this.instance.wtOverlays.refresh(true);
    }
  }
  this.refreshSelections(fastDraw);
  if (!this.isWorkingOnClone()) {
    this.instance.wtOverlays.topOverlay.resetFixedPosition();
    this.instance.wtOverlays.leftOverlay.resetFixedPosition();
    if (this.instance.wtOverlays.topLeftCornerOverlay) {
      this.instance.wtOverlays.topLeftCornerOverlay.resetFixedPosition();
    }
  }
  this.instance.drawn = true;
  return this;
};
WalkontableTable.prototype._doDraw = function() {
  var wtRenderer = new WalkontableTableRenderer(this);
  wtRenderer.render();
};
WalkontableTable.prototype.removeClassFromCells = function(className) {
  var nodes = this.TABLE.querySelectorAll('.' + className);
  for (var i = 0,
      ilen = nodes.length; i < ilen; i++) {
    dom.removeClass(nodes[i], className);
  }
};
WalkontableTable.prototype.refreshSelections = function(fastDraw) {
  var i,
      len;
  if (!this.instance.selections) {
    return;
  }
  len = this.instance.selections.length;
  if (fastDraw) {
    for (i = 0; i < len; i++) {
      if (this.instance.selections[i].settings.className) {
        this.removeClassFromCells(this.instance.selections[i].settings.className);
      }
      if (this.instance.selections[i].settings.highlightRowClassName) {
        this.removeClassFromCells(this.instance.selections[i].settings.highlightRowClassName);
      }
      if (this.instance.selections[i].settings.highlightColumnClassName) {
        this.removeClassFromCells(this.instance.selections[i].settings.highlightColumnClassName);
      }
    }
  }
  for (i = 0; i < len; i++) {
    this.instance.selections[i].draw(this.instance, fastDraw);
  }
};
WalkontableTable.prototype.getCell = function(coords) {
  if (this.isRowBeforeRenderedRows(coords.row)) {
    return -1;
  } else if (this.isRowAfterRenderedRows(coords.row)) {
    return -2;
  }
  var TR = this.TBODY.childNodes[this.rowFilter.sourceToRendered(coords.row)];
  if (TR) {
    return TR.childNodes[this.columnFilter.sourceColumnToVisibleRowHeadedColumn(coords.col)];
  }
};
WalkontableTable.prototype.getColumnHeader = function(col, level) {
  if (!level) {
    level = 0;
  }
  var TR = this.THEAD.childNodes[level];
  if (TR) {
    return TR.childNodes[this.columnFilter.sourceColumnToVisibleRowHeadedColumn(col)];
  }
};
WalkontableTable.prototype.getRowHeader = function(row) {
  if (this.columnFilter.sourceColumnToVisibleRowHeadedColumn(0) === 0) {
    return null;
  }
  var TR = this.TBODY.childNodes[this.rowFilter.sourceToRendered(row)];
  if (TR) {
    return TR.childNodes[0];
  }
};
WalkontableTable.prototype.getCoords = function(TD) {
  var TR = TD.parentNode;
  var row = dom.index(TR);
  if (TR.parentNode === this.THEAD) {
    row = this.rowFilter.visibleColHeadedRowToSourceRow(row);
  } else {
    row = this.rowFilter.renderedToSource(row);
  }
  return new WalkontableCellCoords(row, this.columnFilter.visibleRowHeadedColumnToSourceColumn(TD.cellIndex));
};
WalkontableTable.prototype.getTrForRow = function(row) {
  return this.TBODY.childNodes[this.rowFilter.sourceToRendered(row)];
};
WalkontableTable.prototype.getFirstRenderedRow = function() {
  return this.instance.wtViewport.rowsRenderCalculator.startRow;
};
WalkontableTable.prototype.getFirstVisibleRow = function() {
  return this.instance.wtViewport.rowsVisibleCalculator.startRow;
};
WalkontableTable.prototype.getFirstRenderedColumn = function() {
  return this.instance.wtViewport.columnsRenderCalculator.startColumn;
};
WalkontableTable.prototype.getFirstVisibleColumn = function() {
  return this.instance.wtViewport.columnsVisibleCalculator.startColumn;
};
WalkontableTable.prototype.getLastRenderedRow = function() {
  return this.instance.wtViewport.rowsRenderCalculator.endRow;
};
WalkontableTable.prototype.getLastVisibleRow = function() {
  return this.instance.wtViewport.rowsVisibleCalculator.endRow;
};
WalkontableTable.prototype.getLastRenderedColumn = function() {
  return this.instance.wtViewport.columnsRenderCalculator.endColumn;
};
WalkontableTable.prototype.getLastVisibleColumn = function() {
  return this.instance.wtViewport.columnsVisibleCalculator.endColumn;
};
WalkontableTable.prototype.isRowBeforeRenderedRows = function(r) {
  return (this.rowFilter.sourceToRendered(r) < 0 && r >= 0);
};
WalkontableTable.prototype.isRowAfterViewport = function(r) {
  return (r > this.getLastVisibleRow());
};
WalkontableTable.prototype.isRowAfterRenderedRows = function(r) {
  return (r > this.getLastRenderedRow());
};
WalkontableTable.prototype.isColumnBeforeViewport = function(c) {
  return (this.columnFilter.sourceToRendered(c) < 0 && c >= 0);
};
WalkontableTable.prototype.isColumnAfterViewport = function(c) {
  return (c > this.getLastVisibleColumn());
};
WalkontableTable.prototype.isLastRowFullyVisible = function() {
  return (this.getLastVisibleRow() === this.getLastRenderedRow());
};
WalkontableTable.prototype.isLastColumnFullyVisible = function() {
  return (this.getLastVisibleColumn() === this.getLastRenderedColumn);
};
WalkontableTable.prototype.getRenderedColumnsCount = function() {
  if (this.instance.cloneOverlay instanceof WalkontableDebugOverlay) {
    return this.instance.getSetting('totalColumns');
  } else if (this.instance.cloneOverlay instanceof WalkontableLeftOverlay || this.instance.cloneOverlay instanceof WalkontableCornerOverlay) {
    return this.instance.getSetting('fixedColumnsLeft');
  } else {
    return this.instance.wtViewport.columnsRenderCalculator.count;
  }
};
WalkontableTable.prototype.getRenderedRowsCount = function() {
  if (this.instance.cloneOverlay instanceof WalkontableDebugOverlay) {
    return this.instance.getSetting('totalRows');
  } else if (this.instance.cloneOverlay instanceof WalkontableTopOverlay || this.instance.cloneOverlay instanceof WalkontableCornerOverlay) {
    return this.instance.getSetting('fixedRowsTop');
  }
  return this.instance.wtViewport.rowsRenderCalculator.count;
};
WalkontableTable.prototype.getVisibleRowsCount = function() {
  return this.instance.wtViewport.rowsVisibleCalculator.count;
};
WalkontableTable.prototype.allRowsInViewport = function() {
  return this.instance.getSetting('totalRows') == this.getVisibleRowsCount();
};
WalkontableTable.prototype.getRowHeight = function(sourceRow) {
  var height = this.instance.wtSettings.settings.rowHeight(sourceRow),
      oversizedHeight = this.instance.wtViewport.oversizedRows[sourceRow];
  if (oversizedHeight !== void 0) {
    height = height ? Math.max(height, oversizedHeight) : oversizedHeight;
  }
  return height;
};
WalkontableTable.prototype.getColumnHeaderHeight = function(level) {
  var height = this.instance.wtSettings.settings.defaultRowHeight,
      oversizedHeight = this.instance.wtViewport.oversizedColumnHeaders[level];
  if (oversizedHeight !== void 0) {
    height = height ? Math.max(height, oversizedHeight) : oversizedHeight;
  }
  return height;
};
WalkontableTable.prototype.getVisibleColumnsCount = function() {
  return this.instance.wtViewport.columnsVisibleCalculator.count;
};
WalkontableTable.prototype.allColumnsInViewport = function() {
  return this.instance.getSetting('totalColumns') == this.getVisibleColumnsCount();
};
WalkontableTable.prototype.getColumnWidth = function(sourceColumn) {
  var width = this.instance.wtSettings.settings.columnWidth;
  if (typeof width === 'function') {
    width = width(sourceColumn);
  } else if (typeof width === 'object') {
    width = width[sourceColumn];
  }
  var oversizedWidth = this.instance.wtViewport.oversizedCols[sourceColumn];
  if (oversizedWidth !== void 0) {
    width = width ? Math.max(width, oversizedWidth) : oversizedWidth;
  }
  return width;
};
WalkontableTable.prototype.getStretchedColumnWidth = function(sourceColumn) {
  var width = this.getColumnWidth(sourceColumn) || this.instance.wtSettings.settings.defaultColumnWidth,
      calculator = this.instance.wtViewport.columnsRenderCalculator,
      stretchedWidth;
  if (calculator) {
    stretchedWidth = calculator.getStretchedColumnWidth(sourceColumn, width);
    if (stretchedWidth) {
      width = stretchedWidth;
    }
  }
  return width;
};
;
window.WalkontableTable = WalkontableTable;


//# 
},{"./../../../dom.js":27,"./cell/coords.js":5,"./cell/range.js":6,"./filter/column.js":9,"./filter/row.js":10,"./overlay/corner.js":12,"./overlay/debug.js":13,"./overlay/left.js":14,"./overlay/top.js":15,"./tableRenderer.js":21}],21:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableTableRenderer: {get: function() {
      return WalkontableTableRenderer;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47__46__46__47_dom_46_js__;
var dom = ($___46__46__47__46__46__47__46__46__47_dom_46_js__ = require("./../../../dom.js"), $___46__46__47__46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47__46__46__47_dom_46_js__});
var isRenderedColumnHeaders = {};
var WalkontableTableRenderer = function WalkontableTableRenderer(wtTable) {
  this.wtTable = wtTable;
  this.wot = wtTable.instance;
  this.instance = wtTable.instance;
  this.rowFilter = wtTable.rowFilter;
  this.columnFilter = wtTable.columnFilter;
  this.TABLE = wtTable.TABLE;
  this.THEAD = wtTable.THEAD;
  this.TBODY = wtTable.TBODY;
  this.COLGROUP = wtTable.COLGROUP;
  this.rowHeaders = [];
  this.rowHeaderCount = 0;
  this.columnHeaders = [];
  this.columnHeaderCount = 0;
  this.fixedRowsTop = 0;
};
($traceurRuntime.createClass)(WalkontableTableRenderer, {
  render: function() {
    if (!this.wtTable.isWorkingOnClone()) {
      this.wot.getSetting('beforeDraw', true);
    }
    this.rowHeaders = this.wot.getSetting('rowHeaders');
    this.rowHeaderCount = this.rowHeaders.length;
    this.fixedRowsTop = this.wot.getSetting('fixedRowsTop');
    this.columnHeaders = this.wot.getSetting('columnHeaders');
    this.columnHeaderCount = this.columnHeaders.length;
    var columnsToRender = this.wtTable.getRenderedColumnsCount();
    var rowsToRender = this.wtTable.getRenderedRowsCount();
    var totalColumns = this.wot.getSetting('totalColumns');
    var totalRows = this.wot.getSetting('totalRows');
    var workspaceWidth;
    var adjusted = false;
    if (totalColumns > 0) {
      this.adjustAvailableNodes();
      adjusted = true;
      this.renderColGroups();
      this.renderColumnHeaders();
      this.renderRows(totalRows, rowsToRender, columnsToRender);
      if (!this.wtTable.isWorkingOnClone()) {
        workspaceWidth = this.wot.wtViewport.getWorkspaceWidth();
        this.wot.wtViewport.containerWidth = null;
      } else {
        this.adjustColumnHeaderHeights();
      }
      this.adjustColumnWidths(columnsToRender);
    }
    if (!adjusted) {
      this.adjustAvailableNodes();
    }
    this.removeRedundantRows(rowsToRender);
    if (!this.wtTable.isWorkingOnClone()) {
      this.markOversizedRows();
      this.wot.wtViewport.createVisibleCalculators();
      this.wot.wtOverlays.refresh(false);
      this.wot.wtOverlays.applyToDOM();
      if (workspaceWidth !== this.wot.wtViewport.getWorkspaceWidth()) {
        this.wot.wtViewport.containerWidth = null;
        var firstRendered = this.wtTable.getFirstRenderedColumn();
        var lastRendered = this.wtTable.getLastRenderedColumn();
        for (var i = firstRendered; i < lastRendered; i++) {
          var width = this.wtTable.getStretchedColumnWidth(i);
          var renderedIndex = this.columnFilter.sourceToRendered(i);
          this.COLGROUP.childNodes[renderedIndex + this.rowHeaderCount].style.width = width + 'px';
        }
      }
      this.wot.getSetting('onDraw', true);
    }
  },
  removeRedundantRows: function(renderedRowsCount) {
    while (this.wtTable.tbodyChildrenLength > renderedRowsCount) {
      this.TBODY.removeChild(this.TBODY.lastChild);
      this.wtTable.tbodyChildrenLength--;
    }
  },
  renderRows: function(totalRows, rowsToRender, columnsToRender) {
    var lastTD,
        TR;
    var visibleRowIndex = 0;
    var sourceRowIndex = this.rowFilter.renderedToSource(visibleRowIndex);
    var isWorkingOnClone = this.wtTable.isWorkingOnClone();
    while (sourceRowIndex < totalRows && sourceRowIndex >= 0) {
      if (visibleRowIndex > 1000) {
        throw new Error('Security brake: Too much TRs. Please define height for your table, which will enforce scrollbars.');
      }
      if (rowsToRender !== void 0 && visibleRowIndex === rowsToRender) {
        break;
      }
      TR = this.getOrCreateTrForRow(visibleRowIndex, TR);
      this.renderRowHeaders(sourceRowIndex, TR);
      this.adjustColumns(TR, columnsToRender + this.rowHeaderCount);
      lastTD = this.renderCells(sourceRowIndex, TR, columnsToRender);
      if (!isWorkingOnClone) {
        this.resetOversizedRow(sourceRowIndex);
      }
      if (TR.firstChild) {
        var height = this.wot.wtTable.getRowHeight(sourceRowIndex);
        if (height) {
          TR.firstChild.style.height = height + 'px';
        } else {
          TR.firstChild.style.height = '';
        }
      }
      visibleRowIndex++;
      sourceRowIndex = this.rowFilter.renderedToSource(visibleRowIndex);
    }
  },
  resetOversizedRow: function(sourceRow) {
    if (this.wot.wtViewport.oversizedRows && this.wot.wtViewport.oversizedRows[sourceRow]) {
      this.wot.wtViewport.oversizedRows[sourceRow] = void 0;
    }
  },
  markOversizedRows: function() {
    var rowCount = this.instance.wtTable.TBODY.childNodes.length;
    var expectedTableHeight = rowCount * this.instance.wtSettings.settings.defaultRowHeight;
    var actualTableHeight = dom.innerHeight(this.instance.wtTable.TBODY) - 1;
    var previousRowHeight;
    var rowInnerHeight;
    var sourceRowIndex;
    var currentTr;
    var rowHeader;
    if (expectedTableHeight === actualTableHeight) {
      return;
    }
    while (rowCount) {
      rowCount--;
      sourceRowIndex = this.instance.wtTable.rowFilter.renderedToSource(rowCount);
      previousRowHeight = this.instance.wtTable.getRowHeight(sourceRowIndex);
      currentTr = this.instance.wtTable.getTrForRow(sourceRowIndex);
      rowHeader = currentTr.querySelector('th');
      if (rowHeader) {
        rowInnerHeight = dom.innerHeight(rowHeader);
      } else {
        rowInnerHeight = dom.innerHeight(currentTr) - 1;
      }
      if ((!previousRowHeight && this.instance.wtSettings.settings.defaultRowHeight < rowInnerHeight || previousRowHeight < rowInnerHeight)) {
        this.instance.wtViewport.oversizedRows[sourceRowIndex] = rowInnerHeight;
      }
    }
  },
  adjustColumnHeaderHeights: function() {
    var columnHeaders = this.wot.getSetting('columnHeaders');
    var childs = this.wot.wtTable.THEAD.childNodes;
    var oversizedCols = this.wot.wtViewport.oversizedColumnHeaders;
    for (var i = 0,
        len = columnHeaders.length; i < len; i++) {
      if (oversizedCols[i]) {
        if (childs[i].childNodes.length === 0) {
          return;
        }
        childs[i].childNodes[0].style.height = oversizedCols[i] + 'px';
      }
    }
  },
  markIfOversizedColumnHeader: function(col) {
    var level = this.wot.getSetting('columnHeaders').length;
    var defaultRowHeight = this.wot.wtSettings.settings.defaultRowHeight;
    var sourceColIndex;
    var previousColHeaderHeight;
    var currentHeader;
    var currentHeaderHeight;
    sourceColIndex = this.wot.wtTable.columnFilter.renderedToSource(col);
    while (level) {
      level--;
      previousColHeaderHeight = this.wot.wtTable.getColumnHeaderHeight(level);
      currentHeader = this.wot.wtTable.getColumnHeader(sourceColIndex, level);
      if (!currentHeader) {
        continue;
      }
      currentHeaderHeight = dom.innerHeight(currentHeader);
      if (!previousColHeaderHeight && defaultRowHeight < currentHeaderHeight || previousColHeaderHeight < currentHeaderHeight) {
        this.wot.wtViewport.oversizedColumnHeaders[level] = currentHeaderHeight;
      }
    }
  },
  renderCells: function(sourceRowIndex, TR, columnsToRender) {
    var TD;
    var sourceColIndex;
    for (var visibleColIndex = 0; visibleColIndex < columnsToRender; visibleColIndex++) {
      sourceColIndex = this.columnFilter.renderedToSource(visibleColIndex);
      if (visibleColIndex === 0) {
        TD = TR.childNodes[this.columnFilter.sourceColumnToVisibleRowHeadedColumn(sourceColIndex)];
      } else {
        TD = TD.nextSibling;
      }
      if (TD.nodeName == 'TH') {
        TD = replaceThWithTd(TD, TR);
      }
      if (!dom.hasClass(TD, 'hide')) {
        TD.className = '';
      }
      TD.removeAttribute('style');
      this.wot.wtSettings.settings.cellRenderer(sourceRowIndex, sourceColIndex, TD);
    }
    return TD;
  },
  adjustColumnWidths: function(columnsToRender) {
    var scrollbarCompensation = 0;
    var sourceInstance = this.wot.cloneSource ? this.wot.cloneSource : this.wot;
    var mainHolder = sourceInstance.wtTable.holder;
    if (mainHolder.offsetHeight < mainHolder.scrollHeight) {
      scrollbarCompensation = dom.getScrollbarWidth();
    }
    this.wot.wtViewport.columnsRenderCalculator.refreshStretching(this.wot.wtViewport.getViewportWidth() - scrollbarCompensation);
    for (var renderedColIndex = 0; renderedColIndex < columnsToRender; renderedColIndex++) {
      var width = this.wtTable.getStretchedColumnWidth(this.columnFilter.renderedToSource(renderedColIndex));
      this.COLGROUP.childNodes[renderedColIndex + this.rowHeaderCount].style.width = width + 'px';
    }
  },
  appendToTbody: function(TR) {
    this.TBODY.appendChild(TR);
    this.wtTable.tbodyChildrenLength++;
  },
  getOrCreateTrForRow: function(rowIndex, currentTr) {
    var TR;
    if (rowIndex >= this.wtTable.tbodyChildrenLength) {
      TR = this.createRow();
      this.appendToTbody(TR);
    } else if (rowIndex === 0) {
      TR = this.TBODY.firstChild;
    } else {
      TR = currentTr.nextSibling;
    }
    return TR;
  },
  createRow: function() {
    var TR = document.createElement('TR');
    for (var visibleColIndex = 0; visibleColIndex < this.rowHeaderCount; visibleColIndex++) {
      TR.appendChild(document.createElement('TH'));
    }
    return TR;
  },
  renderRowHeader: function(row, col, TH) {
    TH.className = '';
    TH.removeAttribute('style');
    this.rowHeaders[col](row, TH, col);
  },
  renderRowHeaders: function(row, TR) {
    for (var TH = TR.firstChild,
        visibleColIndex = 0; visibleColIndex < this.rowHeaderCount; visibleColIndex++) {
      if (!TH) {
        TH = document.createElement('TH');
        TR.appendChild(TH);
      } else if (TH.nodeName == 'TD') {
        TH = replaceTdWithTh(TH, TR);
      }
      this.renderRowHeader(row, visibleColIndex, TH);
      TH = TH.nextSibling;
    }
  },
  adjustAvailableNodes: function() {
    this.adjustColGroups();
    this.adjustThead();
  },
  renderColumnHeaders: function() {
    var overlayName = this.wot.getOverlayName();
    if (!this.columnHeaderCount) {
      return;
    }
    var columnCount = this.wtTable.getRenderedColumnsCount();
    for (var i = 0; i < this.columnHeaderCount; i++) {
      var TR = this.getTrForColumnHeaders(i);
      for (var renderedColumnIndex = (-1) * this.rowHeaderCount; renderedColumnIndex < columnCount; renderedColumnIndex++) {
        var sourceCol = this.columnFilter.renderedToSource(renderedColumnIndex);
        this.renderColumnHeader(i, sourceCol, TR.childNodes[renderedColumnIndex + this.rowHeaderCount]);
        if (!isRenderedColumnHeaders[overlayName] && !this.wtTable.isWorkingOnClone()) {
          this.markIfOversizedColumnHeader(renderedColumnIndex);
        }
      }
    }
    isRenderedColumnHeaders[overlayName] = true;
  },
  adjustColGroups: function() {
    var columnCount = this.wtTable.getRenderedColumnsCount();
    while (this.wtTable.colgroupChildrenLength < columnCount + this.rowHeaderCount) {
      this.COLGROUP.appendChild(document.createElement('COL'));
      this.wtTable.colgroupChildrenLength++;
    }
    while (this.wtTable.colgroupChildrenLength > columnCount + this.rowHeaderCount) {
      this.COLGROUP.removeChild(this.COLGROUP.lastChild);
      this.wtTable.colgroupChildrenLength--;
    }
  },
  adjustThead: function() {
    var columnCount = this.wtTable.getRenderedColumnsCount();
    var TR = this.THEAD.firstChild;
    if (this.columnHeaders.length) {
      for (var i = 0,
          len = this.columnHeaders.length; i < len; i++) {
        TR = this.THEAD.childNodes[i];
        if (!TR) {
          TR = document.createElement('TR');
          this.THEAD.appendChild(TR);
        }
        this.theadChildrenLength = TR.childNodes.length;
        while (this.theadChildrenLength < columnCount + this.rowHeaderCount) {
          TR.appendChild(document.createElement('TH'));
          this.theadChildrenLength++;
        }
        while (this.theadChildrenLength > columnCount + this.rowHeaderCount) {
          TR.removeChild(TR.lastChild);
          this.theadChildrenLength--;
        }
      }
      var theadChildrenLength = this.THEAD.childNodes.length;
      if (theadChildrenLength > this.columnHeaders.length) {
        for (var i$__1 = this.columnHeaders.length; i$__1 < theadChildrenLength; i$__1++) {
          this.THEAD.removeChild(this.THEAD.lastChild);
        }
      }
    } else if (TR) {
      dom.empty(TR);
    }
  },
  getTrForColumnHeaders: function(index) {
    return this.THEAD.childNodes[index];
  },
  renderColumnHeader: function(row, col, TH) {
    TH.className = '';
    TH.removeAttribute('style');
    return this.columnHeaders[row](col, TH, row);
  },
  renderColGroups: function() {
    for (var colIndex = 0; colIndex < this.wtTable.colgroupChildrenLength; colIndex++) {
      if (colIndex < this.rowHeaderCount) {
        dom.addClass(this.COLGROUP.childNodes[colIndex], 'rowHeader');
      } else {
        dom.removeClass(this.COLGROUP.childNodes[colIndex], 'rowHeader');
      }
    }
  },
  adjustColumns: function(TR, desiredCount) {
    var count = TR.childNodes.length;
    while (count < desiredCount) {
      var TD = document.createElement('TD');
      TR.appendChild(TD);
      count++;
    }
    while (count > desiredCount) {
      TR.removeChild(TR.lastChild);
      count--;
    }
  },
  removeRedundantColumns: function(columnsToRender) {
    while (this.wtTable.tbodyChildrenLength > columnsToRender) {
      this.TBODY.removeChild(this.TBODY.lastChild);
      this.wtTable.tbodyChildrenLength--;
    }
  }
}, {});
function replaceTdWithTh(TD, TR) {
  var TH = document.createElement('TH');
  TR.insertBefore(TH, TD);
  TR.removeChild(TD);
  return TH;
}
function replaceThWithTd(TH, TR) {
  var TD = document.createElement('TD');
  TR.insertBefore(TD, TH);
  TR.removeChild(TH);
  return TD;
}
;
window.WalkontableTableRenderer = WalkontableTableRenderer;


//# 
},{"./../../../dom.js":27}],22:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  WalkontableViewport: {get: function() {
      return WalkontableViewport;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47__46__46__47_eventManager_46_js__,
    $__calculator_47_viewportColumns_46_js__,
    $__calculator_47_viewportRows_46_js__;
var dom = ($___46__46__47__46__46__47__46__46__47_dom_46_js__ = require("./../../../dom.js"), $___46__46__47__46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47__46__46__47_dom_46_js__});
var eventManagerObject = ($___46__46__47__46__46__47__46__46__47_eventManager_46_js__ = require("./../../../eventManager.js"), $___46__46__47__46__46__47__46__46__47_eventManager_46_js__ && $___46__46__47__46__46__47__46__46__47_eventManager_46_js__.__esModule && $___46__46__47__46__46__47__46__46__47_eventManager_46_js__ || {default: $___46__46__47__46__46__47__46__46__47_eventManager_46_js__}).eventManager;
var WalkontableViewportColumnsCalculator = ($__calculator_47_viewportColumns_46_js__ = require("./calculator/viewportColumns.js"), $__calculator_47_viewportColumns_46_js__ && $__calculator_47_viewportColumns_46_js__.__esModule && $__calculator_47_viewportColumns_46_js__ || {default: $__calculator_47_viewportColumns_46_js__}).WalkontableViewportColumnsCalculator;
var WalkontableViewportRowsCalculator = ($__calculator_47_viewportRows_46_js__ = require("./calculator/viewportRows.js"), $__calculator_47_viewportRows_46_js__ && $__calculator_47_viewportRows_46_js__.__esModule && $__calculator_47_viewportRows_46_js__ || {default: $__calculator_47_viewportRows_46_js__}).WalkontableViewportRowsCalculator;
var WalkontableViewport = function WalkontableViewport(wotInstance) {
  var $__3 = this;
  this.wot = wotInstance;
  this.instance = this.wot;
  this.oversizedRows = [];
  this.oversizedCols = [];
  this.oversizedColumnHeaders = [];
  this.clientHeight = 0;
  this.containerWidth = NaN;
  this.rowHeaderWidth = NaN;
  this.rowsVisibleCalculator = null;
  this.columnsVisibleCalculator = null;
  var eventManager = eventManagerObject(wotInstance);
  eventManager.addEventListener(window, 'resize', (function() {
    $__3.clientHeight = $__3.getWorkspaceHeight();
  }));
};
($traceurRuntime.createClass)(WalkontableViewport, {
  getWorkspaceHeight: function() {
    var trimmingContainer = this.instance.wtOverlays.topOverlay.trimmingContainer;
    var elemHeight;
    var height = 0;
    if (trimmingContainer === window) {
      height = document.documentElement.clientHeight;
    } else {
      elemHeight = dom.outerHeight(trimmingContainer);
      height = (elemHeight > 0 && trimmingContainer.clientHeight > 0) ? trimmingContainer.clientHeight : Infinity;
    }
    return height;
  },
  getWorkspaceWidth: function() {
    var width;
    var totalColumns = this.instance.getSetting("totalColumns");
    var trimmingContainer = this.instance.wtOverlays.leftOverlay.trimmingContainer;
    var overflow;
    var stretchSetting = this.instance.getSetting('stretchH');
    var docOffsetWidth = document.documentElement.offsetWidth;
    if (Handsontable.freezeOverlays) {
      width = Math.min(docOffsetWidth - this.getWorkspaceOffset().left, docOffsetWidth);
    } else {
      width = Math.min(this.getContainerFillWidth(), docOffsetWidth - this.getWorkspaceOffset().left, docOffsetWidth);
    }
    if (trimmingContainer === window && totalColumns > 0 && this.sumColumnWidths(0, totalColumns - 1) > width) {
      return document.documentElement.clientWidth;
    }
    if (trimmingContainer !== window) {
      overflow = dom.getStyle(this.instance.wtOverlays.leftOverlay.trimmingContainer, 'overflow');
      if (overflow == "scroll" || overflow == "hidden" || overflow == "auto") {
        return Math.max(width, trimmingContainer.clientWidth);
      }
    }
    if (stretchSetting === 'none' || !stretchSetting) {
      return Math.max(width, dom.outerWidth(this.instance.wtTable.TABLE));
    } else {
      return width;
    }
  },
  hasVerticalScroll: function() {
    return this.getWorkspaceActualHeight() > this.getWorkspaceHeight();
  },
  hasHorizontalScroll: function() {
    return this.getWorkspaceActualWidth() > this.getWorkspaceWidth();
  },
  sumColumnWidths: function(from, length) {
    var sum = 0;
    var defaultColumnWidth = this.instance.wtSettings.defaultColumnWidth;
    while (from < length) {
      sum += this.wot.wtTable.getColumnWidth(from) || defaultColumnWidth;
      from++;
    }
    return sum;
  },
  getContainerFillWidth: function() {
    if (this.containerWidth) {
      return this.containerWidth;
    }
    var mainContainer = this.instance.wtTable.holder;
    var fillWidth;
    var dummyElement;
    dummyElement = document.createElement("DIV");
    dummyElement.style.width = "100%";
    dummyElement.style.height = "1px";
    mainContainer.appendChild(dummyElement);
    fillWidth = dummyElement.offsetWidth;
    this.containerWidth = fillWidth;
    mainContainer.removeChild(dummyElement);
    return fillWidth;
  },
  getWorkspaceOffset: function() {
    return dom.offset(this.wot.wtTable.TABLE);
  },
  getWorkspaceActualHeight: function() {
    return dom.outerHeight(this.wot.wtTable.TABLE);
  },
  getWorkspaceActualWidth: function() {
    return dom.outerWidth(this.wot.wtTable.TABLE) || dom.outerWidth(this.wot.wtTable.TBODY) || dom.outerWidth(this.wot.wtTable.THEAD);
  },
  getColumnHeaderHeight: function() {
    if (isNaN(this.columnHeaderHeight)) {
      this.columnHeaderHeight = dom.outerHeight(this.wot.wtTable.THEAD);
    }
    return this.columnHeaderHeight;
  },
  getViewportHeight: function() {
    var containerHeight = this.getWorkspaceHeight();
    var columnHeaderHeight;
    if (containerHeight === Infinity) {
      return containerHeight;
    }
    columnHeaderHeight = this.getColumnHeaderHeight();
    if (columnHeaderHeight > 0) {
      containerHeight -= columnHeaderHeight;
    }
    return containerHeight;
  },
  getRowHeaderWidth: function() {
    if (this.wot.cloneSource) {
      return this.wot.cloneSource.wtViewport.getRowHeaderWidth();
    }
    if (isNaN(this.rowHeaderWidth)) {
      var rowHeaders = this.instance.getSetting('rowHeaders');
      if (rowHeaders.length) {
        var TH = this.instance.wtTable.TABLE.querySelector('TH');
        this.rowHeaderWidth = 0;
        for (var i = 0,
            len = rowHeaders.length; i < len; i++) {
          if (TH) {
            this.rowHeaderWidth += dom.outerWidth(TH);
            TH = TH.nextSibling;
          } else {
            this.rowHeaderWidth += 50;
          }
        }
      } else {
        this.rowHeaderWidth = 0;
      }
    }
    return this.rowHeaderWidth;
  },
  getViewportWidth: function() {
    var containerWidth = this.getWorkspaceWidth();
    var rowHeaderWidth;
    if (containerWidth === Infinity) {
      return containerWidth;
    }
    rowHeaderWidth = this.getRowHeaderWidth();
    if (rowHeaderWidth > 0) {
      return containerWidth - rowHeaderWidth;
    }
    return containerWidth;
  },
  createRowsCalculator: function() {
    var visible = arguments[0] !== (void 0) ? arguments[0] : false;
    var $__3 = this;
    var height;
    var pos;
    var fixedRowsTop;
    this.rowHeaderWidth = NaN;
    if (this.wot.wtSettings.settings.renderAllRows) {
      height = Infinity;
    } else {
      height = this.getViewportHeight();
    }
    pos = dom.getScrollTop(this.wot.wtOverlays.mainTableScrollableElement) - this.wot.wtOverlays.topOverlay.getTableParentOffset();
    if (pos < 0) {
      pos = 0;
    }
    fixedRowsTop = this.wot.getSetting('fixedRowsTop');
    if (fixedRowsTop) {
      var fixedRowsHeight = this.wot.wtOverlays.topOverlay.sumCellSizes(0, fixedRowsTop);
      pos += fixedRowsHeight;
      height -= fixedRowsHeight;
    }
    return new WalkontableViewportRowsCalculator(height, pos, this.wot.getSetting('totalRows'), (function(sourceRow) {
      return $__3.wot.wtTable.getRowHeight(sourceRow);
    }), visible ? null : this.wot.wtSettings.settings.viewportRowCalculatorOverride, visible);
  },
  createColumnsCalculator: function() {
    var visible = arguments[0] !== (void 0) ? arguments[0] : false;
    var $__3 = this;
    var width = this.getViewportWidth();
    var pos;
    var fixedColumnsLeft;
    this.columnHeaderHeight = NaN;
    pos = this.wot.wtOverlays.leftOverlay.getScrollPosition() - this.wot.wtOverlays.topOverlay.getTableParentOffset();
    if (pos < 0) {
      pos = 0;
    }
    fixedColumnsLeft = this.wot.getSetting('fixedColumnsLeft');
    if (fixedColumnsLeft) {
      var fixedColumnsWidth = this.wot.wtOverlays.leftOverlay.sumCellSizes(0, fixedColumnsLeft);
      pos += fixedColumnsWidth;
      width -= fixedColumnsWidth;
    }
    if (this.wot.wtTable.holder.clientWidth !== this.wot.wtTable.holder.offsetWidth) {
      width -= dom.getScrollbarWidth();
    }
    return new WalkontableViewportColumnsCalculator(width, pos, this.wot.getSetting('totalColumns'), (function(sourceCol) {
      return $__3.wot.wtTable.getColumnWidth(sourceCol);
    }), visible ? null : this.wot.wtSettings.settings.viewportColumnCalculatorOverride, visible, this.wot.getSetting('stretchH'));
  },
  createRenderCalculators: function() {
    var fastDraw = arguments[0] !== (void 0) ? arguments[0] : false;
    if (fastDraw) {
      var proposedRowsVisibleCalculator = this.createRowsCalculator(true);
      var proposedColumnsVisibleCalculator = this.createColumnsCalculator(true);
      if (!(this.areAllProposedVisibleRowsAlreadyRendered(proposedRowsVisibleCalculator) && this.areAllProposedVisibleColumnsAlreadyRendered(proposedColumnsVisibleCalculator))) {
        fastDraw = false;
      }
    }
    if (!fastDraw) {
      this.rowsRenderCalculator = this.createRowsCalculator();
      this.columnsRenderCalculator = this.createColumnsCalculator();
    }
    this.rowsVisibleCalculator = null;
    this.columnsVisibleCalculator = null;
    return fastDraw;
  },
  createVisibleCalculators: function() {
    this.rowsVisibleCalculator = this.createRowsCalculator(true);
    this.columnsVisibleCalculator = this.createColumnsCalculator(true);
  },
  areAllProposedVisibleRowsAlreadyRendered: function(proposedRowsVisibleCalculator) {
    if (this.rowsVisibleCalculator) {
      if (proposedRowsVisibleCalculator.startRow < this.rowsRenderCalculator.startRow || (proposedRowsVisibleCalculator.startRow === this.rowsRenderCalculator.startRow && proposedRowsVisibleCalculator.startRow > 0)) {
        return false;
      } else if (proposedRowsVisibleCalculator.endRow > this.rowsRenderCalculator.endRow || (proposedRowsVisibleCalculator.endRow === this.rowsRenderCalculator.endRow && proposedRowsVisibleCalculator.endRow < this.wot.getSetting('totalRows') - 1)) {
        return false;
      } else {
        return true;
      }
    }
    return false;
  },
  areAllProposedVisibleColumnsAlreadyRendered: function(proposedColumnsVisibleCalculator) {
    if (this.columnsVisibleCalculator) {
      if (proposedColumnsVisibleCalculator.startColumn < this.columnsRenderCalculator.startColumn || (proposedColumnsVisibleCalculator.startColumn === this.columnsRenderCalculator.startColumn && proposedColumnsVisibleCalculator.startColumn > 0)) {
        return false;
      } else if (proposedColumnsVisibleCalculator.endColumn > this.columnsRenderCalculator.endColumn || (proposedColumnsVisibleCalculator.endColumn === this.columnsRenderCalculator.endColumn && proposedColumnsVisibleCalculator.endColumn < this.wot.getSetting('totalColumns') - 1)) {
        return false;
      } else {
        return true;
      }
    }
    return false;
  }
}, {});
;
window.WalkontableViewport = WalkontableViewport;


//# 
},{"./../../../dom.js":27,"./../../../eventManager.js":41,"./calculator/viewportColumns.js":3,"./calculator/viewportRows.js":4}],23:[function(require,module,exports){
"use strict";
var $__shims_47_array_46_filter_46_js__,
    $__shims_47_array_46_indexOf_46_js__,
    $__shims_47_array_46_isArray_46_js__,
    $__shims_47_classes_46_js__,
    $__shims_47_object_46_keys_46_js__,
    $__shims_47_string_46_trim_46_js__,
    $__shims_47_weakmap_46_js__,
    $__pluginHooks_46_js__,
    $__core_46_js__,
    $__renderers_47__95_cellDecorator_46_js__,
    $__cellTypes_46_js__,
    $___46__46__47_plugins_47_jqueryHandsontable_46_js__;
var version = Handsontable.version;
var buildDate = Handsontable.buildDate;
window.Handsontable = function(rootElement, userSettings) {
  var instance = new Handsontable.Core(rootElement, userSettings || {});
  instance.init();
  return instance;
};
Handsontable.version = version;
Handsontable.buildDate = buildDate;
($__shims_47_array_46_filter_46_js__ = require("./shims/array.filter.js"), $__shims_47_array_46_filter_46_js__ && $__shims_47_array_46_filter_46_js__.__esModule && $__shims_47_array_46_filter_46_js__ || {default: $__shims_47_array_46_filter_46_js__});
($__shims_47_array_46_indexOf_46_js__ = require("./shims/array.indexOf.js"), $__shims_47_array_46_indexOf_46_js__ && $__shims_47_array_46_indexOf_46_js__.__esModule && $__shims_47_array_46_indexOf_46_js__ || {default: $__shims_47_array_46_indexOf_46_js__});
($__shims_47_array_46_isArray_46_js__ = require("./shims/array.isArray.js"), $__shims_47_array_46_isArray_46_js__ && $__shims_47_array_46_isArray_46_js__.__esModule && $__shims_47_array_46_isArray_46_js__ || {default: $__shims_47_array_46_isArray_46_js__});
($__shims_47_classes_46_js__ = require("./shims/classes.js"), $__shims_47_classes_46_js__ && $__shims_47_classes_46_js__.__esModule && $__shims_47_classes_46_js__ || {default: $__shims_47_classes_46_js__});
($__shims_47_object_46_keys_46_js__ = require("./shims/object.keys.js"), $__shims_47_object_46_keys_46_js__ && $__shims_47_object_46_keys_46_js__.__esModule && $__shims_47_object_46_keys_46_js__ || {default: $__shims_47_object_46_keys_46_js__});
($__shims_47_string_46_trim_46_js__ = require("./shims/string.trim.js"), $__shims_47_string_46_trim_46_js__ && $__shims_47_string_46_trim_46_js__.__esModule && $__shims_47_string_46_trim_46_js__ || {default: $__shims_47_string_46_trim_46_js__});
($__shims_47_weakmap_46_js__ = require("./shims/weakmap.js"), $__shims_47_weakmap_46_js__ && $__shims_47_weakmap_46_js__.__esModule && $__shims_47_weakmap_46_js__ || {default: $__shims_47_weakmap_46_js__});
Handsontable.plugins = {};
var Hooks = ($__pluginHooks_46_js__ = require("./pluginHooks.js"), $__pluginHooks_46_js__ && $__pluginHooks_46_js__.__esModule && $__pluginHooks_46_js__ || {default: $__pluginHooks_46_js__}).Hooks;
if (!Handsontable.hooks) {
  Handsontable.hooks = new Hooks();
}
($__core_46_js__ = require("./core.js"), $__core_46_js__ && $__core_46_js__.__esModule && $__core_46_js__ || {default: $__core_46_js__});
($__renderers_47__95_cellDecorator_46_js__ = require("./renderers/_cellDecorator.js"), $__renderers_47__95_cellDecorator_46_js__ && $__renderers_47__95_cellDecorator_46_js__.__esModule && $__renderers_47__95_cellDecorator_46_js__ || {default: $__renderers_47__95_cellDecorator_46_js__});
($__cellTypes_46_js__ = require("./cellTypes.js"), $__cellTypes_46_js__ && $__cellTypes_46_js__.__esModule && $__cellTypes_46_js__ || {default: $__cellTypes_46_js__});
($___46__46__47_plugins_47_jqueryHandsontable_46_js__ = require("./../plugins/jqueryHandsontable.js"), $___46__46__47_plugins_47_jqueryHandsontable_46_js__ && $___46__46__47_plugins_47_jqueryHandsontable_46_js__.__esModule && $___46__46__47_plugins_47_jqueryHandsontable_46_js__ || {default: $___46__46__47_plugins_47_jqueryHandsontable_46_js__});


//# 
},{"./../plugins/jqueryHandsontable.js":1,"./cellTypes.js":24,"./core.js":25,"./pluginHooks.js":44,"./renderers/_cellDecorator.js":71,"./shims/array.filter.js":78,"./shims/array.indexOf.js":79,"./shims/array.isArray.js":80,"./shims/classes.js":81,"./shims/object.keys.js":82,"./shims/string.trim.js":83,"./shims/weakmap.js":84}],24:[function(require,module,exports){
"use strict";
var $__helpers_46_js__,
    $__editors_46_js__,
    $__renderers_46_js__,
    $__editors_47_autocompleteEditor_46_js__,
    $__editors_47_checkboxEditor_46_js__,
    $__editors_47_dateEditor_46_js__,
    $__editors_47_dropdownEditor_46_js__,
    $__editors_47_handsontableEditor_46_js__,
    $__editors_47_mobileTextEditor_46_js__,
    $__editors_47_numericEditor_46_js__,
    $__editors_47_passwordEditor_46_js__,
    $__editors_47_selectEditor_46_js__,
    $__editors_47_textEditor_46_js__,
    $__renderers_47_autocompleteRenderer_46_js__,
    $__renderers_47_checkboxRenderer_46_js__,
    $__renderers_47_htmlRenderer_46_js__,
    $__renderers_47_numericRenderer_46_js__,
    $__renderers_47_passwordRenderer_46_js__,
    $__renderers_47_textRenderer_46_js__,
    $__validators_47_autocompleteValidator_46_js__,
    $__validators_47_dateValidator_46_js__,
    $__validators_47_numericValidator_46_js__;
var helper = ($__helpers_46_js__ = require("./helpers.js"), $__helpers_46_js__ && $__helpers_46_js__.__esModule && $__helpers_46_js__ || {default: $__helpers_46_js__});
var getEditorConstructor = ($__editors_46_js__ = require("./editors.js"), $__editors_46_js__ && $__editors_46_js__.__esModule && $__editors_46_js__ || {default: $__editors_46_js__}).getEditorConstructor;
var getRenderer = ($__renderers_46_js__ = require("./renderers.js"), $__renderers_46_js__ && $__renderers_46_js__.__esModule && $__renderers_46_js__ || {default: $__renderers_46_js__}).getRenderer;
var AutocompleteEditor = ($__editors_47_autocompleteEditor_46_js__ = require("./editors/autocompleteEditor.js"), $__editors_47_autocompleteEditor_46_js__ && $__editors_47_autocompleteEditor_46_js__.__esModule && $__editors_47_autocompleteEditor_46_js__ || {default: $__editors_47_autocompleteEditor_46_js__}).AutocompleteEditor;
var CheckboxEditor = ($__editors_47_checkboxEditor_46_js__ = require("./editors/checkboxEditor.js"), $__editors_47_checkboxEditor_46_js__ && $__editors_47_checkboxEditor_46_js__.__esModule && $__editors_47_checkboxEditor_46_js__ || {default: $__editors_47_checkboxEditor_46_js__}).CheckboxEditor;
var DateEditor = ($__editors_47_dateEditor_46_js__ = require("./editors/dateEditor.js"), $__editors_47_dateEditor_46_js__ && $__editors_47_dateEditor_46_js__.__esModule && $__editors_47_dateEditor_46_js__ || {default: $__editors_47_dateEditor_46_js__}).DateEditor;
var DropdownEditor = ($__editors_47_dropdownEditor_46_js__ = require("./editors/dropdownEditor.js"), $__editors_47_dropdownEditor_46_js__ && $__editors_47_dropdownEditor_46_js__.__esModule && $__editors_47_dropdownEditor_46_js__ || {default: $__editors_47_dropdownEditor_46_js__}).DropdownEditor;
var HandsontableEditor = ($__editors_47_handsontableEditor_46_js__ = require("./editors/handsontableEditor.js"), $__editors_47_handsontableEditor_46_js__ && $__editors_47_handsontableEditor_46_js__.__esModule && $__editors_47_handsontableEditor_46_js__ || {default: $__editors_47_handsontableEditor_46_js__}).HandsontableEditor;
var MobileTextEditor = ($__editors_47_mobileTextEditor_46_js__ = require("./editors/mobileTextEditor.js"), $__editors_47_mobileTextEditor_46_js__ && $__editors_47_mobileTextEditor_46_js__.__esModule && $__editors_47_mobileTextEditor_46_js__ || {default: $__editors_47_mobileTextEditor_46_js__}).MobileTextEditor;
var NumericEditor = ($__editors_47_numericEditor_46_js__ = require("./editors/numericEditor.js"), $__editors_47_numericEditor_46_js__ && $__editors_47_numericEditor_46_js__.__esModule && $__editors_47_numericEditor_46_js__ || {default: $__editors_47_numericEditor_46_js__}).NumericEditor;
var PasswordEditor = ($__editors_47_passwordEditor_46_js__ = require("./editors/passwordEditor.js"), $__editors_47_passwordEditor_46_js__ && $__editors_47_passwordEditor_46_js__.__esModule && $__editors_47_passwordEditor_46_js__ || {default: $__editors_47_passwordEditor_46_js__}).PasswordEditor;
var SelectEditor = ($__editors_47_selectEditor_46_js__ = require("./editors/selectEditor.js"), $__editors_47_selectEditor_46_js__ && $__editors_47_selectEditor_46_js__.__esModule && $__editors_47_selectEditor_46_js__ || {default: $__editors_47_selectEditor_46_js__}).SelectEditor;
var TextEditor = ($__editors_47_textEditor_46_js__ = require("./editors/textEditor.js"), $__editors_47_textEditor_46_js__ && $__editors_47_textEditor_46_js__.__esModule && $__editors_47_textEditor_46_js__ || {default: $__editors_47_textEditor_46_js__}).TextEditor;
var AutocompleteRenderer = ($__renderers_47_autocompleteRenderer_46_js__ = require("./renderers/autocompleteRenderer.js"), $__renderers_47_autocompleteRenderer_46_js__ && $__renderers_47_autocompleteRenderer_46_js__.__esModule && $__renderers_47_autocompleteRenderer_46_js__ || {default: $__renderers_47_autocompleteRenderer_46_js__}).AutocompleteRenderer;
var CheckboxRenderer = ($__renderers_47_checkboxRenderer_46_js__ = require("./renderers/checkboxRenderer.js"), $__renderers_47_checkboxRenderer_46_js__ && $__renderers_47_checkboxRenderer_46_js__.__esModule && $__renderers_47_checkboxRenderer_46_js__ || {default: $__renderers_47_checkboxRenderer_46_js__}).CheckboxRenderer;
var HtmlRenderer = ($__renderers_47_htmlRenderer_46_js__ = require("./renderers/htmlRenderer.js"), $__renderers_47_htmlRenderer_46_js__ && $__renderers_47_htmlRenderer_46_js__.__esModule && $__renderers_47_htmlRenderer_46_js__ || {default: $__renderers_47_htmlRenderer_46_js__}).HtmlRenderer;
var NumericRenderer = ($__renderers_47_numericRenderer_46_js__ = require("./renderers/numericRenderer.js"), $__renderers_47_numericRenderer_46_js__ && $__renderers_47_numericRenderer_46_js__.__esModule && $__renderers_47_numericRenderer_46_js__ || {default: $__renderers_47_numericRenderer_46_js__}).NumericRenderer;
var PasswordRenderer = ($__renderers_47_passwordRenderer_46_js__ = require("./renderers/passwordRenderer.js"), $__renderers_47_passwordRenderer_46_js__ && $__renderers_47_passwordRenderer_46_js__.__esModule && $__renderers_47_passwordRenderer_46_js__ || {default: $__renderers_47_passwordRenderer_46_js__}).PasswordRenderer;
var TextRenderer = ($__renderers_47_textRenderer_46_js__ = require("./renderers/textRenderer.js"), $__renderers_47_textRenderer_46_js__ && $__renderers_47_textRenderer_46_js__.__esModule && $__renderers_47_textRenderer_46_js__ || {default: $__renderers_47_textRenderer_46_js__}).TextRenderer;
var AutocompleteValidator = ($__validators_47_autocompleteValidator_46_js__ = require("./validators/autocompleteValidator.js"), $__validators_47_autocompleteValidator_46_js__ && $__validators_47_autocompleteValidator_46_js__.__esModule && $__validators_47_autocompleteValidator_46_js__ || {default: $__validators_47_autocompleteValidator_46_js__}).AutocompleteValidator;
var DateValidator = ($__validators_47_dateValidator_46_js__ = require("./validators/dateValidator.js"), $__validators_47_dateValidator_46_js__ && $__validators_47_dateValidator_46_js__.__esModule && $__validators_47_dateValidator_46_js__ || {default: $__validators_47_dateValidator_46_js__}).DateValidator;
var NumericValidator = ($__validators_47_numericValidator_46_js__ = require("./validators/numericValidator.js"), $__validators_47_numericValidator_46_js__ && $__validators_47_numericValidator_46_js__.__esModule && $__validators_47_numericValidator_46_js__ || {default: $__validators_47_numericValidator_46_js__}).NumericValidator;
Handsontable.mobileBrowser = helper.isMobileBrowser();
Handsontable.AutocompleteCell = {
  editor: getEditorConstructor('autocomplete'),
  renderer: getRenderer('autocomplete'),
  validator: Handsontable.AutocompleteValidator
};
Handsontable.CheckboxCell = {
  editor: getEditorConstructor('checkbox'),
  renderer: getRenderer('checkbox')
};
Handsontable.TextCell = {
  editor: Handsontable.mobileBrowser ? getEditorConstructor('mobile') : getEditorConstructor('text'),
  renderer: getRenderer('text')
};
Handsontable.NumericCell = {
  editor: getEditorConstructor('numeric'),
  renderer: getRenderer('numeric'),
  validator: Handsontable.NumericValidator,
  dataType: 'number'
};
Handsontable.DateCell = {
  editor: getEditorConstructor('date'),
  validator: Handsontable.DateValidator,
  renderer: getRenderer('autocomplete')
};
Handsontable.HandsontableCell = {
  editor: getEditorConstructor('handsontable'),
  renderer: getRenderer('autocomplete')
};
Handsontable.PasswordCell = {
  editor: getEditorConstructor('password'),
  renderer: getRenderer('password'),
  copyable: false
};
Handsontable.DropdownCell = {
  editor: getEditorConstructor('dropdown'),
  renderer: getRenderer('autocomplete'),
  validator: Handsontable.AutocompleteValidator
};
Handsontable.cellTypes = {
  text: Handsontable.TextCell,
  date: Handsontable.DateCell,
  numeric: Handsontable.NumericCell,
  checkbox: Handsontable.CheckboxCell,
  autocomplete: Handsontable.AutocompleteCell,
  handsontable: Handsontable.HandsontableCell,
  password: Handsontable.PasswordCell,
  dropdown: Handsontable.DropdownCell
};
Handsontable.cellLookup = {validator: {
    numeric: Handsontable.NumericValidator,
    autocomplete: Handsontable.AutocompleteValidator
  }};


//# 
},{"./editors.js":29,"./editors/autocompleteEditor.js":31,"./editors/checkboxEditor.js":32,"./editors/dateEditor.js":33,"./editors/dropdownEditor.js":34,"./editors/handsontableEditor.js":35,"./editors/mobileTextEditor.js":36,"./editors/numericEditor.js":37,"./editors/passwordEditor.js":38,"./editors/selectEditor.js":39,"./editors/textEditor.js":40,"./helpers.js":42,"./renderers.js":70,"./renderers/autocompleteRenderer.js":72,"./renderers/checkboxRenderer.js":73,"./renderers/htmlRenderer.js":74,"./renderers/numericRenderer.js":75,"./renderers/passwordRenderer.js":76,"./renderers/textRenderer.js":77,"./validators/autocompleteValidator.js":86,"./validators/dateValidator.js":87,"./validators/numericValidator.js":88}],25:[function(require,module,exports){
"use strict";
var $__dom_46_js__,
    $__helpers_46_js__,
    $__numeral__,
    $__dataMap_46_js__,
    $__editorManager_46_js__,
    $__eventManager_46_js__,
    $__plugins_46_js__,
    $__renderers_46_js__,
    $__tableView_46_js__,
    $__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__,
    $__3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__,
    $__3rdparty_47_walkontable_47_src_47_selection_46_js__;
var dom = ($__dom_46_js__ = require("./dom.js"), $__dom_46_js__ && $__dom_46_js__.__esModule && $__dom_46_js__ || {default: $__dom_46_js__});
var helper = ($__helpers_46_js__ = require("./helpers.js"), $__helpers_46_js__ && $__helpers_46_js__.__esModule && $__helpers_46_js__ || {default: $__helpers_46_js__});
var numeral = ($__numeral__ = require("numeral"), $__numeral__ && $__numeral__.__esModule && $__numeral__ || {default: $__numeral__}).default;
var DataMap = ($__dataMap_46_js__ = require("./dataMap.js"), $__dataMap_46_js__ && $__dataMap_46_js__.__esModule && $__dataMap_46_js__ || {default: $__dataMap_46_js__}).DataMap;
var EditorManager = ($__editorManager_46_js__ = require("./editorManager.js"), $__editorManager_46_js__ && $__editorManager_46_js__.__esModule && $__editorManager_46_js__ || {default: $__editorManager_46_js__}).EditorManager;
var eventManagerObject = ($__eventManager_46_js__ = require("./eventManager.js"), $__eventManager_46_js__ && $__eventManager_46_js__.__esModule && $__eventManager_46_js__ || {default: $__eventManager_46_js__}).eventManager;
var getPlugin = ($__plugins_46_js__ = require("./plugins.js"), $__plugins_46_js__ && $__plugins_46_js__.__esModule && $__plugins_46_js__ || {default: $__plugins_46_js__}).getPlugin;
var getRenderer = ($__renderers_46_js__ = require("./renderers.js"), $__renderers_46_js__ && $__renderers_46_js__.__esModule && $__renderers_46_js__ || {default: $__renderers_46_js__}).getRenderer;
var TableView = ($__tableView_46_js__ = require("./tableView.js"), $__tableView_46_js__ && $__tableView_46_js__.__esModule && $__tableView_46_js__ || {default: $__tableView_46_js__}).TableView;
var WalkontableCellCoords = ($__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ = require("./3rdparty/walkontable/src/cell/coords.js"), $__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ && $__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__.__esModule && $__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ || {default: $__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__}).WalkontableCellCoords;
var WalkontableCellRange = ($__3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__ = require("./3rdparty/walkontable/src/cell/range.js"), $__3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__ && $__3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__.__esModule && $__3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__ || {default: $__3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__}).WalkontableCellRange;
var WalkontableSelection = ($__3rdparty_47_walkontable_47_src_47_selection_46_js__ = require("./3rdparty/walkontable/src/selection.js"), $__3rdparty_47_walkontable_47_src_47_selection_46_js__ && $__3rdparty_47_walkontable_47_src_47_selection_46_js__.__esModule && $__3rdparty_47_walkontable_47_src_47_selection_46_js__ || {default: $__3rdparty_47_walkontable_47_src_47_selection_46_js__}).WalkontableSelection;
Handsontable.activeGuid = null;
Handsontable.Core = function Core(rootElement, userSettings) {
  var priv,
      datamap,
      grid,
      selection,
      editorManager,
      instance = this,
      GridSettings = function() {},
      eventManager = eventManagerObject(instance);
  helper.extend(GridSettings.prototype, DefaultSettings.prototype);
  helper.extend(GridSettings.prototype, userSettings);
  helper.extend(GridSettings.prototype, expandType(userSettings));
  this.rootElement = rootElement;
  this.isHotTableEnv = dom.isChildOfWebComponentTable(this.rootElement);
  Handsontable.eventManager.isHotTableEnv = this.isHotTableEnv;
  this.container = document.createElement('DIV');
  rootElement.insertBefore(this.container, rootElement.firstChild);
  this.guid = 'ht_' + helper.randomString();
  if (!this.rootElement.id || this.rootElement.id.substring(0, 3) === "ht_") {
    this.rootElement.id = this.guid;
  }
  priv = {
    cellSettings: [],
    columnSettings: [],
    columnsSettingConflicts: ['data', 'width'],
    settings: new GridSettings(),
    selRange: null,
    isPopulated: null,
    scrollable: null,
    firstRun: true
  };
  grid = {
    alter: function(action, index, amount, source, keepEmptyRows) {
      var delta;
      amount = amount || 1;
      switch (action) {
        case "insert_row":
          if (instance.getSettings().maxRows === instance.countRows()) {
            return;
          }
          delta = datamap.createRow(index, amount);
          if (delta) {
            if (selection.isSelected() && priv.selRange.from.row >= index) {
              priv.selRange.from.row = priv.selRange.from.row + delta;
              selection.transformEnd(delta, 0);
            } else {
              selection.refreshBorders();
            }
          }
          break;
        case "insert_col":
          delta = datamap.createCol(index, amount);
          if (delta) {
            if (Array.isArray(instance.getSettings().colHeaders)) {
              var spliceArray = [index, 0];
              spliceArray.length += delta;
              Array.prototype.splice.apply(instance.getSettings().colHeaders, spliceArray);
            }
            if (selection.isSelected() && priv.selRange.from.col >= index) {
              priv.selRange.from.col = priv.selRange.from.col + delta;
              selection.transformEnd(0, delta);
            } else {
              selection.refreshBorders();
            }
          }
          break;
        case "remove_row":
          index = instance.runHooks('modifyCol', index);
          datamap.removeRow(index, amount);
          priv.cellSettings.splice(index, amount);
          var fixedRowsTop = instance.getSettings().fixedRowsTop;
          if (fixedRowsTop >= index + 1) {
            instance.getSettings().fixedRowsTop -= Math.min(amount, fixedRowsTop - index);
          }
          grid.adjustRowsAndCols();
          selection.refreshBorders();
          break;
        case "remove_col":
          datamap.removeCol(index, amount);
          for (var row = 0,
              len = datamap.getAll().length; row < len; row++) {
            if (row in priv.cellSettings) {
              priv.cellSettings[row].splice(index, amount);
            }
          }
          var fixedColumnsLeft = instance.getSettings().fixedColumnsLeft;
          if (fixedColumnsLeft >= index + 1) {
            instance.getSettings().fixedColumnsLeft -= Math.min(amount, fixedColumnsLeft - index);
          }
          if (Array.isArray(instance.getSettings().colHeaders)) {
            if (typeof index == 'undefined') {
              index = -1;
            }
            instance.getSettings().colHeaders.splice(index, amount);
          }
          grid.adjustRowsAndCols();
          selection.refreshBorders();
          break;
        default:
          throw new Error('There is no such action "' + action + '"');
          break;
      }
      if (!keepEmptyRows) {
        grid.adjustRowsAndCols();
      }
    },
    adjustRowsAndCols: function() {
      var r,
          rlen,
          emptyRows,
          emptyCols;
      rlen = instance.countRows();
      if (rlen < priv.settings.minRows) {
        for (r = 0; r < priv.settings.minRows - rlen; r++) {
          datamap.createRow(instance.countRows(), 1, true);
        }
      }
      emptyRows = instance.countEmptyRows(true);
      if (emptyRows < priv.settings.minSpareRows) {
        for (; emptyRows < priv.settings.minSpareRows && instance.countRows() < priv.settings.maxRows; emptyRows++) {
          datamap.createRow(instance.countRows(), 1, true);
        }
      }
      emptyCols = instance.countEmptyCols(true);
      if (!priv.settings.columns && instance.countCols() < priv.settings.minCols) {
        for (; instance.countCols() < priv.settings.minCols; emptyCols++) {
          datamap.createCol(instance.countCols(), 1, true);
        }
      }
      if (!priv.settings.columns && instance.dataType === 'array' && emptyCols < priv.settings.minSpareCols) {
        for (; emptyCols < priv.settings.minSpareCols && instance.countCols() < priv.settings.maxCols; emptyCols++) {
          datamap.createCol(instance.countCols(), 1, true);
        }
      }
      var rowCount = instance.countRows();
      var colCount = instance.countCols();
      if (rowCount === 0 || colCount === 0) {
        selection.deselect();
      }
      if (selection.isSelected()) {
        var selectionChanged;
        var fromRow = priv.selRange.from.row;
        var fromCol = priv.selRange.from.col;
        var toRow = priv.selRange.to.row;
        var toCol = priv.selRange.to.col;
        if (fromRow > rowCount - 1) {
          fromRow = rowCount - 1;
          selectionChanged = true;
          if (toRow > fromRow) {
            toRow = fromRow;
          }
        } else if (toRow > rowCount - 1) {
          toRow = rowCount - 1;
          selectionChanged = true;
          if (fromRow > toRow) {
            fromRow = toRow;
          }
        }
        if (fromCol > colCount - 1) {
          fromCol = colCount - 1;
          selectionChanged = true;
          if (toCol > fromCol) {
            toCol = fromCol;
          }
        } else if (toCol > colCount - 1) {
          toCol = colCount - 1;
          selectionChanged = true;
          if (fromCol > toCol) {
            fromCol = toCol;
          }
        }
        if (selectionChanged) {
          instance.selectCell(fromRow, fromCol, toRow, toCol);
        }
      }
      if (instance.view) {
        instance.view.wt.wtOverlays.adjustElementsSize();
      }
    },
    populateFromArray: function(start, input, end, source, method, direction, deltas) {
      var r,
          rlen,
          c,
          clen,
          setData = [],
          current = {};
      rlen = input.length;
      if (rlen === 0) {
        return false;
      }
      var repeatCol,
          repeatRow,
          cmax,
          rmax;
      switch (method) {
        case 'shift_down':
          repeatCol = end ? end.col - start.col + 1 : 0;
          repeatRow = end ? end.row - start.row + 1 : 0;
          input = helper.translateRowsToColumns(input);
          for (c = 0, clen = input.length, cmax = Math.max(clen, repeatCol); c < cmax; c++) {
            if (c < clen) {
              for (r = 0, rlen = input[c].length; r < repeatRow - rlen; r++) {
                input[c].push(input[c][r % rlen]);
              }
              input[c].unshift(start.col + c, start.row, 0);
              instance.spliceCol.apply(instance, input[c]);
            } else {
              input[c % clen][0] = start.col + c;
              instance.spliceCol.apply(instance, input[c % clen]);
            }
          }
          break;
        case 'shift_right':
          repeatCol = end ? end.col - start.col + 1 : 0;
          repeatRow = end ? end.row - start.row + 1 : 0;
          for (r = 0, rlen = input.length, rmax = Math.max(rlen, repeatRow); r < rmax; r++) {
            if (r < rlen) {
              for (c = 0, clen = input[r].length; c < repeatCol - clen; c++) {
                input[r].push(input[r][c % clen]);
              }
              input[r].unshift(start.row + r, start.col, 0);
              instance.spliceRow.apply(instance, input[r]);
            } else {
              input[r % rlen][0] = start.row + r;
              instance.spliceRow.apply(instance, input[r % rlen]);
            }
          }
          break;
        case 'overwrite':
        default:
          current.row = start.row;
          current.col = start.col;
          var iterators = {
            row: 0,
            col: 0
          },
              selected = {
                row: (end && start) ? (end.row - start.row + 1) : 1,
                col: (end && start) ? (end.col - start.col + 1) : 1
              },
              pushData = true;
          if (['up', 'left'].indexOf(direction) !== -1) {
            iterators = {
              row: Math.ceil(selected.row / rlen) || 1,
              col: Math.ceil(selected.col / input[0].length) || 1
            };
          } else if (['down', 'right'].indexOf(direction) !== -1) {
            iterators = {
              row: 1,
              col: 1
            };
          }
          for (r = 0; r < rlen; r++) {
            if ((end && current.row > end.row) || (!priv.settings.allowInsertRow && current.row > instance.countRows() - 1) || (current.row >= priv.settings.maxRows)) {
              break;
            }
            current.col = start.col;
            clen = input[r] ? input[r].length : 0;
            for (c = 0; c < clen; c++) {
              if ((end && current.col > end.col) || (!priv.settings.allowInsertColumn && current.col > instance.countCols() - 1) || (current.col >= priv.settings.maxCols)) {
                break;
              }
              if (!instance.getCellMeta(current.row, current.col).readOnly) {
                var result,
                    value = input[r][c],
                    orgValue = instance.getDataAtCell(current.row, current.col),
                    index = {
                      row: r,
                      col: c
                    },
                    valueSchema,
                    orgValueSchema;
                if (source === 'autofill') {
                  result = instance.runHooks('beforeAutofillInsidePopulate', index, direction, input, deltas, iterators, selected);
                  if (result) {
                    iterators = typeof(result.iterators) !== 'undefined' ? result.iterators : iterators;
                    value = typeof(result.value) !== 'undefined' ? result.value : value;
                  }
                }
                if (value !== null && typeof value === 'object') {
                  if (orgValue === null || typeof orgValue !== 'object') {
                    pushData = false;
                  } else {
                    orgValueSchema = Handsontable.helper.duckSchema(orgValue[0] || orgValue);
                    valueSchema = Handsontable.helper.duckSchema(value[0] || value);
                    if (Handsontable.helper.isObjectEquals(orgValueSchema, valueSchema)) {
                      value = Handsontable.helper.deepClone(value);
                    } else {
                      pushData = false;
                    }
                  }
                } else if (orgValue !== null && typeof orgValue === 'object') {
                  pushData = false;
                }
                if (pushData) {
                  setData.push([current.row, current.col, value]);
                }
                pushData = true;
              }
              current.col++;
              if (end && c === clen - 1) {
                c = -1;
                if (['down', 'right'].indexOf(direction) !== -1) {
                  iterators.col++;
                } else if (['up', 'left'].indexOf(direction) !== -1) {
                  if (iterators.col > 1) {
                    iterators.col--;
                  }
                }
              }
            }
            current.row++;
            iterators.col = 1;
            if (end && r === rlen - 1) {
              r = -1;
              if (['down', 'right'].indexOf(direction) !== -1) {
                iterators.row++;
              } else if (['up', 'left'].indexOf(direction) !== -1) {
                if (iterators.row > 1) {
                  iterators.row--;
                }
              }
            }
          }
          instance.setDataAtCell(setData, null, null, source || 'populateFromArray');
          break;
      }
    }
  };
  this.selection = selection = {
    inProgress: false,
    selectedHeader: {
      cols: false,
      rows: false
    },
    setSelectedHeaders: function(rows, cols) {
      instance.selection.selectedHeader.rows = rows;
      instance.selection.selectedHeader.cols = cols;
    },
    begin: function() {
      instance.selection.inProgress = true;
    },
    finish: function() {
      var sel = instance.getSelected();
      Handsontable.hooks.run(instance, "afterSelectionEnd", sel[0], sel[1], sel[2], sel[3]);
      Handsontable.hooks.run(instance, "afterSelectionEndByProp", sel[0], instance.colToProp(sel[1]), sel[2], instance.colToProp(sel[3]));
      instance.selection.inProgress = false;
    },
    isInProgress: function() {
      return instance.selection.inProgress;
    },
    setRangeStart: function(coords, keepEditorOpened) {
      Handsontable.hooks.run(instance, "beforeSetRangeStart", coords);
      priv.selRange = new WalkontableCellRange(coords, coords, coords);
      selection.setRangeEnd(coords, null, keepEditorOpened);
    },
    setRangeEnd: function(coords, scrollToCell, keepEditorOpened) {
      if (priv.selRange === null) {
        return;
      }
      var disableVisualSelection;
      Handsontable.hooks.run(instance, "beforeSetRangeEnd", coords);
      instance.selection.begin();
      priv.selRange.to = new WalkontableCellCoords(coords.row, coords.col);
      if (!priv.settings.multiSelect) {
        priv.selRange.from = coords;
      }
      instance.view.wt.selections.current.clear();
      disableVisualSelection = instance.getCellMeta(priv.selRange.highlight.row, priv.selRange.highlight.col).disableVisualSelection;
      if (typeof disableVisualSelection === 'string') {
        disableVisualSelection = [disableVisualSelection];
      }
      if (disableVisualSelection === false || Array.isArray(disableVisualSelection) && disableVisualSelection.indexOf('current') === -1) {
        instance.view.wt.selections.current.add(priv.selRange.highlight);
      }
      instance.view.wt.selections.area.clear();
      if ((disableVisualSelection === false || Array.isArray(disableVisualSelection) && disableVisualSelection.indexOf('area') === -1) && selection.isMultiple()) {
        instance.view.wt.selections.area.add(priv.selRange.from);
        instance.view.wt.selections.area.add(priv.selRange.to);
      }
      if (priv.settings.currentRowClassName || priv.settings.currentColClassName) {
        instance.view.wt.selections.highlight.clear();
        instance.view.wt.selections.highlight.add(priv.selRange.from);
        instance.view.wt.selections.highlight.add(priv.selRange.to);
      }
      Handsontable.hooks.run(instance, "afterSelection", priv.selRange.from.row, priv.selRange.from.col, priv.selRange.to.row, priv.selRange.to.col);
      Handsontable.hooks.run(instance, "afterSelectionByProp", priv.selRange.from.row, datamap.colToProp(priv.selRange.from.col), priv.selRange.to.row, datamap.colToProp(priv.selRange.to.col));
      if (scrollToCell !== false && instance.view.mainViewIsActive()) {
        if (priv.selRange.from && !selection.isMultiple()) {
          instance.view.scrollViewport(priv.selRange.from);
        } else {
          instance.view.scrollViewport(coords);
        }
      }
      selection.refreshBorders(null, keepEditorOpened);
    },
    refreshBorders: function(revertOriginal, keepEditor) {
      if (!keepEditor) {
        editorManager.destroyEditor(revertOriginal);
      }
      instance.view.render();
      if (selection.isSelected() && !keepEditor) {
        editorManager.prepareEditor();
      }
    },
    isMultiple: function() {
      var isMultiple = !(priv.selRange.to.col === priv.selRange.from.col && priv.selRange.to.row === priv.selRange.from.row),
          modifier = Handsontable.hooks.run(instance, 'afterIsMultipleSelection', isMultiple);
      if (isMultiple) {
        return modifier;
      }
    },
    transformStart: function(rowDelta, colDelta, force, keepEditorOpened) {
      var delta = new WalkontableCellCoords(rowDelta, colDelta),
          rowTransformDir = 0,
          colTransformDir = 0,
          totalRows,
          totalCols,
          coords;
      instance.runHooks('modifyTransformStart', delta);
      totalRows = instance.countRows();
      totalCols = instance.countCols();
      if (priv.selRange.highlight.row + rowDelta > totalRows - 1) {
        if (force && priv.settings.minSpareRows > 0) {
          instance.alter("insert_row", totalRows);
          totalRows = instance.countRows();
        } else if (priv.settings.autoWrapCol) {
          delta.row = 1 - totalRows;
          delta.col = priv.selRange.highlight.col + delta.col == totalCols - 1 ? 1 - totalCols : 1;
        }
      } else if (priv.settings.autoWrapCol && priv.selRange.highlight.row + delta.row < 0 && priv.selRange.highlight.col + delta.col >= 0) {
        delta.row = totalRows - 1;
        delta.col = priv.selRange.highlight.col + delta.col == 0 ? totalCols - 1 : -1;
      }
      if (priv.selRange.highlight.col + delta.col > totalCols - 1) {
        if (force && priv.settings.minSpareCols > 0) {
          instance.alter("insert_col", totalCols);
          totalCols = instance.countCols();
        } else if (priv.settings.autoWrapRow) {
          delta.row = priv.selRange.highlight.row + delta.row == totalRows - 1 ? 1 - totalRows : 1;
          delta.col = 1 - totalCols;
        }
      } else if (priv.settings.autoWrapRow && priv.selRange.highlight.col + delta.col < 0 && priv.selRange.highlight.row + delta.row >= 0) {
        delta.row = priv.selRange.highlight.row + delta.row == 0 ? totalRows - 1 : -1;
        delta.col = totalCols - 1;
      }
      coords = new WalkontableCellCoords(priv.selRange.highlight.row + delta.row, priv.selRange.highlight.col + delta.col);
      if (coords.row < 0) {
        rowTransformDir = -1;
        coords.row = 0;
      } else if (coords.row > 0 && coords.row >= totalRows) {
        rowTransformDir = 1;
        coords.row = totalRows - 1;
      }
      if (coords.col < 0) {
        colTransformDir = -1;
        coords.col = 0;
      } else if (coords.col > 0 && coords.col >= totalCols) {
        colTransformDir = 1;
        coords.col = totalCols - 1;
      }
      instance.runHooks('afterModifyTransformStart', coords, rowTransformDir, colTransformDir);
      selection.setRangeStart(coords, keepEditorOpened);
    },
    transformEnd: function(rowDelta, colDelta) {
      var delta = new WalkontableCellCoords(rowDelta, colDelta),
          rowTransformDir = 0,
          colTransformDir = 0,
          totalRows,
          totalCols,
          coords;
      instance.runHooks('modifyTransformEnd', delta);
      totalRows = instance.countRows();
      totalCols = instance.countCols();
      coords = new WalkontableCellCoords(priv.selRange.to.row + delta.row, priv.selRange.to.col + delta.col);
      if (coords.row < 0) {
        rowTransformDir = -1;
        coords.row = 0;
      } else if (coords.row > 0 && coords.row >= totalRows) {
        rowTransformDir = 1;
        coords.row = totalRows - 1;
      }
      if (coords.col < 0) {
        colTransformDir = -1;
        coords.col = 0;
      } else if (coords.col > 0 && coords.col >= totalCols) {
        colTransformDir = 1;
        coords.col = totalCols - 1;
      }
      instance.runHooks('afterModifyTransformEnd', coords, rowTransformDir, colTransformDir);
      selection.setRangeEnd(coords, true);
    },
    isSelected: function() {
      return (priv.selRange !== null);
    },
    inInSelection: function(coords) {
      if (!selection.isSelected()) {
        return false;
      }
      return priv.selRange.includes(coords);
    },
    deselect: function() {
      if (!selection.isSelected()) {
        return;
      }
      instance.selection.inProgress = false;
      priv.selRange = null;
      instance.view.wt.selections.current.clear();
      instance.view.wt.selections.area.clear();
      if (priv.settings.currentRowClassName || priv.settings.currentColClassName) {
        instance.view.wt.selections.highlight.clear();
      }
      editorManager.destroyEditor();
      selection.refreshBorders();
      Handsontable.hooks.run(instance, 'afterDeselect');
    },
    selectAll: function() {
      if (!priv.settings.multiSelect) {
        return;
      }
      selection.setRangeStart(new WalkontableCellCoords(0, 0));
      selection.setRangeEnd(new WalkontableCellCoords(instance.countRows() - 1, instance.countCols() - 1), false);
    },
    empty: function() {
      if (!selection.isSelected()) {
        return;
      }
      var topLeft = priv.selRange.getTopLeftCorner();
      var bottomRight = priv.selRange.getBottomRightCorner();
      var r,
          c,
          changes = [];
      for (r = topLeft.row; r <= bottomRight.row; r++) {
        for (c = topLeft.col; c <= bottomRight.col; c++) {
          if (!instance.getCellMeta(r, c).readOnly) {
            changes.push([r, c, '']);
          }
        }
      }
      instance.setDataAtCell(changes);
    }
  };
  this.init = function() {
    Handsontable.hooks.run(instance, 'beforeInit');
    if (Handsontable.mobileBrowser) {
      dom.addClass(instance.rootElement, 'mobile');
    }
    this.updateSettings(priv.settings, true);
    this.view = new TableView(this);
    editorManager = new EditorManager(instance, priv, selection, datamap);
    this.forceFullRender = true;
    this.view.render();
    if (typeof priv.firstRun === 'object') {
      Handsontable.hooks.run(instance, 'afterChange', priv.firstRun[0], priv.firstRun[1]);
      priv.firstRun = false;
    }
    Handsontable.hooks.run(instance, 'afterInit');
  };
  function ValidatorsQueue() {
    var resolved = false;
    return {
      validatorsInQueue: 0,
      addValidatorToQueue: function() {
        this.validatorsInQueue++;
        resolved = false;
      },
      removeValidatorFormQueue: function() {
        this.validatorsInQueue = this.validatorsInQueue - 1 < 0 ? 0 : this.validatorsInQueue - 1;
        this.checkIfQueueIsEmpty();
      },
      onQueueEmpty: function() {},
      checkIfQueueIsEmpty: function() {
        if (this.validatorsInQueue == 0 && resolved == false) {
          resolved = true;
          this.onQueueEmpty();
        }
      }
    };
  }
  function validateChanges(changes, source, callback) {
    var waitingForValidator = new ValidatorsQueue();
    waitingForValidator.onQueueEmpty = resolve;
    for (var i = changes.length - 1; i >= 0; i--) {
      if (changes[i] === null) {
        changes.splice(i, 1);
      } else {
        var row = changes[i][0];
        var col = datamap.propToCol(changes[i][1]);
        var logicalCol = instance.runHooks('modifyCol', col);
        var cellProperties = instance.getCellMeta(row, logicalCol);
        if (cellProperties.type === 'numeric' && typeof changes[i][3] === 'string') {
          if (changes[i][3].length > 0 && (/^-?[\d\s]*(\.|\,)?\d*$/.test(changes[i][3]) || cellProperties.format)) {
            var len = changes[i][3].length;
            if (typeof cellProperties.language == 'undefined') {
              numeral.language('en');
            } else if (changes[i][3].indexOf(".") === len - 3 && changes[i][3].indexOf(",") === -1) {
              numeral.language('en');
            } else {
              numeral.language(cellProperties.language);
            }
            if (numeral.validate(changes[i][3])) {
              changes[i][3] = numeral().unformat(changes[i][3]);
            }
          }
        }
        if (instance.getCellValidator(cellProperties)) {
          waitingForValidator.addValidatorToQueue();
          instance.validateCell(changes[i][3], cellProperties, (function(i, cellProperties) {
            return function(result) {
              if (typeof result !== 'boolean') {
                throw new Error("Validation error: result is not boolean");
              }
              if (result === false && cellProperties.allowInvalid === false) {
                changes.splice(i, 1);
                cellProperties.valid = true;
                --i;
              }
              waitingForValidator.removeValidatorFormQueue();
            };
          })(i, cellProperties), source);
        }
      }
    }
    waitingForValidator.checkIfQueueIsEmpty();
    function resolve() {
      var beforeChangeResult;
      if (changes.length) {
        beforeChangeResult = Handsontable.hooks.run(instance, "beforeChange", changes, source);
        if (typeof beforeChangeResult === 'function') {
          console.warn("Your beforeChange callback returns a function. It's not supported since Handsontable 0.12.1 (and the returned function will not be executed).");
        } else if (beforeChangeResult === false) {
          changes.splice(0, changes.length);
        }
      }
      callback();
    }
  }
  function applyChanges(changes, source) {
    var i = changes.length - 1;
    if (i < 0) {
      return;
    }
    for (; 0 <= i; i--) {
      if (changes[i] === null) {
        changes.splice(i, 1);
        continue;
      }
      if (changes[i][2] == null && changes[i][3] == null) {
        continue;
      }
      if (priv.settings.allowInsertRow) {
        while (changes[i][0] > instance.countRows() - 1) {
          datamap.createRow();
        }
      }
      if (instance.dataType === 'array' && priv.settings.allowInsertColumn) {
        while (datamap.propToCol(changes[i][1]) > instance.countCols() - 1) {
          datamap.createCol();
        }
      }
      datamap.set(changes[i][0], changes[i][1], changes[i][3]);
    }
    instance.forceFullRender = true;
    grid.adjustRowsAndCols();
    Handsontable.hooks.run(instance, 'beforeChangeRender', changes, source);
    selection.refreshBorders(null, true);
    Handsontable.hooks.run(instance, 'afterChange', changes, source || 'edit');
  }
  this.validateCell = function(value, cellProperties, callback, source) {
    var validator = instance.getCellValidator(cellProperties);
    function done(valid) {
      var col = cellProperties.col,
          row = cellProperties.row,
          td = instance.getCell(row, col, true);
      if (td) {
        instance.view.wt.wtSettings.settings.cellRenderer(row, col, td);
      }
      callback(valid);
    }
    if (Object.prototype.toString.call(validator) === '[object RegExp]') {
      validator = (function(validator) {
        return function(value, callback) {
          callback(validator.test(value));
        };
      })(validator);
    }
    if (typeof validator == 'function') {
      value = Handsontable.hooks.run(instance, "beforeValidate", value, cellProperties.row, cellProperties.prop, source);
      instance._registerTimeout(setTimeout(function() {
        validator.call(cellProperties, value, function(valid) {
          valid = Handsontable.hooks.run(instance, "afterValidate", valid, value, cellProperties.row, cellProperties.prop, source);
          cellProperties.valid = valid;
          done(valid);
          Handsontable.hooks.run(instance, "postAfterValidate", valid, value, cellProperties.row, cellProperties.prop, source);
        });
      }, 0));
    } else {
      cellProperties.valid = true;
      done(cellProperties.valid);
    }
  };
  function setDataInputToArray(row, propOrCol, value) {
    if (typeof row === "object") {
      return row;
    } else {
      return [[row, propOrCol, value]];
    }
  }
  this.setDataAtCell = function(row, col, value, source) {
    var input = setDataInputToArray(row, col, value),
        i,
        ilen,
        changes = [],
        prop;
    for (i = 0, ilen = input.length; i < ilen; i++) {
      if (typeof input[i] !== 'object') {
        throw new Error('Method `setDataAtCell` accepts row number or changes array of arrays as its first parameter');
      }
      if (typeof input[i][1] !== 'number') {
        throw new Error('Method `setDataAtCell` accepts row and column number as its parameters. If you want to use object property name, use method `setDataAtRowProp`');
      }
      prop = datamap.colToProp(input[i][1]);
      changes.push([input[i][0], prop, datamap.get(input[i][0], prop), input[i][2]]);
    }
    if (!source && typeof row === "object") {
      source = col;
    }
    validateChanges(changes, source, function() {
      applyChanges(changes, source);
    });
  };
  this.setDataAtRowProp = function(row, prop, value, source) {
    var input = setDataInputToArray(row, prop, value),
        i,
        ilen,
        changes = [];
    for (i = 0, ilen = input.length; i < ilen; i++) {
      changes.push([input[i][0], input[i][1], datamap.get(input[i][0], input[i][1]), input[i][2]]);
    }
    if (!source && typeof row === "object") {
      source = prop;
    }
    validateChanges(changes, source, function() {
      applyChanges(changes, source);
    });
  };
  this.listen = function() {
    Handsontable.activeGuid = instance.guid;
    if (document.activeElement && document.activeElement !== document.body) {
      document.activeElement.blur();
    } else if (!document.activeElement) {
      document.body.focus();
    }
  };
  this.unlisten = function() {
    Handsontable.activeGuid = null;
  };
  this.isListening = function() {
    return Handsontable.activeGuid === instance.guid;
  };
  this.destroyEditor = function(revertOriginal) {
    selection.refreshBorders(revertOriginal);
  };
  this.populateFromArray = function(row, col, input, endRow, endCol, source, method, direction, deltas) {
    var c;
    if (!(typeof input === 'object' && typeof input[0] === 'object')) {
      throw new Error("populateFromArray parameter `input` must be an array of arrays");
    }
    c = typeof endRow === 'number' ? new WalkontableCellCoords(endRow, endCol) : null;
    return grid.populateFromArray(new WalkontableCellCoords(row, col), input, c, source, method, direction, deltas);
  };
  this.spliceCol = function(col, index, amount) {
    return datamap.spliceCol.apply(datamap, arguments);
  };
  this.spliceRow = function(row, index, amount) {
    return datamap.spliceRow.apply(datamap, arguments);
  };
  this.getSelected = function() {
    if (selection.isSelected()) {
      return [priv.selRange.from.row, priv.selRange.from.col, priv.selRange.to.row, priv.selRange.to.col];
    }
  };
  this.getSelectedRange = function() {
    if (selection.isSelected()) {
      return priv.selRange;
    }
  };
  this.render = function() {
    if (instance.view) {
      instance.forceFullRender = true;
      selection.refreshBorders(null, true);
    }
  };
  this.loadData = function(data) {
    if (typeof data === 'object' && data !== null) {
      if (!(data.push && data.splice)) {
        data = [data];
      }
    } else if (data === null) {
      data = [];
      var row;
      for (var r = 0,
          rlen = priv.settings.startRows; r < rlen; r++) {
        row = [];
        for (var c = 0,
            clen = priv.settings.startCols; c < clen; c++) {
          row.push(null);
        }
        data.push(row);
      }
    } else {
      throw new Error("loadData only accepts array of objects or array of arrays (" + typeof data + " given)");
    }
    priv.isPopulated = false;
    GridSettings.prototype.data = data;
    if (Array.isArray(priv.settings.dataSchema) || Array.isArray(data[0])) {
      instance.dataType = 'array';
    } else if (typeof priv.settings.dataSchema === 'function') {
      instance.dataType = 'function';
    } else {
      instance.dataType = 'object';
    }
    datamap = new DataMap(instance, priv, GridSettings);
    clearCellSettingCache();
    grid.adjustRowsAndCols();
    Handsontable.hooks.run(instance, 'afterLoadData');
    if (priv.firstRun) {
      priv.firstRun = [null, 'loadData'];
    } else {
      Handsontable.hooks.run(instance, 'afterChange', null, 'loadData');
      instance.render();
    }
    priv.isPopulated = true;
    function clearCellSettingCache() {
      priv.cellSettings.length = 0;
    }
  };
  this.getData = function(r, c, r2, c2) {
    if (typeof r === 'undefined') {
      return datamap.getAll();
    } else {
      return datamap.getRange(new WalkontableCellCoords(r, c), new WalkontableCellCoords(r2, c2), datamap.DESTINATION_RENDERER);
    }
  };
  this.getCopyableData = function(startRow, startCol, endRow, endCol) {
    return datamap.getCopyableText(new WalkontableCellCoords(startRow, startCol), new WalkontableCellCoords(endRow, endCol));
  };
  this.getSchema = function() {
    return datamap.getSchema();
  };
  this.updateSettings = function(settings, init) {
    var i,
        clen;
    if (typeof settings.rows !== "undefined") {
      throw new Error("'rows' setting is no longer supported. do you mean startRows, minRows or maxRows?");
    }
    if (typeof settings.cols !== "undefined") {
      throw new Error("'cols' setting is no longer supported. do you mean startCols, minCols or maxCols?");
    }
    for (i in settings) {
      if (i === 'data') {
        continue;
      } else {
        if (Handsontable.hooks.getRegistered().indexOf(i) > -1) {
          if (typeof settings[i] === 'function' || Array.isArray(settings[i])) {
            instance.addHook(i, settings[i]);
          }
        } else {
          if (!init && settings.hasOwnProperty(i)) {
            GridSettings.prototype[i] = settings[i];
          }
        }
      }
    }
    if (settings.data === void 0 && priv.settings.data === void 0) {
      instance.loadData(null);
    } else if (settings.data !== void 0) {
      instance.loadData(settings.data);
    } else if (settings.columns !== void 0) {
      datamap.createMap();
    }
    clen = instance.countCols();
    priv.cellSettings.length = 0;
    if (clen > 0) {
      var proto,
          column;
      for (i = 0; i < clen; i++) {
        priv.columnSettings[i] = helper.columnFactory(GridSettings, priv.columnsSettingConflicts);
        proto = priv.columnSettings[i].prototype;
        if (GridSettings.prototype.columns) {
          column = GridSettings.prototype.columns[i];
          helper.extend(proto, column);
          helper.extend(proto, expandType(column));
        }
      }
    }
    if (typeof settings.cell !== 'undefined') {
      for (i in settings.cell) {
        if (settings.cell.hasOwnProperty(i)) {
          var cell = settings.cell[i];
          instance.setCellMetaObject(cell.row, cell.col, cell);
        }
      }
    }
    Handsontable.hooks.run(instance, 'afterCellMetaReset');
    if (typeof settings.className !== "undefined") {
      if (GridSettings.prototype.className) {
        dom.removeClass(instance.rootElement, GridSettings.prototype.className);
      }
      if (settings.className) {
        dom.addClass(instance.rootElement, settings.className);
      }
    }
    if (typeof settings.height != 'undefined') {
      var height = settings.height;
      if (typeof height == 'function') {
        height = height();
      }
      instance.rootElement.style.height = height + 'px';
    }
    if (typeof settings.width != 'undefined') {
      var width = settings.width;
      if (typeof width == 'function') {
        width = width();
      }
      instance.rootElement.style.width = width + 'px';
    }
    if (height) {
      instance.rootElement.style.overflow = 'hidden';
    }
    if (!init) {
      Handsontable.hooks.run(instance, 'afterUpdateSettings');
    }
    grid.adjustRowsAndCols();
    if (instance.view && !priv.firstRun) {
      instance.forceFullRender = true;
      selection.refreshBorders(null, true);
    }
  };
  this.getValue = function() {
    var sel = instance.getSelected();
    if (GridSettings.prototype.getValue) {
      if (typeof GridSettings.prototype.getValue === 'function') {
        return GridSettings.prototype.getValue.call(instance);
      } else if (sel) {
        return instance.getData()[sel[0]][GridSettings.prototype.getValue];
      }
    } else if (sel) {
      return instance.getDataAtCell(sel[0], sel[1]);
    }
  };
  function expandType(obj) {
    if (!obj.hasOwnProperty('type')) {
      return;
    }
    var type,
        expandedType = {};
    if (typeof obj.type === 'object') {
      type = obj.type;
    } else if (typeof obj.type === 'string') {
      type = Handsontable.cellTypes[obj.type];
      if (type === void 0) {
        throw new Error('You declared cell type "' + obj.type + '" as a string that is not mapped to a known object. Cell type must be an object or a string mapped to an object in Handsontable.cellTypes');
      }
    }
    for (var i in type) {
      if (type.hasOwnProperty(i) && !obj.hasOwnProperty(i)) {
        expandedType[i] = type[i];
      }
    }
    return expandedType;
  }
  this.getSettings = function() {
    return priv.settings;
  };
  this.clear = function() {
    selection.selectAll();
    selection.empty();
  };
  this.alter = function(action, index, amount, source, keepEmptyRows) {
    grid.alter(action, index, amount, source, keepEmptyRows);
  };
  this.getCell = function(row, col, topmost) {
    return instance.view.getCellAtCoords(new WalkontableCellCoords(row, col), topmost);
  };
  this.getCoords = function(elem) {
    return this.view.wt.wtTable.getCoords.call(this.view.wt.wtTable, elem);
  };
  this.colToProp = function(col) {
    return datamap.colToProp(col);
  };
  this.propToCol = function(prop) {
    return datamap.propToCol(prop);
  };
  this.getDataAtCell = function(row, col) {
    return datamap.get(row, datamap.colToProp(col));
  };
  this.getDataAtRowProp = function(row, prop) {
    return datamap.get(row, prop);
  };
  this.getDataAtCol = function(col) {
    var out = [];
    return out.concat.apply(out, datamap.getRange(new WalkontableCellCoords(0, col), new WalkontableCellCoords(priv.settings.data.length - 1, col), datamap.DESTINATION_RENDERER));
  };
  this.getDataAtProp = function(prop) {
    var out = [],
        range;
    range = datamap.getRange(new WalkontableCellCoords(0, datamap.propToCol(prop)), new WalkontableCellCoords(priv.settings.data.length - 1, datamap.propToCol(prop)), datamap.DESTINATION_RENDERER);
    return out.concat.apply(out, range);
  };
  this.getSourceDataAtCol = function(col) {
    var out = [],
        data = priv.settings.data;
    for (var i = 0; i < data.length; i++) {
      out.push(data[i][col]);
    }
    return out;
  };
  this.getSourceDataAtRow = function(row) {
    return priv.settings.data[row];
  };
  this.getDataAtRow = function(row) {
    var data = datamap.getRange(new WalkontableCellCoords(row, 0), new WalkontableCellCoords(row, this.countCols() - 1), datamap.DESTINATION_RENDERER);
    return data[0];
  };
  this.removeCellMeta = function(row, col, key) {
    var cellMeta = instance.getCellMeta(row, col);
    if (cellMeta[key] != undefined) {
      delete priv.cellSettings[row][col][key];
    }
  };
  this.setCellMetaObject = function(row, col, prop) {
    if (typeof prop === 'object') {
      for (var key in prop) {
        if (prop.hasOwnProperty(key)) {
          var value = prop[key];
          this.setCellMeta(row, col, key, value);
        }
      }
    }
  };
  this.setCellMeta = function(row, col, key, val) {
    if (!priv.cellSettings[row]) {
      priv.cellSettings[row] = [];
    }
    if (!priv.cellSettings[row][col]) {
      priv.cellSettings[row][col] = new priv.columnSettings[col]();
    }
    priv.cellSettings[row][col][key] = val;
    Handsontable.hooks.run(instance, 'afterSetCellMeta', row, col, key, val);
  };
  this.getCellMeta = function(row, col) {
    var prop = datamap.colToProp(col),
        cellProperties;
    row = translateRowIndex(row);
    col = translateColIndex(col);
    if (!priv.columnSettings[col]) {
      priv.columnSettings[col] = helper.columnFactory(GridSettings, priv.columnsSettingConflicts);
    }
    if (!priv.cellSettings[row]) {
      priv.cellSettings[row] = [];
    }
    if (!priv.cellSettings[row][col]) {
      priv.cellSettings[row][col] = new priv.columnSettings[col]();
    }
    cellProperties = priv.cellSettings[row][col];
    cellProperties.row = row;
    cellProperties.col = col;
    cellProperties.prop = prop;
    cellProperties.instance = instance;
    Handsontable.hooks.run(instance, 'beforeGetCellMeta', row, col, cellProperties);
    helper.extend(cellProperties, expandType(cellProperties));
    if (cellProperties.cells) {
      var settings = cellProperties.cells.call(cellProperties, row, col, prop);
      if (settings) {
        helper.extend(cellProperties, settings);
        helper.extend(cellProperties, expandType(settings));
      }
    }
    Handsontable.hooks.run(instance, 'afterGetCellMeta', row, col, cellProperties);
    return cellProperties;
  };
  this.isColumnModificationAllowed = function() {
    return !(instance.dataType === 'object' || instance.getSettings().columns);
  };
  function translateRowIndex(row) {
    return Handsontable.hooks.run(instance, 'modifyRow', row);
  }
  function translateColIndex(col) {
    return Handsontable.hooks.run(instance, 'modifyCol', col);
  }
  var rendererLookup = helper.cellMethodLookupFactory('renderer');
  this.getCellRenderer = function(row, col) {
    var renderer = rendererLookup.call(this, row, col);
    return getRenderer(renderer);
  };
  this.getCellEditor = helper.cellMethodLookupFactory('editor');
  this.getCellValidator = helper.cellMethodLookupFactory('validator');
  this.validateCells = function(callback) {
    var waitingForValidator = new ValidatorsQueue();
    waitingForValidator.onQueueEmpty = callback;
    var i = instance.countRows() - 1;
    while (i >= 0) {
      var j = instance.countCols() - 1;
      while (j >= 0) {
        waitingForValidator.addValidatorToQueue();
        instance.validateCell(instance.getDataAtCell(i, j), instance.getCellMeta(i, j), function() {
          waitingForValidator.removeValidatorFormQueue();
        }, 'validateCells');
        j--;
      }
      i--;
    }
    waitingForValidator.checkIfQueueIsEmpty();
  };
  this.getRowHeader = function(row) {
    if (row === void 0) {
      var out = [];
      for (var i = 0,
          ilen = instance.countRows(); i < ilen; i++) {
        out.push(instance.getRowHeader(i));
      }
      return out;
    } else if (Array.isArray(priv.settings.rowHeaders) && priv.settings.rowHeaders[row] !== void 0) {
      return priv.settings.rowHeaders[row];
    } else if (typeof priv.settings.rowHeaders === 'function') {
      return priv.settings.rowHeaders(row);
    } else if (priv.settings.rowHeaders && typeof priv.settings.rowHeaders !== 'string' && typeof priv.settings.rowHeaders !== 'number') {
      return row + 1;
    } else {
      return priv.settings.rowHeaders;
    }
  };
  this.hasRowHeaders = function() {
    return !!priv.settings.rowHeaders;
  };
  this.hasColHeaders = function() {
    if (priv.settings.colHeaders !== void 0 && priv.settings.colHeaders !== null) {
      return !!priv.settings.colHeaders;
    }
    for (var i = 0,
        ilen = instance.countCols(); i < ilen; i++) {
      if (instance.getColHeader(i)) {
        return true;
      }
    }
    return false;
  };
  this.getColHeader = function(col) {
    if (col === void 0) {
      var out = [];
      for (var i = 0,
          ilen = instance.countCols(); i < ilen; i++) {
        out.push(instance.getColHeader(i));
      }
      return out;
    } else {
      var baseCol = col;
      col = Handsontable.hooks.run(instance, 'modifyCol', col);
      if (priv.settings.columns && priv.settings.columns[col] && priv.settings.columns[col].title) {
        return priv.settings.columns[col].title;
      } else if (Array.isArray(priv.settings.colHeaders) && priv.settings.colHeaders[col] !== void 0) {
        return priv.settings.colHeaders[col];
      } else if (typeof priv.settings.colHeaders === 'function') {
        return priv.settings.colHeaders(col);
      } else if (priv.settings.colHeaders && typeof priv.settings.colHeaders !== 'string' && typeof priv.settings.colHeaders !== 'number') {
        return helper.spreadsheetColumnLabel(baseCol);
      } else {
        return priv.settings.colHeaders;
      }
    }
  };
  this._getColWidthFromSettings = function(col) {
    var cellProperties = instance.getCellMeta(0, col);
    var width = cellProperties.width;
    if (width === void 0 || width === priv.settings.width) {
      width = cellProperties.colWidths;
    }
    if (width !== void 0 && width !== null) {
      switch (typeof width) {
        case 'object':
          width = width[col];
          break;
        case 'function':
          width = width(col);
          break;
      }
      if (typeof width === 'string') {
        width = parseInt(width, 10);
      }
    }
    return width;
  };
  this.getColWidth = function(col) {
    var width = instance._getColWidthFromSettings(col);
    if (!width) {
      width = 50;
    }
    width = Handsontable.hooks.run(instance, 'modifyColWidth', width, col);
    return width;
  };
  this._getRowHeightFromSettings = function(row) {
    var height = priv.settings.rowHeights;
    if (height !== void 0 && height !== null) {
      switch (typeof height) {
        case 'object':
          height = height[row];
          break;
        case 'function':
          height = height(row);
          break;
      }
      if (typeof height === 'string') {
        height = parseInt(height, 10);
      }
    }
    return height;
  };
  this.getRowHeight = function(row) {
    var height = instance._getRowHeightFromSettings(row);
    height = Handsontable.hooks.run(instance, 'modifyRowHeight', height, row);
    return height;
  };
  this.countRows = function() {
    return priv.settings.data.length;
  };
  this.countCols = function() {
    if (instance.dataType === 'object' || instance.dataType === 'function') {
      if (priv.settings.columns && priv.settings.columns.length) {
        return priv.settings.columns.length;
      } else {
        return datamap.colToPropCache.length;
      }
    } else if (instance.dataType === 'array') {
      if (priv.settings.columns && priv.settings.columns.length) {
        return priv.settings.columns.length;
      } else if (priv.settings.data && priv.settings.data[0] && priv.settings.data[0].length) {
        return priv.settings.data[0].length;
      } else {
        return 0;
      }
    }
  };
  this.rowOffset = function() {
    return instance.view.wt.wtTable.getFirstRenderedRow();
  };
  this.colOffset = function() {
    return instance.view.wt.wtTable.getFirstRenderedColumn();
  };
  this.countRenderedRows = function() {
    return instance.view.wt.drawn ? instance.view.wt.wtTable.getRenderedRowsCount() : -1;
  };
  this.countVisibleRows = function() {
    return instance.view.wt.drawn ? instance.view.wt.wtTable.getVisibleRowsCount() : -1;
  };
  this.countRenderedCols = function() {
    return instance.view.wt.drawn ? instance.view.wt.wtTable.getRenderedColumnsCount() : -1;
  };
  this.countVisibleCols = function() {
    return instance.view.wt.drawn ? instance.view.wt.wtTable.getVisibleColumnsCount() : -1;
  };
  this.countEmptyRows = function(ending) {
    var i = instance.countRows() - 1,
        empty = 0,
        row;
    while (i >= 0) {
      row = Handsontable.hooks.run(this, 'modifyRow', i);
      if (instance.isEmptyRow(row)) {
        empty++;
      } else if (ending) {
        break;
      }
      i--;
    }
    return empty;
  };
  this.countEmptyCols = function(ending) {
    if (instance.countRows() < 1) {
      return 0;
    }
    var i = instance.countCols() - 1,
        empty = 0;
    while (i >= 0) {
      if (instance.isEmptyCol(i)) {
        empty++;
      } else if (ending) {
        break;
      }
      i--;
    }
    return empty;
  };
  this.isEmptyRow = function(row) {
    return priv.settings.isEmptyRow.call(instance, row);
  };
  this.isEmptyCol = function(col) {
    return priv.settings.isEmptyCol.call(instance, col);
  };
  this.selectCell = function(row, col, endRow, endCol, scrollToCell, changeListener) {
    var coords;
    changeListener = typeof changeListener === 'undefined' || changeListener === true;
    if (typeof row !== 'number' || row < 0 || row >= instance.countRows()) {
      return false;
    }
    if (typeof col !== 'number' || col < 0 || col >= instance.countCols()) {
      return false;
    }
    if (typeof endRow !== 'undefined') {
      if (typeof endRow !== 'number' || endRow < 0 || endRow >= instance.countRows()) {
        return false;
      }
      if (typeof endCol !== 'number' || endCol < 0 || endCol >= instance.countCols()) {
        return false;
      }
    }
    coords = new WalkontableCellCoords(row, col);
    priv.selRange = new WalkontableCellRange(coords, coords, coords);
    if (document.activeElement && document.activeElement !== document.documentElement && document.activeElement !== document.body) {
      document.activeElement.blur();
    }
    if (changeListener) {
      instance.listen();
    }
    if (typeof endRow === 'undefined') {
      selection.setRangeEnd(priv.selRange.from, scrollToCell);
    } else {
      selection.setRangeEnd(new WalkontableCellCoords(endRow, endCol), scrollToCell);
    }
    instance.selection.finish();
    return true;
  };
  this.selectCellByProp = function(row, prop, endRow, endProp, scrollToCell) {
    arguments[1] = datamap.propToCol(arguments[1]);
    if (typeof arguments[3] !== "undefined") {
      arguments[3] = datamap.propToCol(arguments[3]);
    }
    return instance.selectCell.apply(instance, arguments);
  };
  this.deselectCell = function() {
    selection.deselect();
  };
  this.destroy = function() {
    instance._clearTimeouts();
    if (instance.view) {
      instance.view.destroy();
    }
    dom.empty(instance.rootElement);
    eventManager.clear();
    Handsontable.hooks.run(instance, 'afterDestroy');
    Handsontable.hooks.destroy(instance);
    for (var i in instance) {
      if (instance.hasOwnProperty(i)) {
        if (typeof instance[i] === "function") {
          if (i !== "runHooks") {
            instance[i] = postMortem;
          }
        } else if (i !== "guid") {
          instance[i] = null;
        }
      }
    }
    priv = null;
    datamap = null;
    grid = null;
    selection = null;
    editorManager = null;
    instance = null;
    GridSettings = null;
  };
  function postMortem() {
    throw new Error("This method cannot be called because this Handsontable instance has been destroyed");
  }
  this.getActiveEditor = function() {
    return editorManager.getActiveEditor();
  };
  this.getPlugin = function(pluginName) {
    return getPlugin(this, pluginName);
  };
  this.getInstance = function() {
    return instance;
  };
  this.addHook = function(key, callback) {
    Handsontable.hooks.add(key, callback, instance);
  };
  this.addHookOnce = function(key, callback) {
    Handsontable.hooks.once(key, callback, instance);
  };
  this.removeHook = function(key, callback) {
    Handsontable.hooks.remove(key, callback, instance);
  };
  this.runHooks = function(key, p1, p2, p3, p4, p5, p6) {
    return Handsontable.hooks.run(instance, key, p1, p2, p3, p4, p5, p6);
  };
  this.timeouts = [];
  this._registerTimeout = function(handle) {
    this.timeouts.push(handle);
  };
  this._clearTimeouts = function() {
    for (var i = 0,
        ilen = this.timeouts.length; i < ilen; i++) {
      clearTimeout(this.timeouts[i]);
    }
  };
  this.version = Handsontable.version;
};
var DefaultSettings = function() {};
DefaultSettings.prototype = {
  data: void 0,
  dataSchema: void 0,
  width: void 0,
  height: void 0,
  startRows: 5,
  startCols: 5,
  rowHeaders: null,
  colHeaders: null,
  colWidths: void 0,
  columns: void 0,
  cells: void 0,
  cell: [],
  comments: false,
  customBorders: false,
  minRows: 0,
  minCols: 0,
  maxRows: Infinity,
  maxCols: Infinity,
  minSpareRows: 0,
  minSpareCols: 0,
  allowInsertRow: true,
  allowInsertColumn: true,
  allowRemoveRow: true,
  allowRemoveColumn: true,
  multiSelect: true,
  fillHandle: true,
  fixedRowsTop: 0,
  fixedColumnsLeft: 0,
  outsideClickDeselects: true,
  enterBeginsEditing: true,
  enterMoves: {
    row: 1,
    col: 0
  },
  tabMoves: {
    row: 0,
    col: 1
  },
  autoWrapRow: false,
  autoWrapCol: false,
  copyRowsLimit: 1000,
  copyColsLimit: 1000,
  pasteMode: 'overwrite',
  persistentState: false,
  currentRowClassName: void 0,
  currentColClassName: void 0,
  stretchH: 'none',
  isEmptyRow: function(row) {
    var col,
        colLen,
        value,
        meta;
    for (col = 0, colLen = this.countCols(); col < colLen; col++) {
      value = this.getDataAtCell(row, col);
      if (value !== '' && value !== null && typeof value !== 'undefined') {
        if (typeof value === 'object') {
          meta = this.getCellMeta(row, col);
          return helper.isObjectEquals(this.getSchema()[meta.prop], value);
        }
        return false;
      }
    }
    return true;
  },
  isEmptyCol: function(col) {
    var row,
        rowLen,
        value;
    for (row = 0, rowLen = this.countRows(); row < rowLen; row++) {
      value = this.getDataAtCell(row, col);
      if (value !== '' && value !== null && typeof value !== 'undefined') {
        return false;
      }
    }
    return true;
  },
  observeDOMVisibility: true,
  allowInvalid: true,
  invalidCellClassName: 'htInvalid',
  placeholder: false,
  placeholderCellClassName: 'htPlaceholder',
  readOnlyCellClassName: 'htDimmed',
  renderer: void 0,
  commentedCellClassName: 'htCommentCell',
  fragmentSelection: false,
  readOnly: false,
  search: false,
  type: 'text',
  copyable: true,
  editor: void 0,
  autoComplete: void 0,
  debug: false,
  wordWrap: true,
  noWordWrapClassName: 'htNoWrap',
  contextMenu: void 0,
  undo: void 0,
  columnSorting: void 0,
  manualColumnMove: void 0,
  manualColumnResize: void 0,
  manualRowMove: void 0,
  manualRowResize: void 0,
  mergeCells: false,
  viewportRowRenderingOffset: 10,
  viewportColumnRenderingOffset: 10,
  groups: void 0,
  validator: void 0,
  disableVisualSelection: false,
  sortIndicator: false,
  manualColumnFreeze: void 0,
  trimWhitespace: true,
  settings: void 0,
  source: void 0,
  title: void 0,
  checkedTemplate: void 0,
  uncheckedTemplate: void 0,
  format: void 0,
  className: void 0
};
Handsontable.DefaultSettings = DefaultSettings;


//# 
},{"./3rdparty/walkontable/src/cell/coords.js":5,"./3rdparty/walkontable/src/cell/range.js":6,"./3rdparty/walkontable/src/selection.js":18,"./dataMap.js":26,"./dom.js":27,"./editorManager.js":28,"./eventManager.js":41,"./helpers.js":42,"./plugins.js":45,"./renderers.js":70,"./tableView.js":85,"numeral":"numeral"}],26:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  DataMap: {get: function() {
      return DataMap;
    }},
  __esModule: {value: true}
});
var $__helpers_46_js__,
    $__multiMap_46_js__,
    $__SheetClip__;
var helper = ($__helpers_46_js__ = require("./helpers.js"), $__helpers_46_js__ && $__helpers_46_js__.__esModule && $__helpers_46_js__ || {default: $__helpers_46_js__});
var MultiMap = ($__multiMap_46_js__ = require("./multiMap.js"), $__multiMap_46_js__ && $__multiMap_46_js__.__esModule && $__multiMap_46_js__ || {default: $__multiMap_46_js__}).MultiMap;
var SheetClip = ($__SheetClip__ = require("SheetClip"), $__SheetClip__ && $__SheetClip__.__esModule && $__SheetClip__ || {default: $__SheetClip__}).default;
;
Handsontable.DataMap = DataMap;
function DataMap(instance, priv, GridSettings) {
  this.instance = instance;
  this.priv = priv;
  this.GridSettings = GridSettings;
  this.dataSource = this.instance.getSettings().data;
  if (this.dataSource[0]) {
    this.duckSchema = this.recursiveDuckSchema(this.dataSource[0]);
  } else {
    this.duckSchema = {};
  }
  this.createMap();
}
DataMap.prototype.DESTINATION_RENDERER = 1;
DataMap.prototype.DESTINATION_CLIPBOARD_GENERATOR = 2;
DataMap.prototype.recursiveDuckSchema = function(object) {
  return Handsontable.helper.duckSchema(object);
};
DataMap.prototype.recursiveDuckColumns = function(schema, lastCol, parent) {
  var prop,
      i;
  if (typeof lastCol === 'undefined') {
    lastCol = 0;
    parent = '';
  }
  if (typeof schema === "object" && !Array.isArray(schema)) {
    for (i in schema) {
      if (schema.hasOwnProperty(i)) {
        if (schema[i] === null) {
          prop = parent + i;
          this.colToPropCache.push(prop);
          this.propToColCache.set(prop, lastCol);
          lastCol++;
        } else {
          lastCol = this.recursiveDuckColumns(schema[i], lastCol, i + '.');
        }
      }
    }
  }
  return lastCol;
};
DataMap.prototype.createMap = function() {
  var i,
      ilen,
      schema = this.getSchema();
  if (typeof schema === "undefined") {
    throw new Error("trying to create `columns` definition but you didnt' provide `schema` nor `data`");
  }
  this.colToPropCache = [];
  this.propToColCache = new MultiMap();
  var columns = this.instance.getSettings().columns;
  if (columns) {
    for (i = 0, ilen = columns.length; i < ilen; i++) {
      if (typeof columns[i].data != 'undefined') {
        this.colToPropCache[i] = columns[i].data;
        this.propToColCache.set(columns[i].data, i);
      }
    }
  } else {
    this.recursiveDuckColumns(schema);
  }
};
DataMap.prototype.colToProp = function(col) {
  col = Handsontable.hooks.run(this.instance, 'modifyCol', col);
  if (this.colToPropCache && typeof this.colToPropCache[col] !== 'undefined') {
    return this.colToPropCache[col];
  }
  return col;
};
DataMap.prototype.propToCol = function(prop) {
  var col;
  if (typeof this.propToColCache.get(prop) !== 'undefined') {
    col = this.propToColCache.get(prop);
  } else {
    col = prop;
  }
  col = Handsontable.hooks.run(this.instance, 'modifyCol', col);
  return col;
};
DataMap.prototype.getSchema = function() {
  var schema = this.instance.getSettings().dataSchema;
  if (schema) {
    if (typeof schema === 'function') {
      return schema();
    }
    return schema;
  }
  return this.duckSchema;
};
DataMap.prototype.createRow = function(index, amount, createdAutomatically) {
  var row,
      colCount = this.instance.countCols(),
      numberOfCreatedRows = 0,
      currentIndex;
  if (!amount) {
    amount = 1;
  }
  if (typeof index !== 'number' || index >= this.instance.countRows()) {
    index = this.instance.countRows();
  }
  currentIndex = index;
  var maxRows = this.instance.getSettings().maxRows;
  while (numberOfCreatedRows < amount && this.instance.countRows() < maxRows) {
    if (this.instance.dataType === 'array') {
      row = [];
      for (var c = 0; c < colCount; c++) {
        row.push(null);
      }
    } else if (this.instance.dataType === 'function') {
      row = this.instance.getSettings().dataSchema(index);
    } else {
      row = {};
      helper.deepExtend(row, this.getSchema());
    }
    if (index === this.instance.countRows()) {
      this.dataSource.push(row);
    } else {
      this.dataSource.splice(index, 0, row);
    }
    numberOfCreatedRows++;
    currentIndex++;
  }
  Handsontable.hooks.run(this.instance, 'afterCreateRow', index, numberOfCreatedRows, createdAutomatically);
  this.instance.forceFullRender = true;
  return numberOfCreatedRows;
};
DataMap.prototype.createCol = function(index, amount, createdAutomatically) {
  if (!this.instance.isColumnModificationAllowed()) {
    throw new Error("Cannot create new column. When data source in an object, " + "you can only have as much columns as defined in first data row, data schema or in the 'columns' setting." + "If you want to be able to add new columns, you have to use array datasource.");
  }
  var rlen = this.instance.countRows(),
      data = this.dataSource,
      constructor,
      numberOfCreatedCols = 0,
      currentIndex;
  if (!amount) {
    amount = 1;
  }
  currentIndex = index;
  var maxCols = this.instance.getSettings().maxCols;
  while (numberOfCreatedCols < amount && this.instance.countCols() < maxCols) {
    constructor = helper.columnFactory(this.GridSettings, this.priv.columnsSettingConflicts);
    if (typeof index !== 'number' || index >= this.instance.countCols()) {
      for (var r = 0; r < rlen; r++) {
        if (typeof data[r] === 'undefined') {
          data[r] = [];
        }
        data[r].push(null);
      }
      this.priv.columnSettings.push(constructor);
    } else {
      for (var r = 0; r < rlen; r++) {
        data[r].splice(currentIndex, 0, null);
      }
      this.priv.columnSettings.splice(currentIndex, 0, constructor);
    }
    numberOfCreatedCols++;
    currentIndex++;
  }
  Handsontable.hooks.run(this.instance, 'afterCreateCol', index, numberOfCreatedCols, createdAutomatically);
  this.instance.forceFullRender = true;
  return numberOfCreatedCols;
};
DataMap.prototype.removeRow = function(index, amount) {
  if (!amount) {
    amount = 1;
  }
  if (typeof index !== 'number') {
    index = -amount;
  }
  index = (this.instance.countRows() + index) % this.instance.countRows();
  var logicRows = this.physicalRowsToLogical(index, amount);
  var actionWasNotCancelled = Handsontable.hooks.run(this.instance, 'beforeRemoveRow', index, amount);
  if (actionWasNotCancelled === false) {
    return;
  }
  var data = this.dataSource;
  var newData = data.filter(function(row, index) {
    return logicRows.indexOf(index) == -1;
  });
  data.length = 0;
  Array.prototype.push.apply(data, newData);
  Handsontable.hooks.run(this.instance, 'afterRemoveRow', index, amount);
  this.instance.forceFullRender = true;
};
DataMap.prototype.removeCol = function(index, amount) {
  if (this.instance.dataType === 'object' || this.instance.getSettings().columns) {
    throw new Error("cannot remove column with object data source or columns option specified");
  }
  if (!amount) {
    amount = 1;
  }
  if (typeof index !== 'number') {
    index = -amount;
  }
  index = (this.instance.countCols() + index) % this.instance.countCols();
  var actionWasNotCancelled = Handsontable.hooks.run(this.instance, 'beforeRemoveCol', index, amount);
  if (actionWasNotCancelled === false) {
    return;
  }
  var data = this.dataSource;
  for (var r = 0,
      rlen = this.instance.countRows(); r < rlen; r++) {
    data[r].splice(index, amount);
  }
  this.priv.columnSettings.splice(index, amount);
  Handsontable.hooks.run(this.instance, 'afterRemoveCol', index, amount);
  this.instance.forceFullRender = true;
};
DataMap.prototype.spliceCol = function(col, index, amount) {
  var elements = 4 <= arguments.length ? [].slice.call(arguments, 3) : [];
  var colData = this.instance.getDataAtCol(col);
  var removed = colData.slice(index, index + amount);
  var after = colData.slice(index + amount);
  helper.extendArray(elements, after);
  var i = 0;
  while (i < amount) {
    elements.push(null);
    i++;
  }
  helper.to2dArray(elements);
  this.instance.populateFromArray(index, col, elements, null, null, 'spliceCol');
  return removed;
};
DataMap.prototype.spliceRow = function(row, index, amount) {
  var elements = 4 <= arguments.length ? [].slice.call(arguments, 3) : [];
  var rowData = this.instance.getSourceDataAtRow(row);
  var removed = rowData.slice(index, index + amount);
  var after = rowData.slice(index + amount);
  helper.extendArray(elements, after);
  var i = 0;
  while (i < amount) {
    elements.push(null);
    i++;
  }
  this.instance.populateFromArray(row, index, [elements], null, null, 'spliceRow');
  return removed;
};
DataMap.prototype.get = function(row, prop) {
  row = Handsontable.hooks.run(this.instance, 'modifyRow', row);
  if (typeof prop === 'string' && prop.indexOf('.') > -1) {
    var sliced = prop.split(".");
    var out = this.dataSource[row];
    if (!out) {
      return null;
    }
    for (var i = 0,
        ilen = sliced.length; i < ilen; i++) {
      out = out[sliced[i]];
      if (typeof out === 'undefined') {
        return null;
      }
    }
    return out;
  } else if (typeof prop === 'function') {
    return prop(this.dataSource.slice(row, row + 1)[0]);
  } else {
    return this.dataSource[row] ? this.dataSource[row][prop] : null;
  }
};
var copyableLookup = helper.cellMethodLookupFactory('copyable', false);
DataMap.prototype.getCopyable = function(row, prop) {
  if (copyableLookup.call(this.instance, row, this.propToCol(prop))) {
    return this.get(row, prop);
  }
  return '';
};
DataMap.prototype.set = function(row, prop, value, source) {
  row = Handsontable.hooks.run(this.instance, 'modifyRow', row, source || "datamapGet");
  if (typeof prop === 'string' && prop.indexOf('.') > -1) {
    var sliced = prop.split(".");
    var out = this.dataSource[row];
    for (var i = 0,
        ilen = sliced.length - 1; i < ilen; i++) {
      if (typeof out[sliced[i]] === 'undefined') {
        out[sliced[i]] = {};
      }
      out = out[sliced[i]];
    }
    out[sliced[i]] = value;
  } else if (typeof prop === 'function') {
    prop(this.dataSource.slice(row, row + 1)[0], value);
  } else {
    this.dataSource[row][prop] = value;
  }
};
DataMap.prototype.physicalRowsToLogical = function(index, amount) {
  var totalRows = this.instance.countRows();
  var physicRow = (totalRows + index) % totalRows;
  var logicRows = [];
  var rowsToRemove = amount;
  var row;
  while (physicRow < totalRows && rowsToRemove) {
    row = Handsontable.hooks.run(this.instance, 'modifyRow', physicRow);
    logicRows.push(row);
    rowsToRemove--;
    physicRow++;
  }
  return logicRows;
};
DataMap.prototype.clear = function() {
  for (var r = 0; r < this.instance.countRows(); r++) {
    for (var c = 0; c < this.instance.countCols(); c++) {
      this.set(r, this.colToProp(c), '');
    }
  }
};
DataMap.prototype.getAll = function() {
  return this.dataSource;
};
DataMap.prototype.getRange = function(start, end, destination) {
  var r,
      rlen,
      c,
      clen,
      output = [],
      row;
  var getFn = destination === this.DESTINATION_CLIPBOARD_GENERATOR ? this.getCopyable : this.get;
  rlen = Math.max(start.row, end.row);
  clen = Math.max(start.col, end.col);
  for (r = Math.min(start.row, end.row); r <= rlen; r++) {
    row = [];
    for (c = Math.min(start.col, end.col); c <= clen; c++) {
      row.push(getFn.call(this, r, this.colToProp(c)));
    }
    output.push(row);
  }
  return output;
};
DataMap.prototype.getText = function(start, end) {
  return SheetClip.stringify(this.getRange(start, end, this.DESTINATION_RENDERER));
};
DataMap.prototype.getCopyableText = function(start, end) {
  return SheetClip.stringify(this.getRange(start, end, this.DESTINATION_CLIPBOARD_GENERATOR));
};


//# 
},{"./helpers.js":42,"./multiMap.js":43,"SheetClip":undefined}],27:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  enableImmediatePropagation: {get: function() {
      return enableImmediatePropagation;
    }},
  closest: {get: function() {
      return closest;
    }},
  isChildOf: {get: function() {
      return isChildOf;
    }},
  isChildOfWebComponentTable: {get: function() {
      return isChildOfWebComponentTable;
    }},
  polymerWrap: {get: function() {
      return polymerWrap;
    }},
  polymerUnwrap: {get: function() {
      return polymerUnwrap;
    }},
  isWebComponentSupportedNatively: {get: function() {
      return isWebComponentSupportedNatively;
    }},
  index: {get: function() {
      return index;
    }},
  hasClass: {get: function() {
      return hasClass;
    }},
  addClass: {get: function() {
      return addClass;
    }},
  removeClass: {get: function() {
      return removeClass;
    }},
  removeTextNodes: {get: function() {
      return removeTextNodes;
    }},
  empty: {get: function() {
      return empty;
    }},
  HTML_CHARACTERS: {get: function() {
      return HTML_CHARACTERS;
    }},
  fastInnerHTML: {get: function() {
      return fastInnerHTML;
    }},
  fastInnerText: {get: function() {
      return fastInnerText;
    }},
  isVisible: {get: function() {
      return isVisible;
    }},
  offset: {get: function() {
      return offset;
    }},
  getWindowScrollTop: {get: function() {
      return getWindowScrollTop;
    }},
  getWindowScrollLeft: {get: function() {
      return getWindowScrollLeft;
    }},
  getScrollTop: {get: function() {
      return getScrollTop;
    }},
  getScrollLeft: {get: function() {
      return getScrollLeft;
    }},
  getScrollableElement: {get: function() {
      return getScrollableElement;
    }},
  getTrimmingContainer: {get: function() {
      return getTrimmingContainer;
    }},
  getStyle: {get: function() {
      return getStyle;
    }},
  getComputedStyle: {get: function() {
      return getComputedStyle;
    }},
  outerWidth: {get: function() {
      return outerWidth;
    }},
  outerHeight: {get: function() {
      return outerHeight;
    }},
  innerHeight: {get: function() {
      return innerHeight;
    }},
  innerWidth: {get: function() {
      return innerWidth;
    }},
  addEvent: {get: function() {
      return addEvent;
    }},
  removeEvent: {get: function() {
      return removeEvent;
    }},
  hasCaptionProblem: {get: function() {
      return hasCaptionProblem;
    }},
  getCaretPosition: {get: function() {
      return getCaretPosition;
    }},
  getSelectionEndPosition: {get: function() {
      return getSelectionEndPosition;
    }},
  setCaretPosition: {get: function() {
      return setCaretPosition;
    }},
  getScrollbarWidth: {get: function() {
      return getScrollbarWidth;
    }},
  isIE8: {get: function() {
      return isIE8;
    }},
  isIE9: {get: function() {
      return isIE9;
    }},
  isSafari: {get: function() {
      return isSafari;
    }},
  setOverlayPosition: {get: function() {
      return setOverlayPosition;
    }},
  getCssTransform: {get: function() {
      return getCssTransform;
    }},
  resetCssTransform: {get: function() {
      return resetCssTransform;
    }},
  __esModule: {value: true}
});
function enableImmediatePropagation(event) {
  if (event != null && event.isImmediatePropagationEnabled == null) {
    event.stopImmediatePropagation = function() {
      this.isImmediatePropagationEnabled = false;
      this.cancelBubble = true;
    };
    event.isImmediatePropagationEnabled = true;
    event.isImmediatePropagationStopped = function() {
      return !this.isImmediatePropagationEnabled;
    };
  }
}
function closest(element, nodes, until) {
  while (element != null && element !== until) {
    if (element.nodeType === Node.ELEMENT_NODE && (nodes.indexOf(element.nodeName) > -1 || nodes.indexOf(element) > -1)) {
      return element;
    }
    if (element.host && element.nodeType === Node.DOCUMENT_FRAGMENT_NODE) {
      element = element.host;
    } else {
      element = element.parentNode;
    }
  }
  return null;
}
function isChildOf(child, parent) {
  var node = child.parentNode;
  var queriedParents = [];
  if (typeof parent === "string") {
    queriedParents = Array.prototype.slice.call(document.querySelectorAll(parent), 0);
  } else {
    queriedParents.push(parent);
  }
  while (node != null) {
    if (queriedParents.indexOf(node) > -1) {
      return true;
    }
    node = node.parentNode;
  }
  return false;
}
function isChildOfWebComponentTable(element) {
  var hotTableName = 'hot-table',
      result = false,
      parentNode;
  parentNode = polymerWrap(element);
  function isHotTable(element) {
    return element.nodeType === Node.ELEMENT_NODE && element.nodeName === hotTableName.toUpperCase();
  }
  while (parentNode != null) {
    if (isHotTable(parentNode)) {
      result = true;
      break;
    } else if (parentNode.host && parentNode.nodeType === Node.DOCUMENT_FRAGMENT_NODE) {
      result = isHotTable(parentNode.host);
      if (result) {
        break;
      }
      parentNode = parentNode.host;
    }
    parentNode = parentNode.parentNode;
  }
  return result;
}
function polymerWrap(element) {
  return typeof Polymer !== 'undefined' && typeof wrap === 'function' ? wrap(element) : element;
}
function polymerUnwrap(element) {
  return typeof Polymer !== 'undefined' && typeof unwrap === 'function' ? unwrap(element) : element;
}
function isWebComponentSupportedNatively() {
  var test = document.createElement('div');
  return test.createShadowRoot && test.createShadowRoot.toString().match(/\[native code\]/) ? true : false;
}
function index(elem) {
  var i = 0;
  if (elem.previousSibling) {
    while (elem = elem.previousSibling) {
      ++i;
    }
  }
  return i;
}
var classListSupport = document.documentElement.classList ? true : false;
var _hasClass,
    _addClass,
    _removeClass;
function filterEmptyClassNames(classNames) {
  var len = 0,
      result = [];
  if (!classNames || !classNames.length) {
    return result;
  }
  while (classNames[len]) {
    result.push(classNames[len]);
    len++;
  }
  return result;
}
if (classListSupport) {
  var isSupportMultipleClassesArg = (function() {
    var element = document.createElement('div');
    element.classList.add('test', 'test2');
    return element.classList.contains('test2');
  }());
  _hasClass = function _hasClass(element, className) {
    if (className === '') {
      return false;
    }
    return element.classList.contains(className);
  };
  _addClass = function _addClass(element, className) {
    var len = 0;
    if (typeof className === 'string') {
      className = className.split(' ');
    }
    className = filterEmptyClassNames(className);
    if (isSupportMultipleClassesArg) {
      element.classList.add.apply(element.classList, className);
    } else {
      while (className && className[len]) {
        element.classList.add(className[len]);
        len++;
      }
    }
  };
  _removeClass = function _removeClass(element, className) {
    var len = 0;
    if (typeof className === 'string') {
      className = className.split(' ');
    }
    className = filterEmptyClassNames(className);
    if (isSupportMultipleClassesArg) {
      element.classList.remove.apply(element.classList, className);
    } else {
      while (className && className[len]) {
        element.classList.remove(className[len]);
        len++;
      }
    }
  };
} else {
  var createClassNameRegExp = function createClassNameRegExp(className) {
    return new RegExp('(\\s|^)' + className + '(\\s|$)');
  };
  _hasClass = function _hasClass(element, className) {
    return element.className.match(createClassNameRegExp(className)) ? true : false;
  };
  _addClass = function _addClass(element, className) {
    var len = 0,
        _className = element.className;
    if (typeof className === 'string') {
      className = className.split(' ');
    }
    if (_className === '') {
      _className = className.join(' ');
    } else {
      while (className && className[len]) {
        if (!createClassNameRegExp(className[len]).test(_className)) {
          _className += ' ' + className[len];
        }
        len++;
      }
    }
    element.className = _className;
  };
  _removeClass = function _removeClass(element, className) {
    var len = 0,
        _className = element.className;
    if (typeof className === 'string') {
      className = className.split(' ');
    }
    while (className && className[len]) {
      _className = _className.replace(createClassNameRegExp(className[len]), ' ').trim();
      len++;
    }
    if (element.className !== _className) {
      element.className = _className;
    }
  };
}
function hasClass(element, className) {
  return _hasClass(element, className);
}
function addClass(element, className) {
  return _addClass(element, className);
}
function removeClass(element, className) {
  return _removeClass(element, className);
}
function removeTextNodes(elem, parent) {
  if (elem.nodeType === 3) {
    parent.removeChild(elem);
  } else if (['TABLE', 'THEAD', 'TBODY', 'TFOOT', 'TR'].indexOf(elem.nodeName) > -1) {
    var childs = elem.childNodes;
    for (var i = childs.length - 1; i >= 0; i--) {
      removeTextNodes(childs[i], elem);
    }
  }
}
function empty(element) {
  var child;
  while (child = element.lastChild) {
    element.removeChild(child);
  }
}
var HTML_CHARACTERS = /(<(.*)>|&(.*);)/;
function fastInnerHTML(element, content) {
  if (HTML_CHARACTERS.test(content)) {
    element.innerHTML = content;
  } else {
    fastInnerText(element, content);
  }
}
var textContextSupport = document.createTextNode('test').textContent ? true : false;
function fastInnerText(element, content) {
  var child = element.firstChild;
  if (child && child.nodeType === 3 && child.nextSibling === null) {
    if (textContextSupport) {
      child.textContent = content;
    } else {
      child.data = content;
    }
  } else {
    empty(element);
    element.appendChild(document.createTextNode(content));
  }
}
function isVisible(elem) {
  var next = elem;
  while (polymerUnwrap(next) !== document.documentElement) {
    if (next === null) {
      return false;
    } else if (next.nodeType === Node.DOCUMENT_FRAGMENT_NODE) {
      if (next.host) {
        if (next.host.impl) {
          return isVisible(next.host.impl);
        } else if (next.host) {
          return isVisible(next.host);
        } else {
          throw new Error("Lost in Web Components world");
        }
      } else {
        return false;
      }
    } else if (next.style.display === 'none') {
      return false;
    }
    next = next.parentNode;
  }
  return true;
}
function offset(elem) {
  var offsetLeft,
      offsetTop,
      lastElem,
      docElem,
      box;
  docElem = document.documentElement;
  if (hasCaptionProblem() && elem.firstChild && elem.firstChild.nodeName === 'CAPTION') {
    box = elem.getBoundingClientRect();
    return {
      top: box.top + (window.pageYOffset || docElem.scrollTop) - (docElem.clientTop || 0),
      left: box.left + (window.pageXOffset || docElem.scrollLeft) - (docElem.clientLeft || 0)
    };
  }
  offsetLeft = elem.offsetLeft;
  offsetTop = elem.offsetTop;
  lastElem = elem;
  while (elem = elem.offsetParent) {
    if (elem === document.body) {
      break;
    }
    offsetLeft += elem.offsetLeft;
    offsetTop += elem.offsetTop;
    lastElem = elem;
  }
  if (lastElem && lastElem.style.position === 'fixed') {
    offsetLeft += window.pageXOffset || docElem.scrollLeft;
    offsetTop += window.pageYOffset || docElem.scrollTop;
  }
  return {
    left: offsetLeft,
    top: offsetTop
  };
}
function getWindowScrollTop() {
  var res = window.scrollY;
  if (res == void 0) {
    res = document.documentElement.scrollTop;
  }
  return res;
}
function getWindowScrollLeft() {
  var res = window.scrollX;
  if (res == void 0) {
    res = document.documentElement.scrollLeft;
  }
  return res;
}
function getScrollTop(elem) {
  if (elem === window) {
    return getWindowScrollTop(elem);
  } else {
    return elem.scrollTop;
  }
}
function getScrollLeft(elem) {
  if (elem === window) {
    return getWindowScrollLeft(elem);
  } else {
    return elem.scrollLeft;
  }
}
function getScrollableElement(element) {
  var el = element.parentNode,
      props = ['auto', 'scroll'],
      overflow,
      overflowX,
      overflowY,
      computedStyle = '',
      computedOverflow = '',
      computedOverflowY = '',
      computedOverflowX = '';
  while (el && el.style && document.body !== el) {
    overflow = el.style.overflow;
    overflowX = el.style.overflowX;
    overflowY = el.style.overflowY;
    if (overflow == 'scroll' || overflowX == 'scroll' || overflowY == 'scroll') {
      return el;
    } else if (window.getComputedStyle) {
      computedStyle = window.getComputedStyle(el);
      computedOverflow = computedStyle.getPropertyValue('overflow');
      computedOverflowY = computedStyle.getPropertyValue('overflow-y');
      computedOverflowX = computedStyle.getPropertyValue('overflow-x');
      if (computedOverflow === 'scroll' || computedOverflowX === 'scroll' || computedOverflowY === 'scroll') {
        return el;
      }
    }
    if (el.clientHeight <= el.scrollHeight && (props.indexOf(overflowY) !== -1 || props.indexOf(overflow) !== -1 || props.indexOf(computedOverflow) !== -1 || props.indexOf(computedOverflowY) !== -1)) {
      return el;
    }
    if (el.clientWidth <= el.scrollWidth && (props.indexOf(overflowX) !== -1 || props.indexOf(overflow) !== -1 || props.indexOf(computedOverflow) !== -1 || props.indexOf(computedOverflowX) !== -1)) {
      return el;
    }
    el = el.parentNode;
  }
  return window;
}
function getTrimmingContainer(base) {
  var el = base.parentNode;
  while (el && el.style && document.body !== el) {
    if (el.style.overflow !== 'visible' && el.style.overflow !== '') {
      return el;
    } else if (window.getComputedStyle) {
      var computedStyle = window.getComputedStyle(el);
      if (computedStyle.getPropertyValue('overflow') !== 'visible' && computedStyle.getPropertyValue('overflow') !== '') {
        return el;
      }
    }
    el = el.parentNode;
  }
  return window;
}
function getStyle(elem, prop) {
  if (!elem) {
    return;
  } else if (elem === window) {
    if (prop === 'width') {
      return window.innerWidth + 'px';
    } else if (prop === 'height') {
      return window.innerHeight + 'px';
    }
    return;
  }
  var styleProp = elem.style[prop],
      computedStyle;
  if (styleProp !== "" && styleProp !== void 0) {
    return styleProp;
  } else {
    computedStyle = getComputedStyle(elem);
    if (computedStyle[prop] !== "" && computedStyle[prop] !== void 0) {
      return computedStyle[prop];
    }
    return void 0;
  }
}
function getComputedStyle(elem) {
  return elem.currentStyle || document.defaultView.getComputedStyle(elem);
}
function outerWidth(elem) {
  return elem.offsetWidth;
}
function outerHeight(elem) {
  if (hasCaptionProblem() && elem.firstChild && elem.firstChild.nodeName === 'CAPTION') {
    return elem.offsetHeight + elem.firstChild.offsetHeight;
  } else {
    return elem.offsetHeight;
  }
}
function innerHeight(elem) {
  return elem.clientHeight || elem.innerHeight;
}
function innerWidth(elem) {
  return elem.clientWidth || elem.innerWidth;
}
function addEvent(element, event, callback) {
  if (window.addEventListener) {
    element.addEventListener(event, callback, false);
  } else {
    element.attachEvent('on' + event, callback);
  }
}
function removeEvent(element, event, callback) {
  if (window.removeEventListener) {
    element.removeEventListener(event, callback, false);
  } else {
    element.detachEvent('on' + event, callback);
  }
}
var _hasCaptionProblem;
function detectCaptionProblem() {
  var TABLE = document.createElement('TABLE');
  TABLE.style.borderSpacing = 0;
  TABLE.style.borderWidth = 0;
  TABLE.style.padding = 0;
  var TBODY = document.createElement('TBODY');
  TABLE.appendChild(TBODY);
  TBODY.appendChild(document.createElement('TR'));
  TBODY.firstChild.appendChild(document.createElement('TD'));
  TBODY.firstChild.firstChild.innerHTML = '<tr><td>t<br>t</td></tr>';
  var CAPTION = document.createElement('CAPTION');
  CAPTION.innerHTML = 'c<br>c<br>c<br>c';
  CAPTION.style.padding = 0;
  CAPTION.style.margin = 0;
  TABLE.insertBefore(CAPTION, TBODY);
  document.body.appendChild(TABLE);
  _hasCaptionProblem = (TABLE.offsetHeight < 2 * TABLE.lastChild.offsetHeight);
  document.body.removeChild(TABLE);
}
function hasCaptionProblem() {
  if (_hasCaptionProblem === void 0) {
    detectCaptionProblem();
  }
  return _hasCaptionProblem;
}
function getCaretPosition(el) {
  if (el.selectionStart) {
    return el.selectionStart;
  } else if (document.selection) {
    el.focus();
    var r = document.selection.createRange();
    if (r == null) {
      return 0;
    }
    var re = el.createTextRange(),
        rc = re.duplicate();
    re.moveToBookmark(r.getBookmark());
    rc.setEndPoint('EndToStart', re);
    return rc.text.length;
  }
  return 0;
}
function getSelectionEndPosition(el) {
  if (el.selectionEnd) {
    return el.selectionEnd;
  } else if (document.selection) {
    var r = document.selection.createRange();
    if (r == null) {
      return 0;
    }
    var re = el.createTextRange();
    return re.text.indexOf(r.text) + r.text.length;
  }
}
function setCaretPosition(el, pos, endPos) {
  if (endPos === void 0) {
    endPos = pos;
  }
  if (el.setSelectionRange) {
    el.focus();
    el.setSelectionRange(pos, endPos);
  } else if (el.createTextRange) {
    var range = el.createTextRange();
    range.collapse(true);
    range.moveEnd('character', endPos);
    range.moveStart('character', pos);
    range.select();
  }
}
var cachedScrollbarWidth;
function walkontableCalculateScrollbarWidth() {
  var inner = document.createElement('p');
  inner.style.width = "100%";
  inner.style.height = "200px";
  var outer = document.createElement('div');
  outer.style.position = "absolute";
  outer.style.top = "0px";
  outer.style.left = "0px";
  outer.style.visibility = "hidden";
  outer.style.width = "200px";
  outer.style.height = "150px";
  outer.style.overflow = "hidden";
  outer.appendChild(inner);
  (document.body || document.documentElement).appendChild(outer);
  var w1 = inner.offsetWidth;
  outer.style.overflow = 'scroll';
  var w2 = inner.offsetWidth;
  if (w1 == w2) {
    w2 = outer.clientWidth;
  }
  (document.body || document.documentElement).removeChild(outer);
  return (w1 - w2);
}
function getScrollbarWidth() {
  if (cachedScrollbarWidth === void 0) {
    cachedScrollbarWidth = walkontableCalculateScrollbarWidth();
  }
  return cachedScrollbarWidth;
}
var _isIE8 = !(document.createTextNode('test').textContent);
function isIE8() {
  return isIE8;
}
var _isIE9 = !!(document.documentMode);
function isIE9() {
  return _isIE9;
}
var _isSafari = (/Safari/.test(navigator.userAgent) && /Apple Computer/.test(navigator.vendor));
function isSafari() {
  return _isSafari;
}
function setOverlayPosition(overlayElem, left, top) {
  if (_isIE8 || _isIE9) {
    overlayElem.style.top = top;
    overlayElem.style.left = left;
  } else if (_isSafari) {
    overlayElem.style['-webkit-transform'] = 'translate3d(' + left + ',' + top + ',0)';
  } else {
    overlayElem.style.transform = 'translate3d(' + left + ',' + top + ',0)';
  }
}
function getCssTransform(elem) {
  var transform;
  if (elem.style['transform'] && (transform = elem.style['transform']) !== '') {
    return ['transform', transform];
  } else if (elem.style['-webkit-transform'] && (transform = elem.style['-webkit-transform']) !== '') {
    return ['-webkit-transform', transform];
  }
  return -1;
}
function resetCssTransform(elem) {
  if (elem['transform'] && elem['transform'] !== '') {
    elem['transform'] = '';
  } else if (elem['-webkit-transform'] && elem['-webkit-transform'] !== '') {
    elem['-webkit-transform'] = '';
  }
}
window.Handsontable = window.Handsontable || {};
Handsontable.Dom = {
  addClass: addClass,
  addEvent: addEvent,
  closest: closest,
  empty: empty,
  enableImmediatePropagation: enableImmediatePropagation,
  fastInnerHTML: fastInnerHTML,
  fastInnerText: fastInnerText,
  getCaretPosition: getCaretPosition,
  getComputedStyle: getComputedStyle,
  getCssTransform: getCssTransform,
  getScrollableElement: getScrollableElement,
  getScrollbarWidth: getScrollbarWidth,
  getScrollLeft: getScrollLeft,
  getScrollTop: getScrollTop,
  getStyle: getStyle,
  getSelectionEndPosition: getSelectionEndPosition,
  getTrimmingContainer: getTrimmingContainer,
  getWindowScrollLeft: getWindowScrollLeft,
  getWindowScrollTop: getWindowScrollTop,
  hasCaptionProblem: hasCaptionProblem,
  hasClass: hasClass,
  HTML_CHARACTERS: HTML_CHARACTERS,
  index: index,
  innerHeight: innerHeight,
  innerWidth: innerWidth,
  isChildOf: isChildOf,
  isChildOfWebComponentTable: isChildOfWebComponentTable,
  isIE8: isIE8,
  isIE9: isIE9,
  isSafari: isSafari,
  isVisible: isVisible,
  isWebComponentSupportedNatively: isWebComponentSupportedNatively,
  offset: offset,
  outerHeight: outerHeight,
  outerWidth: outerWidth,
  polymerUnwrap: polymerUnwrap,
  polymerWrap: polymerWrap,
  removeClass: removeClass,
  removeEvent: removeEvent,
  removeTextNodes: removeTextNodes,
  resetCssTransform: resetCssTransform,
  setCaretPosition: setCaretPosition,
  setOverlayPosition: setOverlayPosition
};


//# 
},{}],28:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  EditorManager: {get: function() {
      return EditorManager;
    }},
  __esModule: {value: true}
});
var $__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__,
    $__helpers_46_js__,
    $__dom_46_js__,
    $__editors_46_js__,
    $__eventManager_46_js__;
var WalkontableCellCoords = ($__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ = require("./3rdparty/walkontable/src/cell/coords.js"), $__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ && $__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__.__esModule && $__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ || {default: $__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__}).WalkontableCellCoords;
var helper = ($__helpers_46_js__ = require("./helpers.js"), $__helpers_46_js__ && $__helpers_46_js__.__esModule && $__helpers_46_js__ || {default: $__helpers_46_js__});
var dom = ($__dom_46_js__ = require("./dom.js"), $__dom_46_js__ && $__dom_46_js__.__esModule && $__dom_46_js__ || {default: $__dom_46_js__});
var getEditor = ($__editors_46_js__ = require("./editors.js"), $__editors_46_js__ && $__editors_46_js__.__esModule && $__editors_46_js__ || {default: $__editors_46_js__}).getEditor;
var eventManagerObject = ($__eventManager_46_js__ = require("./eventManager.js"), $__eventManager_46_js__ && $__eventManager_46_js__.__esModule && $__eventManager_46_js__ || {default: $__eventManager_46_js__}).eventManager;
;
Handsontable.EditorManager = EditorManager;
function EditorManager(instance, priv, selection) {
  var _this = this,
      keyCodes = helper.keyCode,
      destroyed = false,
      eventManager,
      activeEditor;
  eventManager = eventManagerObject(instance);
  function moveSelectionAfterEnter(shiftKey) {
    var enterMoves = typeof priv.settings.enterMoves === 'function' ? priv.settings.enterMoves(event) : priv.settings.enterMoves;
    if (shiftKey) {
      selection.transformStart(-enterMoves.row, -enterMoves.col);
    } else {
      selection.transformStart(enterMoves.row, enterMoves.col, true);
    }
  }
  function moveSelectionUp(shiftKey) {
    if (shiftKey) {
      selection.transformEnd(-1, 0);
    } else {
      selection.transformStart(-1, 0);
    }
  }
  function moveSelectionDown(shiftKey) {
    if (shiftKey) {
      selection.transformEnd(1, 0);
    } else {
      selection.transformStart(1, 0);
    }
  }
  function moveSelectionRight(shiftKey) {
    if (shiftKey) {
      selection.transformEnd(0, 1);
    } else {
      selection.transformStart(0, 1);
    }
  }
  function moveSelectionLeft(shiftKey) {
    if (shiftKey) {
      selection.transformEnd(0, -1);
    } else {
      selection.transformStart(0, -1);
    }
  }
  function onKeyDown(event) {
    var ctrlDown,
        rangeModifier;
    if (!instance.isListening()) {
      return;
    }
    Handsontable.hooks.run(instance, 'beforeKeyDown', event);
    if (destroyed) {
      return;
    }
    dom.enableImmediatePropagation(event);
    if (event.isImmediatePropagationStopped()) {
      return;
    }
    priv.lastKeyCode = event.keyCode;
    if (!selection.isSelected()) {
      return;
    }
    ctrlDown = (event.ctrlKey || event.metaKey) && !event.altKey;
    if (activeEditor && !activeEditor.isWaiting()) {
      if (!helper.isMetaKey(event.keyCode) && !ctrlDown && !_this.isEditorOpened()) {
        _this.openEditor("", event);
        return;
      }
    }
    rangeModifier = event.shiftKey ? selection.setRangeEnd : selection.setRangeStart;
    switch (event.keyCode) {
      case keyCodes.A:
        if (ctrlDown) {
          selection.selectAll();
          event.preventDefault();
          helper.stopPropagation(event);
        }
        break;
      case keyCodes.ARROW_UP:
        if (_this.isEditorOpened() && activeEditor && !activeEditor.isWaiting()) {
          _this.closeEditorAndSaveChanges(ctrlDown);
        }
        moveSelectionUp(event.shiftKey);
        event.preventDefault();
        helper.stopPropagation(event);
        break;
      case keyCodes.ARROW_DOWN:
        if (_this.isEditorOpened() && activeEditor && !activeEditor.isWaiting()) {
          _this.closeEditorAndSaveChanges(ctrlDown);
        }
        moveSelectionDown(event.shiftKey);
        event.preventDefault();
        helper.stopPropagation(event);
        break;
      case keyCodes.ARROW_RIGHT:
        if (_this.isEditorOpened() && activeEditor && !activeEditor.isWaiting()) {
          _this.closeEditorAndSaveChanges(ctrlDown);
        }
        moveSelectionRight(event.shiftKey);
        event.preventDefault();
        helper.stopPropagation(event);
        break;
      case keyCodes.ARROW_LEFT:
        if (_this.isEditorOpened() && activeEditor && !activeEditor.isWaiting()) {
          _this.closeEditorAndSaveChanges(ctrlDown);
        }
        moveSelectionLeft(event.shiftKey);
        event.preventDefault();
        helper.stopPropagation(event);
        break;
      case keyCodes.TAB:
        var tabMoves = typeof priv.settings.tabMoves === 'function' ? priv.settings.tabMoves(event) : priv.settings.tabMoves;
        if (event.shiftKey) {
          selection.transformStart(-tabMoves.row, -tabMoves.col);
        } else {
          selection.transformStart(tabMoves.row, tabMoves.col, true);
        }
        event.preventDefault();
        helper.stopPropagation(event);
        break;
      case keyCodes.BACKSPACE:
      case keyCodes.DELETE:
        selection.empty(event);
        _this.prepareEditor();
        event.preventDefault();
        break;
      case keyCodes.F2:
        _this.openEditor(null, event);
        event.preventDefault();
        break;
      case keyCodes.ENTER:
        if (_this.isEditorOpened()) {
          if (activeEditor && activeEditor.state !== Handsontable.EditorState.WAITING) {
            _this.closeEditorAndSaveChanges(ctrlDown);
          }
          moveSelectionAfterEnter(event.shiftKey);
        } else {
          if (instance.getSettings().enterBeginsEditing) {
            _this.openEditor(null, event);
          } else {
            moveSelectionAfterEnter(event.shiftKey);
          }
        }
        event.preventDefault();
        event.stopImmediatePropagation();
        break;
      case keyCodes.ESCAPE:
        if (_this.isEditorOpened()) {
          _this.closeEditorAndRestoreOriginalValue(ctrlDown);
        }
        event.preventDefault();
        break;
      case keyCodes.HOME:
        if (event.ctrlKey || event.metaKey) {
          rangeModifier(new WalkontableCellCoords(0, priv.selRange.from.col));
        } else {
          rangeModifier(new WalkontableCellCoords(priv.selRange.from.row, 0));
        }
        event.preventDefault();
        helper.stopPropagation(event);
        break;
      case keyCodes.END:
        if (event.ctrlKey || event.metaKey) {
          rangeModifier(new WalkontableCellCoords(instance.countRows() - 1, priv.selRange.from.col));
        } else {
          rangeModifier(new WalkontableCellCoords(priv.selRange.from.row, instance.countCols() - 1));
        }
        event.preventDefault();
        helper.stopPropagation(event);
        break;
      case keyCodes.PAGE_UP:
        selection.transformStart(-instance.countVisibleRows(), 0);
        event.preventDefault();
        helper.stopPropagation(event);
        break;
      case keyCodes.PAGE_DOWN:
        selection.transformStart(instance.countVisibleRows(), 0);
        event.preventDefault();
        helper.stopPropagation(event);
        break;
    }
  }
  function init() {
    instance.addHook('afterDocumentKeyDown', onKeyDown);
    eventManager.addEventListener(document.documentElement, 'keydown', function(event) {
      instance.runHooks('afterDocumentKeyDown', event);
    });
    function onDblClick(event, coords, elem) {
      if (elem.nodeName == "TD") {
        _this.openEditor();
      }
    }
    instance.view.wt.update('onCellDblClick', onDblClick);
    instance.addHook('afterDestroy', function() {
      destroyed = true;
    });
  }
  this.destroyEditor = function(revertOriginal) {
    this.closeEditor(revertOriginal);
  };
  this.getActiveEditor = function() {
    return activeEditor;
  };
  this.prepareEditor = function() {
    var row,
        col,
        prop,
        td,
        originalValue,
        cellProperties,
        editorClass;
    if (activeEditor && activeEditor.isWaiting()) {
      this.closeEditor(false, false, function(dataSaved) {
        if (dataSaved) {
          _this.prepareEditor();
        }
      });
      return;
    }
    row = priv.selRange.highlight.row;
    col = priv.selRange.highlight.col;
    prop = instance.colToProp(col);
    td = instance.getCell(row, col);
    originalValue = instance.getDataAtCell(row, col);
    cellProperties = instance.getCellMeta(row, col);
    editorClass = instance.getCellEditor(cellProperties);
    if (editorClass) {
      activeEditor = Handsontable.editors.getEditor(editorClass, instance);
      activeEditor.prepare(row, col, prop, td, originalValue, cellProperties);
    } else {
      activeEditor = void 0;
    }
  };
  this.isEditorOpened = function() {
    return activeEditor && activeEditor.isOpened();
  };
  this.openEditor = function(initialValue, event) {
    if (activeEditor && !activeEditor.cellProperties.readOnly) {
      activeEditor.beginEditing(initialValue, event);
    } else if (activeEditor && activeEditor.cellProperties.readOnly) {
      if (event && event.keyCode === helper.keyCode.ENTER) {
        moveSelectionAfterEnter();
      }
    }
  };
  this.closeEditor = function(restoreOriginalValue, ctrlDown, callback) {
    if (!activeEditor) {
      if (callback) {
        callback(false);
      }
    } else {
      activeEditor.finishEditing(restoreOriginalValue, ctrlDown, callback);
    }
  };
  this.closeEditorAndSaveChanges = function(ctrlDown) {
    return this.closeEditor(false, ctrlDown);
  };
  this.closeEditorAndRestoreOriginalValue = function(ctrlDown) {
    return this.closeEditor(true, ctrlDown);
  };
  init();
}


//# 
},{"./3rdparty/walkontable/src/cell/coords.js":5,"./dom.js":27,"./editors.js":29,"./eventManager.js":41,"./helpers.js":42}],29:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  registerEditor: {get: function() {
      return registerEditor;
    }},
  getEditor: {get: function() {
      return getEditor;
    }},
  hasEditor: {get: function() {
      return hasEditor;
    }},
  getEditorConstructor: {get: function() {
      return getEditorConstructor;
    }},
  __esModule: {value: true}
});
var $__helpers_46_js__;
var helper = ($__helpers_46_js__ = require("./helpers.js"), $__helpers_46_js__ && $__helpers_46_js__.__esModule && $__helpers_46_js__ || {default: $__helpers_46_js__});
;
var registeredEditorNames = {},
    registeredEditorClasses = new WeakMap();
Handsontable.editors = Handsontable.editors || {};
Handsontable.editors.registerEditor = registerEditor;
Handsontable.editors.getEditor = getEditor;
function RegisteredEditor(editorClass) {
  var Clazz,
      instances;
  instances = {};
  Clazz = editorClass;
  this.getConstructor = function() {
    return editorClass;
  };
  this.getInstance = function(hotInstance) {
    if (!(hotInstance.guid in instances)) {
      instances[hotInstance.guid] = new Clazz(hotInstance);
    }
    return instances[hotInstance.guid];
  };
}
function registerEditor(editorName, editorClass) {
  var editor = new RegisteredEditor(editorClass);
  if (typeof editorName === "string") {
    registeredEditorNames[editorName] = editor;
  }
  registeredEditorClasses.set(editorClass, editor);
}
function getEditor(editorName, hotInstance) {
  var editor;
  if (typeof editorName == 'function') {
    if (!(registeredEditorClasses.get(editorName))) {
      registerEditor(null, editorName);
    }
    editor = registeredEditorClasses.get(editorName);
  } else if (typeof editorName == 'string') {
    editor = registeredEditorNames[editorName];
  } else {
    throw Error('Only strings and functions can be passed as "editor" parameter ');
  }
  if (!editor) {
    throw Error('No editor registered under name "' + editorName + '"');
  }
  return editor.getInstance(hotInstance);
}
function getEditorConstructor(editorName) {
  var editor;
  if (typeof editorName == 'string') {
    editor = registeredEditorNames[editorName];
  } else {
    throw Error('Only strings and functions can be passed as "editor" parameter ');
  }
  if (!editor) {
    throw Error('No editor registered under name "' + editorName + '"');
  }
  return editor.getConstructor();
}
function hasEditor(editorName) {
  return registeredEditorNames[editorName] ? true : false;
}


//# 
},{"./helpers.js":42}],30:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  BaseEditor: {get: function() {
      return BaseEditor;
    }},
  __esModule: {value: true}
});
var $___46__46__47_helpers_46_js__,
    $___46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__;
var helper = ($___46__46__47_helpers_46_js__ = require("./../helpers.js"), $___46__46__47_helpers_46_js__ && $___46__46__47_helpers_46_js__.__esModule && $___46__46__47_helpers_46_js__ || {default: $___46__46__47_helpers_46_js__});
var WalkontableCellCoords = ($___46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ = require("./../3rdparty/walkontable/src/cell/coords.js"), $___46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ && $___46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__.__esModule && $___46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ || {default: $___46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__}).WalkontableCellCoords;
;
Handsontable.editors = Handsontable.editors || {};
Handsontable.editors.BaseEditor = BaseEditor;
Handsontable.EditorState = {
  VIRGIN: 'STATE_VIRGIN',
  EDITING: 'STATE_EDITING',
  WAITING: 'STATE_WAITING',
  FINISHED: 'STATE_FINISHED'
};
function BaseEditor(instance) {
  this.instance = instance;
  this.state = Handsontable.EditorState.VIRGIN;
  this._opened = false;
  this._closeCallback = null;
  this.init();
}
BaseEditor.prototype._fireCallbacks = function(result) {
  if (this._closeCallback) {
    this._closeCallback(result);
    this._closeCallback = null;
  }
};
BaseEditor.prototype.init = function() {};
BaseEditor.prototype.getValue = function() {
  throw Error('Editor getValue() method unimplemented');
};
BaseEditor.prototype.setValue = function(newValue) {
  throw Error('Editor setValue() method unimplemented');
};
BaseEditor.prototype.open = function() {
  throw Error('Editor open() method unimplemented');
};
BaseEditor.prototype.close = function() {
  throw Error('Editor close() method unimplemented');
};
BaseEditor.prototype.prepare = function(row, col, prop, td, originalValue, cellProperties) {
  this.TD = td;
  this.row = row;
  this.col = col;
  this.prop = prop;
  this.originalValue = originalValue;
  this.cellProperties = cellProperties;
  this.state = Handsontable.EditorState.VIRGIN;
};
BaseEditor.prototype.extend = function() {
  var baseClass = this.constructor;
  function Editor() {
    baseClass.apply(this, arguments);
  }
  function inherit(Child, Parent) {
    function Bridge() {}
    Bridge.prototype = Parent.prototype;
    Child.prototype = new Bridge();
    Child.prototype.constructor = Child;
    return Child;
  }
  return inherit(Editor, baseClass);
};
BaseEditor.prototype.saveValue = function(val, ctrlDown) {
  var sel,
      tmp;
  if (ctrlDown) {
    sel = this.instance.getSelected();
    if (sel[0] > sel[2]) {
      tmp = sel[0];
      sel[0] = sel[2];
      sel[2] = tmp;
    }
    if (sel[1] > sel[3]) {
      tmp = sel[1];
      sel[1] = sel[3];
      sel[3] = tmp;
    }
    this.instance.populateFromArray(sel[0], sel[1], val, sel[2], sel[3], 'edit');
  } else {
    this.instance.populateFromArray(this.row, this.col, val, null, null, 'edit');
  }
};
BaseEditor.prototype.beginEditing = function(initialValue, event) {
  if (this.state != Handsontable.EditorState.VIRGIN) {
    return;
  }
  this.instance.view.scrollViewport(new WalkontableCellCoords(this.row, this.col));
  this.instance.view.render();
  this.state = Handsontable.EditorState.EDITING;
  initialValue = typeof initialValue == 'string' ? initialValue : this.originalValue;
  this.setValue(helper.stringify(initialValue));
  this.open(event);
  this._opened = true;
  this.focus();
  this.instance.view.render();
};
BaseEditor.prototype.finishEditing = function(restoreOriginalValue, ctrlDown, callback) {
  var _this = this,
      val;
  if (callback) {
    var previousCloseCallback = this._closeCallback;
    this._closeCallback = function(result) {
      if (previousCloseCallback) {
        previousCloseCallback(result);
      }
      callback(result);
    };
  }
  if (this.isWaiting()) {
    return;
  }
  if (this.state == Handsontable.EditorState.VIRGIN) {
    this.instance._registerTimeout(setTimeout(function() {
      _this._fireCallbacks(true);
    }, 0));
    return;
  }
  if (this.state == Handsontable.EditorState.EDITING) {
    if (restoreOriginalValue) {
      this.cancelChanges();
      this.instance.view.render();
      return;
    }
    if (this.instance.getSettings().trimWhitespace) {
      val = [[typeof this.getValue() === 'string' ? String.prototype.trim.call(this.getValue() || '') : this.getValue()]];
    } else {
      val = [[this.getValue()]];
    }
    this.state = Handsontable.EditorState.WAITING;
    this.saveValue(val, ctrlDown);
    if (this.instance.getCellValidator(this.cellProperties)) {
      this.instance.addHookOnce('postAfterValidate', function(result) {
        _this.state = Handsontable.EditorState.FINISHED;
        _this.discardEditor(result);
      });
    } else {
      this.state = Handsontable.EditorState.FINISHED;
      this.discardEditor(true);
    }
  }
};
BaseEditor.prototype.cancelChanges = function() {
  this.state = Handsontable.EditorState.FINISHED;
  this.discardEditor();
};
BaseEditor.prototype.discardEditor = function(result) {
  if (this.state !== Handsontable.EditorState.FINISHED) {
    return;
  }
  if (result === false && this.cellProperties.allowInvalid !== true) {
    this.instance.selectCell(this.row, this.col);
    this.focus();
    this.state = Handsontable.EditorState.EDITING;
    this._fireCallbacks(false);
  } else {
    this.close();
    this._opened = false;
    this.state = Handsontable.EditorState.VIRGIN;
    this._fireCallbacks(true);
  }
};
BaseEditor.prototype.isOpened = function() {
  return this._opened;
};
BaseEditor.prototype.isWaiting = function() {
  return this.state === Handsontable.EditorState.WAITING;
};


//# 
},{"./../3rdparty/walkontable/src/cell/coords.js":5,"./../helpers.js":42}],31:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  AutocompleteEditor: {get: function() {
      return AutocompleteEditor;
    }},
  __esModule: {value: true}
});
var $___46__46__47_helpers_46_js__,
    $___46__46__47_dom_46_js__,
    $___46__46__47_editors_46_js__,
    $__handsontableEditor_46_js__;
var helper = ($___46__46__47_helpers_46_js__ = require("./../helpers.js"), $___46__46__47_helpers_46_js__ && $___46__46__47_helpers_46_js__.__esModule && $___46__46__47_helpers_46_js__ || {default: $___46__46__47_helpers_46_js__});
var dom = ($___46__46__47_dom_46_js__ = require("./../dom.js"), $___46__46__47_dom_46_js__ && $___46__46__47_dom_46_js__.__esModule && $___46__46__47_dom_46_js__ || {default: $___46__46__47_dom_46_js__});
var $__0 = ($___46__46__47_editors_46_js__ = require("./../editors.js"), $___46__46__47_editors_46_js__ && $___46__46__47_editors_46_js__.__esModule && $___46__46__47_editors_46_js__ || {default: $___46__46__47_editors_46_js__}),
    getEditorConstructor = $__0.getEditorConstructor,
    registerEditor = $__0.registerEditor;
var HandsontableEditor = ($__handsontableEditor_46_js__ = require("./handsontableEditor.js"), $__handsontableEditor_46_js__ && $__handsontableEditor_46_js__.__esModule && $__handsontableEditor_46_js__ || {default: $__handsontableEditor_46_js__}).HandsontableEditor;
var AutocompleteEditor = HandsontableEditor.prototype.extend();
;
Handsontable.editors = Handsontable.editors || {};
Handsontable.editors.AutocompleteEditor = AutocompleteEditor;
AutocompleteEditor.prototype.init = function() {
  HandsontableEditor.prototype.init.apply(this, arguments);
  this.query = null;
  this.choices = [];
};
AutocompleteEditor.prototype.createElements = function() {
  HandsontableEditor.prototype.createElements.apply(this, arguments);
  dom.addClass(this.htContainer, 'autocompleteEditor');
  dom.addClass(this.htContainer, window.navigator.platform.indexOf('Mac') !== -1 ? 'htMacScroll' : '');
};
var skipOne = false;
function onBeforeKeyDown(event) {
  skipOne = false;
  var editor = this.getActiveEditor();
  var keyCodes = helper.keyCode;
  if (helper.isPrintableChar(event.keyCode) || event.keyCode === keyCodes.BACKSPACE || event.keyCode === keyCodes.DELETE || event.keyCode === keyCodes.INSERT) {
    var timeOffset = 0;
    if (event.keyCode === keyCodes.C && (event.ctrlKey || event.metaKey)) {
      return;
    }
    if (!editor.isOpened()) {
      timeOffset += 10;
    }
    editor.instance._registerTimeout(setTimeout(function() {
      editor.queryChoices(editor.TEXTAREA.value);
      skipOne = true;
    }, timeOffset));
  }
}
AutocompleteEditor.prototype.prepare = function() {
  this.instance.addHook('beforeKeyDown', onBeforeKeyDown);
  HandsontableEditor.prototype.prepare.apply(this, arguments);
};
AutocompleteEditor.prototype.open = function() {
  HandsontableEditor.prototype.open.apply(this, arguments);
  var choicesListHot = this.htEditor.getInstance();
  var that = this;
  this.TEXTAREA.style.visibility = 'visible';
  this.focus();
  choicesListHot.updateSettings({
    'colWidths': [dom.outerWidth(this.TEXTAREA) - 2],
    width: dom.outerWidth(this.TEXTAREA) + dom.getScrollbarWidth() + 2,
    afterRenderer: function(TD, row, col, prop, value) {
      var caseSensitive = this.getCellMeta(row, col).filteringCaseSensitive === true,
          indexOfMatch,
          match,
          value = Handsontable.helper.stringify(value);
      if (value) {
        indexOfMatch = caseSensitive ? value.indexOf(this.query) : value.toLowerCase().indexOf(that.query.toLowerCase());
        if (indexOfMatch != -1) {
          match = value.substr(indexOfMatch, that.query.length);
          TD.innerHTML = value.replace(match, '<strong>' + match + '</strong>');
        }
      }
    }
  });
  this.htEditor.view.wt.wtTable.holder.parentNode.style['padding-right'] = dom.getScrollbarWidth() + 2 + 'px';
  if (skipOne) {
    skipOne = false;
  }
  that.instance._registerTimeout(setTimeout(function() {
    that.queryChoices(that.TEXTAREA.value);
  }, 0));
};
AutocompleteEditor.prototype.close = function() {
  HandsontableEditor.prototype.close.apply(this, arguments);
};
AutocompleteEditor.prototype.queryChoices = function(query) {
  this.query = query;
  if (typeof this.cellProperties.source == 'function') {
    var that = this;
    this.cellProperties.source(query, function(choices) {
      that.updateChoicesList(choices);
    });
  } else if (Array.isArray(this.cellProperties.source)) {
    var choices;
    if (!query || this.cellProperties.filter === false) {
      choices = this.cellProperties.source;
    } else {
      var filteringCaseSensitive = this.cellProperties.filteringCaseSensitive === true;
      var lowerCaseQuery = query.toLowerCase();
      choices = this.cellProperties.source.filter(function(choice) {
        if (filteringCaseSensitive) {
          return choice.indexOf(query) != -1;
        } else {
          return choice.toLowerCase().indexOf(lowerCaseQuery) != -1;
        }
      });
    }
    this.updateChoicesList(choices);
  } else {
    this.updateChoicesList([]);
  }
};
AutocompleteEditor.prototype.updateChoicesList = function(choices) {
  var pos = dom.getCaretPosition(this.TEXTAREA),
      endPos = dom.getSelectionEndPosition(this.TEXTAREA);
  var orderByRelevance = AutocompleteEditor.sortByRelevance(this.getValue(), choices, this.cellProperties.filteringCaseSensitive);
  var highlightIndex;
  if (this.cellProperties.filter != false) {
    var sorted = [];
    for (var i = 0,
        choicesCount = orderByRelevance.length; i < choicesCount; i++) {
      sorted.push(choices[orderByRelevance[i]]);
    }
    highlightIndex = 0;
    choices = sorted;
  } else {
    highlightIndex = orderByRelevance[0];
  }
  this.choices = choices;
  this.htEditor.loadData(helper.pivot([choices]));
  this.updateDropdownHeight();
  if (this.cellProperties.strict === true) {
    this.highlightBestMatchingChoice(highlightIndex);
  }
  this.instance.listen();
  this.TEXTAREA.focus();
  dom.setCaretPosition(this.TEXTAREA, pos, (pos != endPos ? endPos : void 0));
};
AutocompleteEditor.prototype.updateDropdownHeight = function() {
  this.htEditor.updateSettings({height: this.getDropdownHeight()});
  this.htEditor.view.wt.wtTable.alignOverlaysWithTrimmingContainer();
};
AutocompleteEditor.prototype.finishEditing = function(restoreOriginalValue) {
  if (!restoreOriginalValue) {
    this.instance.removeHook('beforeKeyDown', onBeforeKeyDown);
  }
  HandsontableEditor.prototype.finishEditing.apply(this, arguments);
};
AutocompleteEditor.prototype.highlightBestMatchingChoice = function(index) {
  if (typeof index === "number") {
    this.htEditor.selectCell(index, 0);
  } else {
    this.htEditor.deselectCell();
  }
};
AutocompleteEditor.sortByRelevance = function(value, choices, caseSensitive) {
  var choicesRelevance = [],
      currentItem,
      valueLength = value.length,
      valueIndex,
      charsLeft,
      result = [],
      i,
      choicesCount;
  if (valueLength === 0) {
    for (i = 0, choicesCount = choices.length; i < choicesCount; i++) {
      result.push(i);
    }
    return result;
  }
  for (i = 0, choicesCount = choices.length; i < choicesCount; i++) {
    currentItem = Handsontable.helper.stringify(choices[i]);
    if (caseSensitive) {
      valueIndex = currentItem.indexOf(value);
    } else {
      valueIndex = currentItem.toLowerCase().indexOf(value.toLowerCase());
    }
    if (valueIndex == -1) {
      continue;
    }
    charsLeft = currentItem.length - valueIndex - valueLength;
    choicesRelevance.push({
      baseIndex: i,
      index: valueIndex,
      charsLeft: charsLeft,
      value: currentItem
    });
  }
  choicesRelevance.sort(function(a, b) {
    if (b.index === -1) {
      return -1;
    }
    if (a.index === -1) {
      return 1;
    }
    if (a.index < b.index) {
      return -1;
    } else if (b.index < a.index) {
      return 1;
    } else if (a.index === b.index) {
      if (a.charsLeft < b.charsLeft) {
        return -1;
      } else if (a.charsLeft > b.charsLeft) {
        return 1;
      } else {
        return 0;
      }
    }
  });
  for (i = 0, choicesCount = choicesRelevance.length; i < choicesCount; i++) {
    result.push(choicesRelevance[i].baseIndex);
  }
  return result;
};
AutocompleteEditor.prototype.getDropdownHeight = function() {
  var firstRowHeight = this.htEditor.getInstance().getRowHeight(0) || 23;
  return this.choices.length >= 10 ? 10 * firstRowHeight : this.choices.length * firstRowHeight + 8;
};
registerEditor('autocomplete', AutocompleteEditor);


//# 
},{"./../dom.js":27,"./../editors.js":29,"./../helpers.js":42,"./handsontableEditor.js":35}],32:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  CheckboxEditor: {get: function() {
      return CheckboxEditor;
    }},
  __esModule: {value: true}
});
var $___46__46__47_editors_46_js__,
    $___95_baseEditor_46_js__;
var registerEditor = ($___46__46__47_editors_46_js__ = require("./../editors.js"), $___46__46__47_editors_46_js__ && $___46__46__47_editors_46_js__.__esModule && $___46__46__47_editors_46_js__ || {default: $___46__46__47_editors_46_js__}).registerEditor;
var BaseEditor = ($___95_baseEditor_46_js__ = require("./_baseEditor.js"), $___95_baseEditor_46_js__ && $___95_baseEditor_46_js__.__esModule && $___95_baseEditor_46_js__ || {default: $___95_baseEditor_46_js__}).BaseEditor;
var CheckboxEditor = BaseEditor.prototype.extend();
;
Handsontable.editors = Handsontable.editors || {};
Handsontable.editors.CheckboxEditor = CheckboxEditor;
CheckboxEditor.prototype.beginEditing = function() {
  var checkbox = this.TD.querySelector('input[type="checkbox"]');
  if (checkbox) {
    checkbox.click();
  }
};
CheckboxEditor.prototype.finishEditing = function() {};
CheckboxEditor.prototype.init = function() {};
CheckboxEditor.prototype.open = function() {};
CheckboxEditor.prototype.close = function() {};
CheckboxEditor.prototype.getValue = function() {};
CheckboxEditor.prototype.setValue = function() {};
CheckboxEditor.prototype.focus = function() {};
registerEditor('checkbox', CheckboxEditor);


//# 
},{"./../editors.js":29,"./_baseEditor.js":30}],33:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  DateEditor: {get: function() {
      return DateEditor;
    }},
  __esModule: {value: true}
});
var $___46__46__47_helpers_46_js__,
    $___46__46__47_dom_46_js__,
    $___46__46__47_editors_46_js__,
    $__textEditor_46_js__,
    $___46__46__47_eventManager_46_js__,
    $__moment__,
    $__pikaday__;
var helper = ($___46__46__47_helpers_46_js__ = require("./../helpers.js"), $___46__46__47_helpers_46_js__ && $___46__46__47_helpers_46_js__.__esModule && $___46__46__47_helpers_46_js__ || {default: $___46__46__47_helpers_46_js__});
var dom = ($___46__46__47_dom_46_js__ = require("./../dom.js"), $___46__46__47_dom_46_js__ && $___46__46__47_dom_46_js__.__esModule && $___46__46__47_dom_46_js__ || {default: $___46__46__47_dom_46_js__});
var $__0 = ($___46__46__47_editors_46_js__ = require("./../editors.js"), $___46__46__47_editors_46_js__ && $___46__46__47_editors_46_js__.__esModule && $___46__46__47_editors_46_js__ || {default: $___46__46__47_editors_46_js__}),
    getEditor = $__0.getEditor,
    registerEditor = $__0.registerEditor;
var TextEditor = ($__textEditor_46_js__ = require("./textEditor.js"), $__textEditor_46_js__ && $__textEditor_46_js__.__esModule && $__textEditor_46_js__ || {default: $__textEditor_46_js__}).TextEditor;
var eventManagerObject = ($___46__46__47_eventManager_46_js__ = require("./../eventManager.js"), $___46__46__47_eventManager_46_js__ && $___46__46__47_eventManager_46_js__.__esModule && $___46__46__47_eventManager_46_js__ || {default: $___46__46__47_eventManager_46_js__}).eventManager;
var moment = ($__moment__ = require("moment"), $__moment__ && $__moment__.__esModule && $__moment__ || {default: $__moment__}).default;
var Pikaday = ($__pikaday__ = require("pikaday"), $__pikaday__ && $__pikaday__.__esModule && $__pikaday__ || {default: $__pikaday__}).default;
var DateEditor = TextEditor.prototype.extend();
;
Handsontable.editors = Handsontable.editors || {};
Handsontable.editors.DateEditor = DateEditor;
DateEditor.prototype.init = function() {
  if (typeof moment !== 'function') {
    throw new Error("You need to include moment.js to your project.");
  }
  if (typeof Pikaday !== 'function') {
    throw new Error("You need to include Pikaday to your project.");
  }
  TextEditor.prototype.init.apply(this, arguments);
  this.isCellEdited = false;
  var that = this;
  this.instance.addHook('afterDestroy', function() {
    that.parentDestroyed = true;
    that.destroyElements();
  });
};
DateEditor.prototype.createElements = function() {
  var that = this;
  TextEditor.prototype.createElements.apply(this, arguments);
  this.defaultDateFormat = 'DD/MM/YYYY';
  this.datePicker = document.createElement('DIV');
  this.datePickerStyle = this.datePicker.style;
  this.datePickerStyle.position = 'absolute';
  this.datePickerStyle.top = 0;
  this.datePickerStyle.left = 0;
  this.datePickerStyle.zIndex = 9999;
  dom.addClass(this.datePicker, 'htDatepickerHolder');
  document.body.appendChild(this.datePicker);
  var htInput = this.TEXTAREA;
  var defaultOptions = {
    format: that.defaultDateFormat,
    field: htInput,
    trigger: htInput,
    container: that.datePicker,
    reposition: false,
    bound: false,
    onSelect: function(dateStr) {
      if (!isNaN(dateStr.getTime())) {
        dateStr = moment(dateStr).format(that.cellProperties.dateFormat || that.defaultDateFormat);
      }
      that.setValue(dateStr);
      that.hideDatepicker();
    },
    onClose: function() {
      if (!that.parentDestroyed) {
        that.finishEditing(false);
      }
    }
  };
  this.$datePicker = new Pikaday(defaultOptions);
  var eventManager = eventManagerObject(this);
  eventManager.addEventListener(this.datePicker, 'mousedown', function(event) {
    helper.stopPropagation(event);
  });
  this.hideDatepicker();
};
DateEditor.prototype.destroyElements = function() {
  this.$datePicker.destroy();
};
DateEditor.prototype.prepare = function() {
  this._opened = false;
  TextEditor.prototype.prepare.apply(this, arguments);
};
DateEditor.prototype.open = function(event) {
  TextEditor.prototype.open.call(this);
  this.showDatepicker(event);
};
DateEditor.prototype.close = function() {
  var that = this;
  this._opened = false;
  this.instance._registerTimeout(setTimeout(function() {
    that.instance.selection.refreshBorders();
  }, 0));
  TextEditor.prototype.close.apply(this, arguments);
};
DateEditor.prototype.finishEditing = function(isCancelled, ctrlDown) {
  if (isCancelled) {
    var value = this.originalValue;
    if (value !== void 0) {
      this.setValue(value);
    }
  }
  this.hideDatepicker();
  TextEditor.prototype.finishEditing.apply(this, arguments);
};
DateEditor.prototype.showDatepicker = function(event) {
  var offset = this.TD.getBoundingClientRect(),
      dateFormat = this.cellProperties.dateFormat || this.defaultDateFormat,
      datePickerConfig = this.$datePicker.config(),
      dateStr,
      isMouseDown = this.instance.view.isMouseDown(),
      isMeta = event ? helper.isMetaKey(event.keyCode) : false;
  this.datePickerStyle.top = (window.pageYOffset + offset.top + dom.outerHeight(this.TD)) + 'px';
  this.datePickerStyle.left = (window.pageXOffset + offset.left) + 'px';
  this.$datePicker._onInputFocus = function() {};
  datePickerConfig.format = dateFormat;
  if (this.originalValue) {
    dateStr = this.originalValue;
    if (moment(dateStr, dateFormat, true).isValid()) {
      this.$datePicker.setMoment(moment(dateStr, dateFormat), true);
    }
    if (!isMeta) {
      if (!isMouseDown) {
        this.setValue('');
      }
    }
  } else {
    if (this.cellProperties.defaultDate) {
      dateStr = this.cellProperties.defaultDate;
      datePickerConfig.defaultDate = dateStr;
      if (moment(dateStr, dateFormat, true).isValid()) {
        this.$datePicker.setMoment(moment(dateStr, dateFormat), true);
      }
      if (!isMeta) {
        if (!isMouseDown) {
          this.setValue('');
        }
      }
    } else {
      this.$datePicker.gotoToday();
    }
  }
  this.datePickerStyle.display = 'block';
  this.$datePicker.show();
};
DateEditor.prototype.hideDatepicker = function() {
  this.datePickerStyle.display = 'none';
  this.$datePicker.hide();
};
registerEditor('date', DateEditor);


//# 
},{"./../dom.js":27,"./../editors.js":29,"./../eventManager.js":41,"./../helpers.js":42,"./textEditor.js":40,"moment":undefined,"pikaday":undefined}],34:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  DropdownEditor: {get: function() {
      return DropdownEditor;
    }},
  __esModule: {value: true}
});
var $___46__46__47_editors_46_js__,
    $__autocompleteEditor_46_js__;
var $__0 = ($___46__46__47_editors_46_js__ = require("./../editors.js"), $___46__46__47_editors_46_js__ && $___46__46__47_editors_46_js__.__esModule && $___46__46__47_editors_46_js__ || {default: $___46__46__47_editors_46_js__}),
    getEditor = $__0.getEditor,
    registerEditor = $__0.registerEditor;
var AutocompleteEditor = ($__autocompleteEditor_46_js__ = require("./autocompleteEditor.js"), $__autocompleteEditor_46_js__ && $__autocompleteEditor_46_js__.__esModule && $__autocompleteEditor_46_js__ || {default: $__autocompleteEditor_46_js__}).AutocompleteEditor;
var DropdownEditor = AutocompleteEditor.prototype.extend();
;
Handsontable.editors = Handsontable.editors || {};
Handsontable.editors.DropdownEditor = DropdownEditor;
DropdownEditor.prototype.prepare = function() {
  AutocompleteEditor.prototype.prepare.apply(this, arguments);
  this.cellProperties.filter = false;
  this.cellProperties.strict = true;
};
registerEditor('dropdown', DropdownEditor);


//# 
},{"./../editors.js":29,"./autocompleteEditor.js":31}],35:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  HandsontableEditor: {get: function() {
      return HandsontableEditor;
    }},
  __esModule: {value: true}
});
var $___46__46__47_helpers_46_js__,
    $___46__46__47_dom_46_js__,
    $___46__46__47_editors_46_js__,
    $__textEditor_46_js__;
var helper = ($___46__46__47_helpers_46_js__ = require("./../helpers.js"), $___46__46__47_helpers_46_js__ && $___46__46__47_helpers_46_js__.__esModule && $___46__46__47_helpers_46_js__ || {default: $___46__46__47_helpers_46_js__});
var dom = ($___46__46__47_dom_46_js__ = require("./../dom.js"), $___46__46__47_dom_46_js__ && $___46__46__47_dom_46_js__.__esModule && $___46__46__47_dom_46_js__ || {default: $___46__46__47_dom_46_js__});
var $__0 = ($___46__46__47_editors_46_js__ = require("./../editors.js"), $___46__46__47_editors_46_js__ && $___46__46__47_editors_46_js__.__esModule && $___46__46__47_editors_46_js__ || {default: $___46__46__47_editors_46_js__}),
    getEditor = $__0.getEditor,
    registerEditor = $__0.registerEditor;
var TextEditor = ($__textEditor_46_js__ = require("./textEditor.js"), $__textEditor_46_js__ && $__textEditor_46_js__.__esModule && $__textEditor_46_js__ || {default: $__textEditor_46_js__}).TextEditor;
var HandsontableEditor = TextEditor.prototype.extend();
;
Handsontable.editors = Handsontable.editors || {};
Handsontable.editors.HandsontableEditor = HandsontableEditor;
HandsontableEditor.prototype.createElements = function() {
  TextEditor.prototype.createElements.apply(this, arguments);
  var DIV = document.createElement('DIV');
  DIV.className = 'handsontableEditor';
  this.TEXTAREA_PARENT.appendChild(DIV);
  this.htContainer = DIV;
  this.htEditor = new Handsontable(DIV);
  this.assignHooks();
};
HandsontableEditor.prototype.prepare = function(td, row, col, prop, value, cellProperties) {
  TextEditor.prototype.prepare.apply(this, arguments);
  var parent = this;
  var options = {
    startRows: 0,
    startCols: 0,
    minRows: 0,
    minCols: 0,
    className: 'listbox',
    copyPaste: false,
    cells: function() {
      return {readOnly: true};
    },
    fillHandle: false,
    afterOnCellMouseDown: function() {
      var value = this.getValue();
      if (value !== void 0) {
        parent.setValue(value);
      }
      parent.instance.destroyEditor();
    }
  };
  if (this.cellProperties.handsontable) {
    helper.extend(options, cellProperties.handsontable);
  }
  if (this.htEditor) {
    this.htEditor.destroy();
  }
  this.htEditor = new Handsontable(this.htContainer, options);
};
var onBeforeKeyDown = function(event) {
  if (event != null && event.isImmediatePropagationEnabled == null) {
    event.stopImmediatePropagation = function() {
      this.isImmediatePropagationEnabled = false;
      this.cancelBubble = true;
    };
    event.isImmediatePropagationEnabled = true;
    event.isImmediatePropagationStopped = function() {
      return !this.isImmediatePropagationEnabled;
    };
  }
  if (event.isImmediatePropagationStopped()) {
    return;
  }
  var editor = this.getActiveEditor();
  var innerHOT = editor.htEditor.getInstance();
  var rowToSelect;
  if (event.keyCode == helper.keyCode.ARROW_DOWN) {
    if (!innerHOT.getSelected()) {
      rowToSelect = 0;
    } else {
      var selectedRow = innerHOT.getSelected()[0];
      var lastRow = innerHOT.countRows() - 1;
      rowToSelect = Math.min(lastRow, selectedRow + 1);
    }
  } else if (event.keyCode == helper.keyCode.ARROW_UP) {
    if (innerHOT.getSelected()) {
      var selectedRow = innerHOT.getSelected()[0];
      rowToSelect = selectedRow - 1;
    }
  }
  if (rowToSelect !== void 0) {
    if (rowToSelect < 0) {
      innerHOT.deselectCell();
    } else {
      innerHOT.selectCell(rowToSelect, 0);
    }
    event.preventDefault();
    event.stopImmediatePropagation();
    editor.instance.listen();
    editor.TEXTAREA.focus();
  }
};
HandsontableEditor.prototype.open = function() {
  this.instance.addHook('beforeKeyDown', onBeforeKeyDown);
  TextEditor.prototype.open.apply(this, arguments);
  this.htEditor.render();
  if (this.cellProperties.strict) {
    this.htEditor.selectCell(0, 0);
    this.TEXTAREA.style.visibility = 'hidden';
  } else {
    this.htEditor.deselectCell();
    this.TEXTAREA.style.visibility = 'visible';
  }
  dom.setCaretPosition(this.TEXTAREA, 0, this.TEXTAREA.value.length);
};
HandsontableEditor.prototype.close = function() {
  this.instance.removeHook('beforeKeyDown', onBeforeKeyDown);
  this.instance.listen();
  TextEditor.prototype.close.apply(this, arguments);
};
HandsontableEditor.prototype.focus = function() {
  this.instance.listen();
  TextEditor.prototype.focus.apply(this, arguments);
};
HandsontableEditor.prototype.beginEditing = function(initialValue) {
  var onBeginEditing = this.instance.getSettings().onBeginEditing;
  if (onBeginEditing && onBeginEditing() === false) {
    return;
  }
  TextEditor.prototype.beginEditing.apply(this, arguments);
};
HandsontableEditor.prototype.finishEditing = function(isCancelled, ctrlDown) {
  if (this.htEditor.isListening()) {
    this.instance.listen();
  }
  if (this.htEditor.getSelected()) {
    var value = this.htEditor.getInstance().getValue();
    if (value !== void 0) {
      this.setValue(value);
    }
  }
  return TextEditor.prototype.finishEditing.apply(this, arguments);
};
HandsontableEditor.prototype.assignHooks = function() {
  var _this = this;
  this.instance.addHook('afterDestroy', function() {
    if (_this.htEditor) {
      _this.htEditor.destroy();
    }
  });
};
registerEditor('handsontable', HandsontableEditor);


//# 
},{"./../dom.js":27,"./../editors.js":29,"./../helpers.js":42,"./textEditor.js":40}],36:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  MobileTextEditor: {get: function() {
      return MobileTextEditor;
    }},
  __esModule: {value: true}
});
var $___46__46__47_helpers_46_js__,
    $___46__46__47_dom_46_js__,
    $___46__46__47_editors_46_js__,
    $___95_baseEditor_46_js__,
    $___46__46__47_eventManager_46_js__;
var helper = ($___46__46__47_helpers_46_js__ = require("./../helpers.js"), $___46__46__47_helpers_46_js__ && $___46__46__47_helpers_46_js__.__esModule && $___46__46__47_helpers_46_js__ || {default: $___46__46__47_helpers_46_js__});
var dom = ($___46__46__47_dom_46_js__ = require("./../dom.js"), $___46__46__47_dom_46_js__ && $___46__46__47_dom_46_js__.__esModule && $___46__46__47_dom_46_js__ || {default: $___46__46__47_dom_46_js__});
var $__0 = ($___46__46__47_editors_46_js__ = require("./../editors.js"), $___46__46__47_editors_46_js__ && $___46__46__47_editors_46_js__.__esModule && $___46__46__47_editors_46_js__ || {default: $___46__46__47_editors_46_js__}),
    getEditor = $__0.getEditor,
    registerEditor = $__0.registerEditor;
var BaseEditor = ($___95_baseEditor_46_js__ = require("./_baseEditor.js"), $___95_baseEditor_46_js__ && $___95_baseEditor_46_js__.__esModule && $___95_baseEditor_46_js__ || {default: $___95_baseEditor_46_js__}).BaseEditor;
var eventManagerObject = ($___46__46__47_eventManager_46_js__ = require("./../eventManager.js"), $___46__46__47_eventManager_46_js__ && $___46__46__47_eventManager_46_js__.__esModule && $___46__46__47_eventManager_46_js__ || {default: $___46__46__47_eventManager_46_js__}).eventManager;
var MobileTextEditor = BaseEditor.prototype.extend(),
    domDimensionsCache = {};
;
Handsontable.editors = Handsontable.editors || {};
Handsontable.editors.MobileTextEditor = MobileTextEditor;
var createControls = function() {
  this.controls = {};
  this.controls.leftButton = document.createElement('DIV');
  this.controls.leftButton.className = 'leftButton';
  this.controls.rightButton = document.createElement('DIV');
  this.controls.rightButton.className = 'rightButton';
  this.controls.upButton = document.createElement('DIV');
  this.controls.upButton.className = 'upButton';
  this.controls.downButton = document.createElement('DIV');
  this.controls.downButton.className = 'downButton';
  for (var button in this.controls) {
    if (this.controls.hasOwnProperty(button)) {
      this.positionControls.appendChild(this.controls[button]);
    }
  }
};
MobileTextEditor.prototype.valueChanged = function() {
  return this.initValue != this.getValue();
};
MobileTextEditor.prototype.init = function() {
  var that = this;
  this.eventManager = eventManagerObject(this.instance);
  this.createElements();
  this.bindEvents();
  this.instance.addHook('afterDestroy', function() {
    that.destroy();
  });
};
MobileTextEditor.prototype.getValue = function() {
  return this.TEXTAREA.value;
};
MobileTextEditor.prototype.setValue = function(newValue) {
  this.initValue = newValue;
  this.TEXTAREA.value = newValue;
};
MobileTextEditor.prototype.createElements = function() {
  this.editorContainer = document.createElement('DIV');
  this.editorContainer.className = "htMobileEditorContainer";
  this.cellPointer = document.createElement('DIV');
  this.cellPointer.className = "cellPointer";
  this.moveHandle = document.createElement('DIV');
  this.moveHandle.className = "moveHandle";
  this.inputPane = document.createElement('DIV');
  this.inputPane.className = "inputs";
  this.positionControls = document.createElement('DIV');
  this.positionControls.className = "positionControls";
  this.TEXTAREA = document.createElement('TEXTAREA');
  dom.addClass(this.TEXTAREA, 'handsontableInput');
  this.inputPane.appendChild(this.TEXTAREA);
  this.editorContainer.appendChild(this.cellPointer);
  this.editorContainer.appendChild(this.moveHandle);
  this.editorContainer.appendChild(this.inputPane);
  this.editorContainer.appendChild(this.positionControls);
  createControls.call(this);
  document.body.appendChild(this.editorContainer);
};
MobileTextEditor.prototype.onBeforeKeyDown = function(event) {
  var instance = this;
  var that = instance.getActiveEditor();
  dom.enableImmediatePropagation(event);
  if (event.target !== that.TEXTAREA || event.isImmediatePropagationStopped()) {
    return;
  }
  var keyCodes = helper.keyCode;
  switch (event.keyCode) {
    case keyCodes.ENTER:
      that.close();
      event.preventDefault();
      break;
    case keyCodes.BACKSPACE:
      event.stopImmediatePropagation();
      break;
  }
};
MobileTextEditor.prototype.open = function() {
  this.instance.addHook('beforeKeyDown', this.onBeforeKeyDown);
  dom.addClass(this.editorContainer, 'active');
  dom.removeClass(this.cellPointer, 'hidden');
  this.updateEditorPosition();
};
MobileTextEditor.prototype.focus = function() {
  this.TEXTAREA.focus();
  dom.setCaretPosition(this.TEXTAREA, this.TEXTAREA.value.length);
};
MobileTextEditor.prototype.close = function() {
  this.TEXTAREA.blur();
  this.instance.removeHook('beforeKeyDown', this.onBeforeKeyDown);
  dom.removeClass(this.editorContainer, 'active');
};
MobileTextEditor.prototype.scrollToView = function() {
  var coords = this.instance.getSelectedRange().highlight;
  this.instance.view.scrollViewport(coords);
};
MobileTextEditor.prototype.hideCellPointer = function() {
  if (!dom.hasClass(this.cellPointer, 'hidden')) {
    dom.addClass(this.cellPointer, 'hidden');
  }
};
MobileTextEditor.prototype.updateEditorPosition = function(x, y) {
  if (x && y) {
    x = parseInt(x, 10);
    y = parseInt(y, 10);
    this.editorContainer.style.top = y + "px";
    this.editorContainer.style.left = x + "px";
  } else {
    var selection = this.instance.getSelected(),
        selectedCell = this.instance.getCell(selection[0], selection[1]);
    if (!domDimensionsCache.cellPointer) {
      domDimensionsCache.cellPointer = {
        height: dom.outerHeight(this.cellPointer),
        width: dom.outerWidth(this.cellPointer)
      };
    }
    if (!domDimensionsCache.editorContainer) {
      domDimensionsCache.editorContainer = {width: dom.outerWidth(this.editorContainer)};
    }
    if (selectedCell !== undefined) {
      var scrollLeft = this.instance.view.wt.wtOverlays.leftOverlay.trimmingContainer == window ? 0 : dom.getScrollLeft(this.instance.view.wt.wtOverlays.leftOverlay.holder);
      var scrollTop = this.instance.view.wt.wtOverlays.topOverlay.trimmingContainer == window ? 0 : dom.getScrollTop(this.instance.view.wt.wtOverlays.topOverlay.holder);
      var selectedCellOffset = dom.offset(selectedCell),
          selectedCellWidth = dom.outerWidth(selectedCell),
          currentScrollPosition = {
            x: scrollLeft,
            y: scrollTop
          };
      this.editorContainer.style.top = parseInt(selectedCellOffset.top + dom.outerHeight(selectedCell) - currentScrollPosition.y + domDimensionsCache.cellPointer.height, 10) + "px";
      this.editorContainer.style.left = parseInt((window.innerWidth / 2) - (domDimensionsCache.editorContainer.width / 2), 10) + "px";
      if (selectedCellOffset.left + selectedCellWidth / 2 > parseInt(this.editorContainer.style.left, 10) + domDimensionsCache.editorContainer.width) {
        this.editorContainer.style.left = window.innerWidth - domDimensionsCache.editorContainer.width + "px";
      } else if (selectedCellOffset.left + selectedCellWidth / 2 < parseInt(this.editorContainer.style.left, 10) + 20) {
        this.editorContainer.style.left = 0 + "px";
      }
      this.cellPointer.style.left = parseInt(selectedCellOffset.left - (domDimensionsCache.cellPointer.width / 2) - dom.offset(this.editorContainer).left + (selectedCellWidth / 2) - currentScrollPosition.x, 10) + "px";
    }
  }
};
MobileTextEditor.prototype.updateEditorData = function() {
  var selected = this.instance.getSelected(),
      selectedValue = this.instance.getDataAtCell(selected[0], selected[1]);
  this.row = selected[0];
  this.col = selected[1];
  this.setValue(selectedValue);
  this.updateEditorPosition();
};
MobileTextEditor.prototype.prepareAndSave = function() {
  var val;
  if (!this.valueChanged()) {
    return true;
  }
  if (this.instance.getSettings().trimWhitespace) {
    val = [[String.prototype.trim.call(this.getValue())]];
  } else {
    val = [[this.getValue()]];
  }
  this.saveValue(val);
};
MobileTextEditor.prototype.bindEvents = function() {
  var that = this;
  this.eventManager.addEventListener(this.controls.leftButton, "touchend", function(event) {
    that.prepareAndSave();
    that.instance.selection.transformStart(0, -1, null, true);
    that.updateEditorData();
    event.preventDefault();
  });
  this.eventManager.addEventListener(this.controls.rightButton, "touchend", function(event) {
    that.prepareAndSave();
    that.instance.selection.transformStart(0, 1, null, true);
    that.updateEditorData();
    event.preventDefault();
  });
  this.eventManager.addEventListener(this.controls.upButton, "touchend", function(event) {
    that.prepareAndSave();
    that.instance.selection.transformStart(-1, 0, null, true);
    that.updateEditorData();
    event.preventDefault();
  });
  this.eventManager.addEventListener(this.controls.downButton, "touchend", function(event) {
    that.prepareAndSave();
    that.instance.selection.transformStart(1, 0, null, true);
    that.updateEditorData();
    event.preventDefault();
  });
  this.eventManager.addEventListener(this.moveHandle, "touchstart", function(event) {
    if (event.touches.length == 1) {
      var touch = event.touches[0],
          onTouchPosition = {
            x: that.editorContainer.offsetLeft,
            y: that.editorContainer.offsetTop
          },
          onTouchOffset = {
            x: touch.pageX - onTouchPosition.x,
            y: touch.pageY - onTouchPosition.y
          };
      that.eventManager.addEventListener(this, "touchmove", function(event) {
        var touch = event.touches[0];
        that.updateEditorPosition(touch.pageX - onTouchOffset.x, touch.pageY - onTouchOffset.y);
        that.hideCellPointer();
        event.preventDefault();
      });
    }
  });
  this.eventManager.addEventListener(document.body, "touchend", function(event) {
    if (!dom.isChildOf(event.target, that.editorContainer) && !dom.isChildOf(event.target, that.instance.rootElement)) {
      that.close();
    }
  });
  this.eventManager.addEventListener(this.instance.view.wt.wtOverlays.leftOverlay.holder, "scroll", function(event) {
    if (that.instance.view.wt.wtOverlays.leftOverlay.trimmingContainer != window) {
      that.hideCellPointer();
    }
  });
  this.eventManager.addEventListener(this.instance.view.wt.wtOverlays.topOverlay.holder, "scroll", function(event) {
    if (that.instance.view.wt.wtOverlays.topOverlay.trimmingContainer != window) {
      that.hideCellPointer();
    }
  });
};
MobileTextEditor.prototype.destroy = function() {
  this.eventManager.clear();
  this.editorContainer.parentNode.removeChild(this.editorContainer);
};
registerEditor('mobile', MobileTextEditor);


//# 
},{"./../dom.js":27,"./../editors.js":29,"./../eventManager.js":41,"./../helpers.js":42,"./_baseEditor.js":30}],37:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  NumericEditor: {get: function() {
      return NumericEditor;
    }},
  __esModule: {value: true}
});
var $__numeral__,
    $___46__46__47_editors_46_js__,
    $__textEditor_46_js__;
var numeral = ($__numeral__ = require("numeral"), $__numeral__ && $__numeral__.__esModule && $__numeral__ || {default: $__numeral__}).default;
var $__1 = ($___46__46__47_editors_46_js__ = require("./../editors.js"), $___46__46__47_editors_46_js__ && $___46__46__47_editors_46_js__.__esModule && $___46__46__47_editors_46_js__ || {default: $___46__46__47_editors_46_js__}),
    getEditor = $__1.getEditor,
    registerEditor = $__1.registerEditor;
var TextEditor = ($__textEditor_46_js__ = require("./textEditor.js"), $__textEditor_46_js__ && $__textEditor_46_js__.__esModule && $__textEditor_46_js__ || {default: $__textEditor_46_js__}).TextEditor;
var NumericEditor = TextEditor.prototype.extend();
;
Handsontable.editors = Handsontable.editors || {};
Handsontable.editors.NumericEditor = NumericEditor;
NumericEditor.prototype.beginEditing = function(initialValue) {
  var BaseEditor = TextEditor.prototype;
  if (typeof(initialValue) === 'undefined' && this.originalValue) {
    var value = '' + this.originalValue;
    if (typeof this.cellProperties.language !== 'undefined') {
      numeral.language(this.cellProperties.language);
    }
    var decimalDelimiter = numeral.languageData().delimiters.decimal;
    value = value.replace('.', decimalDelimiter);
    BaseEditor.beginEditing.apply(this, [value]);
  } else {
    BaseEditor.beginEditing.apply(this, arguments);
  }
};
registerEditor('numeric', NumericEditor);


//# 
},{"./../editors.js":29,"./textEditor.js":40,"numeral":"numeral"}],38:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  PasswordEditor: {get: function() {
      return PasswordEditor;
    }},
  __esModule: {value: true}
});
var $___46__46__47_dom_46_js__,
    $___46__46__47_editors_46_js__,
    $__textEditor_46_js__;
var dom = ($___46__46__47_dom_46_js__ = require("./../dom.js"), $___46__46__47_dom_46_js__ && $___46__46__47_dom_46_js__.__esModule && $___46__46__47_dom_46_js__ || {default: $___46__46__47_dom_46_js__});
var $__0 = ($___46__46__47_editors_46_js__ = require("./../editors.js"), $___46__46__47_editors_46_js__ && $___46__46__47_editors_46_js__.__esModule && $___46__46__47_editors_46_js__ || {default: $___46__46__47_editors_46_js__}),
    getEditor = $__0.getEditor,
    registerEditor = $__0.registerEditor;
var TextEditor = ($__textEditor_46_js__ = require("./textEditor.js"), $__textEditor_46_js__ && $__textEditor_46_js__.__esModule && $__textEditor_46_js__ || {default: $__textEditor_46_js__}).TextEditor;
var PasswordEditor = TextEditor.prototype.extend();
;
Handsontable.editors = Handsontable.editors || {};
Handsontable.editors.PasswordEditor = PasswordEditor;
PasswordEditor.prototype.createElements = function() {
  TextEditor.prototype.createElements.apply(this, arguments);
  this.TEXTAREA = document.createElement('input');
  this.TEXTAREA.setAttribute('type', 'password');
  this.TEXTAREA.className = 'handsontableInput';
  this.textareaStyle = this.TEXTAREA.style;
  this.textareaStyle.width = 0;
  this.textareaStyle.height = 0;
  dom.empty(this.TEXTAREA_PARENT);
  this.TEXTAREA_PARENT.appendChild(this.TEXTAREA);
};
registerEditor('password', PasswordEditor);


//# 
},{"./../dom.js":27,"./../editors.js":29,"./textEditor.js":40}],39:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  SelectEditor: {get: function() {
      return SelectEditor;
    }},
  __esModule: {value: true}
});
var $___46__46__47_dom_46_js__,
    $___46__46__47_helpers_46_js__,
    $___46__46__47_editors_46_js__,
    $___95_baseEditor_46_js__;
var dom = ($___46__46__47_dom_46_js__ = require("./../dom.js"), $___46__46__47_dom_46_js__ && $___46__46__47_dom_46_js__.__esModule && $___46__46__47_dom_46_js__ || {default: $___46__46__47_dom_46_js__});
var helper = ($___46__46__47_helpers_46_js__ = require("./../helpers.js"), $___46__46__47_helpers_46_js__ && $___46__46__47_helpers_46_js__.__esModule && $___46__46__47_helpers_46_js__ || {default: $___46__46__47_helpers_46_js__});
var $__0 = ($___46__46__47_editors_46_js__ = require("./../editors.js"), $___46__46__47_editors_46_js__ && $___46__46__47_editors_46_js__.__esModule && $___46__46__47_editors_46_js__ || {default: $___46__46__47_editors_46_js__}),
    getEditor = $__0.getEditor,
    registerEditor = $__0.registerEditor;
var BaseEditor = ($___95_baseEditor_46_js__ = require("./_baseEditor.js"), $___95_baseEditor_46_js__ && $___95_baseEditor_46_js__.__esModule && $___95_baseEditor_46_js__ || {default: $___95_baseEditor_46_js__}).BaseEditor;
var SelectEditor = BaseEditor.prototype.extend();
;
Handsontable.editors = Handsontable.editors || {};
Handsontable.editors.SelectEditor = SelectEditor;
SelectEditor.prototype.init = function() {
  this.select = document.createElement('SELECT');
  dom.addClass(this.select, 'htSelectEditor');
  this.select.style.display = 'none';
  this.instance.rootElement.appendChild(this.select);
};
SelectEditor.prototype.prepare = function() {
  BaseEditor.prototype.prepare.apply(this, arguments);
  var selectOptions = this.cellProperties.selectOptions;
  var options;
  if (typeof selectOptions == 'function') {
    options = this.prepareOptions(selectOptions(this.row, this.col, this.prop));
  } else {
    options = this.prepareOptions(selectOptions);
  }
  dom.empty(this.select);
  for (var option in options) {
    if (options.hasOwnProperty(option)) {
      var optionElement = document.createElement('OPTION');
      optionElement.value = option;
      dom.fastInnerHTML(optionElement, options[option]);
      this.select.appendChild(optionElement);
    }
  }
};
SelectEditor.prototype.prepareOptions = function(optionsToPrepare) {
  var preparedOptions = {};
  if (Array.isArray(optionsToPrepare)) {
    for (var i = 0,
        len = optionsToPrepare.length; i < len; i++) {
      preparedOptions[optionsToPrepare[i]] = optionsToPrepare[i];
    }
  } else if (typeof optionsToPrepare == 'object') {
    preparedOptions = optionsToPrepare;
  }
  return preparedOptions;
};
SelectEditor.prototype.getValue = function() {
  return this.select.value;
};
SelectEditor.prototype.setValue = function(value) {
  this.select.value = value;
};
var onBeforeKeyDown = function(event) {
  var instance = this;
  var editor = instance.getActiveEditor();
  if (event != null && event.isImmediatePropagationEnabled == null) {
    event.stopImmediatePropagation = function() {
      this.isImmediatePropagationEnabled = false;
    };
    event.isImmediatePropagationEnabled = true;
    event.isImmediatePropagationStopped = function() {
      return !this.isImmediatePropagationEnabled;
    };
  }
  switch (event.keyCode) {
    case helper.keyCode.ARROW_UP:
      var previousOptionIndex = editor.select.selectedIndex - 1;
      if (previousOptionIndex >= 0) {
        editor.select[previousOptionIndex].selected = true;
      }
      event.stopImmediatePropagation();
      event.preventDefault();
      break;
    case helper.keyCode.ARROW_DOWN:
      var nextOptionIndex = editor.select.selectedIndex + 1;
      if (nextOptionIndex <= editor.select.length - 1) {
        editor.select[nextOptionIndex].selected = true;
      }
      event.stopImmediatePropagation();
      event.preventDefault();
      break;
  }
};
SelectEditor.prototype.checkEditorSection = function() {
  if (this.row < this.instance.getSettings().fixedRowsTop) {
    if (this.col < this.instance.getSettings().fixedColumnsLeft) {
      return 'corner';
    } else {
      return 'top';
    }
  } else {
    if (this.col < this.instance.getSettings().fixedColumnsLeft) {
      return 'left';
    }
  }
};
SelectEditor.prototype.open = function() {
  var width = dom.outerWidth(this.TD);
  var height = dom.outerHeight(this.TD);
  var rootOffset = dom.offset(this.instance.rootElement);
  var tdOffset = dom.offset(this.TD);
  var editorSection = this.checkEditorSection();
  var cssTransformOffset;
  switch (editorSection) {
    case 'top':
      cssTransformOffset = dom.getCssTransform(this.instance.view.wt.wtOverlays.topOverlay.clone.wtTable.holder.parentNode);
      break;
    case 'left':
      cssTransformOffset = dom.getCssTransform(this.instance.view.wt.wtOverlays.leftOverlay.clone.wtTable.holder.parentNode);
      break;
    case 'corner':
      cssTransformOffset = dom.getCssTransform(this.instance.view.wt.wtOverlays.topLeftCornerOverlay.clone.wtTable.holder.parentNode);
      break;
  }
  var selectStyle = this.select.style;
  if (cssTransformOffset && cssTransformOffset != -1) {
    selectStyle[cssTransformOffset[0]] = cssTransformOffset[1];
  } else {
    dom.resetCssTransform(this.select);
  }
  selectStyle.height = height + 'px';
  selectStyle.minWidth = width + 'px';
  selectStyle.top = tdOffset.top - rootOffset.top + 'px';
  selectStyle.left = tdOffset.left - rootOffset.left + 'px';
  selectStyle.margin = '0px';
  selectStyle.display = '';
  this.instance.addHook('beforeKeyDown', onBeforeKeyDown);
};
SelectEditor.prototype.close = function() {
  this.select.style.display = 'none';
  this.instance.removeHook('beforeKeyDown', onBeforeKeyDown);
};
SelectEditor.prototype.focus = function() {
  this.select.focus();
};
registerEditor('select', SelectEditor);


//# 
},{"./../dom.js":27,"./../editors.js":29,"./../helpers.js":42,"./_baseEditor.js":30}],40:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  TextEditor: {get: function() {
      return TextEditor;
    }},
  __esModule: {value: true}
});
var $___46__46__47_dom_46_js__,
    $___46__46__47_helpers_46_js__,
    $__autoResize__,
    $___95_baseEditor_46_js__,
    $___46__46__47_eventManager_46_js__,
    $___46__46__47_editors_46_js__;
var dom = ($___46__46__47_dom_46_js__ = require("./../dom.js"), $___46__46__47_dom_46_js__ && $___46__46__47_dom_46_js__.__esModule && $___46__46__47_dom_46_js__ || {default: $___46__46__47_dom_46_js__});
var helper = ($___46__46__47_helpers_46_js__ = require("./../helpers.js"), $___46__46__47_helpers_46_js__ && $___46__46__47_helpers_46_js__.__esModule && $___46__46__47_helpers_46_js__ || {default: $___46__46__47_helpers_46_js__});
var autoResize = ($__autoResize__ = require("autoResize"), $__autoResize__ && $__autoResize__.__esModule && $__autoResize__ || {default: $__autoResize__}).default;
var BaseEditor = ($___95_baseEditor_46_js__ = require("./_baseEditor.js"), $___95_baseEditor_46_js__ && $___95_baseEditor_46_js__.__esModule && $___95_baseEditor_46_js__ || {default: $___95_baseEditor_46_js__}).BaseEditor;
var eventManagerObject = ($___46__46__47_eventManager_46_js__ = require("./../eventManager.js"), $___46__46__47_eventManager_46_js__ && $___46__46__47_eventManager_46_js__.__esModule && $___46__46__47_eventManager_46_js__ || {default: $___46__46__47_eventManager_46_js__}).eventManager;
var $__3 = ($___46__46__47_editors_46_js__ = require("./../editors.js"), $___46__46__47_editors_46_js__ && $___46__46__47_editors_46_js__.__esModule && $___46__46__47_editors_46_js__ || {default: $___46__46__47_editors_46_js__}),
    getEditor = $__3.getEditor,
    registerEditor = $__3.registerEditor;
var TextEditor = BaseEditor.prototype.extend();
;
Handsontable.editors = Handsontable.editors || {};
Handsontable.editors.TextEditor = TextEditor;
TextEditor.prototype.init = function() {
  var that = this;
  this.createElements();
  this.eventManager = eventManagerObject(this);
  this.bindEvents();
  this.autoResize = autoResize();
  this.instance.addHook('afterDestroy', function() {
    that.destroy();
  });
};
TextEditor.prototype.getValue = function() {
  return this.TEXTAREA.value;
};
TextEditor.prototype.setValue = function(newValue) {
  this.TEXTAREA.value = newValue;
};
var onBeforeKeyDown = function onBeforeKeyDown(event) {
  var instance = this,
      that = instance.getActiveEditor(),
      keyCodes,
      ctrlDown;
  keyCodes = helper.keyCode;
  ctrlDown = (event.ctrlKey || event.metaKey) && !event.altKey;
  dom.enableImmediatePropagation(event);
  if (event.target !== that.TEXTAREA || event.isImmediatePropagationStopped()) {
    return;
  }
  if (event.keyCode === 17 || event.keyCode === 224 || event.keyCode === 91 || event.keyCode === 93) {
    event.stopImmediatePropagation();
    return;
  }
  switch (event.keyCode) {
    case keyCodes.ARROW_RIGHT:
      if (dom.getCaretPosition(that.TEXTAREA) !== that.TEXTAREA.value.length) {
        event.stopImmediatePropagation();
      }
      break;
    case keyCodes.ARROW_LEFT:
      if (dom.getCaretPosition(that.TEXTAREA) !== 0) {
        event.stopImmediatePropagation();
      }
      break;
    case keyCodes.ENTER:
      var selected = that.instance.getSelected();
      var isMultipleSelection = !(selected[0] === selected[2] && selected[1] === selected[3]);
      if ((ctrlDown && !isMultipleSelection) || event.altKey) {
        if (that.isOpened()) {
          var caretPosition = dom.getCaretPosition(that.TEXTAREA),
              value = that.getValue();
          var newValue = value.slice(0, caretPosition) + '\n' + value.slice(caretPosition);
          that.setValue(newValue);
          dom.setCaretPosition(that.TEXTAREA, caretPosition + 1);
        } else {
          that.beginEditing(that.originalValue + '\n');
        }
        event.stopImmediatePropagation();
      }
      event.preventDefault();
      break;
    case keyCodes.A:
    case keyCodes.X:
    case keyCodes.C:
    case keyCodes.V:
      if (ctrlDown) {
        event.stopImmediatePropagation();
      }
      break;
    case keyCodes.BACKSPACE:
    case keyCodes.DELETE:
    case keyCodes.HOME:
    case keyCodes.END:
      event.stopImmediatePropagation();
      break;
  }
  that.autoResize.resize(String.fromCharCode(event.keyCode));
};
TextEditor.prototype.open = function() {
  this.refreshDimensions();
  this.instance.addHook('beforeKeyDown', onBeforeKeyDown);
};
TextEditor.prototype.close = function() {
  this.textareaParentStyle.display = 'none';
  this.autoResize.unObserve();
  if (document.activeElement === this.TEXTAREA) {
    this.instance.listen();
  }
  this.instance.removeHook('beforeKeyDown', onBeforeKeyDown);
};
TextEditor.prototype.focus = function() {
  this.TEXTAREA.focus();
  dom.setCaretPosition(this.TEXTAREA, this.TEXTAREA.value.length);
};
TextEditor.prototype.createElements = function() {
  this.TEXTAREA = document.createElement('TEXTAREA');
  dom.addClass(this.TEXTAREA, 'handsontableInput');
  this.textareaStyle = this.TEXTAREA.style;
  this.textareaStyle.width = 0;
  this.textareaStyle.height = 0;
  this.TEXTAREA_PARENT = document.createElement('DIV');
  dom.addClass(this.TEXTAREA_PARENT, 'handsontableInputHolder');
  this.textareaParentStyle = this.TEXTAREA_PARENT.style;
  this.textareaParentStyle.top = 0;
  this.textareaParentStyle.left = 0;
  this.textareaParentStyle.display = 'none';
  this.TEXTAREA_PARENT.appendChild(this.TEXTAREA);
  this.instance.rootElement.appendChild(this.TEXTAREA_PARENT);
  var that = this;
  this.instance._registerTimeout(setTimeout(function() {
    that.refreshDimensions();
  }, 0));
};
TextEditor.prototype.checkEditorSection = function() {
  if (this.row < this.instance.getSettings().fixedRowsTop) {
    if (this.col < this.instance.getSettings().fixedColumnsLeft) {
      return 'corner';
    } else {
      return 'top';
    }
  } else {
    if (this.col < this.instance.getSettings().fixedColumnsLeft) {
      return 'left';
    }
  }
};
TextEditor.prototype.getEditedCell = function() {
  var editorSection = this.checkEditorSection(),
      editedCell;
  switch (editorSection) {
    case 'top':
      editedCell = this.instance.view.wt.wtOverlays.topOverlay.clone.wtTable.getCell({
        row: this.row,
        col: this.col
      });
      this.textareaParentStyle.zIndex = 101;
      break;
    case 'corner':
      editedCell = this.instance.view.wt.wtOverlays.topLeftCornerOverlay.clone.wtTable.getCell({
        row: this.row,
        col: this.col
      });
      this.textareaParentStyle.zIndex = 103;
      break;
    case 'left':
      editedCell = this.instance.view.wt.wtOverlays.leftOverlay.clone.wtTable.getCell({
        row: this.row,
        col: this.col
      });
      this.textareaParentStyle.zIndex = 102;
      break;
    default:
      editedCell = this.instance.getCell(this.row, this.col);
      this.textareaParentStyle.zIndex = "";
      break;
  }
  return editedCell != -1 && editedCell != -2 ? editedCell : void 0;
};
TextEditor.prototype.refreshDimensions = function() {
  if (this.state !== Handsontable.EditorState.EDITING) {
    return;
  }
  this.TD = this.getEditedCell();
  if (!this.TD) {
    return;
  }
  var currentOffset = dom.offset(this.TD),
      containerOffset = dom.offset(this.instance.rootElement),
      scrollableContainer = dom.getScrollableElement(this.TD),
      editTop = currentOffset.top - containerOffset.top - 1 - (scrollableContainer.scrollTop || 0),
      editLeft = currentOffset.left - containerOffset.left - 1 - (scrollableContainer.scrollLeft || 0),
      settings = this.instance.getSettings(),
      rowHeadersCount = settings.rowHeaders ? 1 : 0,
      colHeadersCount = settings.colHeaders ? 1 : 0,
      editorSection = this.checkEditorSection(),
      backgroundColor = this.TD.style.backgroundColor,
      cssTransformOffset;
  switch (editorSection) {
    case 'top':
      cssTransformOffset = dom.getCssTransform(this.instance.view.wt.wtOverlays.topOverlay.clone.wtTable.holder.parentNode);
      break;
    case 'left':
      cssTransformOffset = dom.getCssTransform(this.instance.view.wt.wtOverlays.leftOverlay.clone.wtTable.holder.parentNode);
      break;
    case 'corner':
      cssTransformOffset = dom.getCssTransform(this.instance.view.wt.wtOverlays.topLeftCornerOverlay.clone.wtTable.holder.parentNode);
      break;
  }
  if (editTop < 0) {
    editTop = 0;
  }
  if (editLeft < 0) {
    editLeft = 0;
  }
  if (colHeadersCount && this.instance.getSelected()[0] === 0) {
    editTop += 1;
  }
  if (rowHeadersCount && this.instance.getSelected()[1] === 0) {
    editLeft += 1;
  }
  if (cssTransformOffset && cssTransformOffset != -1) {
    this.textareaParentStyle[cssTransformOffset[0]] = cssTransformOffset[1];
  } else {
    dom.resetCssTransform(this.textareaParentStyle);
  }
  this.textareaParentStyle.top = editTop + 'px';
  this.textareaParentStyle.left = editLeft + 'px';
  var cellTopOffset = this.TD.offsetTop - this.instance.view.wt.wtOverlays.topOverlay.getScrollPosition(),
      cellLeftOffset = this.TD.offsetLeft - this.instance.view.wt.wtOverlays.leftOverlay.getScrollPosition();
  var width = dom.innerWidth(this.TD) - 8,
      maxWidth = this.instance.view.maximumVisibleElementWidth(cellLeftOffset) - 10,
      height = this.TD.scrollHeight + 1,
      maxHeight = this.instance.view.maximumVisibleElementHeight(cellTopOffset) - 2;
  if (parseInt(this.TD.style.borderTopWidth, 10) > 0) {
    height -= 1;
  }
  if (parseInt(this.TD.style.borderLeftWidth, 10) > 0) {
    if (rowHeadersCount > 0) {
      width -= 1;
    }
  }
  this.TEXTAREA.style.fontSize = dom.getComputedStyle(this.TD).fontSize;
  this.TEXTAREA.style.fontFamily = dom.getComputedStyle(this.TD).fontFamily;
  this.TEXTAREA.style.backgroundColor = '';
  this.TEXTAREA.style.backgroundColor = backgroundColor ? backgroundColor : dom.getComputedStyle(this.TEXTAREA).backgroundColor;
  this.autoResize.init(this.TEXTAREA, {
    minHeight: Math.min(height, maxHeight),
    maxHeight: maxHeight,
    minWidth: Math.min(width, maxWidth),
    maxWidth: maxWidth
  }, true);
  this.textareaParentStyle.display = 'block';
};
TextEditor.prototype.bindEvents = function() {
  var editor = this;
  this.eventManager.addEventListener(this.TEXTAREA, 'cut', function(event) {
    helper.stopPropagation(event);
  });
  this.eventManager.addEventListener(this.TEXTAREA, 'paste', function(event) {
    helper.stopPropagation(event);
  });
  this.instance.addHook('afterScrollVertically', function() {
    editor.refreshDimensions();
  });
  this.instance.addHook('afterColumnResize', function() {
    editor.refreshDimensions();
    editor.focus();
  });
  this.instance.addHook('afterRowResize', function() {
    editor.refreshDimensions();
    editor.focus();
  });
  this.instance.addHook('afterDestroy', function() {
    editor.eventManager.clear();
  });
};
TextEditor.prototype.destroy = function() {
  this.eventManager.clear();
};
registerEditor('text', TextEditor);


//# 
},{"./../dom.js":27,"./../editors.js":29,"./../eventManager.js":41,"./../helpers.js":42,"./_baseEditor.js":30,"autoResize":undefined}],41:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  EventManager: {get: function() {
      return EventManager;
    }},
  eventManager: {get: function() {
      return eventManager;
    }},
  __esModule: {value: true}
});
var $__dom_46_js__;
var dom = ($__dom_46_js__ = require("./dom.js"), $__dom_46_js__ && $__dom_46_js__.__esModule && $__dom_46_js__ || {default: $__dom_46_js__});
var EventManager = function EventManager() {
  var context = arguments[0] !== (void 0) ? arguments[0] : null;
  this.context = context || this;
  if (!this.context.eventListeners) {
    this.context.eventListeners = [];
  }
};
($traceurRuntime.createClass)(EventManager, {
  addEventListener: function(element, eventName, callback) {
    var $__0 = this;
    var context = this.context;
    function callbackProxy(event) {
      if (event.target == void 0 && event.srcElement != void 0) {
        if (event.definePoperty) {
          event.definePoperty('target', {value: event.srcElement});
        } else {
          event.target = event.srcElement;
        }
      }
      if (event.preventDefault == void 0) {
        if (event.definePoperty) {
          event.definePoperty('preventDefault', {value: function() {
              this.returnValue = false;
            }});
        } else {
          event.preventDefault = function() {
            this.returnValue = false;
          };
        }
      }
      event = extendEvent(context, event);
      callback.call(this, event);
    }
    this.context.eventListeners.push({
      element: element,
      event: eventName,
      callback: callback,
      callbackProxy: callbackProxy
    });
    if (window.addEventListener) {
      element.addEventListener(eventName, callbackProxy, false);
    } else {
      element.attachEvent('on' + eventName, callbackProxy);
    }
    Handsontable.countEventManagerListeners++;
    return (function() {
      $__0.removeEventListener(element, eventName, callback);
    });
  },
  removeEventListener: function(element, eventName, callback) {
    var len = this.context.eventListeners.length;
    var tmpEvent;
    while (len--) {
      tmpEvent = this.context.eventListeners[len];
      if (tmpEvent.event == eventName && tmpEvent.element == element) {
        if (callback && callback != tmpEvent.callback) {
          continue;
        }
        this.context.eventListeners.splice(len, 1);
        if (tmpEvent.element.removeEventListener) {
          tmpEvent.element.removeEventListener(tmpEvent.event, tmpEvent.callbackProxy, false);
        } else {
          tmpEvent.element.detachEvent('on' + tmpEvent.event, tmpEvent.callbackProxy);
        }
        Handsontable.countEventManagerListeners--;
      }
    }
  },
  clearEvents: function() {
    var len = this.context.eventListeners.length;
    while (len--) {
      var event = this.context.eventListeners[len];
      if (event) {
        this.removeEventListener(event.element, event.event, event.callback);
      }
    }
  },
  clear: function() {
    this.clearEvents();
  },
  fireEvent: function(element, eventName) {
    var options = {
      bubbles: true,
      cancelable: (eventName !== 'mousemove'),
      view: window,
      detail: 0,
      screenX: 0,
      screenY: 0,
      clientX: 1,
      clientY: 1,
      ctrlKey: false,
      altKey: false,
      shiftKey: false,
      metaKey: false,
      button: 0,
      relatedTarget: undefined
    };
    var event;
    if (document.createEvent) {
      event = document.createEvent('MouseEvents');
      event.initMouseEvent(eventName, options.bubbles, options.cancelable, options.view, options.detail, options.screenX, options.screenY, options.clientX, options.clientY, options.ctrlKey, options.altKey, options.shiftKey, options.metaKey, options.button, options.relatedTarget || document.body.parentNode);
    } else {
      event = document.createEventObject();
    }
    if (element.dispatchEvent) {
      element.dispatchEvent(event);
    } else {
      element.fireEvent('on' + eventName, event);
    }
  }
}, {});
function extendEvent(context, event) {
  var componentName = 'HOT-TABLE';
  var isHotTableSpotted;
  var fromElement;
  var realTarget;
  var target;
  var len;
  event.isTargetWebComponent = false;
  event.realTarget = event.target;
  if (!Handsontable.eventManager.isHotTableEnv) {
    return event;
  }
  event = dom.polymerWrap(event);
  len = event.path ? event.path.length : 0;
  while (len--) {
    if (event.path[len].nodeName === componentName) {
      isHotTableSpotted = true;
    } else if (isHotTableSpotted && event.path[len].shadowRoot) {
      target = event.path[len];
      break;
    }
    if (len === 0 && !target) {
      target = event.path[len];
    }
  }
  if (!target) {
    target = event.target;
  }
  event.isTargetWebComponent = true;
  if (dom.isWebComponentSupportedNatively()) {
    event.realTarget = event.srcElement || event.toElement;
  } else if (context instanceof Handsontable.Core || context instanceof Walkontable) {
    if (context instanceof Handsontable.Core) {
      fromElement = context.view.wt.wtTable.TABLE;
    } else if (context instanceof Walkontable) {
      fromElement = context.wtTable.TABLE.parentNode.parentNode;
    }
    realTarget = dom.closest(event.target, [componentName], fromElement);
    if (realTarget) {
      event.realTarget = fromElement.querySelector(componentName) || event.target;
    } else {
      event.realTarget = event.target;
    }
  }
  Object.defineProperty(event, 'target', {
    get: function() {
      return dom.polymerWrap(target);
    },
    enumerable: true,
    configurable: true
  });
  return event;
}
;
window.Handsontable = window.Handsontable || {};
Handsontable.countEventManagerListeners = 0;
Handsontable.eventManager = eventManager;
function eventManager(context) {
  return new EventManager(context);
}


//# 
},{"./dom.js":27}],42:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  isPrintableChar: {get: function() {
      return isPrintableChar;
    }},
  isMetaKey: {get: function() {
      return isMetaKey;
    }},
  isCtrlKey: {get: function() {
      return isCtrlKey;
    }},
  stringify: {get: function() {
      return stringify;
    }},
  toUpperCaseFirst: {get: function() {
      return toUpperCaseFirst;
    }},
  duckSchema: {get: function() {
      return duckSchema;
    }},
  spreadsheetColumnLabel: {get: function() {
      return spreadsheetColumnLabel;
    }},
  createSpreadsheetData: {get: function() {
      return createSpreadsheetData;
    }},
  createSpreadsheetObjectData: {get: function() {
      return createSpreadsheetObjectData;
    }},
  isNumeric: {get: function() {
      return isNumeric;
    }},
  randomString: {get: function() {
      return randomString;
    }},
  inherit: {get: function() {
      return inherit;
    }},
  extend: {get: function() {
      return extend;
    }},
  deepExtend: {get: function() {
      return deepExtend;
    }},
  deepClone: {get: function() {
      return deepClone;
    }},
  isObjectEquals: {get: function() {
      return isObjectEquals;
    }},
  getPrototypeOf: {get: function() {
      return getPrototypeOf;
    }},
  columnFactory: {get: function() {
      return columnFactory;
    }},
  translateRowsToColumns: {get: function() {
      return translateRowsToColumns;
    }},
  to2dArray: {get: function() {
      return to2dArray;
    }},
  extendArray: {get: function() {
      return extendArray;
    }},
  isInput: {get: function() {
      return isInput;
    }},
  isOutsideInput: {get: function() {
      return isOutsideInput;
    }},
  keyCode: {get: function() {
      return keyCode;
    }},
  isObject: {get: function() {
      return isObject;
    }},
  pivot: {get: function() {
      return pivot;
    }},
  proxy: {get: function() {
      return proxy;
    }},
  cellMethodLookupFactory: {get: function() {
      return cellMethodLookupFactory;
    }},
  isMobileBrowser: {get: function() {
      return isMobileBrowser;
    }},
  isTouchSupported: {get: function() {
      return isTouchSupported;
    }},
  stopPropagation: {get: function() {
      return stopPropagation;
    }},
  pageX: {get: function() {
      return pageX;
    }},
  pageY: {get: function() {
      return pageY;
    }},
  defineGetter: {get: function() {
      return defineGetter;
    }},
  requestAnimationFrame: {get: function() {
      return requestAnimationFrame;
    }},
  cancelAnimationFrame: {get: function() {
      return cancelAnimationFrame;
    }},
  __esModule: {value: true}
});
var $__dom_46_js__;
var dom = ($__dom_46_js__ = require("./dom.js"), $__dom_46_js__ && $__dom_46_js__.__esModule && $__dom_46_js__ || {default: $__dom_46_js__});
function isPrintableChar(keyCode) {
  return ((keyCode == 32) || (keyCode >= 48 && keyCode <= 57) || (keyCode >= 96 && keyCode <= 111) || (keyCode >= 186 && keyCode <= 192) || (keyCode >= 219 && keyCode <= 222) || keyCode >= 226 || (keyCode >= 65 && keyCode <= 90));
}
function isMetaKey(_keyCode) {
  var metaKeys = [keyCode.ARROW_DOWN, keyCode.ARROW_UP, keyCode.ARROW_LEFT, keyCode.ARROW_RIGHT, keyCode.HOME, keyCode.END, keyCode.DELETE, keyCode.BACKSPACE, keyCode.F1, keyCode.F2, keyCode.F3, keyCode.F4, keyCode.F5, keyCode.F6, keyCode.F7, keyCode.F8, keyCode.F9, keyCode.F10, keyCode.F11, keyCode.F12, keyCode.TAB, keyCode.PAGE_DOWN, keyCode.PAGE_UP, keyCode.ENTER, keyCode.ESCAPE, keyCode.SHIFT, keyCode.CAPS_LOCK, keyCode.ALT];
  return metaKeys.indexOf(_keyCode) != -1;
}
function isCtrlKey(_keyCode) {
  return [keyCode.CONTROL_LEFT, 224, keyCode.COMMAND_LEFT, keyCode.COMMAND_RIGHT].indexOf(_keyCode) != -1;
}
function stringify(value) {
  switch (typeof value) {
    case 'string':
    case 'number':
      return value + '';
    case 'object':
      if (value === null) {
        return '';
      } else {
        return value.toString();
      }
      break;
    case 'undefined':
      return '';
    default:
      return value.toString();
  }
}
function toUpperCaseFirst(string) {
  return string[0].toUpperCase() + string.substr(1);
}
function duckSchema(object) {
  var schema;
  if (Array.isArray(object)) {
    schema = [];
  } else {
    schema = {};
    for (var i in object) {
      if (object.hasOwnProperty(i)) {
        if (object[i] && typeof object[i] === 'object' && !Array.isArray(object[i])) {
          schema[i] = duckSchema(object[i]);
        } else if (Array.isArray(object[i])) {
          if (object[i].length && typeof object[i][0] === 'object' && !Array.isArray(object[i][0])) {
            schema[i] = [duckSchema(object[i][0])];
          } else {
            schema[i] = [];
          }
        } else {
          schema[i] = null;
        }
      }
    }
  }
  return schema;
}
function spreadsheetColumnLabel(index) {
  var dividend = index + 1;
  var columnLabel = '';
  var modulo;
  while (dividend > 0) {
    modulo = (dividend - 1) % 26;
    columnLabel = String.fromCharCode(65 + modulo) + columnLabel;
    dividend = parseInt((dividend - modulo) / 26, 10);
  }
  return columnLabel;
}
function createSpreadsheetData(rowCount, colCount) {
  rowCount = typeof rowCount === 'number' ? rowCount : 100;
  colCount = typeof colCount === 'number' ? colCount : 4;
  var rows = [],
      i,
      j;
  for (i = 0; i < rowCount; i++) {
    var row = [];
    for (j = 0; j < colCount; j++) {
      row.push(spreadsheetColumnLabel(j) + (i + 1));
    }
    rows.push(row);
  }
  return rows;
}
function createSpreadsheetObjectData(rowCount, colCount) {
  rowCount = typeof rowCount === 'number' ? rowCount : 100;
  colCount = typeof colCount === 'number' ? colCount : 4;
  var rows = [],
      i,
      j;
  for (i = 0; i < rowCount; i++) {
    var row = {};
    for (j = 0; j < colCount; j++) {
      row['prop' + j] = spreadsheetColumnLabel(j) + (i + 1);
    }
    rows.push(row);
  }
  return rows;
}
function isNumeric(n) {
  var t = typeof n;
  return t == 'number' ? !isNaN(n) && isFinite(n) : t == 'string' ? !n.length ? false : n.length == 1 ? /\d/.test(n) : /^\s*[+-]?\s*(?:(?:\d+(?:\.\d+)?(?:e[+-]?\d+)?)|(?:0x[a-f\d]+))\s*$/i.test(n) : t == 'object' ? !!n && typeof n.valueOf() == "number" && !(n instanceof Date) : false;
}
function randomString() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
  }
  return s4() + s4() + s4() + s4();
}
function inherit(Child, Parent) {
  Parent.prototype.constructor = Parent;
  Child.prototype = new Parent();
  Child.prototype.constructor = Child;
  return Child;
}
function extend(target, extension) {
  for (var i in extension) {
    if (extension.hasOwnProperty(i)) {
      target[i] = extension[i];
    }
  }
}
function deepExtend(target, extension) {
  for (var key in extension) {
    if (extension.hasOwnProperty(key)) {
      if (extension[key] && typeof extension[key] === 'object') {
        if (!target[key]) {
          if (Array.isArray(extension[key])) {
            target[key] = [];
          } else {
            target[key] = {};
          }
        }
        deepExtend(target[key], extension[key]);
      } else {
        target[key] = extension[key];
      }
    }
  }
}
function deepClone(obj) {
  if (typeof obj === "object") {
    return JSON.parse(JSON.stringify(obj));
  } else {
    return obj;
  }
}
function isObjectEquals(object1, object2) {
  return JSON.stringify(object1) === JSON.stringify(object2);
}
function getPrototypeOf(obj) {
  var prototype;
  if (typeof obj.__proto__ == "object") {
    prototype = obj.__proto__;
  } else {
    var oldConstructor,
        constructor = obj.constructor;
    if (typeof obj.constructor == "function") {
      oldConstructor = constructor;
      if (delete obj.constructor) {
        constructor = obj.constructor;
        obj.constructor = oldConstructor;
      }
    }
    prototype = constructor ? constructor.prototype : null;
  }
  return prototype;
}
function columnFactory(GridSettings, conflictList) {
  function ColumnSettings() {}
  inherit(ColumnSettings, GridSettings);
  for (var i = 0,
      len = conflictList.length; i < len; i++) {
    ColumnSettings.prototype[conflictList[i]] = void 0;
  }
  return ColumnSettings;
}
function translateRowsToColumns(input) {
  var i,
      ilen,
      j,
      jlen,
      output = [],
      olen = 0;
  for (i = 0, ilen = input.length; i < ilen; i++) {
    for (j = 0, jlen = input[i].length; j < jlen; j++) {
      if (j == olen) {
        output.push([]);
        olen++;
      }
      output[j].push(input[i][j]);
    }
  }
  return output;
}
function to2dArray(arr) {
  var i = 0,
      ilen = arr.length;
  while (i < ilen) {
    arr[i] = [arr[i]];
    i++;
  }
}
function extendArray(arr, extension) {
  var i = 0,
      ilen = extension.length;
  while (i < ilen) {
    arr.push(extension[i]);
    i++;
  }
}
function isInput(element) {
  var inputs = ['INPUT', 'SELECT', 'TEXTAREA'];
  return inputs.indexOf(element.nodeName) > -1 || element.contentEditable === 'true';
}
function isOutsideInput(element) {
  return isInput(element) && element.className.indexOf('handsontableInput') == -1;
}
var keyCode = {
  MOUSE_LEFT: 1,
  MOUSE_RIGHT: 3,
  MOUSE_MIDDLE: 2,
  BACKSPACE: 8,
  COMMA: 188,
  INSERT: 45,
  DELETE: 46,
  END: 35,
  ENTER: 13,
  ESCAPE: 27,
  CONTROL_LEFT: 91,
  COMMAND_LEFT: 17,
  COMMAND_RIGHT: 93,
  ALT: 18,
  HOME: 36,
  PAGE_DOWN: 34,
  PAGE_UP: 33,
  PERIOD: 190,
  SPACE: 32,
  SHIFT: 16,
  CAPS_LOCK: 20,
  TAB: 9,
  ARROW_RIGHT: 39,
  ARROW_LEFT: 37,
  ARROW_UP: 38,
  ARROW_DOWN: 40,
  F1: 112,
  F2: 113,
  F3: 114,
  F4: 115,
  F5: 116,
  F6: 117,
  F7: 118,
  F8: 119,
  F9: 120,
  F10: 121,
  F11: 122,
  F12: 123,
  A: 65,
  X: 88,
  C: 67,
  V: 86
};
function isObject(obj) {
  return Object.prototype.toString.call(obj) == '[object Object]';
}
function pivot(arr) {
  var pivotedArr = [];
  if (!arr || arr.length === 0 || !arr[0] || arr[0].length === 0) {
    return pivotedArr;
  }
  var rowCount = arr.length;
  var colCount = arr[0].length;
  for (var i = 0; i < rowCount; i++) {
    for (var j = 0; j < colCount; j++) {
      if (!pivotedArr[j]) {
        pivotedArr[j] = [];
      }
      pivotedArr[j][i] = arr[i][j];
    }
  }
  return pivotedArr;
}
function proxy(fun, context) {
  return function() {
    return fun.apply(context, arguments);
  };
}
function cellMethodLookupFactory(methodName, allowUndefined) {
  allowUndefined = typeof allowUndefined == 'undefined' ? true : allowUndefined;
  return function cellMethodLookup(row, col) {
    return (function getMethodFromProperties(properties) {
      if (!properties) {
        return;
      } else if (properties.hasOwnProperty(methodName) && properties[methodName] !== void 0) {
        return properties[methodName];
      } else if (properties.hasOwnProperty('type') && properties.type) {
        var type;
        if (typeof properties.type != 'string') {
          throw new Error('Cell type must be a string ');
        }
        type = translateTypeNameToObject(properties.type);
        if (type.hasOwnProperty(methodName)) {
          return type[methodName];
        } else if (allowUndefined) {
          return;
        }
      }
      return getMethodFromProperties(getPrototypeOf(properties));
    })(typeof row == 'number' ? this.getCellMeta(row, col) : row);
  };
  function translateTypeNameToObject(typeName) {
    var type = Handsontable.cellTypes[typeName];
    if (typeof type == 'undefined') {
      throw new Error('You declared cell type "' + typeName + '" as a string that is not mapped to a known object. ' + 'Cell type must be an object or a string mapped to an object in Handsontable.cellTypes');
    }
    return type;
  }
}
function isMobileBrowser(userAgent) {
  if (!userAgent) {
    userAgent = navigator.userAgent;
  }
  return (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(userAgent));
}
function isTouchSupported() {
  return ('ontouchstart' in window);
}
function stopPropagation(event) {
  if (typeof(event.stopPropagation) === 'function') {
    event.stopPropagation();
  } else {
    event.cancelBubble = true;
  }
}
function pageX(event) {
  if (event.pageX) {
    return event.pageX;
  }
  var scrollLeft = dom.getWindowScrollLeft();
  var cursorX = event.clientX + scrollLeft;
  return cursorX;
}
function pageY(event) {
  if (event.pageY) {
    return event.pageY;
  }
  var scrollTop = dom.getWindowScrollTop();
  var cursorY = event.clientY + scrollTop;
  return cursorY;
}
function defineGetter(object, property, value, options) {
  options.value = value;
  options.writable = options.writable === false ? false : true;
  options.enumerable = options.enumerable === false ? false : true;
  options.configurable = options.configurable === false ? false : true;
  Object.defineProperty(object, property, options);
}
var lastTime = 0;
var vendors = ['ms', 'moz', 'webkit', 'o'];
var _requestAnimationFrame = window.requestAnimationFrame;
var _cancelAnimationFrame = window.cancelAnimationFrame;
for (var x = 0; x < vendors.length && !_requestAnimationFrame; ++x) {
  _requestAnimationFrame = window[vendors[x] + 'RequestAnimationFrame'];
  _cancelAnimationFrame = window[vendors[x] + 'CancelAnimationFrame'] || window[vendors[x] + 'CancelRequestAnimationFrame'];
}
if (!_requestAnimationFrame) {
  _requestAnimationFrame = function(callback) {
    var currTime = new Date().getTime();
    var timeToCall = Math.max(0, 16 - (currTime - lastTime));
    var id = window.setTimeout(function() {
      callback(currTime + timeToCall);
    }, timeToCall);
    lastTime = currTime + timeToCall;
    return id;
  };
}
if (!_cancelAnimationFrame) {
  _cancelAnimationFrame = function(id) {
    clearTimeout(id);
  };
}
function requestAnimationFrame(callback) {
  return _requestAnimationFrame.call(window, callback);
}
function cancelAnimationFrame(id) {
  _cancelAnimationFrame.call(window, id);
}
window.Handsontable = window.Handsontable || {};
Handsontable.helper = {
  cancelAnimationFrame: cancelAnimationFrame,
  cellMethodLookupFactory: cellMethodLookupFactory,
  columnFactory: columnFactory,
  createSpreadsheetData: createSpreadsheetData,
  createSpreadsheetObjectData: createSpreadsheetObjectData,
  duckSchema: duckSchema,
  deepClone: deepClone,
  deepExtend: deepExtend,
  defineGetter: defineGetter,
  extend: extend,
  extendArray: extendArray,
  getPrototypeOf: getPrototypeOf,
  inherit: inherit,
  isCtrlKey: isCtrlKey,
  isInput: isInput,
  isMetaKey: isMetaKey,
  isMobileBrowser: isMobileBrowser,
  isNumeric: isNumeric,
  isObject: isObject,
  isObjectEquals: isObjectEquals,
  isOutsideInput: isOutsideInput,
  isPrintableChar: isPrintableChar,
  isTouchSupported: isTouchSupported,
  keyCode: keyCode,
  pageX: pageX,
  pageY: pageY,
  pivot: pivot,
  proxy: proxy,
  randomString: randomString,
  requestAnimationFrame: requestAnimationFrame,
  spreadsheetColumnLabel: spreadsheetColumnLabel,
  stopPropagation: stopPropagation,
  stringify: stringify,
  to2dArray: to2dArray,
  toUpperCaseFirst: toUpperCaseFirst,
  translateRowsToColumns: translateRowsToColumns
};


//# 
},{"./dom.js":27}],43:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  MultiMap: {get: function() {
      return MultiMap;
    }},
  __esModule: {value: true}
});
;
window.MultiMap = MultiMap;
function MultiMap() {
  var map = {
    arrayMap: [],
    weakMap: new WeakMap()
  };
  return {
    'get': function(key) {
      if (canBeAnArrayMapKey(key)) {
        return map.arrayMap[key];
      } else if (canBeAWeakMapKey(key)) {
        return map.weakMap.get(key);
      }
    },
    'set': function(key, value) {
      if (canBeAnArrayMapKey(key)) {
        map.arrayMap[key] = value;
      } else if (canBeAWeakMapKey(key)) {
        map.weakMap.set(key, value);
      } else {
        throw new Error('Invalid key type');
      }
    },
    'delete': function(key) {
      if (canBeAnArrayMapKey(key)) {
        delete map.arrayMap[key];
      } else if (canBeAWeakMapKey(key)) {
        map.weakMap['delete'](key);
      }
    }
  };
  function canBeAnArrayMapKey(obj) {
    return obj !== null && !isNaNSymbol(obj) && (typeof obj == 'string' || typeof obj == 'number');
  }
  function canBeAWeakMapKey(obj) {
    return obj !== null && (typeof obj == 'object' || typeof obj == 'function');
  }
  function isNaNSymbol(obj) {
    return obj !== obj;
  }
}


//# 
},{}],44:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  Hooks: {get: function() {
      return Hooks;
    }},
  __esModule: {value: true}
});
var $__eventManager_46_js__;
var REGISTERED_HOOKS = ["afterCellMetaReset", "afterChange", "afterChangesObserved", "afterColumnMove", "afterColumnResize", "afterContextMenuDefaultOptions", "afterContextMenuHide", "afterContextMenuShow", "afterCopyLimit", "afterCreateCol", "afterCreateRow", "afterDeselect", "afterDestroy", "afterDocumentKeyDown", "afterGetCellMeta", "afterGetColHeader", "afterGetRowHeader", "afterInit", "afterIsMultipleSelectionCheck", "afterLoadData", "afterMomentumScroll", "afterOnCellCornerMouseDown", "afterOnCellMouseDown", "afterOnCellMouseOver", "afterRemoveCol", "afterRemoveRow", "afterRender", "afterRenderer", "afterRowMove", "afterRowResize", "afterScrollHorizontally", "afterScrollVertically", "afterSelection", "afterSelectionByProp", "afterSelectionEnd", "afterSelectionEndByProp", "afterSetCellMeta", "afterUpdateSettings", "afterValidate", "beforeAutofill", "beforeCellAlignment", "beforeChange", "beforeChangeRender", "beforeDrawBorders", "beforeGetCellMeta", "beforeInit", "beforeInitWalkontable", "beforeKeyDown", "beforeOnCellMouseDown", "beforeRemoveCol", "beforeRemoveRow", "beforeRender", "beforeSetRangeEnd", "beforeTouchScroll", "beforeValidate", "modifyCol", "modifyColWidth", "modifyRow", "modifyRowHeight", "persistentStateLoad", "persistentStateReset", "persistentStateSave"];
var EventManager = ($__eventManager_46_js__ = require("./eventManager.js"), $__eventManager_46_js__ && $__eventManager_46_js__.__esModule && $__eventManager_46_js__ || {default: $__eventManager_46_js__}).EventManager;
var Hooks = function Hooks() {
  this.globalBucket = this.createEmptyBucket();
};
($traceurRuntime.createClass)(Hooks, {
  createEmptyBucket: function() {
    var handler = Object.create(null);
    for (var i = 0,
        len = REGISTERED_HOOKS.length; i < len; i++) {
      handler[REGISTERED_HOOKS[i]] = [];
    }
    return handler;
  },
  getBucket: function() {
    var context = arguments[0] !== (void 0) ? arguments[0] : null;
    if (context) {
      if (!context.pluginHookBucket) {
        context.pluginHookBucket = this.createEmptyBucket();
      }
      return context.pluginHookBucket;
    }
    return this.globalBucket;
  },
  add: function(key, callback) {
    var context = arguments[2] !== (void 0) ? arguments[2] : null;
    if (Array.isArray(callback)) {
      for (var i = 0,
          len = callback.length; i < len; i++) {
        this.add(key, callback[i]);
      }
    } else {
      var bucket = this.getBucket(context);
      if (typeof bucket[key] === 'undefined') {
        this.register(key);
        bucket[key] = [];
      }
      callback.skip = false;
      if (bucket[key].indexOf(callback) === -1) {
        bucket[key].push(callback);
      }
    }
    return this;
  },
  once: function(key, callback) {
    var context = arguments[2] !== (void 0) ? arguments[2] : null;
    if (Array.isArray(callback)) {
      for (var i = 0,
          len = callback.length; i < len; i++) {
        callback[i].runOnce = true;
        this.add(key, callback[i], context);
      }
    } else {
      callback.runOnce = true;
      this.add(key, callback, context);
    }
  },
  remove: function(key, callback) {
    var context = arguments[2] !== (void 0) ? arguments[2] : null;
    var bucket = this.getBucket(context);
    if (typeof bucket[key] !== 'undefined') {
      if (bucket[key].indexOf(callback) >= 0) {
        callback.skip = true;
        return true;
      }
    }
    return false;
  },
  run: function(context, key, p1, p2, p3, p4, p5, p6) {
    {
      var globalHandlers = this.globalBucket[key];
      var len = globalHandlers ? globalHandlers.length : 0;
      for (var i = 0; i < len; i++) {
        if (globalHandlers[i].skip) {
          continue;
        }
        var res = globalHandlers[i].call(context, p1, p2, p3, p4, p5, p6);
        if (res !== void 0) {
          p1 = res;
        }
        if (globalHandlers[i].runOnce) {
          this.remove(key, globalHandlers[i]);
        }
      }
    }
    {
      var localHandlers = this.getBucket(context)[key];
      var len$__2 = localHandlers ? localHandlers.length : 0;
      for (var i$__3 = 0; i$__3 < len$__2; i$__3++) {
        if (localHandlers[i$__3].skip) {
          continue;
        }
        var res$__4 = localHandlers[i$__3].call(context, p1, p2, p3, p4, p5, p6);
        if (res$__4 !== void 0) {
          p1 = res$__4;
        }
        if (localHandlers[i$__3].runOnce) {
          this.remove(key, localHandlers[i$__3], context);
        }
      }
    }
    return p1;
  },
  destroy: function() {
    var context = arguments[0] !== (void 0) ? arguments[0] : null;
    var bucket = this.getBucket(context);
    for (var key in bucket) {
      for (var i = 0,
          len = bucket[key].length; i < len; i++) {
        this.remove(key, bucket[key], context);
      }
    }
  },
  register: function(key) {
    if (!this.isRegistered(key)) {
      REGISTERED_HOOKS.push(key);
    }
  },
  deregister: function(key) {
    if (this.isRegistered(key)) {
      REGISTERED_HOOKS.splice(REGISTERED_HOOKS.indexOf(key), 1);
    }
  },
  isRegistered: function(key) {
    return REGISTERED_HOOKS.indexOf(key) >= 0;
  },
  getRegistered: function() {
    return REGISTERED_HOOKS;
  }
}, {});
;


//# 
},{"./eventManager.js":41}],45:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  registerPlugin: {get: function() {
      return registerPlugin;
    }},
  getPlugin: {get: function() {
      return getPlugin;
    }},
  __esModule: {value: true}
});
;
var registeredPlugins = new WeakMap();
function registerPlugin(pluginName, PluginClass) {
  Handsontable.hooks.add('beforeInit', function() {
    var holder;
    pluginName = pluginName.toLowerCase();
    if (!registeredPlugins.has(this)) {
      registeredPlugins.set(this, {});
    }
    holder = registeredPlugins.get(this);
    if (!holder[pluginName]) {
      holder[pluginName] = new PluginClass(this);
    }
  });
  Handsontable.hooks.add('afterDestroy', function() {
    var i,
        pluginsHolder;
    if (registeredPlugins.has(this)) {
      pluginsHolder = registeredPlugins.get(this);
      for (i in pluginsHolder) {
        if (pluginsHolder.hasOwnProperty(i)) {
          pluginsHolder[i].destroy();
        }
      }
      registeredPlugins.delete(this);
    }
  });
}
function getPlugin(instance, pluginName) {
  if (typeof pluginName != 'string') {
    throw Error('Only strings can be passed as "plugin" parameter');
  }
  var _pluginName = pluginName.toLowerCase();
  if (!registeredPlugins.has(instance) || !registeredPlugins.get(instance)[_pluginName]) {
    throw Error('No plugin registered under name "' + pluginName + '"');
  }
  return registeredPlugins.get(instance)[_pluginName];
}


//# 
},{}],46:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  default: {get: function() {
      return $__default;
    }},
  __esModule: {value: true}
});
var $___46__46__47_helpers_46_js__;
var defineGetter = ($___46__46__47_helpers_46_js__ = require("./../helpers.js"), $___46__46__47_helpers_46_js__ && $___46__46__47_helpers_46_js__.__esModule && $___46__46__47_helpers_46_js__ || {default: $___46__46__47_helpers_46_js__}).defineGetter;
var BasePlugin = function BasePlugin(hotInstance) {
  defineGetter(this, 'hot', hotInstance, {writable: false});
};
($traceurRuntime.createClass)(BasePlugin, {destroy: function() {
    delete this.hot;
  }}, {});
var $__default = BasePlugin;


//# 
},{"./../helpers.js":42}],47:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  AutoColumnSize: {get: function() {
      return AutoColumnSize;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_helpers_46_js__,
    $___46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47_plugins_46_js__;
var helper = ($___46__46__47__46__46__47_helpers_46_js__ = require("./../../helpers.js"), $___46__46__47__46__46__47_helpers_46_js__ && $___46__46__47__46__46__47_helpers_46_js__.__esModule && $___46__46__47__46__46__47_helpers_46_js__ || {default: $___46__46__47__46__46__47_helpers_46_js__});
var dom = ($___46__46__47__46__46__47_dom_46_js__ = require("./../../dom.js"), $___46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47_dom_46_js__});
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
;
function AutoColumnSize() {
  var plugin = this,
      sampleCount = 5;
  this.beforeInit = function() {
    var instance = this;
    instance.autoColumnWidths = [];
    if (instance.getSettings().autoColumnSize !== false) {
      if (!instance.autoColumnSizeTmp) {
        instance.autoColumnSizeTmp = {
          table: null,
          tableStyle: null,
          theadTh: null,
          tbody: null,
          container: null,
          containerStyle: null,
          determineBeforeNextRender: true
        };
        instance.addHook('beforeRender', htAutoColumnSize.determineIfChanged);
        instance.addHook('modifyColWidth', htAutoColumnSize.modifyColWidth);
        instance.addHook('afterDestroy', htAutoColumnSize.afterDestroy);
        instance.determineColumnWidth = plugin.determineColumnWidth;
      }
    } else {
      if (instance.autoColumnSizeTmp) {
        instance.removeHook('beforeRender', htAutoColumnSize.determineIfChanged);
        instance.removeHook('modifyColWidth', htAutoColumnSize.modifyColWidth);
        instance.removeHook('afterDestroy', htAutoColumnSize.afterDestroy);
        delete instance.determineColumnWidth;
        plugin.afterDestroy.call(instance);
      }
    }
  };
  this.determineIfChanged = function(force) {
    if (force) {
      htAutoColumnSize.determineColumnsWidth.apply(this, arguments);
    }
  };
  this.determineColumnWidth = function(col) {
    var instance = this,
        tmp = instance.autoColumnSizeTmp;
    if (!tmp.container) {
      createTmpContainer.call(tmp, instance);
    }
    tmp.container.className = instance.rootElement.className + ' htAutoColumnSize';
    tmp.table.className = instance.table.className;
    var rows = instance.countRows();
    var samples = {};
    for (var r = 0; r < rows; r++) {
      var value = instance.getDataAtCell(r, col);
      if (!Array.isArray(value)) {
        value = helper.stringify(value);
      }
      var len = value.length;
      if (!samples[len]) {
        samples[len] = {
          needed: sampleCount,
          strings: []
        };
      }
      if (samples[len].needed) {
        samples[len].strings.push({
          value: value,
          row: r
        });
        samples[len].needed--;
      }
    }
    var settings = instance.getSettings();
    if (settings.colHeaders) {
      instance.view.appendColHeader(col, tmp.theadTh);
    }
    dom.empty(tmp.tbody);
    for (var i in samples) {
      if (samples.hasOwnProperty(i)) {
        for (var j = 0,
            jlen = samples[i].strings.length; j < jlen; j++) {
          var row = samples[i].strings[j].row;
          var cellProperties = instance.getCellMeta(row, col);
          cellProperties.col = col;
          cellProperties.row = row;
          var renderer = instance.getCellRenderer(cellProperties);
          var tr = document.createElement('tr');
          var td = document.createElement('td');
          renderer(instance, td, row, col, instance.colToProp(col), samples[i].strings[j].value, cellProperties);
          r++;
          tr.appendChild(td);
          tmp.tbody.appendChild(tr);
        }
      }
    }
    var parent = instance.rootElement.parentNode;
    parent.appendChild(tmp.container);
    var width = dom.outerWidth(tmp.table);
    parent.removeChild(tmp.container);
    return width;
  };
  this.determineColumnsWidth = function() {
    var instance = this;
    var settings = this.getSettings();
    if (settings.autoColumnSize || !settings.colWidths) {
      var cols = this.countCols();
      for (var c = 0; c < cols; c++) {
        if (!instance._getColWidthFromSettings(c)) {
          this.autoColumnWidths[c] = plugin.determineColumnWidth.call(instance, c);
        }
      }
    }
  };
  this.modifyColWidth = function(width, col) {
    if (this.autoColumnWidths[col] && this.autoColumnWidths[col] > width) {
      return this.autoColumnWidths[col];
    }
    return width;
  };
  this.afterDestroy = function() {
    var instance = this;
    if (instance.autoColumnSizeTmp && instance.autoColumnSizeTmp.container && instance.autoColumnSizeTmp.container.parentNode) {
      instance.autoColumnSizeTmp.container.parentNode.removeChild(instance.autoColumnSizeTmp.container);
    }
    instance.autoColumnSizeTmp = null;
  };
  function createTmpContainer(instance) {
    var d = document,
        tmp = this;
    tmp.table = d.createElement('table');
    tmp.theadTh = d.createElement('th');
    tmp.table.appendChild(d.createElement('thead')).appendChild(d.createElement('tr')).appendChild(tmp.theadTh);
    tmp.tableStyle = tmp.table.style;
    tmp.tableStyle.tableLayout = 'auto';
    tmp.tableStyle.width = 'auto';
    tmp.tbody = d.createElement('tbody');
    tmp.table.appendChild(tmp.tbody);
    tmp.container = d.createElement('div');
    tmp.container.className = instance.rootElement.className + ' hidden';
    tmp.containerStyle = tmp.container.style;
    tmp.container.appendChild(tmp.table);
  }
}
var htAutoColumnSize = new AutoColumnSize();
Handsontable.hooks.add('beforeInit', htAutoColumnSize.beforeInit);
Handsontable.hooks.add('afterUpdateSettings', htAutoColumnSize.beforeInit);


//# 
},{"./../../dom.js":27,"./../../helpers.js":42,"./../../plugins.js":45}],48:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  Autofill: {get: function() {
      return Autofill;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47_eventManager_46_js__,
    $___46__46__47__46__46__47_plugins_46_js__,
    $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__;
var dom = ($___46__46__47__46__46__47_dom_46_js__ = require("./../../dom.js"), $___46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47_dom_46_js__});
var eventManagerObject = ($___46__46__47__46__46__47_eventManager_46_js__ = require("./../../eventManager.js"), $___46__46__47__46__46__47_eventManager_46_js__ && $___46__46__47__46__46__47_eventManager_46_js__.__esModule && $___46__46__47__46__46__47_eventManager_46_js__ || {default: $___46__46__47__46__46__47_eventManager_46_js__}).eventManager;
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
var WalkontableCellCoords = ($___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ = require("./../../3rdparty/walkontable/src/cell/coords.js"), $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__.__esModule && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ || {default: $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__}).WalkontableCellCoords;
;
function getDeltas(start, end, data, direction) {
  var rlength = data.length,
      clength = data ? data[0].length : 0,
      deltas = [],
      arr = [],
      diffRow,
      diffCol,
      startValue,
      endValue,
      delta;
  diffRow = end.row - start.row;
  diffCol = end.col - start.col;
  if (['down', 'up'].indexOf(direction) !== -1) {
    for (var col = 0; col <= diffCol; col++) {
      startValue = parseInt(data[0][col], 10);
      endValue = parseInt(data[rlength - 1][col], 10);
      delta = (direction === 'down' ? (endValue - startValue) : (startValue - endValue)) / (rlength - 1) || 0;
      arr.push(delta);
    }
    deltas.push(arr);
  }
  if (['right', 'left'].indexOf(direction) !== -1) {
    for (var row = 0; row <= diffRow; row++) {
      startValue = parseInt(data[row][0], 10);
      endValue = parseInt(data[row][clength - 1], 10);
      delta = (direction === 'right' ? (endValue - startValue) : (startValue - endValue)) / (clength - 1) || 0;
      arr = [];
      arr.push(delta);
      deltas.push(arr);
    }
  }
  return deltas;
}
function Autofill(instance) {
  var _this = this,
      mouseDownOnCellCorner = false,
      wtOnCellCornerMouseDown,
      wtOnCellMouseOver,
      eventManager;
  this.instance = instance;
  this.addingStarted = false;
  eventManager = eventManagerObject(instance);
  function mouseUpCallback(event) {
    if (!instance.autofill) {
      return true;
    }
    if (instance.autofill.handle && instance.autofill.handle.isDragged) {
      if (instance.autofill.handle.isDragged > 1) {
        instance.autofill.apply();
      }
      instance.autofill.handle.isDragged = 0;
      mouseDownOnCellCorner = false;
    }
  }
  function mouseMoveCallback(event) {
    var tableBottom,
        tableRight;
    if (!_this.instance.autofill) {
      return false;
    }
    tableBottom = dom.offset(_this.instance.table).top - (window.pageYOffset || document.documentElement.scrollTop) + dom.outerHeight(_this.instance.table);
    tableRight = dom.offset(_this.instance.table).left - (window.pageXOffset || document.documentElement.scrollLeft) + dom.outerWidth(_this.instance.table);
    if (_this.addingStarted === false && _this.instance.autofill.handle.isDragged > 0 && event.clientY > tableBottom && event.clientX <= tableRight) {
      _this.instance.mouseDragOutside = true;
      _this.addingStarted = true;
    } else {
      _this.instance.mouseDragOutside = false;
    }
    if (_this.instance.mouseDragOutside) {
      setTimeout(function() {
        _this.addingStarted = false;
        _this.instance.alter('insert_row');
      }, 200);
    }
  }
  eventManager.addEventListener(document, 'mouseup', mouseUpCallback);
  eventManager.addEventListener(document, 'mousemove', mouseMoveCallback);
  wtOnCellCornerMouseDown = this.instance.view.wt.wtSettings.settings.onCellCornerMouseDown;
  this.instance.view.wt.wtSettings.settings.onCellCornerMouseDown = function(event) {
    instance.autofill.handle.isDragged = 1;
    mouseDownOnCellCorner = true;
    wtOnCellCornerMouseDown(event);
  };
  wtOnCellMouseOver = this.instance.view.wt.wtSettings.settings.onCellMouseOver;
  this.instance.view.wt.wtSettings.settings.onCellMouseOver = function(event, coords, TD, wt) {
    if (instance.autofill && mouseDownOnCellCorner && !instance.view.isMouseDown() && instance.autofill.handle && instance.autofill.handle.isDragged) {
      instance.autofill.handle.isDragged++;
      instance.autofill.showBorder(coords);
      instance.autofill.checkIfNewRowNeeded();
    }
    wtOnCellMouseOver(event, coords, TD, wt);
  };
  this.instance.view.wt.wtSettings.settings.onCellCornerDblClick = function() {
    instance.autofill.selectAdjacent();
  };
}
Autofill.prototype.init = function() {
  this.handle = {};
};
Autofill.prototype.disable = function() {
  this.handle.disabled = true;
};
Autofill.prototype.selectAdjacent = function() {
  var select,
      data,
      r,
      maxR,
      c;
  if (this.instance.selection.isMultiple()) {
    select = this.instance.view.wt.selections.area.getCorners();
  } else {
    select = this.instance.view.wt.selections.current.getCorners();
  }
  data = this.instance.getData();
  rows: for (r = select[2] + 1; r < this.instance.countRows(); r++) {
    for (c = select[1]; c <= select[3]; c++) {
      if (data[r][c]) {
        break rows;
      }
    }
    if (!!data[r][select[1] - 1] || !!data[r][select[3] + 1]) {
      maxR = r;
    }
  }
  if (maxR) {
    this.instance.view.wt.selections.fill.clear();
    this.instance.view.wt.selections.fill.add(new WalkontableCellCoords(select[0], select[1]));
    this.instance.view.wt.selections.fill.add(new WalkontableCellCoords(maxR, select[3]));
    this.apply();
  }
};
Autofill.prototype.apply = function() {
  var drag,
      select,
      start,
      end,
      _data,
      direction,
      deltas,
      selRange;
  this.handle.isDragged = 0;
  drag = this.instance.view.wt.selections.fill.getCorners();
  if (!drag) {
    return;
  }
  this.instance.view.wt.selections.fill.clear();
  if (this.instance.selection.isMultiple()) {
    select = this.instance.view.wt.selections.area.getCorners();
  } else {
    select = this.instance.view.wt.selections.current.getCorners();
  }
  Handsontable.hooks.run(this.instance, 'afterAutofillApplyValues', select, drag);
  if (drag[0] === select[0] && drag[1] < select[1]) {
    direction = 'left';
    start = new WalkontableCellCoords(drag[0], drag[1]);
    end = new WalkontableCellCoords(drag[2], select[1] - 1);
  } else if (drag[0] === select[0] && drag[3] > select[3]) {
    direction = 'right';
    start = new WalkontableCellCoords(drag[0], select[3] + 1);
    end = new WalkontableCellCoords(drag[2], drag[3]);
  } else if (drag[0] < select[0] && drag[1] === select[1]) {
    direction = 'up';
    start = new WalkontableCellCoords(drag[0], drag[1]);
    end = new WalkontableCellCoords(select[0] - 1, drag[3]);
  } else if (drag[2] > select[2] && drag[1] === select[1]) {
    direction = 'down';
    start = new WalkontableCellCoords(select[2] + 1, drag[1]);
    end = new WalkontableCellCoords(drag[2], drag[3]);
  }
  if (start && start.row > -1 && start.col > -1) {
    selRange = {
      from: this.instance.getSelectedRange().from,
      to: this.instance.getSelectedRange().to
    };
    _data = this.instance.getData(selRange.from.row, selRange.from.col, selRange.to.row, selRange.to.col);
    deltas = getDeltas(start, end, _data, direction);
    Handsontable.hooks.run(this.instance, 'beforeAutofill', start, end, _data);
    this.instance.populateFromArray(start.row, start.col, _data, end.row, end.col, 'autofill', null, direction, deltas);
    this.instance.selection.setRangeStart(new WalkontableCellCoords(drag[0], drag[1]));
    this.instance.selection.setRangeEnd(new WalkontableCellCoords(drag[2], drag[3]));
  } else {
    this.instance.selection.refreshBorders();
  }
};
Autofill.prototype.showBorder = function(coords) {
  var topLeft = this.instance.getSelectedRange().getTopLeftCorner(),
      bottomRight = this.instance.getSelectedRange().getBottomRightCorner();
  if (this.instance.getSettings().fillHandle !== 'horizontal' && (bottomRight.row < coords.row || topLeft.row > coords.row)) {
    coords = new WalkontableCellCoords(coords.row, bottomRight.col);
  } else if (this.instance.getSettings().fillHandle !== 'vertical') {
    coords = new WalkontableCellCoords(bottomRight.row, coords.col);
  } else {
    return;
  }
  this.instance.view.wt.selections.fill.clear();
  this.instance.view.wt.selections.fill.add(this.instance.getSelectedRange().from);
  this.instance.view.wt.selections.fill.add(this.instance.getSelectedRange().to);
  this.instance.view.wt.selections.fill.add(coords);
  this.instance.view.render();
};
Autofill.prototype.checkIfNewRowNeeded = function() {
  var fillCorners,
      selection,
      tableRows = this.instance.countRows(),
      that = this;
  if (this.instance.view.wt.selections.fill.cellRange && this.addingStarted === false) {
    selection = this.instance.getSelected();
    fillCorners = this.instance.view.wt.selections.fill.getCorners();
    if (selection[2] < tableRows - 1 && fillCorners[2] === tableRows - 1) {
      this.addingStarted = true;
      this.instance._registerTimeout(setTimeout(function() {
        that.instance.alter('insert_row');
        that.addingStarted = false;
      }, 200));
    }
  }
};
Handsontable.hooks.add('afterInit', function() {
  var autofill = new Autofill(this);
  if (typeof this.getSettings().fillHandle !== 'undefined') {
    if (autofill.handle && this.getSettings().fillHandle === false) {
      autofill.disable();
    } else if (!autofill.handle && this.getSettings().fillHandle !== false) {
      this.autofill = autofill;
      this.autofill.init();
    }
  }
});
Handsontable.Autofill = Autofill;


//# 
},{"./../../3rdparty/walkontable/src/cell/coords.js":5,"./../../dom.js":27,"./../../eventManager.js":41,"./../../plugins.js":45}],49:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  default: {get: function() {
      return $__default;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47_eventManager_46_js__,
    $___46__46__47__95_base_46_js__,
    $___46__46__47__46__46__47_plugins_46_js__;
var dom = ($___46__46__47__46__46__47_dom_46_js__ = require("./../../dom.js"), $___46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47_dom_46_js__});
var eventManagerObject = ($___46__46__47__46__46__47_eventManager_46_js__ = require("./../../eventManager.js"), $___46__46__47__46__46__47_eventManager_46_js__ && $___46__46__47__46__46__47_eventManager_46_js__.__esModule && $___46__46__47__46__46__47_eventManager_46_js__ || {default: $___46__46__47__46__46__47_eventManager_46_js__}).eventManager;
var BasePlugin = ($___46__46__47__95_base_46_js__ = require("./../_base.js"), $___46__46__47__95_base_46_js__ && $___46__46__47__95_base_46_js__.__esModule && $___46__46__47__95_base_46_js__ || {default: $___46__46__47__95_base_46_js__}).default;
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
var ColumnSorting = function ColumnSorting(hotInstance) {
  var $__3 = this;
  $traceurRuntime.superConstructor($ColumnSorting).call(this, hotInstance);
  var _this = this;
  this.sortIndicators = [];
  this.hot.addHook('afterInit', (function() {
    return $__3.init.call($__3, 'afterInit');
  }));
  this.hot.addHook('afterUpdateSettings', (function() {
    return $__3.init.call($__3, 'afterUpdateSettings');
  }));
  this.hot.addHook('modifyRow', function() {
    return _this.translateRow.apply(_this, arguments);
  });
  this.hot.addHook('afterGetColHeader', function() {
    return _this.getColHeader.apply(_this, arguments);
  });
  Handsontable.hooks.register('beforeColumnSort');
  Handsontable.hooks.register('afterColumnSort');
};
var $ColumnSorting = ColumnSorting;
($traceurRuntime.createClass)(ColumnSorting, {
  init: function(source) {
    var sortingSettings = this.hot.getSettings().columnSorting,
        _this = this;
    this.hot.sortingEnabled = !!(sortingSettings);
    if (this.hot.sortingEnabled) {
      this.hot.sortIndex = [];
      var loadedSortingState = this.loadSortingState(),
          sortingColumn,
          sortingOrder;
      if (typeof loadedSortingState != 'undefined') {
        sortingColumn = loadedSortingState.sortColumn;
        sortingOrder = loadedSortingState.sortOrder;
      } else {
        sortingColumn = sortingSettings.column;
        sortingOrder = sortingSettings.sortOrder;
      }
      this.sortByColumn(sortingColumn, sortingOrder);
      this.hot.sort = function() {
        var args = Array.prototype.slice.call(arguments);
        return _this.sortByColumn.apply(_this, args);
      };
      if (typeof this.hot.getSettings().observeChanges == 'undefined') {
        this.enableObserveChangesPlugin();
      }
      if (source == 'afterInit') {
        this.bindColumnSortingAfterClick();
        this.hot.addHook('afterCreateRow', function() {
          _this.afterCreateRow.apply(_this, arguments);
        });
        this.hot.addHook('afterRemoveRow', function() {
          _this.afterRemoveRow.apply(_this, arguments);
        });
        this.hot.addHook('afterLoadData', function() {
          _this.init.apply(_this, arguments);
        });
      }
    } else {
      this.hot.sort = void 0;
      this.hot.removeHook('afterCreateRow', this.afterCreateRow);
      this.hot.removeHook('afterRemoveRow', this.afterRemoveRow);
      this.hot.removeHook('afterLoadData', this.init);
    }
  },
  setSortingColumn: function(col, order) {
    if (typeof col == 'undefined') {
      this.hot.sortColumn = void 0;
      this.hot.sortOrder = void 0;
      return;
    } else if (this.hot.sortColumn === col && typeof order == 'undefined') {
      if (this.hot.sortOrder === false) {
        this.hot.sortOrder = void 0;
      } else {
        this.hot.sortOrder = !this.hot.sortOrder;
      }
    } else {
      this.hot.sortOrder = typeof order != 'undefined' ? order : true;
    }
    this.hot.sortColumn = col;
  },
  sortByColumn: function(col, order) {
    this.setSortingColumn(col, order);
    if (typeof this.hot.sortColumn == 'undefined') {
      return;
    }
    Handsontable.hooks.run(this.hot, 'beforeColumnSort', this.hot.sortColumn, this.hot.sortOrder);
    this.sort();
    this.hot.render();
    this.saveSortingState();
    Handsontable.hooks.run(this.hot, 'afterColumnSort', this.hot.sortColumn, this.hot.sortOrder);
  },
  saveSortingState: function() {
    var sortingState = {};
    if (typeof this.hot.sortColumn != 'undefined') {
      sortingState.sortColumn = this.hot.sortColumn;
    }
    if (typeof this.hot.sortOrder != 'undefined') {
      sortingState.sortOrder = this.hot.sortOrder;
    }
    if (sortingState.hasOwnProperty('sortColumn') || sortingState.hasOwnProperty('sortOrder')) {
      Handsontable.hooks.run(this.hot, 'persistentStateSave', 'columnSorting', sortingState);
    }
  },
  loadSortingState: function() {
    var storedState = {};
    Handsontable.hooks.run(this.hot, 'persistentStateLoad', 'columnSorting', storedState);
    return storedState.value;
  },
  bindColumnSortingAfterClick: function() {
    var eventManager = eventManagerObject(this.hot),
        _this = this;
    eventManager.addEventListener(this.hot.rootElement, 'click', function(e) {
      if (dom.hasClass(e.target, 'columnSorting')) {
        var col = getColumn(e.target);
        if (col !== this.lastSortedColumn) {
          _this.sortOrderClass = 'ascending';
        } else {
          switch (_this.hot.sortOrder) {
            case void 0:
              _this.sortOrderClass = 'ascending';
              break;
            case true:
              _this.sortOrderClass = 'descending';
              break;
            case false:
              _this.sortOrderClass = void 0;
          }
        }
        this.lastSortedColumn = col;
        _this.sortByColumn(col);
      }
    });
    function countRowHeaders() {
      var THs = _this.hot.view.TBODY.querySelector('tr').querySelectorAll('th');
      return THs.length;
    }
    function getColumn(target) {
      var TH = dom.closest(target, 'TH');
      return dom.index(TH) - countRowHeaders();
    }
  },
  enableObserveChangesPlugin: function() {
    var _this = this;
    this.hot._registerTimeout(setTimeout(function() {
      _this.hot.updateSettings({observeChanges: true});
    }, 0));
  },
  defaultSort: function(sortOrder) {
    return function(a, b) {
      if (typeof a[1] == "string") {
        a[1] = a[1].toLowerCase();
      }
      if (typeof b[1] == "string") {
        b[1] = b[1].toLowerCase();
      }
      if (a[1] === b[1]) {
        return 0;
      }
      if (a[1] === null || a[1] === "") {
        return 1;
      }
      if (b[1] === null || b[1] === "") {
        return -1;
      }
      if (a[1] < b[1]) {
        return sortOrder ? -1 : 1;
      }
      if (a[1] > b[1]) {
        return sortOrder ? 1 : -1;
      }
      return 0;
    };
  },
  dateSort: function(sortOrder) {
    return function(a, b) {
      if (a[1] === b[1]) {
        return 0;
      }
      if (a[1] === null) {
        return 1;
      }
      if (b[1] === null) {
        return -1;
      }
      var aDate = new Date(a[1]);
      var bDate = new Date(b[1]);
      if (aDate < bDate) {
        return sortOrder ? -1 : 1;
      }
      if (aDate > bDate) {
        return sortOrder ? 1 : -1;
      }
      return 0;
    };
  },
  sort: function() {
    if (typeof this.hot.sortOrder == 'undefined') {
      return;
    }
    var colMeta,
        sortFunction;
    this.hot.sortingEnabled = false;
    this.hot.sortIndex.length = 0;
    var colOffset = this.hot.colOffset();
    for (var i = 0,
        ilen = this.hot.countRows() - this.hot.getSettings().minSpareRows; i < ilen; i++) {
      this.hot.sortIndex.push([i, this.hot.getDataAtCell(i, this.hot.sortColumn + colOffset)]);
    }
    colMeta = this.hot.getCellMeta(0, this.hot.sortColumn);
    this.sortIndicators[this.hot.sortColumn] = colMeta.sortIndicator;
    switch (colMeta.type) {
      case 'date':
        sortFunction = this.dateSort;
        break;
      default:
        sortFunction = this.defaultSort;
    }
    this.hot.sortIndex.sort(sortFunction(this.hot.sortOrder));
    for (var i = this.hot.sortIndex.length; i < this.hot.countRows(); i++) {
      this.hot.sortIndex.push([i, this.hot.getDataAtCell(i, this.hot.sortColumn + colOffset)]);
    }
    this.hot.sortingEnabled = true;
  },
  translateRow: function(row) {
    if (this.hot.sortingEnabled && (typeof this.hot.sortOrder !== 'undefined') && this.hot.sortIndex && this.hot.sortIndex.length && this.hot.sortIndex[row]) {
      return this.hot.sortIndex[row][0];
    }
    return row;
  },
  untranslateRow: function(row) {
    if (this.hot.sortingEnabled && this.hot.sortIndex && this.hot.sortIndex.length) {
      for (var i = 0; i < this.hot.sortIndex.length; i++) {
        if (this.hot.sortIndex[i][0] == row) {
          return i;
        }
      }
    }
  },
  getColHeader: function(col, TH) {
    var headerLink = TH.querySelector('.colHeader');
    if (this.hot.getSettings().columnSorting && col >= 0) {
      dom.addClass(headerLink, 'columnSorting');
    }
    dom.removeClass(headerLink, 'descending');
    dom.removeClass(headerLink, 'ascending');
    if (this.sortIndicators[col]) {
      if (col === this.hot.sortColumn) {
        if (this.sortOrderClass === 'ascending') {
          dom.addClass(headerLink, 'ascending');
        } else if (this.sortOrderClass === 'descending') {
          dom.addClass(headerLink, 'descending');
        }
      }
    }
  },
  isSorted: function() {
    return typeof this.hot.sortColumn != 'undefined';
  },
  afterCreateRow: function(index, amount) {
    if (!this.isSorted()) {
      return;
    }
    for (var i = 0; i < this.hot.sortIndex.length; i++) {
      if (this.hot.sortIndex[i][0] >= index) {
        this.hot.sortIndex[i][0] += amount;
      }
    }
    for (var i = 0; i < amount; i++) {
      this.hot.sortIndex.splice(index + i, 0, [index + i, this.hot.getData()[index + i][this.hot.sortColumn + this.hot.colOffset()]]);
    }
    this.saveSortingState();
  },
  afterRemoveRow: function(index, amount) {
    if (!this.isSorted()) {
      return;
    }
    var physicalRemovedIndex = this.translateRow(index);
    this.hot.sortIndex.splice(index, amount);
    for (var i = 0; i < this.hot.sortIndex.length; i++) {
      if (this.hot.sortIndex[i][0] > physicalRemovedIndex) {
        this.hot.sortIndex[i][0] -= amount;
      }
    }
    this.saveSortingState();
  }
}, {}, BasePlugin);
var $__default = ColumnSorting;
registerPlugin('columnSorting', ColumnSorting);


//# 
},{"./../../dom.js":27,"./../../eventManager.js":41,"./../../plugins.js":45,"./../_base.js":46}],50:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  CommentEditor: {get: function() {
      return CommentEditor;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_dom_46_js__;
var dom = ($___46__46__47__46__46__47_dom_46_js__ = require("./../../dom.js"), $___46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47_dom_46_js__});
var CommentEditor = function CommentEditor() {
  this.editor = this.createEditor();
  this.editorStyle = this.editor.style;
  this.editorStyle.position = 'absolute';
  this.editorStyle.zIndex = 100;
  this.hide();
};
var $CommentEditor = CommentEditor;
($traceurRuntime.createClass)(CommentEditor, {
  setPosition: function(x, y) {
    this.editorStyle.left = x + 'px';
    this.editorStyle.top = y + 'px';
  },
  show: function() {
    this.editorStyle.display = 'block';
  },
  hide: function() {
    this.editorStyle.display = 'none';
  },
  isVisible: function() {
    return this.editorStyle.display === 'block';
  },
  setValue: function() {
    var value = arguments[0] !== (void 0) ? arguments[0] : '';
    value = value || '';
    this.getInputElement().value = value;
  },
  getValue: function() {
    return this.getInputElement().value;
  },
  isFocused: function() {
    return document.activeElement === this.getInputElement();
  },
  focus: function() {
    this.getInputElement().focus();
  },
  createEditor: function() {
    var container = document.querySelector('.' + $CommentEditor.CLASS_EDITOR_CONTAINER);
    var editor;
    var textArea;
    if (!container) {
      container = document.createElement('div');
      dom.addClass(container, $CommentEditor.CLASS_EDITOR_CONTAINER);
      document.body.appendChild(container);
    }
    editor = document.createElement('div');
    dom.addClass(editor, $CommentEditor.CLASS_EDITOR);
    textArea = document.createElement('textarea');
    dom.addClass(textArea, $CommentEditor.CLASS_INPUT);
    editor.appendChild(textArea);
    container.appendChild(editor);
    return editor;
  },
  getInputElement: function() {
    return this.editor.querySelector('.' + $CommentEditor.CLASS_INPUT);
  },
  destroy: function() {
    this.editor.parentNode.removeChild(this.editor);
    this.editor = null;
    this.editorStyle = null;
  }
}, {
  get CLASS_EDITOR_CONTAINER() {
    return 'htCommentsContainer';
  },
  get CLASS_EDITOR() {
    return 'htComments';
  },
  get CLASS_INPUT() {
    return 'htCommentTextArea';
  },
  get CLASS_CELL() {
    return 'htCommentCell';
  }
});
;


//# 
},{"./../../dom.js":27}],51:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  Comments: {get: function() {
      return Comments;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47_eventManager_46_js__,
    $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__,
    $___46__46__47__46__46__47_plugins_46_js__,
    $___46__46__47__95_base_46_js__,
    $__commentEditor_46_js__;
var dom = ($___46__46__47__46__46__47_dom_46_js__ = require("./../../dom.js"), $___46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47_dom_46_js__});
var EventManager = ($___46__46__47__46__46__47_eventManager_46_js__ = require("./../../eventManager.js"), $___46__46__47__46__46__47_eventManager_46_js__ && $___46__46__47__46__46__47_eventManager_46_js__.__esModule && $___46__46__47__46__46__47_eventManager_46_js__ || {default: $___46__46__47__46__46__47_eventManager_46_js__}).EventManager;
var WalkontableCellCoords = ($___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ = require("./../../3rdparty/walkontable/src/cell/coords.js"), $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__.__esModule && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ || {default: $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__}).WalkontableCellCoords;
var $__2 = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}),
    registerPlugin = $__2.registerPlugin,
    getPlugin = $__2.getPlugin;
var BasePlugin = ($___46__46__47__95_base_46_js__ = require("./../_base.js"), $___46__46__47__95_base_46_js__ && $___46__46__47__95_base_46_js__.__esModule && $___46__46__47__95_base_46_js__ || {default: $___46__46__47__95_base_46_js__}).default;
var CommentEditor = ($__commentEditor_46_js__ = require("./commentEditor.js"), $__commentEditor_46_js__ && $__commentEditor_46_js__.__esModule && $__commentEditor_46_js__ || {default: $__commentEditor_46_js__}).CommentEditor;
var Comments = function Comments(hotInstance) {
  var $__5 = this;
  $traceurRuntime.superConstructor($Comments).call(this, hotInstance);
  if (!this.hot.getSettings().comments) {
    return;
  }
  this.editor = new CommentEditor();
  this.eventManager = new EventManager(this);
  this.range = {};
  this.mouseDown = false;
  this.contextMenuEvent = false;
  this.timer = null;
  this.hot.addHook('afterInit', (function() {
    return $__5.registerListeners();
  }));
  this.hot.addHook('afterContextMenuDefaultOptions', (function(options) {
    return $__5.addToContextMenu(options);
  }));
  this.hot.addHook('afterRenderer', (function(TD, row, col, prop, value, cellProperties) {
    return $__5.onAfterRenderer(TD, cellProperties);
  }));
  this.hot.addHook('afterScrollVertically', (function() {
    return $__5.refreshEditorPosition();
  }));
  this.hot.addHook('afterColumnResize', (function() {
    return $__5.refreshEditorPosition();
  }));
  this.hot.addHook('afterRowResize', (function() {
    return $__5.refreshEditorPosition();
  }));
};
var $Comments = Comments;
($traceurRuntime.createClass)(Comments, {
  registerListeners: function() {
    var $__5 = this;
    this.eventManager.addEventListener(document, 'mouseover', (function(event) {
      return $__5.onMouseOver(event);
    }));
    this.eventManager.addEventListener(document, 'mousedown', (function(event) {
      return $__5.onMouseDown(event);
    }));
    this.eventManager.addEventListener(document, 'mousemove', (function(event) {
      return $__5.onMouseMove(event);
    }));
    this.eventManager.addEventListener(document, 'mouseup', (function(event) {
      return $__5.onMouseUp(event);
    }));
    this.eventManager.addEventListener(this.editor.getInputElement(), 'blur', (function(event) {
      return $__5.onEditorBlur(event);
    }));
  },
  setRange: function(range) {
    this.range = range;
  },
  clearRange: function() {
    this.range = {};
  },
  targetIsCellWithComment: function(event) {
    return dom.hasClass(event.target, 'htCommentCell') && dom.closest(event.target, [this.hot.rootElement]) ? true : false;
  },
  targetIsCommentTextArea: function(event) {
    return this.editor.getInputElement() === event.target;
  },
  saveComment: function() {
    if (!this.range.from) {
      throw new Error('Before using this method, first set cell range (hot.getPlugin("comment").setRange())');
    }
    var comment = this.editor.getValue();
    var row = this.range.from.row;
    var col = this.range.from.col;
    this.hot.setCellMeta(row, col, 'comment', comment);
    this.hot.render();
  },
  saveCommentAtCell: function(row, col) {
    this.setRange({from: new WalkontableCellCoords(row, col)});
    this.saveComment();
  },
  removeComment: function() {
    if (!this.range.from) {
      throw new Error('Before using this method, first set cell range (hot.getPlugin("comment").setRange())');
    }
    this.hot.removeCellMeta(this.range.from.row, this.range.from.col, 'comment');
    this.hot.render();
    this.hide();
  },
  removeCommentAtCell: function(row, col) {
    this.setRange({from: new WalkontableCellCoords(row, col)});
    this.removeComment();
  },
  show: function() {
    if (!this.range.from) {
      throw new Error('Before using this method, first set cell range (hot.getPlugin("comment").setRange())');
    }
    var meta = this.hot.getCellMeta(this.range.from.row, this.range.from.col);
    this.refreshEditorPosition(true);
    this.editor.setValue(meta.comment || '');
    this.editor.show();
    return true;
  },
  showAtCell: function(row, col) {
    this.setRange({from: new WalkontableCellCoords(row, col)});
    return this.show();
  },
  hide: function() {
    this.editor.hide();
  },
  refreshEditorPosition: function() {
    var force = arguments[0] !== (void 0) ? arguments[0] : false;
    if (!force && (!this.range.from || !this.editor.isVisible())) {
      return;
    }
    var TD = this.hot.view.wt.wtTable.getCell(this.range.from);
    var offset = dom.offset(TD);
    var lastColWidth = this.hot.getColWidth(this.range.from.col);
    var cellTopOffset = offset.top;
    var cellLeftOffset = offset.left;
    var verticalCompensation = 0;
    var horizontalCompensation = 0;
    if (this.hot.view.wt.wtViewport.hasVerticalScroll()) {
      cellTopOffset = cellTopOffset - this.hot.view.wt.wtOverlays.topOverlay.getScrollPosition();
      verticalCompensation = 20;
    }
    if (this.hot.view.wt.wtViewport.hasHorizontalScroll()) {
      cellLeftOffset = cellLeftOffset - this.hot.view.wt.wtOverlays.leftOverlay.getScrollPosition();
      horizontalCompensation = 20;
    }
    var x = cellLeftOffset + lastColWidth;
    var y = cellTopOffset;
    var rect = this.hot.view.wt.wtTable.holder.getBoundingClientRect();
    var holderPos = {
      left: rect.left + dom.getWindowScrollLeft() + horizontalCompensation,
      right: rect.right + dom.getWindowScrollLeft() - 15,
      top: rect.top + dom.getWindowScrollTop() + verticalCompensation,
      bottom: rect.bottom + dom.getWindowScrollTop()
    };
    if (x <= holderPos.left || x > holderPos.right || y <= holderPos.top || y > holderPos.bottom) {
      this.hide();
    } else {
      this.editor.setPosition(x, y);
    }
  },
  onMouseDown: function(event) {
    this.mouseDown = true;
    if (!this.hot.view || !this.hot.view.wt) {
      return;
    }
    if (!this.contextMenuEvent && !this.targetIsCommentTextArea(event) && !this.targetIsCellWithComment(event)) {
      this.hide();
    }
    this.contextMenuEvent = false;
  },
  onMouseOver: function(event) {
    if (this.mouseDown || this.editor.isFocused()) {
      return;
    }
    if (this.targetIsCellWithComment(event)) {
      var coordinates = this.hot.view.wt.wtTable.getCoords(event.target);
      var range = {from: new WalkontableCellCoords(coordinates.row, coordinates.col)};
      this.setRange(range);
      this.show();
    } else if (!this.targetIsCommentTextArea(event) && !this.editor.isFocused()) {
      this.hide();
    }
  },
  onMouseMove: function(event) {
    var $__5 = this;
    if (this.targetIsCommentTextArea(event)) {
      this.mouseDown = true;
      clearTimeout(this.timer);
      this.timer = setTimeout((function() {
        $__5.mouseDown = false;
      }), 200);
    }
  },
  onMouseUp: function(event) {
    this.mouseDown = false;
  },
  onAfterRenderer: function(TD, cellProperties) {
    if (cellProperties.comment) {
      dom.addClass(TD, cellProperties.commentedCellClassName);
    }
  },
  onEditorBlur: function(event) {
    this.saveComment();
  },
  checkSelectionCommentsConsistency: function() {
    var hasComment = false;
    var cell = this.hot.getSelectedRange().from;
    if (this.hot.getCellMeta(cell.row, cell.col).comment) {
      hasComment = true;
    }
    return hasComment;
  },
  onContextMenuAddComment: function() {
    var $__5 = this;
    var coords = this.hot.getSelectedRange();
    this.contextMenuEvent = true;
    this.setRange({from: coords.from});
    this.show();
    setTimeout((function() {
      if ($__5.hot) {
        $__5.hot.deselectCell();
        $__5.editor.focus();
      }
    }), 10);
  },
  onContextMenuRemoveComment: function(key, selection) {
    this.contextMenuEvent = true;
    this.removeCommentAtCell(selection.start.row, selection.start.col);
  },
  addToContextMenu: function(defaultOptions) {
    var $__5 = this;
    defaultOptions.items.push(Handsontable.ContextMenu.SEPARATOR, {
      key: 'commentsAddEdit',
      name: (function() {
        return $__5.checkSelectionCommentsConsistency() ? 'Edit Comment' : 'Add Comment';
      }),
      callback: (function() {
        return $__5.onContextMenuAddComment();
      }),
      disabled: function() {
        return false;
      }
    }, {
      key: 'commentsRemove',
      name: function() {
        return 'Delete Comment';
      },
      callback: (function(key, selection) {
        return $__5.onContextMenuRemoveComment(key, selection);
      }),
      disabled: (function() {
        return !$__5.checkSelectionCommentsConsistency();
      })
    });
  },
  destroy: function() {
    if (this.eventManager) {
      this.eventManager.clear();
    }
    if (this.editor) {
      this.editor.destroy();
    }
    $traceurRuntime.superGet(this, $Comments.prototype, "destroy").call(this);
  }
}, {}, BasePlugin);
;
registerPlugin('comments', Comments);


//# 
},{"./../../3rdparty/walkontable/src/cell/coords.js":5,"./../../dom.js":27,"./../../eventManager.js":41,"./../../plugins.js":45,"./../_base.js":46,"./commentEditor.js":50}],52:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  ContextMenu: {get: function() {
      return ContextMenu;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_helpers_46_js__,
    $___46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47_eventManager_46_js__,
    $___46__46__47__46__46__47_plugins_46_js__;
var helper = ($___46__46__47__46__46__47_helpers_46_js__ = require("./../../helpers.js"), $___46__46__47__46__46__47_helpers_46_js__ && $___46__46__47__46__46__47_helpers_46_js__.__esModule && $___46__46__47__46__46__47_helpers_46_js__ || {default: $___46__46__47__46__46__47_helpers_46_js__});
var dom = ($___46__46__47__46__46__47_dom_46_js__ = require("./../../dom.js"), $___46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47_dom_46_js__});
var eventManagerObject = ($___46__46__47__46__46__47_eventManager_46_js__ = require("./../../eventManager.js"), $___46__46__47__46__46__47_eventManager_46_js__ && $___46__46__47__46__46__47_eventManager_46_js__.__esModule && $___46__46__47__46__46__47_eventManager_46_js__ || {default: $___46__46__47__46__46__47_eventManager_46_js__}).eventManager;
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
;
function ContextMenu(instance, customOptions) {
  this.instance = instance;
  var contextMenu = this;
  contextMenu.menus = [];
  contextMenu.htMenus = {};
  contextMenu.triggerRows = [];
  contextMenu.eventManager = eventManagerObject(contextMenu);
  this.enabled = true;
  this.instance.addHook('afterDestroy', function() {
    contextMenu.destroy();
  });
  this.defaultOptions = {items: [{
      key: 'row_above',
      name: 'Insert row above',
      callback: function(key, selection) {
        this.alter("insert_row", selection.start.row);
      },
      disabled: function() {
        var selected = this.getSelected(),
            entireColumnSelection = [0, selected[1], this.countRows() - 1, selected[1]],
            columnSelected = entireColumnSelection.join(',') == selected.join(',');
        return selected[0] < 0 || this.countRows() >= this.getSettings().maxRows || columnSelected;
      }
    }, {
      key: 'row_below',
      name: 'Insert row below',
      callback: function(key, selection) {
        this.alter("insert_row", selection.end.row + 1);
      },
      disabled: function() {
        var selected = this.getSelected(),
            entireColumnSelection = [0, selected[1], this.countRows() - 1, selected[1]],
            columnSelected = entireColumnSelection.join(',') == selected.join(',');
        return this.getSelected()[0] < 0 || this.countRows() >= this.getSettings().maxRows || columnSelected;
      }
    }, ContextMenu.SEPARATOR, {
      key: 'col_left',
      name: 'Insert column on the left',
      callback: function(key, selection) {
        this.alter("insert_col", selection.start.col);
      },
      disabled: function() {
        if (!this.isColumnModificationAllowed()) {
          return true;
        }
        var selected = this.getSelected(),
            entireRowSelection = [selected[0], 0, selected[0], this.countCols() - 1],
            rowSelected = entireRowSelection.join(',') == selected.join(',');
        return this.getSelected()[1] < 0 || this.countCols() >= this.getSettings().maxCols || rowSelected;
      }
    }, {
      key: 'col_right',
      name: 'Insert column on the right',
      callback: function(key, selection) {
        this.alter("insert_col", selection.end.col + 1);
      },
      disabled: function() {
        if (!this.isColumnModificationAllowed()) {
          return true;
        }
        var selected = this.getSelected(),
            entireRowSelection = [selected[0], 0, selected[0], this.countCols() - 1],
            rowSelected = entireRowSelection.join(',') == selected.join(',');
        return selected[1] < 0 || this.countCols() >= this.getSettings().maxCols || rowSelected;
      }
    }, ContextMenu.SEPARATOR, {
      key: 'remove_row',
      name: 'Remove row',
      callback: function(key, selection) {
        var amount = selection.end.row - selection.start.row + 1;
        this.alter("remove_row", selection.start.row, amount);
      },
      disabled: function() {
        var selected = this.getSelected(),
            entireColumnSelection = [0, selected[1], this.countRows() - 1, selected[1]],
            columnSelected = entireColumnSelection.join(',') == selected.join(',');
        return (selected[0] < 0 || columnSelected);
      }
    }, {
      key: 'remove_col',
      name: 'Remove column',
      callback: function(key, selection) {
        var amount = selection.end.col - selection.start.col + 1;
        this.alter("remove_col", selection.start.col, amount);
      },
      disabled: function() {
        if (!this.isColumnModificationAllowed()) {
          return true;
        }
        var selected = this.getSelected(),
            entireRowSelection = [selected[0], 0, selected[0], this.countCols() - 1],
            rowSelected = entireRowSelection.join(',') == selected.join(',');
        return (selected[1] < 0 || rowSelected);
      }
    }, ContextMenu.SEPARATOR, {
      key: 'undo',
      name: 'Undo',
      callback: function() {
        this.undo();
      },
      disabled: function() {
        return this.undoRedo && !this.undoRedo.isUndoAvailable();
      }
    }, {
      key: 'redo',
      name: 'Redo',
      callback: function() {
        this.redo();
      },
      disabled: function() {
        return this.undoRedo && !this.undoRedo.isRedoAvailable();
      }
    }, ContextMenu.SEPARATOR, {
      key: 'make_read_only',
      name: function() {
        var label = "Read only";
        var atLeastOneReadOnly = contextMenu.checkSelectionReadOnlyConsistency(this);
        if (atLeastOneReadOnly) {
          label = contextMenu.markSelected(label);
        }
        return label;
      },
      callback: function() {
        var atLeastOneReadOnly = contextMenu.checkSelectionReadOnlyConsistency(this);
        var that = this;
        this.getSelectedRange().forAll(function(r, c) {
          that.getCellMeta(r, c).readOnly = atLeastOneReadOnly ? false : true;
        });
        this.render();
      }
    }, ContextMenu.SEPARATOR, {
      key: 'alignment',
      name: 'Alignment',
      submenu: {items: [{
          name: function() {
            var label = "Left";
            var hasClass = contextMenu.checkSelectionAlignment(this, 'htLeft');
            if (hasClass) {
              label = contextMenu.markSelected(label);
            }
            return label;
          },
          callback: function() {
            align.call(this, this.getSelectedRange(), 'horizontal', 'htLeft');
          },
          disabled: false
        }, {
          name: function() {
            var label = "Center";
            var hasClass = contextMenu.checkSelectionAlignment(this, 'htCenter');
            if (hasClass) {
              label = contextMenu.markSelected(label);
            }
            return label;
          },
          callback: function() {
            align.call(this, this.getSelectedRange(), 'horizontal', 'htCenter');
          },
          disabled: false
        }, {
          name: function() {
            var label = "Right";
            var hasClass = contextMenu.checkSelectionAlignment(this, 'htRight');
            if (hasClass) {
              label = contextMenu.markSelected(label);
            }
            return label;
          },
          callback: function() {
            align.call(this, this.getSelectedRange(), 'horizontal', 'htRight');
          },
          disabled: false
        }, {
          name: function() {
            var label = "Justify";
            var hasClass = contextMenu.checkSelectionAlignment(this, 'htJustify');
            if (hasClass) {
              label = contextMenu.markSelected(label);
            }
            return label;
          },
          callback: function() {
            align.call(this, this.getSelectedRange(), 'horizontal', 'htJustify');
          },
          disabled: false
        }, ContextMenu.SEPARATOR, {
          name: function() {
            var label = "Top";
            var hasClass = contextMenu.checkSelectionAlignment(this, 'htTop');
            if (hasClass) {
              label = contextMenu.markSelected(label);
            }
            return label;
          },
          callback: function() {
            align.call(this, this.getSelectedRange(), 'vertical', 'htTop');
          },
          disabled: false
        }, {
          name: function() {
            var label = "Middle";
            var hasClass = contextMenu.checkSelectionAlignment(this, 'htMiddle');
            if (hasClass) {
              label = contextMenu.markSelected(label);
            }
            return label;
          },
          callback: function() {
            align.call(this, this.getSelectedRange(), 'vertical', 'htMiddle');
          },
          disabled: false
        }, {
          name: function() {
            var label = "Bottom";
            var hasClass = contextMenu.checkSelectionAlignment(this, 'htBottom');
            if (hasClass) {
              label = contextMenu.markSelected(label);
            }
            return label;
          },
          callback: function() {
            align.call(this, this.getSelectedRange(), 'vertical', 'htBottom');
          },
          disabled: false
        }]}
    }]};
  contextMenu.options = {};
  helper.extend(contextMenu.options, this.options);
  this.bindMouseEvents();
  this.markSelected = function(label) {
    return "<span class='selected'>" + String.fromCharCode(10003) + "</span>" + label;
  };
  this.checkSelectionAlignment = function(hot, className) {
    var hasAlignment = false;
    hot.getSelectedRange().forAll(function(r, c) {
      var metaClassName = hot.getCellMeta(r, c).className;
      if (metaClassName && metaClassName.indexOf(className) != -1) {
        hasAlignment = true;
        return false;
      }
    });
    return hasAlignment;
  };
  if (!this.instance.getSettings().allowInsertRow) {
    var rowAboveIndex = findIndexByKey(this.defaultOptions.items, 'row_above');
    this.defaultOptions.items.splice(rowAboveIndex, 1);
    var rowBelowIndex = findIndexByKey(this.defaultOptions.items, 'row_above');
    this.defaultOptions.items.splice(rowBelowIndex, 1);
    this.defaultOptions.items.splice(rowBelowIndex, 1);
  }
  if (!this.instance.getSettings().allowInsertColumn) {
    var colLeftIndex = findIndexByKey(this.defaultOptions.items, 'col_left');
    this.defaultOptions.items.splice(colLeftIndex, 1);
    var colRightIndex = findIndexByKey(this.defaultOptions.items, 'col_right');
    this.defaultOptions.items.splice(colRightIndex, 1);
    this.defaultOptions.items.splice(colRightIndex, 1);
  }
  var removeRow = false;
  var removeCol = false;
  var removeRowIndex,
      removeColumnIndex;
  if (!this.instance.getSettings().allowRemoveRow) {
    removeRowIndex = findIndexByKey(this.defaultOptions.items, 'remove_row');
    this.defaultOptions.items.splice(removeRowIndex, 1);
    removeRow = true;
  }
  if (!this.instance.getSettings().allowRemoveColumn) {
    removeColumnIndex = findIndexByKey(this.defaultOptions.items, 'remove_col');
    this.defaultOptions.items.splice(removeColumnIndex, 1);
    removeCol = true;
  }
  if (removeRow && removeCol) {
    this.defaultOptions.items.splice(removeColumnIndex, 1);
  }
  this.checkSelectionReadOnlyConsistency = function(hot) {
    var atLeastOneReadOnly = false;
    hot.getSelectedRange().forAll(function(r, c) {
      if (hot.getCellMeta(r, c).readOnly) {
        atLeastOneReadOnly = true;
        return false;
      }
    });
    return atLeastOneReadOnly;
  };
  Handsontable.hooks.run(instance, 'afterContextMenuDefaultOptions', this.defaultOptions);
}
ContextMenu.prototype.createMenu = function(menuName, row) {
  if (menuName) {
    menuName = menuName.replace(/ /g, '_');
    menuName = 'htContextSubMenu_' + menuName;
  }
  var menu;
  if (menuName) {
    menu = document.querySelector('.htContextMenu.' + menuName);
  } else {
    menu = document.querySelector('.htContextMenu');
  }
  if (!menu) {
    menu = document.createElement('DIV');
    dom.addClass(menu, 'htContextMenu');
    if (menuName) {
      dom.addClass(menu, menuName);
    }
    document.getElementsByTagName('body')[0].appendChild(menu);
  }
  if (this.menus.indexOf(menu) < 0) {
    this.menus.push(menu);
    row = row || 0;
    this.triggerRows.push(row);
  }
  return menu;
};
ContextMenu.prototype.bindMouseEvents = function() {
  function contextMenuOpenListener(event) {
    var settings = this.instance.getSettings(),
        showRowHeaders = this.instance.getSettings().rowHeaders,
        showColHeaders = this.instance.getSettings().colHeaders,
        containsCornerHeader,
        element,
        items,
        menu;
    function isValidElement(element) {
      return element.nodeName === 'TD' || element.parentNode.nodeName === 'TD';
    }
    element = event.realTarget;
    this.closeAll();
    event.preventDefault();
    helper.stopPropagation(event);
    if (!(showRowHeaders || showColHeaders)) {
      if (!isValidElement(element) && !(dom.hasClass(element, 'current') && dom.hasClass(element, 'wtBorder'))) {
        return;
      }
    } else if (showRowHeaders && showColHeaders) {
      containsCornerHeader = element.parentNode.querySelectorAll('.cornerHeader').length > 0;
      if (containsCornerHeader) {
        return;
      }
    }
    menu = this.createMenu();
    items = this.getItems(settings.contextMenu);
    this.show(menu, items);
    this.setMenuPosition(event, menu);
    this.eventManager.addEventListener(document.documentElement, 'mousedown', helper.proxy(ContextMenu.prototype.closeAll, this));
  }
  var eventManager = eventManagerObject(this.instance);
  eventManager.addEventListener(this.instance.rootElement, 'contextmenu', helper.proxy(contextMenuOpenListener, this));
};
ContextMenu.prototype.bindTableEvents = function() {
  this._afterScrollCallback = function() {};
  this.instance.addHook('afterScrollVertically', this._afterScrollCallback);
  this.instance.addHook('afterScrollHorizontally', this._afterScrollCallback);
};
ContextMenu.prototype.unbindTableEvents = function() {
  if (this._afterScrollCallback) {
    this.instance.removeHook('afterScrollVertically', this._afterScrollCallback);
    this.instance.removeHook('afterScrollHorizontally', this._afterScrollCallback);
    this._afterScrollCallback = null;
  }
};
ContextMenu.prototype.performAction = function(event, hot) {
  var contextMenu = this;
  var selectedItemIndex = hot.getSelected()[0];
  var selectedItem = hot.getData()[selectedItemIndex];
  if (selectedItem.disabled === true || (typeof selectedItem.disabled == 'function' && selectedItem.disabled.call(this.instance) === true)) {
    return;
  }
  if (!selectedItem.hasOwnProperty('submenu')) {
    if (typeof selectedItem.callback != 'function') {
      return;
    }
    var selRange = this.instance.getSelectedRange();
    var normalizedSelection = ContextMenu.utils.normalizeSelection(selRange);
    selectedItem.callback.call(this.instance, selectedItem.key, normalizedSelection, event);
    contextMenu.closeAll();
  }
};
ContextMenu.prototype.unbindMouseEvents = function() {
  this.eventManager.clear();
  var eventManager = eventManagerObject(this.instance);
  eventManager.removeEventListener(this.instance.rootElement, 'contextmenu');
};
ContextMenu.prototype.show = function(menu, items) {
  var that = this;
  menu.removeAttribute('style');
  menu.style.display = 'block';
  var settings = {
    data: items,
    colHeaders: false,
    colWidths: [200],
    readOnly: true,
    copyPaste: false,
    columns: [{
      data: 'name',
      renderer: helper.proxy(this.renderer, this)
    }],
    renderAllRows: true,
    beforeKeyDown: function(event) {
      that.onBeforeKeyDown(event, htContextMenu);
    },
    afterOnCellMouseOver: function(event, coords, TD) {
      that.onCellMouseOver(event, coords, TD, htContextMenu);
    }
  };
  var htContextMenu = new Handsontable(menu, settings);
  htContextMenu.isHotTableEnv = this.instance.isHotTableEnv;
  Handsontable.eventManager.isHotTableEnv = this.instance.isHotTableEnv;
  this.eventManager.removeEventListener(menu, 'mousedown');
  this.eventManager.addEventListener(menu, 'mousedown', function(event) {
    that.performAction(event, htContextMenu);
  });
  this.bindTableEvents();
  htContextMenu.listen();
  this.htMenus[htContextMenu.guid] = htContextMenu;
  Handsontable.hooks.run(this.instance, 'afterContextMenuShow', htContextMenu);
};
ContextMenu.prototype.close = function(menu) {
  this.hide(menu);
  this.eventManager.clear();
  this.unbindTableEvents();
  this.instance.listen();
};
ContextMenu.prototype.closeAll = function() {
  while (this.menus.length > 0) {
    var menu = this.menus.pop();
    if (menu) {
      this.close(menu);
    }
  }
  this.triggerRows = [];
};
ContextMenu.prototype.closeLastOpenedSubMenu = function() {
  var menu = this.menus.pop();
  if (menu) {
    this.hide(menu);
  }
};
ContextMenu.prototype.hide = function(menu) {
  menu.style.display = 'none';
  var instance = this.htMenus[menu.id];
  Handsontable.hooks.run(this.instance, 'afterContextMenuHide', instance);
  instance.destroy();
  delete this.htMenus[menu.id];
};
ContextMenu.prototype.renderer = function(instance, TD, row, col, prop, value) {
  var contextMenu = this;
  var item = instance.getData()[row];
  var wrapper = document.createElement('DIV');
  if (typeof value === 'function') {
    value = value.call(this.instance);
  }
  dom.empty(TD);
  TD.appendChild(wrapper);
  if (itemIsSeparator(item)) {
    dom.addClass(TD, 'htSeparator');
  } else {
    dom.fastInnerHTML(wrapper, value);
  }
  if (itemIsDisabled(item)) {
    dom.addClass(TD, 'htDisabled');
    this.eventManager.addEventListener(wrapper, 'mouseenter', function() {
      instance.deselectCell();
    });
  } else {
    if (isSubMenu(item)) {
      dom.addClass(TD, 'htSubmenu');
      this.eventManager.addEventListener(wrapper, 'mouseenter', function() {
        instance.selectCell(row, col);
      });
    } else {
      dom.removeClass(TD, 'htSubmenu');
      dom.removeClass(TD, 'htDisabled');
      this.eventManager.addEventListener(wrapper, 'mouseenter', function() {
        instance.selectCell(row, col);
      });
    }
  }
  function isSubMenu(item) {
    return item.hasOwnProperty('submenu');
  }
  function itemIsSeparator(item) {
    return new RegExp(ContextMenu.SEPARATOR.name, 'i').test(item.name);
  }
  function itemIsDisabled(item) {
    return item.disabled === true || (typeof item.disabled == 'function' && item.disabled.call(contextMenu.instance) === true);
  }
};
ContextMenu.prototype.onCellMouseOver = function(event, coords, TD, hot) {
  var menusLength = this.menus.length;
  if (menusLength > 0) {
    var lastMenu = this.menus[menusLength - 1];
    if (lastMenu.id != hot.guid) {
      this.closeLastOpenedSubMenu();
    }
  } else {
    this.closeLastOpenedSubMenu();
  }
  if (TD.className.indexOf('htSubmenu') != -1) {
    var selectedItem = hot.getData()[coords.row];
    var items = this.getItems(selectedItem.submenu);
    var subMenu = this.createMenu(selectedItem.name, coords.row);
    var tdCoords = TD.getBoundingClientRect();
    this.show(subMenu, items);
    this.setSubMenuPosition(tdCoords, subMenu);
  }
};
ContextMenu.prototype.onBeforeKeyDown = function(event, instance) {
  dom.enableImmediatePropagation(event);
  var contextMenu = this;
  var selection = instance.getSelected();
  switch (event.keyCode) {
    case helper.keyCode.ESCAPE:
      contextMenu.closeAll();
      event.preventDefault();
      event.stopImmediatePropagation();
      break;
    case helper.keyCode.ENTER:
      if (selection) {
        contextMenu.performAction(event, instance);
      }
      break;
    case helper.keyCode.ARROW_DOWN:
      if (!selection) {
        selectFirstCell(instance, contextMenu);
      } else {
        selectNextCell(selection[0], selection[1], instance, contextMenu);
      }
      event.preventDefault();
      event.stopImmediatePropagation();
      break;
    case helper.keyCode.ARROW_UP:
      if (!selection) {
        selectLastCell(instance, contextMenu);
      } else {
        selectPrevCell(selection[0], selection[1], instance, contextMenu);
      }
      event.preventDefault();
      event.stopImmediatePropagation();
      break;
    case helper.keyCode.ARROW_RIGHT:
      if (selection) {
        var row = selection[0];
        var cell = instance.getCell(selection[0], 0);
        if (ContextMenu.utils.hasSubMenu(cell)) {
          openSubMenu(instance, contextMenu, cell, row);
        }
      }
      event.preventDefault();
      event.stopImmediatePropagation();
      break;
    case helper.keyCode.ARROW_LEFT:
      if (selection) {
        if (instance.rootElement.className.indexOf('htContextSubMenu_') != -1) {
          contextMenu.closeLastOpenedSubMenu();
          var index = contextMenu.menus.length;
          if (index > 0) {
            var menu = contextMenu.menus[index - 1];
            var triggerRow = contextMenu.triggerRows.pop();
            instance = this.htMenus[menu.id];
            instance.selectCell(triggerRow, 0);
          }
        }
        event.preventDefault();
        event.stopImmediatePropagation();
      }
      break;
  }
  function selectFirstCell(instance) {
    var firstCell = instance.getCell(0, 0);
    if (ContextMenu.utils.isSeparator(firstCell) || ContextMenu.utils.isDisabled(firstCell)) {
      selectNextCell(0, 0, instance);
    } else {
      instance.selectCell(0, 0);
    }
  }
  function selectLastCell(instance) {
    var lastRow = instance.countRows() - 1;
    var lastCell = instance.getCell(lastRow, 0);
    if (ContextMenu.utils.isSeparator(lastCell) || ContextMenu.utils.isDisabled(lastCell)) {
      selectPrevCell(lastRow, 0, instance);
    } else {
      instance.selectCell(lastRow, 0);
    }
  }
  function selectNextCell(row, col, instance) {
    var nextRow = row + 1;
    var nextCell = nextRow < instance.countRows() ? instance.getCell(nextRow, col) : null;
    if (!nextCell) {
      return;
    }
    if (ContextMenu.utils.isSeparator(nextCell) || ContextMenu.utils.isDisabled(nextCell)) {
      selectNextCell(nextRow, col, instance);
    } else {
      instance.selectCell(nextRow, col);
    }
  }
  function selectPrevCell(row, col, instance) {
    var prevRow = row - 1;
    var prevCell = prevRow >= 0 ? instance.getCell(prevRow, col) : null;
    if (!prevCell) {
      return;
    }
    if (ContextMenu.utils.isSeparator(prevCell) || ContextMenu.utils.isDisabled(prevCell)) {
      selectPrevCell(prevRow, col, instance);
    } else {
      instance.selectCell(prevRow, col);
    }
  }
  function openSubMenu(instance, contextMenu, cell, row) {
    var selectedItem = instance.getData()[row];
    var items = contextMenu.getItems(selectedItem.submenu);
    var subMenu = contextMenu.createMenu(selectedItem.name, row);
    var coords = cell.getBoundingClientRect();
    var subMenuInstance = contextMenu.show(subMenu, items);
    contextMenu.setSubMenuPosition(coords, subMenu);
    subMenuInstance.selectCell(0, 0);
  }
};
function findByKey(items, key) {
  for (var i = 0,
      ilen = items.length; i < ilen; i++) {
    if (items[i].key === key) {
      return items[i];
    }
  }
}
function findIndexByKey(items, key) {
  for (var i = 0,
      ilen = items.length; i < ilen; i++) {
    if (items[i].key === key) {
      return i;
    }
  }
}
ContextMenu.prototype.getItems = function(items) {
  var menu,
      item;
  function ContextMenuItem(rawItem) {
    if (typeof rawItem == 'string') {
      this.name = rawItem;
    } else {
      helper.extend(this, rawItem);
    }
  }
  ContextMenuItem.prototype = items;
  if (items && items.items) {
    items = items.items;
  }
  if (items === true) {
    items = this.defaultOptions.items;
  }
  if (1 == 1) {
    menu = [];
    for (var key in items) {
      if (items.hasOwnProperty(key)) {
        if (typeof items[key] === 'string') {
          item = findByKey(this.defaultOptions.items, items[key]);
        } else {
          item = findByKey(this.defaultOptions.items, key);
        }
        if (!item) {
          item = items[key];
        }
        item = new ContextMenuItem(item);
        if (typeof items[key] === 'object') {
          helper.extend(item, items[key]);
        }
        if (!item.key) {
          item.key = key;
        }
        menu.push(item);
      }
    }
  }
  return menu;
};
ContextMenu.prototype.setSubMenuPosition = function(coords, menu) {
  var scrollTop = dom.getWindowScrollTop();
  var scrollLeft = dom.getWindowScrollLeft();
  var cursor = {
    top: scrollTop + coords.top,
    topRelative: coords.top,
    left: coords.left,
    leftRelative: coords.left - scrollLeft,
    scrollTop: scrollTop,
    scrollLeft: scrollLeft,
    cellHeight: coords.height,
    cellWidth: coords.width
  };
  if (this.menuFitsBelowCursor(cursor, menu, document.body.clientWidth)) {
    this.positionMenuBelowCursor(cursor, menu, true);
  } else {
    if (this.menuFitsAboveCursor(cursor, menu)) {
      this.positionMenuAboveCursor(cursor, menu, true);
    } else {
      this.positionMenuBelowCursor(cursor, menu, true);
    }
  }
  if (this.menuFitsOnRightOfCursor(cursor, menu, document.body.clientWidth)) {
    this.positionMenuOnRightOfCursor(cursor, menu, true);
  } else {
    this.positionMenuOnLeftOfCursor(cursor, menu, true);
  }
};
ContextMenu.prototype.setMenuPosition = function(event, menu) {
  var scrollTop = dom.getWindowScrollTop();
  var scrollLeft = dom.getWindowScrollLeft();
  var cursorY = event.pageY || (event.clientY + scrollTop);
  var cursorX = event.pageX || (event.clientX + scrollLeft);
  var cursor = {
    top: cursorY,
    topRelative: cursorY - scrollTop,
    left: cursorX,
    leftRelative: cursorX - scrollLeft,
    scrollTop: scrollTop,
    scrollLeft: scrollLeft,
    cellHeight: event.target.clientHeight,
    cellWidth: event.target.clientWidth
  };
  if (this.menuFitsBelowCursor(cursor, menu, document.body.clientHeight)) {
    this.positionMenuBelowCursor(cursor, menu);
  } else {
    if (this.menuFitsAboveCursor(cursor, menu)) {
      this.positionMenuAboveCursor(cursor, menu);
    } else {
      this.positionMenuBelowCursor(cursor, menu);
    }
  }
  if (this.menuFitsOnRightOfCursor(cursor, menu, document.body.clientWidth)) {
    this.positionMenuOnRightOfCursor(cursor, menu);
  } else {
    this.positionMenuOnLeftOfCursor(cursor, menu);
  }
};
ContextMenu.prototype.menuFitsAboveCursor = function(cursor, menu) {
  return cursor.topRelative >= menu.offsetHeight;
};
ContextMenu.prototype.menuFitsBelowCursor = function(cursor, menu, viewportHeight) {
  return cursor.topRelative + menu.offsetHeight <= viewportHeight;
};
ContextMenu.prototype.menuFitsOnRightOfCursor = function(cursor, menu, viewportHeight) {
  return cursor.leftRelative + menu.offsetWidth <= viewportHeight;
};
ContextMenu.prototype.positionMenuBelowCursor = function(cursor, menu) {
  menu.style.top = cursor.top + 'px';
};
ContextMenu.prototype.positionMenuAboveCursor = function(cursor, menu, subMenu) {
  if (subMenu) {
    menu.style.top = (cursor.top + cursor.cellHeight - menu.offsetHeight) + 'px';
  } else {
    menu.style.top = (cursor.top - menu.offsetHeight) + 'px';
  }
};
ContextMenu.prototype.positionMenuOnRightOfCursor = function(cursor, menu, subMenu) {
  if (subMenu) {
    menu.style.left = 1 + cursor.left + cursor.cellWidth + 'px';
  } else {
    menu.style.left = 1 + cursor.left + 'px';
  }
};
ContextMenu.prototype.positionMenuOnLeftOfCursor = function(cursor, menu, subMenu) {
  if (subMenu) {
    menu.style.left = (cursor.left - menu.offsetWidth) + 'px';
  } else {
    menu.style.left = (cursor.left - menu.offsetWidth) + 'px';
  }
};
ContextMenu.utils = {};
ContextMenu.utils.normalizeSelection = function(selRange) {
  return {
    start: selRange.getTopLeftCorner(),
    end: selRange.getBottomRightCorner()
  };
};
ContextMenu.utils.isSeparator = function(cell) {
  return dom.hasClass(cell, 'htSeparator');
};
ContextMenu.utils.hasSubMenu = function(cell) {
  return dom.hasClass(cell, 'htSubmenu');
};
ContextMenu.utils.isDisabled = function(cell) {
  return dom.hasClass(cell, 'htDisabled');
};
ContextMenu.prototype.enable = function() {
  if (!this.enabled) {
    this.enabled = true;
    this.bindMouseEvents();
  }
};
ContextMenu.prototype.disable = function() {
  if (this.enabled) {
    this.enabled = false;
    this.closeAll();
    this.unbindMouseEvents();
    this.unbindTableEvents();
  }
};
ContextMenu.prototype.destroy = function() {
  this.closeAll();
  while (this.menus.length > 0) {
    var menu = this.menus.pop();
    this.triggerRows.pop();
    if (menu) {
      this.close(menu);
      if (!this.isMenuEnabledByOtherHotInstance()) {
        this.removeMenu(menu);
      }
    }
  }
  this.unbindMouseEvents();
  this.unbindTableEvents();
};
ContextMenu.prototype.isMenuEnabledByOtherHotInstance = function() {
  var hotContainers = document.querySelectorAll('.handsontable');
  var menuEnabled = false;
  for (var i = 0,
      len = hotContainers.length; i < len; i++) {
    var instance = this.htMenus[hotContainers[i].id];
    if (instance && instance.getSettings().contextMenu) {
      menuEnabled = true;
      break;
    }
  }
  return menuEnabled;
};
ContextMenu.prototype.removeMenu = function(menu) {
  if (menu.parentNode) {
    this.menu.parentNode.removeChild(menu);
  }
};
ContextMenu.prototype.align = function(range, type, alignment) {
  align.call(this, range, type, alignment);
};
ContextMenu.SEPARATOR = {name: "---------"};
function updateHeight() {
  if (this.rootElement.className.indexOf('htContextMenu')) {
    return;
  }
  var realSeparatorHeight = 0,
      realEntrySize = 0,
      dataSize = this.getSettings().data.length,
      currentHiderWidth = parseInt(this.view.wt.wtTable.hider.style.width, 10);
  for (var i = 0; i < dataSize; i++) {
    if (this.getSettings().data[i].name == ContextMenu.SEPARATOR.name) {
      realSeparatorHeight += 1;
    } else {
      realEntrySize += 26;
    }
  }
  this.view.wt.wtTable.holder.style.width = currentHiderWidth + 22 + "px";
  this.view.wt.wtTable.holder.style.height = realEntrySize + realSeparatorHeight + 4 + "px";
}
function prepareVerticalAlignClass(className, alignment) {
  if (className.indexOf(alignment) != -1) {
    return className;
  }
  className = className.replace('htTop', '').replace('htMiddle', '').replace('htBottom', '').replace('  ', '');
  className += " " + alignment;
  return className;
}
function prepareHorizontalAlignClass(className, alignment) {
  if (className.indexOf(alignment) != -1) {
    return className;
  }
  className = className.replace('htLeft', '').replace('htCenter', '').replace('htRight', '').replace('htJustify', '').replace('  ', '');
  className += " " + alignment;
  return className;
}
function getAlignmentClasses(range) {
  var classesArray = {};
  for (var row = range.from.row; row <= range.to.row; row++) {
    for (var col = range.from.col; col <= range.to.col; col++) {
      if (!classesArray[row]) {
        classesArray[row] = [];
      }
      classesArray[row][col] = this.getCellMeta(row, col).className;
    }
  }
  return classesArray;
}
function doAlign(row, col, type, alignment) {
  var cellMeta = this.getCellMeta(row, col),
      className = alignment;
  if (cellMeta.className) {
    if (type === 'vertical') {
      className = prepareVerticalAlignClass(cellMeta.className, alignment);
    } else {
      className = prepareHorizontalAlignClass(cellMeta.className, alignment);
    }
  }
  this.setCellMeta(row, col, 'className', className);
}
function align(range, type, alignment) {
  var stateBefore = getAlignmentClasses.call(this, range);
  this.runHooks('beforeCellAlignment', stateBefore, range, type, alignment);
  if (range.from.row == range.to.row && range.from.col == range.to.col) {
    doAlign.call(this, range.from.row, range.from.col, type, alignment);
  } else {
    for (var row = range.from.row; row <= range.to.row; row++) {
      for (var col = range.from.col; col <= range.to.col; col++) {
        doAlign.call(this, row, col, type, alignment);
      }
    }
  }
  this.render();
}
function init() {
  var instance = this;
  var contextMenuSetting = instance.getSettings().contextMenu;
  var customOptions = helper.isObject(contextMenuSetting) ? contextMenuSetting : {};
  if (contextMenuSetting) {
    if (!instance.contextMenu) {
      instance.contextMenu = new ContextMenu(instance, customOptions);
    }
    instance.contextMenu.enable();
  } else if (instance.contextMenu) {
    instance.contextMenu.destroy();
    delete instance.contextMenu;
  }
}
Handsontable.hooks.add('afterInit', init);
Handsontable.hooks.add('afterUpdateSettings', init);
Handsontable.hooks.add('afterInit', updateHeight);
Handsontable.hooks.register('afterContextMenuDefaultOptions');
Handsontable.hooks.register('afterContextMenuShow');
Handsontable.hooks.register('afterContextMenuHide');
Handsontable.ContextMenu = ContextMenu;


//# 
},{"./../../dom.js":27,"./../../eventManager.js":41,"./../../helpers.js":42,"./../../plugins.js":45}],53:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  ContextMenuCopyPaste: {get: function() {
      return ContextMenuCopyPaste;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47_eventManager_46_js__,
    $___46__46__47__46__46__47_plugins_46_js__,
    $___46__46__47__95_base_46_js__,
    $__zeroclipboard__;
var dom = ($___46__46__47__46__46__47_dom_46_js__ = require("./../../dom.js"), $___46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47_dom_46_js__});
var eventManagerObject = ($___46__46__47__46__46__47_eventManager_46_js__ = require("./../../eventManager.js"), $___46__46__47__46__46__47_eventManager_46_js__ && $___46__46__47__46__46__47_eventManager_46_js__.__esModule && $___46__46__47__46__46__47_eventManager_46_js__ || {default: $___46__46__47__46__46__47_eventManager_46_js__}).eventManager;
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
var BasePlugin = ($___46__46__47__95_base_46_js__ = require("./../_base.js"), $___46__46__47__95_base_46_js__ && $___46__46__47__95_base_46_js__.__esModule && $___46__46__47__95_base_46_js__ || {default: $___46__46__47__95_base_46_js__}).default;
var ZeroClipboard = ($__zeroclipboard__ = require("zeroclipboard"), $__zeroclipboard__ && $__zeroclipboard__.__esModule && $__zeroclipboard__ || {default: $__zeroclipboard__}).default;
var ContextMenuCopyPaste = function ContextMenuCopyPaste(hotInstance) {
  var $__4 = this;
  $traceurRuntime.superConstructor($ContextMenuCopyPaste).call(this, hotInstance);
  this.swfPath = null;
  this.hotContextMenu = null;
  this.outsideClickDeselectsCache = null;
  this.hot.addHook('afterContextMenuShow', (function(htContextMenu) {
    return $__4.setupZeroClipboard(htContextMenu);
  }));
  this.hot.addHook('afterInit', (function() {
    return $__4.afterInit();
  }));
  this.hot.addHook('afterContextMenuDefaultOptions', (function(options) {
    return $__4.addToContextMenu(options);
  }));
};
var $ContextMenuCopyPaste = ContextMenuCopyPaste;
($traceurRuntime.createClass)(ContextMenuCopyPaste, {
  afterInit: function() {
    if (!this.hot.getSettings().contextMenuCopyPaste) {
      return;
    } else if (typeof this.hot.getSettings().contextMenuCopyPaste == 'object') {
      this.swfPath = this.hot.getSettings().contextMenuCopyPaste.swfPath;
    }
    if (typeof ZeroClipboard === 'undefined') {
      throw new Error("To be able to use the Copy/Paste feature from the context menu, you need to manualy include ZeroClipboard.js file to your website.");
    }
    try {
      new ActiveXObject('ShockwaveFlash.ShockwaveFlash');
    } catch (exception) {
      if ('undefined' == typeof navigator.mimeTypes['application/x-shockwave-flash']) {
        throw new Error("To be able to use the Copy/Paste feature from the context menu, your browser needs to have Flash Plugin installed.");
      }
    }
    this.prepareZeroClipboard();
  },
  prepareZeroClipboard: function() {
    if (this.swfPath) {
      ZeroClipboard.config({swfPath: this.swfPath});
    }
  },
  getCopyValue: function() {
    this.hot.copyPaste.setCopyableText();
    return this.hot.copyPaste.copyPasteInstance.elTextarea.value;
  },
  addToContextMenu: function(defaultOptions) {
    if (!this.hot.getSettings().contextMenuCopyPaste) {
      return;
    }
    defaultOptions.items.unshift({
      key: 'copy',
      name: 'Copy'
    }, {
      key: 'paste',
      name: 'Paste',
      callback: function() {
        this.copyPaste.triggerPaste();
      }
    }, Handsontable.ContextMenu.SEPARATOR);
  },
  setupZeroClipboard: function(hotContextMenu) {
    var $__4 = this;
    var data,
        zeroClipboardInstance;
    if (!this.hot.getSettings().contextMenuCopyPaste) {
      return;
    }
    this.hotContextMenu = hotContextMenu;
    data = this.hotContextMenu.getData();
    for (var i = 0,
        ilen = data.length; i < ilen; i++) {
      if (data[i].key === 'copy') {
        zeroClipboardInstance = new ZeroClipboard(this.hotContextMenu.getCell(i, 0));
        zeroClipboardInstance.off();
        zeroClipboardInstance.on('copy', (function(event) {
          var clipboard = event.clipboardData;
          clipboard.setData('text/plain', $__4.getCopyValue());
          $__4.hot.getSettings().outsideClickDeselects = $__4.outsideClickDeselectsCache;
        }));
        this.bindEvents();
        break;
      }
    }
  },
  removeCurrentClass: function() {
    if (this.hotContextMenu.rootElement) {
      var element = this.hotContextMenu.rootElement.querySelector('td.current');
      if (element) {
        dom.removeClass(element, 'current');
      }
    }
    this.outsideClickDeselectsCache = this.hot.getSettings().outsideClickDeselects;
    this.hot.getSettings().outsideClickDeselects = false;
  },
  removeZeroClipboardClass: function() {
    if (this.hotContextMenu.rootElement) {
      var element = this.hotContextMenu.rootElement.querySelector('td.zeroclipboard-is-hover');
      if (element) {
        dom.removeClass(element, 'zeroclipboard-is-hover');
      }
    }
    this.hot.getSettings().outsideClickDeselects = this.outsideClickDeselectsCache;
  },
  bindEvents: function() {
    var $__4 = this;
    var eventManager = eventManagerObject(this.hotContextMenu);
    eventManager.addEventListener(document, 'mouseenter', (function() {
      return $__4.removeCurrentClass();
    }));
    eventManager.addEventListener(document, 'mouseleave', (function() {
      return $__4.removeZeroClipboardClass();
    }));
  }
}, {}, BasePlugin);
;
registerPlugin('contextMenuCopyPaste', ContextMenuCopyPaste);


//# 
},{"./../../dom.js":27,"./../../eventManager.js":41,"./../../plugins.js":45,"./../_base.js":46,"zeroclipboard":undefined}],54:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  CopyPaste: {get: function() {
      return CopyPaste;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_helpers_46_js__,
    $__copyPaste__,
    $__SheetClip__,
    $___46__46__47__46__46__47_plugins_46_js__,
    $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__,
    $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__;
var helper = ($___46__46__47__46__46__47_helpers_46_js__ = require("./../../helpers.js"), $___46__46__47__46__46__47_helpers_46_js__ && $___46__46__47__46__46__47_helpers_46_js__.__esModule && $___46__46__47__46__46__47_helpers_46_js__ || {default: $___46__46__47__46__46__47_helpers_46_js__});
var copyPaste = ($__copyPaste__ = require("copyPaste"), $__copyPaste__ && $__copyPaste__.__esModule && $__copyPaste__ || {default: $__copyPaste__}).default;
var SheetClip = ($__SheetClip__ = require("SheetClip"), $__SheetClip__ && $__SheetClip__.__esModule && $__SheetClip__ || {default: $__SheetClip__}).default;
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
var WalkontableCellCoords = ($___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ = require("./../../3rdparty/walkontable/src/cell/coords.js"), $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__.__esModule && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ || {default: $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__}).WalkontableCellCoords;
var WalkontableCellRange = ($___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__ = require("./../../3rdparty/walkontable/src/cell/range.js"), $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__ && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__.__esModule && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__ || {default: $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__}).WalkontableCellRange;
;
function CopyPastePlugin(instance) {
  var _this = this;
  this.copyPasteInstance = copyPaste();
  this.copyPasteInstance.onCut(onCut);
  this.copyPasteInstance.onPaste(onPaste);
  instance.addHook('beforeKeyDown', onBeforeKeyDown);
  function onCut() {
    if (!instance.isListening()) {
      return;
    }
    instance.selection.empty();
  }
  function onPaste(str) {
    var input,
        inputArray,
        selected,
        coordsFrom,
        coordsTo,
        cellRange,
        topLeftCorner,
        bottomRightCorner,
        areaStart,
        areaEnd;
    if (!instance.isListening() || !instance.selection.isSelected()) {
      return;
    }
    input = str;
    inputArray = SheetClip.parse(input);
    selected = instance.getSelected();
    coordsFrom = new WalkontableCellCoords(selected[0], selected[1]);
    coordsTo = new WalkontableCellCoords(selected[2], selected[3]);
    cellRange = new WalkontableCellRange(coordsFrom, coordsFrom, coordsTo);
    topLeftCorner = cellRange.getTopLeftCorner();
    bottomRightCorner = cellRange.getBottomRightCorner();
    areaStart = topLeftCorner;
    areaEnd = new WalkontableCellCoords(Math.max(bottomRightCorner.row, inputArray.length - 1 + topLeftCorner.row), Math.max(bottomRightCorner.col, inputArray[0].length - 1 + topLeftCorner.col));
    instance.addHookOnce('afterChange', function(changes, source) {
      if (changes && changes.length) {
        this.selectCell(areaStart.row, areaStart.col, areaEnd.row, areaEnd.col);
      }
    });
    instance.populateFromArray(areaStart.row, areaStart.col, inputArray, areaEnd.row, areaEnd.col, 'paste', instance.getSettings().pasteMode);
  }
  function onBeforeKeyDown(event) {
    var ctrlDown;
    if (instance.getSelected()) {
      if (helper.isCtrlKey(event.keyCode)) {
        _this.setCopyableText();
        event.stopImmediatePropagation();
        return;
      }
      ctrlDown = (event.ctrlKey || event.metaKey) && !event.altKey;
      if (event.keyCode == helper.keyCode.A && ctrlDown) {
        instance._registerTimeout(setTimeout(helper.proxy(_this.setCopyableText, _this), 0));
      }
    }
  }
  this.destroy = function() {
    this.copyPasteInstance.removeCallback(onCut);
    this.copyPasteInstance.removeCallback(onPaste);
    this.copyPasteInstance.destroy();
    instance.removeHook('beforeKeyDown', onBeforeKeyDown);
  };
  instance.addHook('afterDestroy', helper.proxy(this.destroy, this));
  this.triggerPaste = helper.proxy(this.copyPasteInstance.triggerPaste, this.copyPasteInstance);
  this.triggerCut = helper.proxy(this.copyPasteInstance.triggerCut, this.copyPasteInstance);
  this.setCopyableText = function() {
    var settings = instance.getSettings();
    var copyRowsLimit = settings.copyRowsLimit;
    var copyColsLimit = settings.copyColsLimit;
    var selRange = instance.getSelectedRange();
    var topLeft = selRange.getTopLeftCorner();
    var bottomRight = selRange.getBottomRightCorner();
    var startRow = topLeft.row;
    var startCol = topLeft.col;
    var endRow = bottomRight.row;
    var endCol = bottomRight.col;
    var finalEndRow = Math.min(endRow, startRow + copyRowsLimit - 1);
    var finalEndCol = Math.min(endCol, startCol + copyColsLimit - 1);
    instance.copyPaste.copyPasteInstance.copyable(instance.getCopyableData(startRow, startCol, finalEndRow, finalEndCol));
    if (endRow !== finalEndRow || endCol !== finalEndCol) {
      Handsontable.hooks.run(instance, "afterCopyLimit", endRow - startRow + 1, endCol - startCol + 1, copyRowsLimit, copyColsLimit);
    }
  };
}
function init() {
  var instance = this,
      pluginEnabled = instance.getSettings().copyPaste !== false;
  if (pluginEnabled && !instance.copyPaste) {
    instance.copyPaste = new CopyPastePlugin(instance);
  } else if (!pluginEnabled && instance.copyPaste) {
    instance.copyPaste.destroy();
    delete instance.copyPaste;
  }
}
Handsontable.hooks.add('afterInit', init);
Handsontable.hooks.add('afterUpdateSettings', init);
Handsontable.hooks.register('afterCopyLimit');


//# 
},{"./../../3rdparty/walkontable/src/cell/coords.js":5,"./../../3rdparty/walkontable/src/cell/range.js":6,"./../../helpers.js":42,"./../../plugins.js":45,"SheetClip":undefined,"copyPaste":undefined}],55:[function(require,module,exports){
"use strict";
var $___46__46__47__46__46__47_plugins_46_js__,
    $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__,
    $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_selection_46_js__;
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
var WalkontableCellRange = ($___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__ = require("./../../3rdparty/walkontable/src/cell/range.js"), $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__ && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__.__esModule && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__ || {default: $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__}).WalkontableCellRange;
var WalkontableSelection = ($___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_selection_46_js__ = require("./../../3rdparty/walkontable/src/selection.js"), $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_selection_46_js__ && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_selection_46_js__.__esModule && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_selection_46_js__ || {default: $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_selection_46_js__}).WalkontableSelection;
function CustomBorders() {}
var instance;
var checkEnable = function(customBorders) {
  if (typeof customBorders === "boolean") {
    if (customBorders === true) {
      return true;
    }
  }
  if (typeof customBorders === "object") {
    if (customBorders.length > 0) {
      return true;
    }
  }
  return false;
};
var init = function() {
  if (checkEnable(this.getSettings().customBorders)) {
    if (!this.customBorders) {
      instance = this;
      this.customBorders = new CustomBorders();
    }
  }
};
var getSettingIndex = function(className) {
  for (var i = 0; i < instance.view.wt.selections.length; i++) {
    if (instance.view.wt.selections[i].settings.className == className) {
      return i;
    }
  }
  return -1;
};
var insertBorderIntoSettings = function(border) {
  var coordinates = {
    row: border.row,
    col: border.col
  };
  var selection = new WalkontableSelection(border, new WalkontableCellRange(coordinates, coordinates, coordinates));
  var index = getSettingIndex(border.className);
  if (index >= 0) {
    instance.view.wt.selections[index] = selection;
  } else {
    instance.view.wt.selections.push(selection);
  }
};
var prepareBorderFromCustomAdded = function(row, col, borderObj) {
  var border = createEmptyBorders(row, col);
  border = extendDefaultBorder(border, borderObj);
  this.setCellMeta(row, col, 'borders', border);
  insertBorderIntoSettings(border);
};
var prepareBorderFromCustomAddedRange = function(rowObj) {
  var range = rowObj.range;
  for (var row = range.from.row; row <= range.to.row; row++) {
    for (var col = range.from.col; col <= range.to.col; col++) {
      var border = createEmptyBorders(row, col);
      var add = 0;
      if (row == range.from.row) {
        add++;
        if (rowObj.hasOwnProperty('top')) {
          border.top = rowObj.top;
        }
      }
      if (row == range.to.row) {
        add++;
        if (rowObj.hasOwnProperty('bottom')) {
          border.bottom = rowObj.bottom;
        }
      }
      if (col == range.from.col) {
        add++;
        if (rowObj.hasOwnProperty('left')) {
          border.left = rowObj.left;
        }
      }
      if (col == range.to.col) {
        add++;
        if (rowObj.hasOwnProperty('right')) {
          border.right = rowObj.right;
        }
      }
      if (add > 0) {
        this.setCellMeta(row, col, 'borders', border);
        insertBorderIntoSettings(border);
      }
    }
  }
};
var createClassName = function(row, col) {
  return "border_row" + row + "col" + col;
};
var createDefaultCustomBorder = function() {
  return {
    width: 1,
    color: '#000'
  };
};
var createSingleEmptyBorder = function() {
  return {hide: true};
};
var createDefaultHtBorder = function() {
  return {
    width: 1,
    color: '#000',
    cornerVisible: false
  };
};
var createEmptyBorders = function(row, col) {
  return {
    className: createClassName(row, col),
    border: createDefaultHtBorder(),
    row: row,
    col: col,
    top: createSingleEmptyBorder(),
    right: createSingleEmptyBorder(),
    bottom: createSingleEmptyBorder(),
    left: createSingleEmptyBorder()
  };
};
var extendDefaultBorder = function(defaultBorder, customBorder) {
  if (customBorder.hasOwnProperty('border')) {
    defaultBorder.border = customBorder.border;
  }
  if (customBorder.hasOwnProperty('top')) {
    defaultBorder.top = customBorder.top;
  }
  if (customBorder.hasOwnProperty('right')) {
    defaultBorder.right = customBorder.right;
  }
  if (customBorder.hasOwnProperty('bottom')) {
    defaultBorder.bottom = customBorder.bottom;
  }
  if (customBorder.hasOwnProperty('left')) {
    defaultBorder.left = customBorder.left;
  }
  return defaultBorder;
};
var removeBordersFromDom = function(borderClassName) {
  var borders = document.querySelectorAll("." + borderClassName);
  for (var i = 0; i < borders.length; i++) {
    if (borders[i]) {
      if (borders[i].nodeName != 'TD') {
        var parent = borders[i].parentNode;
        if (parent.parentNode) {
          parent.parentNode.removeChild(parent);
        }
      }
    }
  }
};
var removeAllBorders = function(row, col) {
  var borderClassName = createClassName(row, col);
  removeBordersFromDom(borderClassName);
  this.removeCellMeta(row, col, 'borders');
};
var setBorder = function(row, col, place, remove) {
  var bordersMeta = this.getCellMeta(row, col).borders;
  if (!bordersMeta || bordersMeta.border == undefined) {
    bordersMeta = createEmptyBorders(row, col);
  }
  if (remove) {
    bordersMeta[place] = createSingleEmptyBorder();
  } else {
    bordersMeta[place] = createDefaultCustomBorder();
  }
  this.setCellMeta(row, col, 'borders', bordersMeta);
  var borderClassName = createClassName(row, col);
  removeBordersFromDom(borderClassName);
  insertBorderIntoSettings(bordersMeta);
  this.render();
};
var prepareBorder = function(range, place, remove) {
  if (range.from.row == range.to.row && range.from.col == range.to.col) {
    if (place == "noBorders") {
      removeAllBorders.call(this, range.from.row, range.from.col);
    } else {
      setBorder.call(this, range.from.row, range.from.col, place, remove);
    }
  } else {
    switch (place) {
      case "noBorders":
        for (var column = range.from.col; column <= range.to.col; column++) {
          for (var row = range.from.row; row <= range.to.row; row++) {
            removeAllBorders.call(this, row, column);
          }
        }
        break;
      case "top":
        for (var topCol = range.from.col; topCol <= range.to.col; topCol++) {
          setBorder.call(this, range.from.row, topCol, place, remove);
        }
        break;
      case "right":
        for (var rowRight = range.from.row; rowRight <= range.to.row; rowRight++) {
          setBorder.call(this, rowRight, range.to.col, place);
        }
        break;
      case "bottom":
        for (var bottomCol = range.from.col; bottomCol <= range.to.col; bottomCol++) {
          setBorder.call(this, range.to.row, bottomCol, place);
        }
        break;
      case "left":
        for (var rowLeft = range.from.row; rowLeft <= range.to.row; rowLeft++) {
          setBorder.call(this, rowLeft, range.from.col, place);
        }
        break;
    }
  }
};
var checkSelectionBorders = function(hot, direction) {
  var atLeastOneHasBorder = false;
  hot.getSelectedRange().forAll(function(r, c) {
    var metaBorders = hot.getCellMeta(r, c).borders;
    if (metaBorders) {
      if (direction) {
        if (!metaBorders[direction].hasOwnProperty('hide')) {
          atLeastOneHasBorder = true;
          return false;
        }
      } else {
        atLeastOneHasBorder = true;
        return false;
      }
    }
  });
  return atLeastOneHasBorder;
};
var markSelected = function(label) {
  return "<span class='selected'>" + String.fromCharCode(10003) + "</span>" + label;
};
var addBordersOptionsToContextMenu = function(defaultOptions) {
  if (!this.getSettings().customBorders) {
    return;
  }
  defaultOptions.items.push(Handsontable.ContextMenu.SEPARATOR);
  defaultOptions.items.push({
    key: 'borders',
    name: 'Borders',
    submenu: {items: {
        top: {
          name: function() {
            var label = "Top";
            var hasBorder = checkSelectionBorders(this, 'top');
            if (hasBorder) {
              label = markSelected(label);
            }
            return label;
          },
          callback: function() {
            var hasBorder = checkSelectionBorders(this, 'top');
            prepareBorder.call(this, this.getSelectedRange(), 'top', hasBorder);
          },
          disabled: false
        },
        right: {
          name: function() {
            var label = 'Right';
            var hasBorder = checkSelectionBorders(this, 'right');
            if (hasBorder) {
              label = markSelected(label);
            }
            return label;
          },
          callback: function() {
            var hasBorder = checkSelectionBorders(this, 'right');
            prepareBorder.call(this, this.getSelectedRange(), 'right', hasBorder);
          },
          disabled: false
        },
        bottom: {
          name: function() {
            var label = 'Bottom';
            var hasBorder = checkSelectionBorders(this, 'bottom');
            if (hasBorder) {
              label = markSelected(label);
            }
            return label;
          },
          callback: function() {
            var hasBorder = checkSelectionBorders(this, 'bottom');
            prepareBorder.call(this, this.getSelectedRange(), 'bottom', hasBorder);
          },
          disabled: false
        },
        left: {
          name: function() {
            var label = 'Left';
            var hasBorder = checkSelectionBorders(this, 'left');
            if (hasBorder) {
              label = markSelected(label);
            }
            return label;
          },
          callback: function() {
            var hasBorder = checkSelectionBorders(this, 'left');
            prepareBorder.call(this, this.getSelectedRange(), 'left', hasBorder);
          },
          disabled: false
        },
        remove: {
          name: 'Remove border(s)',
          callback: function() {
            prepareBorder.call(this, this.getSelectedRange(), 'noBorders');
          },
          disabled: function() {
            return !checkSelectionBorders(this);
          }
        }
      }}
  });
};
Handsontable.hooks.add('beforeInit', init);
Handsontable.hooks.add('afterContextMenuDefaultOptions', addBordersOptionsToContextMenu);
Handsontable.hooks.add('afterInit', function() {
  var customBorders = this.getSettings().customBorders;
  if (customBorders) {
    for (var i = 0; i < customBorders.length; i++) {
      if (customBorders[i].range) {
        prepareBorderFromCustomAddedRange.call(this, customBorders[i]);
      } else {
        prepareBorderFromCustomAdded.call(this, customBorders[i].row, customBorders[i].col, customBorders[i]);
      }
    }
    this.render();
    this.view.wt.draw(true);
  }
});
Handsontable.CustomBorders = CustomBorders;


//# 
},{"./../../3rdparty/walkontable/src/cell/range.js":6,"./../../3rdparty/walkontable/src/selection.js":18,"./../../plugins.js":45}],56:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  DragToScroll: {get: function() {
      return DragToScroll;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_eventManager_46_js__,
    $___46__46__47__46__46__47_plugins_46_js__;
var eventManagerObject = ($___46__46__47__46__46__47_eventManager_46_js__ = require("./../../eventManager.js"), $___46__46__47__46__46__47_eventManager_46_js__ && $___46__46__47__46__46__47_eventManager_46_js__.__esModule && $___46__46__47__46__46__47_eventManager_46_js__ || {default: $___46__46__47__46__46__47_eventManager_46_js__}).eventManager;
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
;
Handsontable.plugins.DragToScroll = DragToScroll;
function DragToScroll() {
  this.boundaries = null;
  this.callback = null;
}
DragToScroll.prototype.setBoundaries = function(boundaries) {
  this.boundaries = boundaries;
};
DragToScroll.prototype.setCallback = function(callback) {
  this.callback = callback;
};
DragToScroll.prototype.check = function(x, y) {
  var diffX = 0;
  var diffY = 0;
  if (y < this.boundaries.top) {
    diffY = y - this.boundaries.top;
  } else if (y > this.boundaries.bottom) {
    diffY = y - this.boundaries.bottom;
  }
  if (x < this.boundaries.left) {
    diffX = x - this.boundaries.left;
  } else if (x > this.boundaries.right) {
    diffX = x - this.boundaries.right;
  }
  this.callback(diffX, diffY);
};
var dragToScroll;
var instance;
if (typeof Handsontable !== 'undefined') {
  var setupListening = function(instance) {
    instance.dragToScrollListening = false;
    var scrollHandler = instance.view.wt.wtTable.holder;
    dragToScroll = new DragToScroll();
    if (scrollHandler === window) {
      return;
    } else {
      dragToScroll.setBoundaries(scrollHandler.getBoundingClientRect());
    }
    dragToScroll.setCallback(function(scrollX, scrollY) {
      if (scrollX < 0) {
        scrollHandler.scrollLeft -= 50;
      } else if (scrollX > 0) {
        scrollHandler.scrollLeft += 50;
      }
      if (scrollY < 0) {
        scrollHandler.scrollTop -= 20;
      } else if (scrollY > 0) {
        scrollHandler.scrollTop += 20;
      }
    });
    instance.dragToScrollListening = true;
  };
}
Handsontable.hooks.add('afterInit', function() {
  var instance = this;
  var eventManager = eventManagerObject(this);
  eventManager.addEventListener(document, 'mouseup', function() {
    instance.dragToScrollListening = false;
  });
  eventManager.addEventListener(document, 'mousemove', function(event) {
    if (instance.dragToScrollListening) {
      dragToScroll.check(event.clientX, event.clientY);
    }
  });
});
Handsontable.hooks.add('afterDestroy', function() {
  eventManagerObject(this).clear();
});
Handsontable.hooks.add('afterOnCellMouseDown', function() {
  setupListening(this);
});
Handsontable.hooks.add('afterOnCellCornerMouseDown', function() {
  setupListening(this);
});
Handsontable.plugins.DragToScroll = DragToScroll;


//# 
},{"./../../eventManager.js":41,"./../../plugins.js":45}],57:[function(require,module,exports){
"use strict";
var $___46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47_plugins_46_js__;
var dom = ($___46__46__47__46__46__47_dom_46_js__ = require("./../../dom.js"), $___46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47_dom_46_js__});
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
function Grouping(instance) {
  var groups = [];
  var item = {
    id: '',
    level: 0,
    hidden: 0,
    rows: [],
    cols: []
  };
  var counters = {
    rows: 0,
    cols: 0
  };
  var levels = {
    rows: 0,
    cols: 0
  };
  var hiddenRows = [];
  var hiddenCols = [];
  var classes = {
    'groupIndicatorContainer': 'htGroupIndicatorContainer',
    'groupIndicator': function(direction) {
      return 'ht' + direction + 'Group';
    },
    'groupStart': 'htGroupStart',
    'collapseButton': 'htCollapseButton',
    'expandButton': 'htExpandButton',
    'collapseGroupId': function(id) {
      return 'htCollapse-' + id;
    },
    'collapseFromLevel': function(direction, level) {
      return 'htCollapse' + direction + 'FromLevel-' + level;
    },
    'clickable': 'clickable',
    'levelTrigger': 'htGroupLevelTrigger'
  };
  var compare = function(property, orderDirection) {
    return function(item1, item2) {
      return typeof(orderDirection) === 'undefined' || orderDirection === 'asc' ? item1[property] - item2[property] : item2[property] - item1[property];
    };
  };
  var range = function(from, to) {
    var arr = [];
    while (from <= to) {
      arr.push(from++);
    }
    return arr;
  };
  var getRangeGroups = function(dataType, from, to) {
    var cells = [],
        cell = {
          row: null,
          col: null
        };
    if (dataType == "cols") {
      while (from <= to) {
        cell = {
          row: -1,
          col: from++
        };
        cells.push(cell);
      }
    } else {
      while (from <= to) {
        cell = {
          row: from++,
          col: -1
        };
        cells.push(cell);
      }
    }
    var cellsGroups = getCellsGroups(cells),
        totalRows = 0,
        totalCols = 0;
    for (var i = 0; i < cellsGroups.length; i++) {
      totalRows += cellsGroups[i].filter(function(item) {
        return item['rows'];
      }).length;
      totalCols += cellsGroups[i].filter(function(item) {
        return item['cols'];
      }).length;
    }
    return {
      total: {
        rows: totalRows,
        cols: totalCols
      },
      groups: cellsGroups
    };
  };
  var getCellsGroups = function(cells) {
    var _groups = [];
    for (var i = 0; i < cells.length; i++) {
      _groups.push(getCellGroups(cells[i]));
    }
    return _groups;
  };
  var getCellGroups = function(coords, groupLevel, groupType) {
    var row = coords.row,
        col = coords.col;
    var tmpRow = (row === -1 ? 0 : row),
        tmpCol = (col === -1 ? 0 : col);
    var _groups = [];
    for (var i = 0; i < groups.length; i++) {
      var group = groups[i],
          id = group['id'],
          level = group['level'],
          rows = group['rows'] || [],
          cols = group['cols'] || [];
      if (_groups.indexOf(id) === -1) {
        if (rows.indexOf(tmpRow) !== -1 || cols.indexOf(tmpCol) !== -1) {
          _groups.push(group);
        }
      }
    }
    if (col === -1) {
      _groups = _groups.concat(getColGroups());
    } else if (row === -1) {
      _groups = _groups.concat(getRowGroups());
    }
    if (groupLevel) {
      _groups = _groups.filter(function(item) {
        return item['level'] === groupLevel;
      });
    }
    if (groupType) {
      if (groupType === 'cols') {
        _groups = _groups.filter(function(item) {
          return item['cols'];
        });
      } else if (groupType === 'rows') {
        _groups = _groups.filter(function(item) {
          return item['rows'];
        });
      }
    }
    var tmp = [];
    return _groups.filter(function(item) {
      if (tmp.indexOf(item.id) === -1) {
        tmp.push(item.id);
        return item;
      }
    });
  };
  var getGroupById = function(id) {
    for (var i = 0,
        groupsLength = groups.length; i < groupsLength; i++) {
      if (groups[i].id == id) {
        return groups[i];
      }
    }
    return false;
  };
  var getGroupByRowAndLevel = function(row, level) {
    for (var i = 0,
        groupsLength = groups.length; i < groupsLength; i++) {
      if (groups[i].level == level && groups[i].rows && groups[i].rows.indexOf(row) > -1) {
        return groups[i];
      }
    }
    return false;
  };
  var getGroupByColAndLevel = function(col, level) {
    for (var i = 0,
        groupsLength = groups.length; i < groupsLength; i++) {
      if (groups[i].level == level && groups[i].cols && groups[i].cols.indexOf(col) > -1) {
        return groups[i];
      }
    }
    return false;
  };
  var getColGroups = function() {
    var result = [];
    for (var i = 0,
        groupsLength = groups.length; i < groupsLength; i++) {
      if (Array.isArray(groups[i]['cols'])) {
        result.push(groups[i]);
      }
    }
    return result;
  };
  var getColGroupsByLevel = function(level) {
    var result = [];
    for (var i = 0,
        groupsLength = groups.length; i < groupsLength; i++) {
      if (groups[i]['cols'] && groups[i]['level'] === level) {
        result.push(groups[i]);
      }
    }
    return result;
  };
  var getRowGroups = function() {
    var result = [];
    for (var i = 0,
        groupsLength = groups.length; i < groupsLength; i++) {
      if (Array.isArray(groups[i]['rows'])) {
        result.push(groups[i]);
      }
    }
    return result;
  };
  var getRowGroupsByLevel = function(level) {
    var result = [];
    for (var i = 0,
        groupsLength = groups.length; i < groupsLength; i++) {
      if (groups[i]['rows'] && groups[i]['level'] === level) {
        result.push(groups[i]);
      }
    }
    return result;
  };
  var getLastLevelColsInRange = function(rangeGroups) {
    var level = 0;
    if (rangeGroups.length) {
      rangeGroups.forEach(function(items) {
        items = items.filter(function(item) {
          return item['cols'];
        });
        if (items.length) {
          var sortedGroup = items.sort(compare('level', 'desc')),
              lastLevel = sortedGroup[0].level;
          if (level < lastLevel) {
            level = lastLevel;
          }
        }
      });
    }
    return level;
  };
  var getLastLevelRowsInRange = function(rangeGroups) {
    var level = 0;
    if (rangeGroups.length) {
      rangeGroups.forEach(function(items) {
        items = items.filter(function(item) {
          return item['rows'];
        });
        if (items.length) {
          var sortedGroup = items.sort(compare('level', 'desc')),
              lastLevel = sortedGroup[0].level;
          if (level < lastLevel) {
            level = lastLevel;
          }
        }
      });
    }
    return level;
  };
  var groupCols = function(from, to) {
    var rangeGroups = getRangeGroups("cols", from, to),
        lastLevel = getLastLevelColsInRange(rangeGroups.groups);
    if (lastLevel === levels.cols) {
      levels.cols++;
    } else if (lastLevel > levels.cols) {
      levels.cols = lastLevel + 1;
    }
    if (!counters.cols) {
      counters.cols = getColGroups().length;
    }
    counters.cols++;
    groups.push({
      id: 'c' + counters.cols,
      level: lastLevel + 1,
      cols: range(from, to),
      hidden: 0
    });
  };
  var groupRows = function(from, to) {
    var rangeGroups = getRangeGroups("rows", from, to),
        lastLevel = getLastLevelRowsInRange(rangeGroups.groups);
    levels.rows = Math.max(levels.rows, lastLevel + 1);
    if (!counters.rows) {
      counters.rows = getRowGroups().length;
    }
    counters.rows++;
    groups.push({
      id: 'r' + counters.rows,
      level: lastLevel + 1,
      rows: range(from, to),
      hidden: 0
    });
  };
  var showHideGroups = function(hidden, groups) {
    var level;
    for (var i = 0,
        groupsLength = groups.length; i < groupsLength; i++) {
      groups[i].hidden = hidden;
      level = groups[i].level;
      if (!hiddenRows[level]) {
        hiddenRows[level] = [];
      }
      if (!hiddenCols[level]) {
        hiddenCols[level] = [];
      }
      if (groups[i].rows) {
        for (var j = 0,
            rowsLength = groups[i].rows.length; j < rowsLength; j++) {
          if (hidden > 0) {
            hiddenRows[level][groups[i].rows[j]] = true;
          } else {
            hiddenRows[level][groups[i].rows[j]] = void 0;
          }
        }
      } else if (groups[i].cols) {
        for (var j = 0,
            colsLength = groups[i].cols.length; j < colsLength; j++) {
          if (hidden > 0) {
            hiddenCols[level][groups[i].cols[j]] = true;
          } else {
            hiddenCols[level][groups[i].cols[j]] = void 0;
          }
        }
      }
    }
  };
  var nextIndexSharesLevel = function(dimension, currentPosition, level, currentGroupId) {
    var nextCellGroupId,
        levelsByOrder;
    switch (dimension) {
      case 'rows':
        nextCellGroupId = getGroupByRowAndLevel(currentPosition + 1, level).id;
        levelsByOrder = Handsontable.Grouping.getGroupLevelsByRows();
        break;
      case 'cols':
        nextCellGroupId = getGroupByColAndLevel(currentPosition + 1, level).id;
        levelsByOrder = Handsontable.Grouping.getGroupLevelsByCols();
        break;
    }
    return !!(levelsByOrder[currentPosition + 1] && levelsByOrder[currentPosition + 1].indexOf(level) > -1 && currentGroupId == nextCellGroupId);
  };
  var previousIndexSharesLevel = function(dimension, currentPosition, level, currentGroupId) {
    var previousCellGroupId,
        levelsByOrder;
    switch (dimension) {
      case 'rows':
        previousCellGroupId = getGroupByRowAndLevel(currentPosition - 1, level).id;
        levelsByOrder = Handsontable.Grouping.getGroupLevelsByRows();
        break;
      case 'cols':
        previousCellGroupId = getGroupByColAndLevel(currentPosition - 1, level).id;
        levelsByOrder = Handsontable.Grouping.getGroupLevelsByCols();
        break;
    }
    return !!(levelsByOrder[currentPosition - 1] && levelsByOrder[currentPosition - 1].indexOf(level) > -1 && currentGroupId == previousCellGroupId);
  };
  var isLastIndexOfTheLine = function(dimension, index, level, currentGroupId) {
    if (index === 0) {
      return false;
    }
    var levelsByOrder,
        entriesLength,
        previousSharesLevel = previousIndexSharesLevel(dimension, index, level, currentGroupId),
        nextSharesLevel = nextIndexSharesLevel(dimension, index, level, currentGroupId),
        nextIsHidden = false;
    switch (dimension) {
      case 'rows':
        levelsByOrder = Handsontable.Grouping.getGroupLevelsByRows();
        entriesLength = instance.countRows();
        for (var i = 0; i <= levels.rows; i++) {
          if (hiddenRows[i] && hiddenRows[i][index + 1]) {
            nextIsHidden = true;
            break;
          }
        }
        break;
      case 'cols':
        levelsByOrder = Handsontable.Grouping.getGroupLevelsByCols();
        entriesLength = instance.countCols();
        for (var i = 0; i <= levels.cols; i++) {
          if (hiddenCols[i] && hiddenCols[i][index + 1]) {
            nextIsHidden = true;
            break;
          }
        }
        break;
    }
    if (previousSharesLevel) {
      if (index == entriesLength - 1) {
        return true;
      } else if (!nextSharesLevel || (nextSharesLevel && nextIsHidden)) {
        return true;
      } else if (!levelsByOrder[index + 1]) {
        return true;
      }
    }
    return false;
  };
  var isLastHidden = function(dataType) {
    var levelAmount;
    switch (dataType) {
      case 'rows':
        levelAmount = levels.rows;
        for (var j = 0; j <= levelAmount; j++) {
          if (hiddenRows[j] && hiddenRows[j][instance.countRows() - 1]) {
            return true;
          }
        }
        break;
      case 'cols':
        levelAmount = levels.cols;
        for (var j = 0; j <= levelAmount; j++) {
          if (hiddenCols[j] && hiddenCols[j][instance.countCols() - 1]) {
            return true;
          }
        }
        break;
    }
    return false;
  };
  var isFirstIndexOfTheLine = function(dimension, index, level, currentGroupId) {
    var levelsByOrder,
        entriesLength,
        currentGroup = getGroupById(currentGroupId),
        previousAreHidden = false,
        arePreviousHidden = function(dimension) {
          var hidden = false,
              hiddenArr = dimension == 'rows' ? hiddenRows : hiddenCols;
          for (var i = 0; i <= levels[dimension]; i++) {
            tempInd = index;
            while (currentGroup[dimension].indexOf(tempInd) > -1) {
              hidden = !!(hiddenArr[i] && hiddenArr[i][tempInd]);
              tempInd--;
            }
            if (hidden) {
              break;
            }
          }
          return hidden;
        },
        previousSharesLevel = previousIndexSharesLevel(dimension, index, level, currentGroupId),
        nextSharesLevel = nextIndexSharesLevel(dimension, index, level, currentGroupId),
        tempInd;
    switch (dimension) {
      case 'rows':
        levelsByOrder = Handsontable.Grouping.getGroupLevelsByRows();
        entriesLength = instance.countRows();
        previousAreHidden = arePreviousHidden(dimension);
        break;
      case 'cols':
        levelsByOrder = Handsontable.Grouping.getGroupLevelsByCols();
        entriesLength = instance.countCols();
        previousAreHidden = arePreviousHidden(dimension);
        break;
    }
    if (index == entriesLength - 1) {
      return false;
    } else if (index === 0) {
      if (nextSharesLevel) {
        return true;
      }
    } else if (!previousSharesLevel || (previousSharesLevel && previousAreHidden)) {
      if (nextSharesLevel) {
        return true;
      }
    } else if (!levelsByOrder[index - 1]) {
      if (nextSharesLevel) {
        return true;
      }
    }
    return false;
  };
  var addGroupExpander = function(dataType, index, level, id, elem) {
    var previousIndexGroupId;
    switch (dataType) {
      case 'rows':
        previousIndexGroupId = getGroupByRowAndLevel(index - 1, level).id;
        break;
      case 'cols':
        previousIndexGroupId = getGroupByColAndLevel(index - 1, level).id;
        break;
    }
    if (!previousIndexGroupId) {
      return null;
    }
    if (index > 0) {
      if (previousIndexSharesLevel(dataType, index - 1, level, previousIndexGroupId) && previousIndexGroupId != id) {
        var expanderButton = document.createElement('DIV');
        dom.addClass(expanderButton, classes.expandButton);
        expanderButton.id = 'htExpand-' + previousIndexGroupId;
        expanderButton.appendChild(document.createTextNode('+'));
        expanderButton.setAttribute('data-level', level);
        expanderButton.setAttribute('data-type', dataType);
        expanderButton.setAttribute('data-hidden', "1");
        elem.appendChild(expanderButton);
        return expanderButton;
      }
    }
    return null;
  };
  var isCollapsed = function(currentPosition) {
    var rowGroups = getRowGroups(),
        colGroups = getColGroups();
    for (var i = 0,
        rowGroupsCount = rowGroups.length; i < rowGroupsCount; i++) {
      if (rowGroups[i].rows.indexOf(currentPosition.row) > -1 && rowGroups[i].hidden) {
        return true;
      }
    }
    if (currentPosition.col === null) {
      return false;
    }
    for (var i = 0,
        colGroupsCount = colGroups.length; i < colGroupsCount; i++) {
      if (colGroups[i].cols.indexOf(currentPosition.col) > -1 && colGroups[i].hidden) {
        return true;
      }
    }
    return false;
  };
  return {
    getGroups: function() {
      return groups;
    },
    getLevels: function() {
      return levels;
    },
    instance: instance,
    baseSpareRows: instance.getSettings().minSpareRows,
    baseSpareCols: instance.getSettings().minSpareCols,
    getRowGroups: getRowGroups,
    getColGroups: getColGroups,
    init: function() {
      var groupsSetting = instance.getSettings().groups;
      if (groupsSetting) {
        if (Array.isArray(groupsSetting)) {
          Handsontable.Grouping.initGroups(groupsSetting);
        }
      }
    },
    initGroups: function(initialGroups) {
      var that = this;
      groups = [];
      initialGroups.forEach(function(item) {
        var _group = [],
            isRow = false,
            isCol = false;
        if (Array.isArray(item.rows)) {
          _group = item.rows;
          isRow = true;
        } else if (Array.isArray(item.cols)) {
          _group = item.cols;
          isCol = true;
        }
        var from = _group[0],
            to = _group[_group.length - 1];
        if (isRow) {
          groupRows(from, to);
        } else if (isCol) {
          groupCols(from, to);
        }
      });
    },
    resetGroups: function() {
      groups = [];
      counters = {
        rows: 0,
        cols: 0
      };
      levels = {
        rows: 0,
        cols: 0
      };
      var allOccurrences;
      for (var i in classes) {
        if (typeof classes[i] != 'function') {
          allOccurrences = document.querySelectorAll('.' + classes[i]);
          for (var j = 0,
              occurrencesLength = allOccurrences.length; j < occurrencesLength; j++) {
            dom.removeClass(allOccurrences[j], classes[i]);
          }
        }
      }
      var otherClasses = ['htGroupColClosest', 'htGroupCol'];
      for (var i = 0,
          otherClassesLength = otherClasses.length; i < otherClassesLength; i++) {
        allOccurrences = document.querySelectorAll('.' + otherClasses[i]);
        for (var j = 0,
            occurrencesLength = allOccurrences.length; j < occurrencesLength; j++) {
          dom.removeClass(allOccurrences[j], otherClasses[i]);
        }
      }
    },
    updateGroups: function() {
      var groupSettings = this.getSettings().groups;
      Handsontable.Grouping.resetGroups();
      Handsontable.Grouping.initGroups(groupSettings);
    },
    afterGetRowHeader: function(row, TH) {
      var currentRowHidden = false;
      for (var i = 0,
          levels = hiddenRows.length; i < levels; i++) {
        if (hiddenRows[i] && hiddenRows[i][row] === true) {
          currentRowHidden = true;
        }
      }
      if (currentRowHidden) {
        dom.addClass(TH.parentNode, 'hidden');
      } else if (!currentRowHidden && dom.hasClass(TH.parentNode, 'hidden')) {
        dom.removeClass(TH.parentNode, 'hidden');
      }
    },
    afterGetColHeader: function(col, TH) {
      var rowHeaders = this.view.wt.wtSettings.getSetting('rowHeaders').length,
          thisColgroup = instance.rootElement.querySelectorAll('colgroup col:nth-child(' + parseInt(col + rowHeaders + 1, 10) + ')');
      if (thisColgroup.length === 0) {
        return;
      }
      var currentColHidden = false;
      for (var i = 0,
          levels = hiddenCols.length; i < levels; i++) {
        if (hiddenCols[i] && hiddenCols[i][col] === true) {
          currentColHidden = true;
        }
      }
      if (currentColHidden) {
        for (var i = 0,
            colsAmount = thisColgroup.length; i < colsAmount; i++) {
          dom.addClass(thisColgroup[i], 'hidden');
        }
      } else if (!currentColHidden && dom.hasClass(thisColgroup[0], 'hidden')) {
        for (var i = 0,
            colsAmount = thisColgroup.length; i < colsAmount; i++) {
          dom.removeClass(thisColgroup[i], 'hidden');
        }
      }
    },
    groupIndicatorsFactory: function(renderersArr, direction) {
      var groupsLevelsList,
          getCurrentLevel,
          getCurrentGroupId,
          dataType,
          getGroupByIndexAndLevel,
          headersType,
          currentHeaderModifier,
          createLevelTriggers;
      switch (direction) {
        case 'horizontal':
          groupsLevelsList = Handsontable.Grouping.getGroupLevelsByCols();
          getCurrentLevel = function(elem) {
            return Array.prototype.indexOf.call(elem.parentNode.parentNode.childNodes, elem.parentNode) + 1;
          };
          getCurrentGroupId = function(col, level) {
            return getGroupByColAndLevel(col, level).id;
          };
          dataType = 'cols';
          getGroupByIndexAndLevel = function(col, level) {
            return getGroupByColAndLevel(col - 1, level);
          };
          headersType = "columnHeaders";
          currentHeaderModifier = function(headerRenderers) {
            if (headerRenderers.length === 1) {
              var oldFn = headerRenderers[0];
              headerRenderers[0] = function(index, elem, level) {
                if (index < -1) {
                  makeGroupIndicatorsForLevel()(index, elem, level);
                } else {
                  dom.removeClass(elem, classes.groupIndicatorContainer);
                  oldFn(index, elem, level);
                }
              };
            }
            return function() {
              return headerRenderers;
            };
          };
          createLevelTriggers = true;
          break;
        case 'vertical':
          groupsLevelsList = Handsontable.Grouping.getGroupLevelsByRows();
          getCurrentLevel = function(elem) {
            return dom.index(elem) + 1;
          };
          getCurrentGroupId = function(row, level) {
            return getGroupByRowAndLevel(row, level).id;
          };
          dataType = 'rows';
          getGroupByIndexAndLevel = function(row, level) {
            return getGroupByRowAndLevel(row - 1, level);
          };
          headersType = "rowHeaders";
          currentHeaderModifier = function(headerRenderers) {
            return headerRenderers;
          };
          break;
      }
      var createButton = function(parent) {
        var button = document.createElement('div');
        parent.appendChild(button);
        return {
          button: button,
          addClass: function(className) {
            dom.addClass(button, className);
          }
        };
      };
      var makeGroupIndicatorsForLevel = function() {
        var directionClassname = direction.charAt(0).toUpperCase() + direction.slice(1);
        return function(index, elem, level) {
          level++;
          var child,
              collapseButton;
          while (child = elem.lastChild) {
            elem.removeChild(child);
          }
          dom.addClass(elem, classes.groupIndicatorContainer);
          var currentGroupId = getCurrentGroupId(index, level);
          if (index > -1 && (groupsLevelsList[index] && groupsLevelsList[index].indexOf(level) > -1)) {
            collapseButton = createButton(elem);
            collapseButton.addClass(classes.groupIndicator(directionClassname));
            if (isFirstIndexOfTheLine(dataType, index, level, currentGroupId)) {
              collapseButton.addClass(classes.groupStart);
            }
            if (isLastIndexOfTheLine(dataType, index, level, currentGroupId)) {
              collapseButton.button.appendChild(document.createTextNode('-'));
              collapseButton.addClass(classes.collapseButton);
              collapseButton.button.id = classes.collapseGroupId(currentGroupId);
              collapseButton.button.setAttribute('data-level', level);
              collapseButton.button.setAttribute('data-type', dataType);
            }
          }
          if (createLevelTriggers) {
            var rowInd = dom.index(elem.parentNode);
            if (index === -1 || (index < -1 && rowInd === Handsontable.Grouping.getLevels().cols + 1) || (rowInd === 0 && Handsontable.Grouping.getLevels().cols === 0)) {
              collapseButton = createButton(elem);
              collapseButton.addClass(classes.levelTrigger);
              if (index === -1) {
                collapseButton.button.id = classes.collapseFromLevel("Cols", level);
                collapseButton.button.appendChild(document.createTextNode(level));
              } else if (index < -1 && rowInd === Handsontable.Grouping.getLevels().cols + 1 || (rowInd === 0 && Handsontable.Grouping.getLevels().cols === 0)) {
                var colInd = dom.index(elem) + 1;
                collapseButton.button.id = classes.collapseFromLevel("Rows", colInd);
                collapseButton.button.appendChild(document.createTextNode(colInd));
              }
            }
          }
          var expanderButton = addGroupExpander(dataType, index, level, currentGroupId, elem);
          if (index > 0) {
            var previousGroupObj = getGroupByIndexAndLevel(index - 1, level);
            if (expanderButton && previousGroupObj.hidden) {
              dom.addClass(expanderButton, classes.clickable);
            }
          }
          updateHeaderWidths();
        };
      };
      renderersArr = currentHeaderModifier(renderersArr);
      if (counters[dataType] > 0) {
        for (var i = 0; i < levels[dataType] + 1; i++) {
          if (!Array.isArray(renderersArr)) {
            renderersArr = typeof renderersArr === 'function' ? renderersArr() : new Array(renderersArr);
          }
          renderersArr.unshift(makeGroupIndicatorsForLevel());
        }
      }
    },
    getGroupLevelsByRows: function() {
      var rowGroups = getRowGroups(),
          result = [];
      for (var i = 0,
          groupsLength = rowGroups.length; i < groupsLength; i++) {
        if (rowGroups[i].rows) {
          for (var j = 0,
              groupRowsLength = rowGroups[i].rows.length; j < groupRowsLength; j++) {
            if (!result[rowGroups[i].rows[j]]) {
              result[rowGroups[i].rows[j]] = [];
            }
            result[rowGroups[i].rows[j]].push(rowGroups[i].level);
          }
        }
      }
      return result;
    },
    getGroupLevelsByCols: function() {
      var colGroups = getColGroups(),
          result = [];
      for (var i = 0,
          groupsLength = colGroups.length; i < groupsLength; i++) {
        if (colGroups[i].cols) {
          for (var j = 0,
              groupColsLength = colGroups[i].cols.length; j < groupColsLength; j++) {
            if (!result[colGroups[i].cols[j]]) {
              result[colGroups[i].cols[j]] = [];
            }
            result[colGroups[i].cols[j]].push(colGroups[i].level);
          }
        }
      }
      return result;
    },
    toggleGroupVisibility: function(event, coords, TD) {
      if (dom.hasClass(event.target, classes.expandButton) || dom.hasClass(event.target, classes.collapseButton) || dom.hasClass(event.target, classes.levelTrigger)) {
        var element = event.target,
            elemIdSplit = element.id.split('-');
        var groups = [],
            id,
            level,
            type,
            hidden;
        var prepareGroupData = function(componentElement) {
          if (componentElement) {
            element = componentElement;
          }
          elemIdSplit = element.id.split('-');
          id = elemIdSplit[1];
          level = parseInt(element.getAttribute('data-level'), 10);
          type = element.getAttribute('data-type');
          hidden = parseInt(element.getAttribute('data-hidden'));
          if (isNaN(hidden)) {
            hidden = 1;
          } else {
            hidden = (hidden ? 0 : 1);
          }
          element.setAttribute('data-hidden', hidden.toString());
          groups.push(getGroupById(id));
        };
        if (element.className.indexOf(classes.levelTrigger) > -1) {
          var groupsInLevel,
              groupsToExpand = [],
              groupsToCollapse = [],
              levelType = element.id.indexOf("Rows") > -1 ? "rows" : "cols";
          for (var i = 1,
              levelsCount = levels[levelType]; i <= levelsCount; i++) {
            groupsInLevel = levelType == "rows" ? getRowGroupsByLevel(i) : getColGroupsByLevel(i);
            if (i >= parseInt(elemIdSplit[1], 10)) {
              for (var j = 0,
                  groupCount = groupsInLevel.length; j < groupCount; j++) {
                groupsToCollapse.push(groupsInLevel[j]);
              }
            } else {
              for (var j = 0,
                  groupCount = groupsInLevel.length; j < groupCount; j++) {
                groupsToExpand.push(groupsInLevel[j]);
              }
            }
          }
          showHideGroups(true, groupsToCollapse);
          showHideGroups(false, groupsToExpand);
        } else {
          prepareGroupData();
          showHideGroups(hidden, groups);
        }
        type = type || levelType;
        var lastHidden = isLastHidden(type),
            typeUppercase = type.charAt(0).toUpperCase() + type.slice(1),
            spareElements = Handsontable.Grouping['baseSpare' + typeUppercase];
        if (lastHidden) {
          if (spareElements == 0) {
            instance.alter('insert_' + type.slice(0, -1), instance['count' + typeUppercase]());
            Handsontable.Grouping["dummy" + type.slice(0, -1)] = true;
          }
        } else {
          if (spareElements == 0) {
            if (Handsontable.Grouping["dummy" + type.slice(0, -1)]) {
              instance.alter('remove_' + type.slice(0, -1), instance['count' + typeUppercase]() - 1);
              Handsontable.Grouping["dummy" + type.slice(0, -1)] = false;
            }
          }
        }
        instance.render();
        event.stopImmediatePropagation();
      }
    },
    modifySelectionFactory: function(position) {
      var instance = this.instance;
      var currentlySelected,
          nextPosition = new WalkontableCellCoords(0, 0),
          nextVisible = function(direction, currentPosition) {
            var updateDelta = 0;
            switch (direction) {
              case 'down':
                while (isCollapsed(currentPosition)) {
                  updateDelta++;
                  currentPosition.row += 1;
                }
                break;
              case 'up':
                while (isCollapsed(currentPosition)) {
                  updateDelta--;
                  currentPosition.row -= 1;
                }
                break;
              case 'right':
                while (isCollapsed(currentPosition)) {
                  updateDelta++;
                  currentPosition.col += 1;
                }
                break;
              case 'left':
                while (isCollapsed(currentPosition)) {
                  updateDelta--;
                  currentPosition.col -= 1;
                }
                break;
            }
            return updateDelta;
          },
          updateDelta = function(delta, nextPosition) {
            if (delta.row > 0) {
              if (isCollapsed(nextPosition)) {
                delta.row += nextVisible('down', nextPosition);
              }
            } else if (delta.row < 0) {
              if (isCollapsed(nextPosition)) {
                delta.row += nextVisible('up', nextPosition);
              }
            }
            if (delta.col > 0) {
              if (isCollapsed(nextPosition)) {
                delta.col += nextVisible('right', nextPosition);
              }
            } else if (delta.col < 0) {
              if (isCollapsed(nextPosition)) {
                delta.col += nextVisible('left', nextPosition);
              }
            }
          };
      switch (position) {
        case 'start':
          return function(delta) {
            currentlySelected = instance.getSelected();
            nextPosition.row = currentlySelected[0] + delta.row;
            nextPosition.col = currentlySelected[1] + delta.col;
            updateDelta(delta, nextPosition);
          };
          break;
        case 'end':
          return function(delta) {
            currentlySelected = instance.getSelected();
            nextPosition.row = currentlySelected[2] + delta.row;
            nextPosition.col = currentlySelected[3] + delta.col;
            updateDelta(delta, nextPosition);
          };
          break;
      }
    },
    modifyRowHeight: function(height, row) {
      if (instance.view.wt.wtTable.rowFilter && isCollapsed({
        row: row,
        col: null
      })) {
        return 0;
      }
    },
    validateGroups: function() {
      var areRangesOverlapping = function(a, b) {
        if ((a[0] < b[0] && a[1] < b[1] && b[0] <= a[1]) || (a[0] > b[0] && b[1] < a[1] && a[0] <= b[1])) {
          return true;
        }
      };
      var configGroups = instance.getSettings().groups,
          cols = [],
          rows = [];
      for (var i = 0,
          groupsLength = configGroups.length; i < groupsLength; i++) {
        if (configGroups[i].rows) {
          if (configGroups[i].rows.length === 1) {
            throw new Error("Grouping error:  Group {" + configGroups[i].rows[0] + "} is invalid. Cannot define single-entry groups.");
            return false;
          } else if (configGroups[i].rows.length === 0) {
            throw new Error("Grouping error:  Cannot define empty groups.");
            return false;
          }
          rows.push(configGroups[i].rows);
          for (var j = 0,
              rowsLength = rows.length; j < rowsLength; j++) {
            if (areRangesOverlapping(configGroups[i].rows, rows[j])) {
              throw new Error("Grouping error:  ranges {" + configGroups[i].rows[0] + ", " + configGroups[i].rows[1] + "} and {" + rows[j][0] + ", " + rows[j][1] + "} are overlapping.");
              return false;
            }
          }
        } else if (configGroups[i].cols) {
          if (configGroups[i].cols.length === 1) {
            throw new Error("Grouping error:  Group {" + configGroups[i].cols[0] + "} is invalid. Cannot define single-entry groups.");
            return false;
          } else if (configGroups[i].cols.length === 0) {
            throw new Error("Grouping error:  Cannot define empty groups.");
            return false;
          }
          cols.push(configGroups[i].cols);
          for (var j = 0,
              colsLength = cols.length; j < colsLength; j++) {
            if (areRangesOverlapping(configGroups[i].cols, cols[j])) {
              throw new Error("Grouping error:  ranges {" + configGroups[i].cols[0] + ", " + configGroups[i].cols[1] + "} and {" + cols[j][0] + ", " + cols[j][1] + "} are overlapping.");
              return false;
            }
          }
        }
      }
      return true;
    },
    afterGetRowHeaderRenderers: function(arr) {
      Handsontable.Grouping.groupIndicatorsFactory(arr, 'vertical');
    },
    afterGetColumnHeaderRenderers: function(arr) {
      Handsontable.Grouping.groupIndicatorsFactory(arr, 'horizontal');
    },
    hookProxy: function(fn, arg) {
      return function() {
        if (instance.getSettings().groups) {
          return arg ? Handsontable.Grouping[fn](arg).apply(this, arguments) : Handsontable.Grouping[fn].apply(this, arguments);
        } else {
          return void 0;
        }
      };
    }
  };
}
Grouping.prototype.beforeInit = function() {};
var init = function() {
  var instance = this,
      groupingSetting = !!(instance.getSettings().groups);
  if (groupingSetting) {
    var headerUpdates = {};
    Handsontable.Grouping = new Grouping(instance);
    if (!instance.getSettings().rowHeaders) {
      headerUpdates.rowHeaders = true;
    }
    if (!instance.getSettings().colHeaders) {
      headerUpdates.colHeaders = true;
    }
    if (headerUpdates.colHeaders || headerUpdates.rowHeaders) {
      instance.updateSettings(headerUpdates);
    }
    var groupConfigValid = Handsontable.Grouping.validateGroups();
    if (!groupConfigValid) {
      return;
    }
    instance.addHook('beforeInit', Handsontable.Grouping.hookProxy('init'));
    instance.addHook('afterUpdateSettings', Handsontable.Grouping.hookProxy('updateGroups'));
    instance.addHook('afterGetColumnHeaderRenderers', Handsontable.Grouping.hookProxy('afterGetColumnHeaderRenderers'));
    instance.addHook('afterGetRowHeaderRenderers', Handsontable.Grouping.hookProxy('afterGetRowHeaderRenderers'));
    instance.addHook('afterGetRowHeader', Handsontable.Grouping.hookProxy('afterGetRowHeader'));
    instance.addHook('afterGetColHeader', Handsontable.Grouping.hookProxy('afterGetColHeader'));
    instance.addHook('beforeOnCellMouseDown', Handsontable.Grouping.hookProxy('toggleGroupVisibility'));
    instance.addHook('modifyTransformStart', Handsontable.Grouping.hookProxy('modifySelectionFactory', 'start'));
    instance.addHook('modifyTransformEnd', Handsontable.Grouping.hookProxy('modifySelectionFactory', 'end'));
    instance.addHook('modifyRowHeight', Handsontable.Grouping.hookProxy('modifyRowHeight'));
  }
};
var updateHeaderWidths = function() {
  var colgroups = document.querySelectorAll('colgroup');
  for (var i = 0,
      colgroupsLength = colgroups.length; i < colgroupsLength; i++) {
    var rowHeaders = colgroups[i].querySelectorAll('col.rowHeader');
    if (rowHeaders.length === 0) {
      return;
    }
    for (var j = 0,
        rowHeadersLength = rowHeaders.length + 1; j < rowHeadersLength; j++) {
      if (rowHeadersLength == 2) {
        return;
      }
      if (j < Handsontable.Grouping.getLevels().rows + 1) {
        if (j == Handsontable.Grouping.getLevels().rows) {
          dom.addClass(rowHeaders[j], 'htGroupColClosest');
        } else {
          dom.addClass(rowHeaders[j], 'htGroupCol');
        }
      }
    }
  }
};
Handsontable.hooks.add('beforeInit', init);
Handsontable.hooks.add('afterUpdateSettings', function() {
  if (this.getSettings().groups && !Handsontable.Grouping) {
    init.call(this, arguments);
  } else if (!this.getSettings().groups && Handsontable.Grouping) {
    Handsontable.Grouping.resetGroups();
    Handsontable.Grouping = void 0;
  }
});
Handsontable.plugins.Grouping = Grouping;


//# 
},{"./../../dom.js":27,"./../../plugins.js":45}],58:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  ManualColumnFreeze: {get: function() {
      return ManualColumnFreeze;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_plugins_46_js__;
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
;
function ManualColumnFreeze(instance) {
  var fixedColumnsCount = instance.getSettings().fixedColumnsLeft;
  var init = function() {
    if (typeof instance.manualColumnPositionsPluginUsages !== 'undefined') {
      instance.manualColumnPositionsPluginUsages.push('manualColumnFreeze');
    } else {
      instance.manualColumnPositionsPluginUsages = ['manualColumnFreeze'];
    }
    bindHooks();
  };
  function addContextMenuEntry(defaultOptions) {
    defaultOptions.items.push(Handsontable.ContextMenu.SEPARATOR, {
      key: 'freeze_column',
      name: function() {
        var selectedColumn = instance.getSelected()[1];
        if (selectedColumn > fixedColumnsCount - 1) {
          return 'Freeze this column';
        } else {
          return 'Unfreeze this column';
        }
      },
      disabled: function() {
        var selection = instance.getSelected();
        return selection[1] !== selection[3];
      },
      callback: function() {
        var selectedColumn = instance.getSelected()[1];
        if (selectedColumn > fixedColumnsCount - 1) {
          freezeColumn(selectedColumn);
        } else {
          unfreezeColumn(selectedColumn);
        }
      }
    });
  }
  function addFixedColumn() {
    instance.updateSettings({fixedColumnsLeft: fixedColumnsCount + 1});
    fixedColumnsCount++;
  }
  function removeFixedColumn() {
    instance.updateSettings({fixedColumnsLeft: fixedColumnsCount - 1});
    fixedColumnsCount--;
  }
  function checkPositionData(col) {
    if (!instance.manualColumnPositions || instance.manualColumnPositions.length === 0) {
      if (!instance.manualColumnPositions) {
        instance.manualColumnPositions = [];
      }
    }
    if (col) {
      if (!instance.manualColumnPositions[col]) {
        createPositionData(col + 1);
      }
    } else {
      createPositionData(instance.countCols());
    }
  }
  function createPositionData(len) {
    if (instance.manualColumnPositions.length < len) {
      for (var i = instance.manualColumnPositions.length; i < len; i++) {
        instance.manualColumnPositions[i] = i;
      }
    }
  }
  function modifyColumnOrder(col, actualCol, returnCol, action) {
    if (returnCol == null) {
      returnCol = col;
    }
    if (action === 'freeze') {
      instance.manualColumnPositions.splice(fixedColumnsCount, 0, instance.manualColumnPositions.splice(actualCol, 1)[0]);
    } else if (action === 'unfreeze') {
      instance.manualColumnPositions.splice(returnCol, 0, instance.manualColumnPositions.splice(actualCol, 1)[0]);
    }
  }
  function getBestColumnReturnPosition(col) {
    var i = fixedColumnsCount,
        j = getModifiedColumnIndex(i),
        initialCol = getModifiedColumnIndex(col);
    while (j < initialCol) {
      i++;
      j = getModifiedColumnIndex(i);
    }
    return i - 1;
  }
  function freezeColumn(col) {
    if (col <= fixedColumnsCount - 1) {
      return;
    }
    var modifiedColumn = getModifiedColumnIndex(col) || col;
    checkPositionData(modifiedColumn);
    modifyColumnOrder(modifiedColumn, col, null, 'freeze');
    addFixedColumn();
    instance.view.wt.wtOverlays.leftOverlay.refresh();
    instance.view.wt.wtOverlays.adjustElementsSize();
  }
  function unfreezeColumn(col) {
    if (col > fixedColumnsCount - 1) {
      return;
    }
    var returnCol = getBestColumnReturnPosition(col);
    var modifiedColumn = getModifiedColumnIndex(col) || col;
    checkPositionData(modifiedColumn);
    modifyColumnOrder(modifiedColumn, col, returnCol, 'unfreeze');
    removeFixedColumn();
    instance.view.wt.wtOverlays.leftOverlay.refresh();
  }
  function getModifiedColumnIndex(col) {
    return instance.manualColumnPositions[col];
  }
  function onModifyCol(col) {
    if (this.manualColumnPositionsPluginUsages.length > 1) {
      return col;
    }
    return getModifiedColumnIndex(col);
  }
  function bindHooks() {
    instance.addHook('modifyCol', onModifyCol);
    instance.addHook('afterContextMenuDefaultOptions', addContextMenuEntry);
  }
  return {
    init: init,
    freezeColumn: freezeColumn,
    unfreezeColumn: unfreezeColumn,
    helpers: {
      addFixedColumn: addFixedColumn,
      removeFixedColumn: removeFixedColumn,
      checkPositionData: checkPositionData,
      modifyColumnOrder: modifyColumnOrder,
      getBestColumnReturnPosition: getBestColumnReturnPosition
    }
  };
}
var init = function init() {
  if (!this.getSettings().manualColumnFreeze) {
    return;
  }
  var mcfPlugin;
  Handsontable.plugins.manualColumnFreeze = ManualColumnFreeze;
  this.manualColumnFreeze = new ManualColumnFreeze(this);
  mcfPlugin = this.manualColumnFreeze;
  mcfPlugin.init.call(this);
};
Handsontable.hooks.add('beforeInit', init);


//# 
},{"./../../plugins.js":45}],59:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  ManualColumnMove: {get: function() {
      return ManualColumnMove;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_helpers_46_js__,
    $___46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47_eventManager_46_js__,
    $___46__46__47__46__46__47_plugins_46_js__;
var helper = ($___46__46__47__46__46__47_helpers_46_js__ = require("./../../helpers.js"), $___46__46__47__46__46__47_helpers_46_js__ && $___46__46__47__46__46__47_helpers_46_js__.__esModule && $___46__46__47__46__46__47_helpers_46_js__ || {default: $___46__46__47__46__46__47_helpers_46_js__});
var dom = ($___46__46__47__46__46__47_dom_46_js__ = require("./../../dom.js"), $___46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47_dom_46_js__});
var eventManagerObject = ($___46__46__47__46__46__47_eventManager_46_js__ = require("./../../eventManager.js"), $___46__46__47__46__46__47_eventManager_46_js__ && $___46__46__47__46__46__47_eventManager_46_js__.__esModule && $___46__46__47__46__46__47_eventManager_46_js__ || {default: $___46__46__47__46__46__47_eventManager_46_js__}).eventManager;
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
;
function ManualColumnMove() {
  var startCol,
      endCol,
      startX,
      startOffset,
      currentCol,
      instance,
      currentTH,
      handle = document.createElement('DIV'),
      guide = document.createElement('DIV'),
      eventManager = eventManagerObject(this);
  handle.className = 'manualColumnMover';
  guide.className = 'manualColumnMoverGuide';
  var saveManualColumnPositions = function() {
    var instance = this;
    Handsontable.hooks.run(instance, 'persistentStateSave', 'manualColumnPositions', instance.manualColumnPositions);
  };
  var loadManualColumnPositions = function() {
    var instance = this;
    var storedState = {};
    Handsontable.hooks.run(instance, 'persistentStateLoad', 'manualColumnPositions', storedState);
    return storedState.value;
  };
  function setupHandlePosition(TH) {
    instance = this;
    currentTH = TH;
    var col = this.view.wt.wtTable.getCoords(TH).col;
    if (col >= 0) {
      currentCol = col;
      var box = currentTH.getBoundingClientRect();
      startOffset = box.left;
      handle.style.top = box.top + 'px';
      handle.style.left = startOffset + 'px';
      instance.rootElement.appendChild(handle);
    }
  }
  function refreshHandlePosition(TH, delta) {
    var box = TH.getBoundingClientRect();
    var handleWidth = 6;
    if (delta > 0) {
      handle.style.left = (box.left + box.width - handleWidth) + 'px';
    } else {
      handle.style.left = box.left + 'px';
    }
  }
  function setupGuidePosition() {
    var instance = this;
    dom.addClass(handle, 'active');
    dom.addClass(guide, 'active');
    var box = currentTH.getBoundingClientRect();
    guide.style.width = box.width + 'px';
    guide.style.height = instance.view.maximumVisibleElementHeight(0) + 'px';
    guide.style.top = handle.style.top;
    guide.style.left = startOffset + 'px';
    instance.rootElement.appendChild(guide);
  }
  function refreshGuidePosition(diff) {
    guide.style.left = startOffset + diff + 'px';
  }
  function hideHandleAndGuide() {
    dom.removeClass(handle, 'active');
    dom.removeClass(guide, 'active');
  }
  var checkColumnHeader = function(element) {
    if (element.tagName != 'BODY') {
      if (element.parentNode.tagName == 'THEAD') {
        return true;
      } else {
        element = element.parentNode;
        return checkColumnHeader(element);
      }
    }
    return false;
  };
  var getTHFromTargetElement = function(element) {
    if (element.tagName != 'TABLE') {
      if (element.tagName == 'TH') {
        return element;
      } else {
        return getTHFromTargetElement(element.parentNode);
      }
    }
    return null;
  };
  var bindEvents = function() {
    var instance = this;
    var pressed;
    eventManager.addEventListener(instance.rootElement, 'mouseover', function(e) {
      if (checkColumnHeader(e.target)) {
        var th = getTHFromTargetElement(e.target);
        if (th) {
          if (pressed) {
            var col = instance.view.wt.wtTable.getCoords(th).col;
            if (col >= 0) {
              endCol = col;
              refreshHandlePosition(e.target, endCol - startCol);
            }
          } else {
            setupHandlePosition.call(instance, th);
          }
        }
      }
    });
    eventManager.addEventListener(instance.rootElement, 'mousedown', function(e) {
      if (dom.hasClass(e.target, 'manualColumnMover')) {
        startX = helper.pageX(e);
        setupGuidePosition.call(instance);
        pressed = instance;
        startCol = currentCol;
        endCol = currentCol;
      }
    });
    eventManager.addEventListener(window, 'mousemove', function(e) {
      if (pressed) {
        refreshGuidePosition(helper.pageX(e) - startX);
      }
    });
    eventManager.addEventListener(window, 'mouseup', function(e) {
      if (pressed) {
        hideHandleAndGuide();
        pressed = false;
        createPositionData(instance.manualColumnPositions, instance.countCols());
        instance.manualColumnPositions.splice(endCol, 0, instance.manualColumnPositions.splice(startCol, 1)[0]);
        instance.forceFullRender = true;
        instance.view.render();
        saveManualColumnPositions.call(instance);
        Handsontable.hooks.run(instance, 'afterColumnMove', startCol, endCol);
        setupHandlePosition.call(instance, currentTH);
      }
    });
    instance.addHook('afterDestroy', unbindEvents);
  };
  var unbindEvents = function() {
    eventManager.clear();
  };
  var createPositionData = function(positionArr, len) {
    if (positionArr.length < len) {
      for (var i = positionArr.length; i < len; i++) {
        positionArr[i] = i;
      }
    }
  };
  this.beforeInit = function() {
    this.manualColumnPositions = [];
  };
  this.init = function(source) {
    var instance = this;
    var manualColMoveEnabled = !!(this.getSettings().manualColumnMove);
    if (manualColMoveEnabled) {
      var initialManualColumnPositions = this.getSettings().manualColumnMove;
      var loadedManualColumnPositions = loadManualColumnPositions.call(instance);
      if (typeof loadedManualColumnPositions != 'undefined') {
        this.manualColumnPositions = loadedManualColumnPositions;
      } else if (Array.isArray(initialManualColumnPositions)) {
        this.manualColumnPositions = initialManualColumnPositions;
      } else {
        this.manualColumnPositions = [];
      }
      if (source == 'afterInit') {
        if (typeof instance.manualColumnPositionsPluginUsages != 'undefined') {
          instance.manualColumnPositionsPluginUsages.push('manualColumnMove');
        } else {
          instance.manualColumnPositionsPluginUsages = ['manualColumnMove'];
        }
        bindEvents.call(this);
        if (this.manualColumnPositions.length > 0) {
          this.forceFullRender = true;
          this.render();
        }
      }
    } else {
      var pluginUsagesIndex = instance.manualColumnPositionsPluginUsages ? instance.manualColumnPositionsPluginUsages.indexOf('manualColumnMove') : -1;
      if (pluginUsagesIndex > -1) {
        unbindEvents.call(this);
        this.manualColumnPositions = [];
        instance.manualColumnPositionsPluginUsages[pluginUsagesIndex] = void 0;
      }
    }
  };
  this.modifyCol = function(col) {
    if (this.getSettings().manualColumnMove) {
      if (typeof this.manualColumnPositions[col] === 'undefined') {
        createPositionData(this.manualColumnPositions, col + 1);
      }
      return this.manualColumnPositions[col];
    }
    return col;
  };
  this.afterRemoveCol = function(index, amount) {
    if (!this.getSettings().manualColumnMove) {
      return;
    }
    var rmindx,
        colpos = this.manualColumnPositions;
    rmindx = colpos.splice(index, amount);
    colpos = colpos.map(function(colpos) {
      var i,
          newpos = colpos;
      for (i = 0; i < rmindx.length; i++) {
        if (colpos > rmindx[i]) {
          newpos--;
        }
      }
      return newpos;
    });
    this.manualColumnPositions = colpos;
  };
  this.afterCreateCol = function(index, amount) {
    if (!this.getSettings().manualColumnMove) {
      return;
    }
    var colpos = this.manualColumnPositions;
    if (!colpos.length) {
      return;
    }
    var addindx = [];
    for (var i = 0; i < amount; i++) {
      addindx.push(index + i);
    }
    if (index >= colpos.length) {
      colpos.concat(addindx);
    } else {
      colpos = colpos.map(function(colpos) {
        return (colpos >= index) ? (colpos + amount) : colpos;
      });
      colpos.splice.apply(colpos, [index, 0].concat(addindx));
    }
    this.manualColumnPositions = colpos;
  };
}
var htManualColumnMove = new ManualColumnMove();
Handsontable.hooks.add('beforeInit', htManualColumnMove.beforeInit);
Handsontable.hooks.add('afterInit', function() {
  htManualColumnMove.init.call(this, 'afterInit');
});
Handsontable.hooks.add('afterUpdateSettings', function() {
  htManualColumnMove.init.call(this, 'afterUpdateSettings');
});
Handsontable.hooks.add('modifyCol', htManualColumnMove.modifyCol);
Handsontable.hooks.add('afterRemoveCol', htManualColumnMove.afterRemoveCol);
Handsontable.hooks.add('afterCreateCol', htManualColumnMove.afterCreateCol);
Handsontable.hooks.register('afterColumnMove');


//# 
},{"./../../dom.js":27,"./../../eventManager.js":41,"./../../helpers.js":42,"./../../plugins.js":45}],60:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  ManualColumnResize: {get: function() {
      return ManualColumnResize;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_helpers_46_js__,
    $___46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47_eventManager_46_js__,
    $___46__46__47__46__46__47_plugins_46_js__;
var helper = ($___46__46__47__46__46__47_helpers_46_js__ = require("./../../helpers.js"), $___46__46__47__46__46__47_helpers_46_js__ && $___46__46__47__46__46__47_helpers_46_js__.__esModule && $___46__46__47__46__46__47_helpers_46_js__ || {default: $___46__46__47__46__46__47_helpers_46_js__});
var dom = ($___46__46__47__46__46__47_dom_46_js__ = require("./../../dom.js"), $___46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47_dom_46_js__});
var eventManagerObject = ($___46__46__47__46__46__47_eventManager_46_js__ = require("./../../eventManager.js"), $___46__46__47__46__46__47_eventManager_46_js__ && $___46__46__47__46__46__47_eventManager_46_js__.__esModule && $___46__46__47__46__46__47_eventManager_46_js__ || {default: $___46__46__47__46__46__47_eventManager_46_js__}).eventManager;
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
;
function ManualColumnResize() {
  var currentTH,
      currentCol,
      currentWidth,
      instance,
      newSize,
      startX,
      startWidth,
      startOffset,
      handle = document.createElement('DIV'),
      guide = document.createElement('DIV'),
      eventManager = eventManagerObject(this);
  handle.className = 'manualColumnResizer';
  guide.className = 'manualColumnResizerGuide';
  var saveManualColumnWidths = function() {
    var instance = this;
    Handsontable.hooks.run(instance, 'persistentStateSave', 'manualColumnWidths', instance.manualColumnWidths);
  };
  var loadManualColumnWidths = function() {
    var instance = this;
    var storedState = {};
    Handsontable.hooks.run(instance, 'persistentStateLoad', 'manualColumnWidths', storedState);
    return storedState.value;
  };
  function setupHandlePosition(TH) {
    instance = this;
    currentTH = TH;
    var col = this.view.wt.wtTable.getCoords(TH).col;
    if (col >= 0) {
      currentCol = col;
      var box = currentTH.getBoundingClientRect();
      startOffset = box.left - 6;
      startWidth = parseInt(box.width, 10);
      handle.style.top = box.top + 'px';
      handle.style.left = startOffset + startWidth + 'px';
      instance.rootElement.appendChild(handle);
    }
  }
  function refreshHandlePosition() {
    handle.style.left = startOffset + currentWidth + 'px';
  }
  function setupGuidePosition() {
    var instance = this;
    dom.addClass(handle, 'active');
    dom.addClass(guide, 'active');
    guide.style.top = handle.style.top;
    guide.style.left = handle.style.left;
    guide.style.height = instance.view.maximumVisibleElementHeight(0) + 'px';
    instance.rootElement.appendChild(guide);
  }
  function refreshGuidePosition() {
    guide.style.left = handle.style.left;
  }
  function hideHandleAndGuide() {
    dom.removeClass(handle, 'active');
    dom.removeClass(guide, 'active');
  }
  var checkColumnHeader = function(element) {
    if (element.tagName != 'BODY') {
      if (element.parentNode.tagName == 'THEAD') {
        return true;
      } else {
        element = element.parentNode;
        return checkColumnHeader(element);
      }
    }
    return false;
  };
  var getTHFromTargetElement = function(element) {
    if (element.tagName != 'TABLE') {
      if (element.tagName == 'TH') {
        return element;
      } else {
        return getTHFromTargetElement(element.parentNode);
      }
    }
    return null;
  };
  var bindEvents = function() {
    var instance = this;
    var pressed;
    var dblclick = 0;
    var autoresizeTimeout = null;
    eventManager.addEventListener(instance.rootElement, 'mouseover', function(e) {
      if (checkColumnHeader(e.target)) {
        var th = getTHFromTargetElement(e.target);
        if (th) {
          if (!pressed) {
            setupHandlePosition.call(instance, th);
          }
        }
      }
    });
    eventManager.addEventListener(instance.rootElement, 'mousedown', function(e) {
      if (dom.hasClass(e.target, 'manualColumnResizer')) {
        setupGuidePosition.call(instance);
        pressed = instance;
        if (autoresizeTimeout == null) {
          autoresizeTimeout = setTimeout(function() {
            if (dblclick >= 2) {
              newSize = instance.determineColumnWidth.call(instance, currentCol);
              setManualSize(currentCol, newSize);
              instance.forceFullRender = true;
              instance.view.render();
              Handsontable.hooks.run(instance, 'afterColumnResize', currentCol, newSize);
            }
            dblclick = 0;
            autoresizeTimeout = null;
          }, 500);
          instance._registerTimeout(autoresizeTimeout);
        }
        dblclick++;
        startX = helper.pageX(e);
        newSize = startWidth;
      }
    });
    eventManager.addEventListener(window, 'mousemove', function(e) {
      if (pressed) {
        currentWidth = startWidth + (helper.pageX(e) - startX);
        newSize = setManualSize(currentCol, currentWidth);
        refreshHandlePosition();
        refreshGuidePosition();
      }
    });
    eventManager.addEventListener(window, 'mouseup', function() {
      if (pressed) {
        hideHandleAndGuide();
        pressed = false;
        if (newSize != startWidth) {
          instance.forceFullRender = true;
          instance.view.render();
          instance.view.wt.wtOverlays.adjustElementsSize();
          saveManualColumnWidths.call(instance);
          Handsontable.hooks.run(instance, 'afterColumnResize', currentCol, newSize);
        }
        setupHandlePosition.call(instance, currentTH);
      }
    });
    instance.addHook('afterDestroy', unbindEvents);
  };
  var unbindEvents = function() {
    eventManager.clear();
  };
  this.beforeInit = function() {
    this.manualColumnWidths = [];
  };
  this.init = function(source) {
    var instance = this;
    var manualColumnWidthEnabled = !!(this.getSettings().manualColumnResize);
    if (manualColumnWidthEnabled) {
      var initialColumnWidths = this.getSettings().manualColumnResize;
      var loadedManualColumnWidths = loadManualColumnWidths.call(instance);
      if (typeof instance.manualColumnWidthsPluginUsages != 'undefined') {
        instance.manualColumnWidthsPluginUsages.push('manualColumnResize');
      } else {
        instance.manualColumnWidthsPluginUsages = ['manualColumnResize'];
      }
      if (typeof loadedManualColumnWidths != 'undefined') {
        this.manualColumnWidths = loadedManualColumnWidths;
      } else if (Array.isArray(initialColumnWidths)) {
        this.manualColumnWidths = initialColumnWidths;
      } else {
        this.manualColumnWidths = [];
      }
      if (source == 'afterInit') {
        bindEvents.call(this);
        if (this.manualColumnWidths.length > 0) {
          this.forceFullRender = true;
          this.render();
        }
      }
    } else {
      var pluginUsagesIndex = instance.manualColumnWidthsPluginUsages ? instance.manualColumnWidthsPluginUsages.indexOf('manualColumnResize') : -1;
      if (pluginUsagesIndex > -1) {
        unbindEvents.call(this);
        this.manualColumnWidths = [];
      }
    }
  };
  var setManualSize = function(col, width) {
    width = Math.max(width, 20);
    col = Handsontable.hooks.run(instance, 'modifyCol', col);
    instance.manualColumnWidths[col] = width;
    return width;
  };
  this.modifyColWidth = function(width, col) {
    col = this.runHooks('modifyCol', col);
    if (this.getSettings().manualColumnResize && this.manualColumnWidths[col]) {
      return this.manualColumnWidths[col];
    }
    return width;
  };
}
var htManualColumnResize = new ManualColumnResize();
Handsontable.hooks.add('beforeInit', htManualColumnResize.beforeInit);
Handsontable.hooks.add('afterInit', function() {
  htManualColumnResize.init.call(this, 'afterInit');
});
Handsontable.hooks.add('afterUpdateSettings', function() {
  htManualColumnResize.init.call(this, 'afterUpdateSettings');
});
Handsontable.hooks.add('modifyColWidth', htManualColumnResize.modifyColWidth);
Handsontable.hooks.register('afterColumnResize');


//# 
},{"./../../dom.js":27,"./../../eventManager.js":41,"./../../helpers.js":42,"./../../plugins.js":45}],61:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  ManualRowMove: {get: function() {
      return ManualRowMove;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_helpers_46_js__,
    $___46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47_eventManager_46_js__,
    $___46__46__47__46__46__47_plugins_46_js__;
var helper = ($___46__46__47__46__46__47_helpers_46_js__ = require("./../../helpers.js"), $___46__46__47__46__46__47_helpers_46_js__ && $___46__46__47__46__46__47_helpers_46_js__.__esModule && $___46__46__47__46__46__47_helpers_46_js__ || {default: $___46__46__47__46__46__47_helpers_46_js__});
var dom = ($___46__46__47__46__46__47_dom_46_js__ = require("./../../dom.js"), $___46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47_dom_46_js__});
var eventManagerObject = ($___46__46__47__46__46__47_eventManager_46_js__ = require("./../../eventManager.js"), $___46__46__47__46__46__47_eventManager_46_js__ && $___46__46__47__46__46__47_eventManager_46_js__.__esModule && $___46__46__47__46__46__47_eventManager_46_js__ || {default: $___46__46__47__46__46__47_eventManager_46_js__}).eventManager;
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
;
function ManualRowMove() {
  var startRow,
      endRow,
      startY,
      startOffset,
      currentRow,
      currentTH,
      handle = document.createElement('DIV'),
      guide = document.createElement('DIV'),
      eventManager = eventManagerObject(this);
  handle.className = 'manualRowMover';
  guide.className = 'manualRowMoverGuide';
  var saveManualRowPositions = function() {
    var instance = this;
    Handsontable.hooks.run(instance, 'persistentStateSave', 'manualRowPositions', instance.manualRowPositions);
  };
  var loadManualRowPositions = function() {
    var instance = this,
        storedState = {};
    Handsontable.hooks.run(instance, 'persistentStateLoad', 'manualRowPositions', storedState);
    return storedState.value;
  };
  function setupHandlePosition(TH) {
    var instance = this;
    currentTH = TH;
    var row = this.view.wt.wtTable.getCoords(TH).row;
    if (row >= 0) {
      currentRow = row;
      var box = currentTH.getBoundingClientRect();
      startOffset = box.top;
      handle.style.top = startOffset + 'px';
      handle.style.left = box.left + 'px';
      instance.rootElement.appendChild(handle);
    }
  }
  function refreshHandlePosition(TH, delta) {
    var box = TH.getBoundingClientRect();
    var handleHeight = 6;
    if (delta > 0) {
      handle.style.top = (box.top + box.height - handleHeight) + 'px';
    } else {
      handle.style.top = box.top + 'px';
    }
  }
  function setupGuidePosition() {
    var instance = this;
    dom.addClass(handle, 'active');
    dom.addClass(guide, 'active');
    var box = currentTH.getBoundingClientRect();
    guide.style.width = instance.view.maximumVisibleElementWidth(0) + 'px';
    guide.style.height = box.height + 'px';
    guide.style.top = startOffset + 'px';
    guide.style.left = handle.style.left;
    instance.rootElement.appendChild(guide);
  }
  function refreshGuidePosition(diff) {
    guide.style.top = startOffset + diff + 'px';
  }
  function hideHandleAndGuide() {
    dom.removeClass(handle, 'active');
    dom.removeClass(guide, 'active');
  }
  var checkRowHeader = function(element) {
    if (element.tagName != 'BODY') {
      if (element.parentNode.tagName == 'TBODY') {
        return true;
      } else {
        element = element.parentNode;
        return checkRowHeader(element);
      }
    }
    return false;
  };
  var getTHFromTargetElement = function(element) {
    if (element.tagName != 'TABLE') {
      if (element.tagName == 'TH') {
        return element;
      } else {
        return getTHFromTargetElement(element.parentNode);
      }
    }
    return null;
  };
  var bindEvents = function() {
    var instance = this;
    var pressed;
    eventManager.addEventListener(instance.rootElement, 'mouseover', function(e) {
      if (checkRowHeader(e.target)) {
        var th = getTHFromTargetElement(e.target);
        if (th) {
          if (pressed) {
            endRow = instance.view.wt.wtTable.getCoords(th).row;
            refreshHandlePosition(th, endRow - startRow);
          } else {
            setupHandlePosition.call(instance, th);
          }
        }
      }
    });
    eventManager.addEventListener(instance.rootElement, 'mousedown', function(e) {
      if (dom.hasClass(e.target, 'manualRowMover')) {
        startY = helper.pageY(e);
        setupGuidePosition.call(instance);
        pressed = instance;
        startRow = currentRow;
        endRow = currentRow;
      }
    });
    eventManager.addEventListener(window, 'mousemove', function(e) {
      if (pressed) {
        refreshGuidePosition(helper.pageY(e) - startY);
      }
    });
    eventManager.addEventListener(window, 'mouseup', function(e) {
      if (pressed) {
        hideHandleAndGuide();
        pressed = false;
        createPositionData(instance.manualRowPositions, instance.countRows());
        instance.manualRowPositions.splice(endRow, 0, instance.manualRowPositions.splice(startRow, 1)[0]);
        instance.forceFullRender = true;
        instance.view.render();
        saveManualRowPositions.call(instance);
        Handsontable.hooks.run(instance, 'afterRowMove', startRow, endRow);
        setupHandlePosition.call(instance, currentTH);
      }
    });
    instance.addHook('afterDestroy', unbindEvents);
  };
  var unbindEvents = function() {
    eventManager.clear();
  };
  var createPositionData = function(positionArr, len) {
    if (positionArr.length < len) {
      for (var i = positionArr.length; i < len; i++) {
        positionArr[i] = i;
      }
    }
  };
  this.beforeInit = function() {
    this.manualRowPositions = [];
  };
  this.init = function(source) {
    var instance = this;
    var manualRowMoveEnabled = !!(instance.getSettings().manualRowMove);
    if (manualRowMoveEnabled) {
      var initialManualRowPositions = instance.getSettings().manualRowMove;
      var loadedManualRowPostions = loadManualRowPositions.call(instance);
      if (typeof instance.manualRowPositionsPluginUsages != 'undefined') {
        instance.manualRowPositionsPluginUsages.push('manualColumnMove');
      } else {
        instance.manualRowPositionsPluginUsages = ['manualColumnMove'];
      }
      if (typeof loadedManualRowPostions != 'undefined') {
        this.manualRowPositions = loadedManualRowPostions;
      } else if (Array.isArray(initialManualRowPositions)) {
        this.manualRowPositions = initialManualRowPositions;
      } else {
        this.manualRowPositions = [];
      }
      if (source === 'afterInit') {
        bindEvents.call(this);
        if (this.manualRowPositions.length > 0) {
          instance.forceFullRender = true;
          instance.render();
        }
      }
    } else {
      var pluginUsagesIndex = instance.manualRowPositionsPluginUsages ? instance.manualRowPositionsPluginUsages.indexOf('manualColumnMove') : -1;
      if (pluginUsagesIndex > -1) {
        unbindEvents.call(this);
        instance.manualRowPositions = [];
        instance.manualRowPositionsPluginUsages[pluginUsagesIndex] = void 0;
      }
    }
  };
  this.modifyRow = function(row) {
    var instance = this;
    if (instance.getSettings().manualRowMove) {
      if (typeof instance.manualRowPositions[row] === 'undefined') {
        createPositionData(this.manualRowPositions, row + 1);
      }
      return instance.manualRowPositions[row];
    }
    return row;
  };
}
var htManualRowMove = new ManualRowMove();
Handsontable.hooks.add('beforeInit', htManualRowMove.beforeInit);
Handsontable.hooks.add('afterInit', function() {
  htManualRowMove.init.call(this, 'afterInit');
});
Handsontable.hooks.add('afterUpdateSettings', function() {
  htManualRowMove.init.call(this, 'afterUpdateSettings');
});
Handsontable.hooks.add('modifyRow', htManualRowMove.modifyRow);
Handsontable.hooks.register('afterRowMove');


//# 
},{"./../../dom.js":27,"./../../eventManager.js":41,"./../../helpers.js":42,"./../../plugins.js":45}],62:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  ManualRowResize: {get: function() {
      return ManualRowResize;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_helpers_46_js__,
    $___46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47_eventManager_46_js__,
    $___46__46__47__46__46__47_plugins_46_js__;
var helper = ($___46__46__47__46__46__47_helpers_46_js__ = require("./../../helpers.js"), $___46__46__47__46__46__47_helpers_46_js__ && $___46__46__47__46__46__47_helpers_46_js__.__esModule && $___46__46__47__46__46__47_helpers_46_js__ || {default: $___46__46__47__46__46__47_helpers_46_js__});
var dom = ($___46__46__47__46__46__47_dom_46_js__ = require("./../../dom.js"), $___46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47_dom_46_js__});
var eventManagerObject = ($___46__46__47__46__46__47_eventManager_46_js__ = require("./../../eventManager.js"), $___46__46__47__46__46__47_eventManager_46_js__ && $___46__46__47__46__46__47_eventManager_46_js__.__esModule && $___46__46__47__46__46__47_eventManager_46_js__ || {default: $___46__46__47__46__46__47_eventManager_46_js__}).eventManager;
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
;
function ManualRowResize() {
  var currentTH,
      currentRow,
      currentHeight,
      instance,
      newSize,
      startY,
      startHeight,
      startOffset,
      handle = document.createElement('DIV'),
      guide = document.createElement('DIV'),
      eventManager = eventManagerObject(this);
  handle.className = 'manualRowResizer';
  guide.className = 'manualRowResizerGuide';
  var saveManualRowHeights = function() {
    var instance = this;
    Handsontable.hooks.run(instance, 'persistentStateSave', 'manualRowHeights', instance.manualRowHeights);
  };
  var loadManualRowHeights = function() {
    var instance = this,
        storedState = {};
    Handsontable.hooks.run(instance, 'persistentStateLoad', 'manualRowHeights', storedState);
    return storedState.value;
  };
  function setupHandlePosition(TH) {
    instance = this;
    currentTH = TH;
    var row = this.view.wt.wtTable.getCoords(TH).row;
    if (row >= 0) {
      currentRow = row;
      var box = currentTH.getBoundingClientRect();
      startOffset = box.top - 6;
      startHeight = parseInt(box.height, 10);
      handle.style.left = box.left + 'px';
      handle.style.top = startOffset + startHeight + 'px';
      instance.rootElement.appendChild(handle);
    }
  }
  function refreshHandlePosition() {
    handle.style.top = startOffset + currentHeight + 'px';
  }
  function setupGuidePosition() {
    var instance = this;
    dom.addClass(handle, 'active');
    dom.addClass(guide, 'active');
    guide.style.top = handle.style.top;
    guide.style.left = handle.style.left;
    guide.style.width = instance.view.maximumVisibleElementWidth(0) + 'px';
    instance.rootElement.appendChild(guide);
  }
  function refreshGuidePosition() {
    guide.style.top = handle.style.top;
  }
  function hideHandleAndGuide() {
    dom.removeClass(handle, 'active');
    dom.removeClass(guide, 'active');
  }
  var checkRowHeader = function(element) {
    if (element.tagName != 'BODY') {
      if (element.parentNode.tagName == 'TBODY') {
        return true;
      } else {
        element = element.parentNode;
        return checkRowHeader(element);
      }
    }
    return false;
  };
  var getTHFromTargetElement = function(element) {
    if (element.tagName != 'TABLE') {
      if (element.tagName == 'TH') {
        return element;
      } else {
        return getTHFromTargetElement(element.parentNode);
      }
    }
    return null;
  };
  var bindEvents = function() {
    var instance = this;
    var pressed;
    var dblclick = 0;
    var autoresizeTimeout = null;
    eventManager.addEventListener(instance.rootElement, 'mouseover', function(e) {
      if (checkRowHeader(e.target)) {
        var th = getTHFromTargetElement(e.target);
        if (th) {
          if (!pressed) {
            setupHandlePosition.call(instance, th);
          }
        }
      }
    });
    eventManager.addEventListener(instance.rootElement, 'mousedown', function(e) {
      if (dom.hasClass(e.target, 'manualRowResizer')) {
        setupGuidePosition.call(instance);
        pressed = instance;
        if (autoresizeTimeout == null) {
          autoresizeTimeout = setTimeout(function() {
            if (dblclick >= 2) {
              setManualSize(currentRow, null);
              instance.forceFullRender = true;
              instance.view.render();
              Handsontable.hooks.run(instance, 'afterRowResize', currentRow, newSize);
            }
            dblclick = 0;
            autoresizeTimeout = null;
          }, 500);
          instance._registerTimeout(autoresizeTimeout);
        }
        dblclick++;
        startY = helper.pageY(e);
        newSize = startHeight;
      }
    });
    eventManager.addEventListener(window, 'mousemove', function(e) {
      if (pressed) {
        currentHeight = startHeight + (helper.pageY(e) - startY);
        newSize = setManualSize(currentRow, currentHeight);
        refreshHandlePosition();
        refreshGuidePosition();
      }
    });
    eventManager.addEventListener(window, 'mouseup', function(e) {
      if (pressed) {
        hideHandleAndGuide();
        pressed = false;
        if (newSize != startHeight) {
          instance.forceFullRender = true;
          instance.view.render();
          saveManualRowHeights.call(instance);
          Handsontable.hooks.run(instance, 'afterRowResize', currentRow, newSize);
        }
        setupHandlePosition.call(instance, currentTH);
      }
    });
    instance.addHook('afterDestroy', unbindEvents);
  };
  var unbindEvents = function() {
    eventManager.clear();
  };
  this.beforeInit = function() {
    this.manualRowHeights = [];
  };
  this.init = function(source) {
    var instance = this;
    var manualColumnHeightEnabled = !!(this.getSettings().manualRowResize);
    if (manualColumnHeightEnabled) {
      var initialRowHeights = this.getSettings().manualRowResize;
      var loadedManualRowHeights = loadManualRowHeights.call(instance);
      if (typeof instance.manualRowHeightsPluginUsages != 'undefined') {
        instance.manualRowHeightsPluginUsages.push('manualRowResize');
      } else {
        instance.manualRowHeightsPluginUsages = ['manualRowResize'];
      }
      if (typeof loadedManualRowHeights != 'undefined') {
        this.manualRowHeights = loadedManualRowHeights;
      } else if (Array.isArray(initialRowHeights)) {
        this.manualRowHeights = initialRowHeights;
      } else {
        this.manualRowHeights = [];
      }
      if (source === 'afterInit') {
        bindEvents.call(this);
        if (this.manualRowHeights.length > 0) {
          this.forceFullRender = true;
          this.render();
        }
      } else {
        this.forceFullRender = true;
        this.render();
      }
    } else {
      var pluginUsagesIndex = instance.manualRowHeightsPluginUsages ? instance.manualRowHeightsPluginUsages.indexOf('manualRowResize') : -1;
      if (pluginUsagesIndex > -1) {
        unbindEvents.call(this);
        this.manualRowHeights = [];
        instance.manualRowHeightsPluginUsages[pluginUsagesIndex] = void 0;
      }
    }
  };
  var setManualSize = function(row, height) {
    row = Handsontable.hooks.run(instance, 'modifyRow', row);
    instance.manualRowHeights[row] = height;
    return height;
  };
  this.modifyRowHeight = function(height, row) {
    if (this.getSettings().manualRowResize) {
      row = this.runHooks('modifyRow', row);
      if (this.manualRowHeights[row] !== void 0) {
        return this.manualRowHeights[row];
      }
    }
    return height;
  };
}
var htManualRowResize = new ManualRowResize();
Handsontable.hooks.add('beforeInit', htManualRowResize.beforeInit);
Handsontable.hooks.add('afterInit', function() {
  htManualRowResize.init.call(this, 'afterInit');
});
Handsontable.hooks.add('afterUpdateSettings', function() {
  htManualRowResize.init.call(this, 'afterUpdateSettings');
});
Handsontable.hooks.add('modifyRowHeight', htManualRowResize.modifyRowHeight);
Handsontable.hooks.register('afterRowResize');


//# 
},{"./../../dom.js":27,"./../../eventManager.js":41,"./../../helpers.js":42,"./../../plugins.js":45}],63:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  MergeCells: {get: function() {
      return MergeCells;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_plugins_46_js__,
    $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__,
    $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__,
    $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_table_46_js__;
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
var WalkontableCellCoords = ($___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ = require("./../../3rdparty/walkontable/src/cell/coords.js"), $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__.__esModule && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ || {default: $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__}).WalkontableCellCoords;
var WalkontableCellRange = ($___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__ = require("./../../3rdparty/walkontable/src/cell/range.js"), $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__ && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__.__esModule && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__ || {default: $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_range_46_js__}).WalkontableCellRange;
var WalkontableTable = ($___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_table_46_js__ = require("./../../3rdparty/walkontable/src/table.js"), $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_table_46_js__ && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_table_46_js__.__esModule && $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_table_46_js__ || {default: $___46__46__47__46__46__47_3rdparty_47_walkontable_47_src_47_table_46_js__}).WalkontableTable;
;
function CellInfoCollection() {
  var collection = [];
  collection.getInfo = function(row, col) {
    for (var i = 0,
        ilen = this.length; i < ilen; i++) {
      if (this[i].row <= row && this[i].row + this[i].rowspan - 1 >= row && this[i].col <= col && this[i].col + this[i].colspan - 1 >= col) {
        return this[i];
      }
    }
  };
  collection.setInfo = function(info) {
    for (var i = 0,
        ilen = this.length; i < ilen; i++) {
      if (this[i].row === info.row && this[i].col === info.col) {
        this[i] = info;
        return;
      }
    }
    this.push(info);
  };
  collection.removeInfo = function(row, col) {
    for (var i = 0,
        ilen = this.length; i < ilen; i++) {
      if (this[i].row === row && this[i].col === col) {
        this.splice(i, 1);
        break;
      }
    }
  };
  return collection;
}
function MergeCells(mergeCellsSetting) {
  this.mergedCellInfoCollection = new CellInfoCollection();
  if (Array.isArray(mergeCellsSetting)) {
    for (var i = 0,
        ilen = mergeCellsSetting.length; i < ilen; i++) {
      this.mergedCellInfoCollection.setInfo(mergeCellsSetting[i]);
    }
  }
}
MergeCells.prototype.canMergeRange = function(cellRange) {
  return !cellRange.isSingle();
};
MergeCells.prototype.mergeRange = function(cellRange) {
  if (!this.canMergeRange(cellRange)) {
    return;
  }
  var topLeft = cellRange.getTopLeftCorner();
  var bottomRight = cellRange.getBottomRightCorner();
  var mergeParent = {};
  mergeParent.row = topLeft.row;
  mergeParent.col = topLeft.col;
  mergeParent.rowspan = bottomRight.row - topLeft.row + 1;
  mergeParent.colspan = bottomRight.col - topLeft.col + 1;
  this.mergedCellInfoCollection.setInfo(mergeParent);
};
MergeCells.prototype.mergeOrUnmergeSelection = function(cellRange) {
  var info = this.mergedCellInfoCollection.getInfo(cellRange.from.row, cellRange.from.col);
  if (info) {
    this.unmergeSelection(cellRange.from);
  } else {
    this.mergeSelection(cellRange);
  }
};
MergeCells.prototype.mergeSelection = function(cellRange) {
  this.mergeRange(cellRange);
};
MergeCells.prototype.unmergeSelection = function(cellRange) {
  var info = this.mergedCellInfoCollection.getInfo(cellRange.row, cellRange.col);
  this.mergedCellInfoCollection.removeInfo(info.row, info.col);
};
MergeCells.prototype.applySpanProperties = function(TD, row, col) {
  var info = this.mergedCellInfoCollection.getInfo(row, col);
  if (info) {
    if (info.row === row && info.col === col) {
      TD.setAttribute('rowspan', info.rowspan);
      TD.setAttribute('colspan', info.colspan);
    } else {
      TD.removeAttribute('rowspan');
      TD.removeAttribute('colspan');
      TD.style.display = "none";
    }
  } else {
    TD.removeAttribute('rowspan');
    TD.removeAttribute('colspan');
  }
};
MergeCells.prototype.modifyTransform = function(hook, currentSelectedRange, delta) {
  var sameRowspan = function(merged, coords) {
    if (coords.row >= merged.row && coords.row <= (merged.row + merged.rowspan - 1)) {
      return true;
    }
    return false;
  },
      sameColspan = function(merged, coords) {
        if (coords.col >= merged.col && coords.col <= (merged.col + merged.colspan - 1)) {
          return true;
        }
        return false;
      },
      getNextPosition = function(newDelta) {
        return new WalkontableCellCoords(currentSelectedRange.to.row + newDelta.row, currentSelectedRange.to.col + newDelta.col);
      };
  var newDelta = {
    row: delta.row,
    col: delta.col
  };
  if (hook == 'modifyTransformStart') {
    if (!this.lastDesiredCoords) {
      this.lastDesiredCoords = new WalkontableCellCoords(null, null);
    }
    var currentPosition = new WalkontableCellCoords(currentSelectedRange.highlight.row, currentSelectedRange.highlight.col),
        mergedParent = this.mergedCellInfoCollection.getInfo(currentPosition.row, currentPosition.col),
        currentRangeContainsMerge;
    for (var i = 0,
        mergesLength = this.mergedCellInfoCollection.length; i < mergesLength; i++) {
      var range = this.mergedCellInfoCollection[i];
      range = new WalkontableCellCoords(range.row + range.rowspan - 1, range.col + range.colspan - 1);
      if (currentSelectedRange.includes(range)) {
        currentRangeContainsMerge = true;
        break;
      }
    }
    if (mergedParent) {
      var mergeTopLeft = new WalkontableCellCoords(mergedParent.row, mergedParent.col),
          mergeBottomRight = new WalkontableCellCoords(mergedParent.row + mergedParent.rowspan - 1, mergedParent.col + mergedParent.colspan - 1),
          mergeRange = new WalkontableCellRange(mergeTopLeft, mergeTopLeft, mergeBottomRight);
      if (!mergeRange.includes(this.lastDesiredCoords)) {
        this.lastDesiredCoords = new WalkontableCellCoords(null, null);
      }
      newDelta.row = this.lastDesiredCoords.row ? this.lastDesiredCoords.row - currentPosition.row : newDelta.row;
      newDelta.col = this.lastDesiredCoords.col ? this.lastDesiredCoords.col - currentPosition.col : newDelta.col;
      if (delta.row > 0) {
        newDelta.row = mergedParent.row + mergedParent.rowspan - 1 - currentPosition.row + delta.row;
      } else if (delta.row < 0) {
        newDelta.row = currentPosition.row - mergedParent.row + delta.row;
      }
      if (delta.col > 0) {
        newDelta.col = mergedParent.col + mergedParent.colspan - 1 - currentPosition.col + delta.col;
      } else if (delta.col < 0) {
        newDelta.col = currentPosition.col - mergedParent.col + delta.col;
      }
    }
    var nextPosition = new WalkontableCellCoords(currentSelectedRange.highlight.row + newDelta.row, currentSelectedRange.highlight.col + newDelta.col),
        nextParentIsMerged = this.mergedCellInfoCollection.getInfo(nextPosition.row, nextPosition.col);
    if (nextParentIsMerged) {
      this.lastDesiredCoords = nextPosition;
      newDelta = {
        row: nextParentIsMerged.row - currentPosition.row,
        col: nextParentIsMerged.col - currentPosition.col
      };
    }
  } else if (hook == 'modifyTransformEnd') {
    for (var i = 0,
        mergesLength = this.mergedCellInfoCollection.length; i < mergesLength; i++) {
      var currentMerge = this.mergedCellInfoCollection[i],
          mergeTopLeft = new WalkontableCellCoords(currentMerge.row, currentMerge.col),
          mergeBottomRight = new WalkontableCellCoords(currentMerge.row + currentMerge.rowspan - 1, currentMerge.col + currentMerge.colspan - 1),
          mergedRange = new WalkontableCellRange(mergeTopLeft, mergeTopLeft, mergeBottomRight),
          sharedBorders = currentSelectedRange.getBordersSharedWith(mergedRange);
      if (mergedRange.isEqual(currentSelectedRange)) {
        currentSelectedRange.setDirection("NW-SE");
      } else if (sharedBorders.length > 0) {
        var mergeHighlighted = (currentSelectedRange.highlight.isEqual(mergedRange.from));
        if (sharedBorders.indexOf('top') > -1) {
          if (currentSelectedRange.to.isSouthEastOf(mergedRange.from) && mergeHighlighted) {
            currentSelectedRange.setDirection("NW-SE");
          } else if (currentSelectedRange.to.isSouthWestOf(mergedRange.from) && mergeHighlighted) {
            currentSelectedRange.setDirection("NE-SW");
          }
        } else if (sharedBorders.indexOf('bottom') > -1) {
          if (currentSelectedRange.to.isNorthEastOf(mergedRange.from) && mergeHighlighted) {
            currentSelectedRange.setDirection("SW-NE");
          } else if (currentSelectedRange.to.isNorthWestOf(mergedRange.from) && mergeHighlighted) {
            currentSelectedRange.setDirection("SE-NW");
          }
        }
      }
      var nextPosition = getNextPosition(newDelta),
          withinRowspan = sameRowspan(currentMerge, nextPosition),
          withinColspan = sameColspan(currentMerge, nextPosition);
      if (currentSelectedRange.includesRange(mergedRange) && (mergedRange.includes(nextPosition) || withinRowspan || withinColspan)) {
        if (withinRowspan) {
          if (newDelta.row < 0) {
            newDelta.row -= currentMerge.rowspan - 1;
          } else if (newDelta.row > 0) {
            newDelta.row += currentMerge.rowspan - 1;
          }
        }
        if (withinColspan) {
          if (newDelta.col < 0) {
            newDelta.col -= currentMerge.colspan - 1;
          } else if (newDelta.col > 0) {
            newDelta.col += currentMerge.colspan - 1;
          }
        }
      }
    }
  }
  if (newDelta.row !== 0) {
    delta.row = newDelta.row;
  }
  if (newDelta.col !== 0) {
    delta.col = newDelta.col;
  }
};
var beforeInit = function() {
  var instance = this;
  var mergeCellsSetting = instance.getSettings().mergeCells;
  if (mergeCellsSetting) {
    if (!instance.mergeCells) {
      instance.mergeCells = new MergeCells(mergeCellsSetting);
    }
  }
};
var afterInit = function() {
  var instance = this;
  if (instance.mergeCells) {
    instance.view.wt.wtTable.getCell = function(coords) {
      if (instance.getSettings().mergeCells) {
        var mergeParent = instance.mergeCells.mergedCellInfoCollection.getInfo(coords.row, coords.col);
        if (mergeParent) {
          coords = mergeParent;
        }
      }
      return WalkontableTable.prototype.getCell.call(this, coords);
    };
  }
};
var onBeforeKeyDown = function(event) {
  if (!this.mergeCells) {
    return;
  }
  var ctrlDown = (event.ctrlKey || event.metaKey) && !event.altKey;
  if (ctrlDown) {
    if (event.keyCode === 77) {
      this.mergeCells.mergeOrUnmergeSelection(this.getSelectedRange());
      this.render();
      event.stopImmediatePropagation();
    }
  }
};
var addMergeActionsToContextMenu = function(defaultOptions) {
  if (!this.getSettings().mergeCells) {
    return;
  }
  defaultOptions.items.push(Handsontable.ContextMenu.SEPARATOR);
  defaultOptions.items.push({
    key: 'mergeCells',
    name: function() {
      var sel = this.getSelected();
      var info = this.mergeCells.mergedCellInfoCollection.getInfo(sel[0], sel[1]);
      if (info) {
        return 'Unmerge cells';
      } else {
        return 'Merge cells';
      }
    },
    callback: function() {
      this.mergeCells.mergeOrUnmergeSelection(this.getSelectedRange());
      this.render();
    },
    disabled: function() {
      return false;
    }
  });
};
var afterRenderer = function(TD, row, col, prop, value, cellProperties) {
  if (this.mergeCells) {
    this.mergeCells.applySpanProperties(TD, row, col);
  }
};
var modifyTransformFactory = function(hook) {
  return function(delta) {
    var mergeCellsSetting = this.getSettings().mergeCells;
    if (mergeCellsSetting) {
      var currentSelectedRange = this.getSelectedRange();
      this.mergeCells.modifyTransform(hook, currentSelectedRange, delta);
      if (hook === "modifyTransformEnd") {
        var totalRows = this.countRows();
        var totalCols = this.countCols();
        if (currentSelectedRange.from.row < 0) {
          currentSelectedRange.from.row = 0;
        } else if (currentSelectedRange.from.row > 0 && currentSelectedRange.from.row >= totalRows) {
          currentSelectedRange.from.row = currentSelectedRange.from - 1;
        }
        if (currentSelectedRange.from.col < 0) {
          currentSelectedRange.from.col = 0;
        } else if (currentSelectedRange.from.col > 0 && currentSelectedRange.from.col >= totalCols) {
          currentSelectedRange.from.col = totalCols - 1;
        }
      }
    }
  };
};
var beforeSetRangeEnd = function(coords) {
  this.lastDesiredCoords = null;
  var mergeCellsSetting = this.getSettings().mergeCells;
  if (mergeCellsSetting) {
    var selRange = this.getSelectedRange();
    selRange.highlight = new WalkontableCellCoords(selRange.highlight.row, selRange.highlight.col);
    selRange.to = coords;
    var rangeExpanded = false;
    do {
      rangeExpanded = false;
      for (var i = 0,
          ilen = this.mergeCells.mergedCellInfoCollection.length; i < ilen; i++) {
        var cellInfo = this.mergeCells.mergedCellInfoCollection[i];
        var mergedCellTopLeft = new WalkontableCellCoords(cellInfo.row, cellInfo.col);
        var mergedCellBottomRight = new WalkontableCellCoords(cellInfo.row + cellInfo.rowspan - 1, cellInfo.col + cellInfo.colspan - 1);
        var mergedCellRange = new WalkontableCellRange(mergedCellTopLeft, mergedCellTopLeft, mergedCellBottomRight);
        if (selRange.expandByRange(mergedCellRange)) {
          coords.row = selRange.to.row;
          coords.col = selRange.to.col;
          rangeExpanded = true;
        }
      }
    } while (rangeExpanded);
  }
};
var beforeDrawAreaBorders = function(corners, className) {
  if (className && className == 'area') {
    var mergeCellsSetting = this.getSettings().mergeCells;
    if (mergeCellsSetting) {
      var selRange = this.getSelectedRange();
      var startRange = new WalkontableCellRange(selRange.from, selRange.from, selRange.from);
      var stopRange = new WalkontableCellRange(selRange.to, selRange.to, selRange.to);
      for (var i = 0,
          ilen = this.mergeCells.mergedCellInfoCollection.length; i < ilen; i++) {
        var cellInfo = this.mergeCells.mergedCellInfoCollection[i];
        var mergedCellTopLeft = new WalkontableCellCoords(cellInfo.row, cellInfo.col);
        var mergedCellBottomRight = new WalkontableCellCoords(cellInfo.row + cellInfo.rowspan - 1, cellInfo.col + cellInfo.colspan - 1);
        var mergedCellRange = new WalkontableCellRange(mergedCellTopLeft, mergedCellTopLeft, mergedCellBottomRight);
        if (startRange.expandByRange(mergedCellRange)) {
          corners[0] = startRange.from.row;
          corners[1] = startRange.from.col;
        }
        if (stopRange.expandByRange(mergedCellRange)) {
          corners[2] = stopRange.from.row;
          corners[3] = stopRange.from.col;
        }
      }
    }
  }
};
var afterGetCellMeta = function(row, col, cellProperties) {
  var mergeCellsSetting = this.getSettings().mergeCells;
  if (mergeCellsSetting) {
    var mergeParent = this.mergeCells.mergedCellInfoCollection.getInfo(row, col);
    if (mergeParent && (mergeParent.row != row || mergeParent.col != col)) {
      cellProperties.copyable = false;
    }
  }
};
var afterViewportRowCalculatorOverride = function(calc) {
  var mergeCellsSetting = this.getSettings().mergeCells;
  if (mergeCellsSetting) {
    var colCount = this.countCols();
    var mergeParent;
    for (var c = 0; c < colCount; c++) {
      mergeParent = this.mergeCells.mergedCellInfoCollection.getInfo(calc.startRow, c);
      if (mergeParent) {
        if (mergeParent.row < calc.startRow) {
          calc.startRow = mergeParent.row;
          return afterViewportRowCalculatorOverride.call(this, calc);
        }
      }
      mergeParent = this.mergeCells.mergedCellInfoCollection.getInfo(calc.endRow, c);
      if (mergeParent) {
        var mergeEnd = mergeParent.row + mergeParent.rowspan - 1;
        if (mergeEnd > calc.endRow) {
          calc.endRow = mergeEnd;
          return afterViewportRowCalculatorOverride.call(this, calc);
        }
      }
    }
  }
};
var afterViewportColumnCalculatorOverride = function(calc) {
  var mergeCellsSetting = this.getSettings().mergeCells;
  if (mergeCellsSetting) {
    var rowCount = this.countRows();
    var mergeParent;
    for (var r = 0; r < rowCount; r++) {
      mergeParent = this.mergeCells.mergedCellInfoCollection.getInfo(r, calc.startColumn);
      if (mergeParent) {
        if (mergeParent.col < calc.startColumn) {
          calc.startColumn = mergeParent.col;
          return afterViewportColumnCalculatorOverride.call(this, calc);
        }
      }
      mergeParent = this.mergeCells.mergedCellInfoCollection.getInfo(r, calc.endColumn);
      if (mergeParent) {
        var mergeEnd = mergeParent.col + mergeParent.colspan - 1;
        if (mergeEnd > calc.endColumn) {
          calc.endColumn = mergeEnd;
          return afterViewportColumnCalculatorOverride.call(this, calc);
        }
      }
    }
  }
};
var isMultipleSelection = function(isMultiple) {
  if (isMultiple && this.mergeCells) {
    var mergedCells = this.mergeCells.mergedCellInfoCollection,
        selectionRange = this.getSelectedRange();
    for (var group in mergedCells) {
      if (selectionRange.highlight.row == mergedCells[group].row && selectionRange.highlight.col == mergedCells[group].col && selectionRange.to.row == mergedCells[group].row + mergedCells[group].rowspan - 1 && selectionRange.to.col == mergedCells[group].col + mergedCells[group].colspan - 1) {
        return false;
      }
    }
  }
  return isMultiple;
};
function afterAutofillApplyValues(select, drag) {
  var mergeCellsSetting = this.getSettings().mergeCells;
  if (!mergeCellsSetting || this.selection.isMultiple()) {
    return;
  }
  var info = this.mergeCells.mergedCellInfoCollection.getInfo(select[0], select[1]);
  if (info) {
    select[0] = info.row;
    select[1] = info.col;
    select[2] = info.row + info.rowspan - 1;
    select[3] = info.col + info.colspan - 1;
  }
}
Handsontable.hooks.add('beforeInit', beforeInit);
Handsontable.hooks.add('afterInit', afterInit);
Handsontable.hooks.add('beforeKeyDown', onBeforeKeyDown);
Handsontable.hooks.add('modifyTransformStart', modifyTransformFactory('modifyTransformStart'));
Handsontable.hooks.add('modifyTransformEnd', modifyTransformFactory('modifyTransformEnd'));
Handsontable.hooks.add('beforeSetRangeEnd', beforeSetRangeEnd);
Handsontable.hooks.add('beforeDrawBorders', beforeDrawAreaBorders);
Handsontable.hooks.add('afterIsMultipleSelection', isMultipleSelection);
Handsontable.hooks.add('afterRenderer', afterRenderer);
Handsontable.hooks.add('afterContextMenuDefaultOptions', addMergeActionsToContextMenu);
Handsontable.hooks.add('afterGetCellMeta', afterGetCellMeta);
Handsontable.hooks.add('afterViewportRowCalculatorOverride', afterViewportRowCalculatorOverride);
Handsontable.hooks.add('afterViewportColumnCalculatorOverride', afterViewportColumnCalculatorOverride);
Handsontable.hooks.add('afterAutofillApplyValues', afterAutofillApplyValues);
Handsontable.MergeCells = MergeCells;


//# 
},{"./../../3rdparty/walkontable/src/cell/coords.js":5,"./../../3rdparty/walkontable/src/cell/range.js":6,"./../../3rdparty/walkontable/src/table.js":20,"./../../plugins.js":45}],64:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  default: {get: function() {
      return $__default;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__95_base_46_js__,
    $___46__46__47__46__46__47_eventManager_46_js__,
    $___46__46__47__46__46__47_plugins_46_js__;
var dom = ($___46__46__47__46__46__47_dom_46_js__ = require("./../../dom.js"), $___46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47_dom_46_js__});
var BasePlugin = ($___46__46__47__95_base_46_js__ = require("./../_base.js"), $___46__46__47__95_base_46_js__ && $___46__46__47__95_base_46_js__.__esModule && $___46__46__47__95_base_46_js__ || {default: $___46__46__47__95_base_46_js__}).default;
var eventManagerObject = ($___46__46__47__46__46__47_eventManager_46_js__ = require("./../../eventManager.js"), $___46__46__47__46__46__47_eventManager_46_js__ && $___46__46__47__46__46__47_eventManager_46_js__.__esModule && $___46__46__47__46__46__47_eventManager_46_js__ || {default: $___46__46__47__46__46__47_eventManager_46_js__}).eventManager;
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
var MultipleSelectionHandles = function MultipleSelectionHandles(hotInstance) {
  var $__3 = this;
  $traceurRuntime.superConstructor($MultipleSelectionHandles).call(this, hotInstance);
  this.dragged = [];
  this.eventManager = eventManagerObject(this.hot);
  this.bindTouchEvents();
  this.hot.addHook('afterInit', (function() {
    return $__3.init();
  }));
};
var $MultipleSelectionHandles = MultipleSelectionHandles;
($traceurRuntime.createClass)(MultipleSelectionHandles, {
  init: function() {
    this.lastSetCell = null;
    Handsontable.plugins.multipleSelectionHandles = new $MultipleSelectionHandles(this.hot);
  },
  bindTouchEvents: function() {
    var _this = this;
    function removeFromDragged(query) {
      if (_this.dragged.length === 1) {
        _this.dragged.splice(0, _this.dragged.length);
        return true;
      }
      var entryPosition = _this.dragged.indexOf(query);
      if (entryPosition == -1) {
        return false;
      } else if (entryPosition === 0) {
        _this.dragged = _this.dragged.slice(0, 1);
      } else if (entryPosition == 1) {
        _this.dragged = _this.dragged.slice(-1);
      }
    }
    this.eventManager.addEventListener(this.hot.rootElement, 'touchstart', function(event) {
      var selectedRange;
      if (dom.hasClass(event.target, "topLeftSelectionHandle-HitArea")) {
        selectedRange = _this.hot.getSelectedRange();
        _this.dragged.push("topLeft");
        _this.touchStartRange = {
          width: selectedRange.getWidth(),
          height: selectedRange.getHeight(),
          direction: selectedRange.getDirection()
        };
        event.preventDefault();
        return false;
      } else if (dom.hasClass(event.target, "bottomRightSelectionHandle-HitArea")) {
        selectedRange = _this.hot.getSelectedRange();
        _this.dragged.push("bottomRight");
        _this.touchStartRange = {
          width: selectedRange.getWidth(),
          height: selectedRange.getHeight(),
          direction: selectedRange.getDirection()
        };
        event.preventDefault();
        return false;
      }
    });
    this.eventManager.addEventListener(this.hot.rootElement, 'touchend', function(event) {
      if (dom.hasClass(event.target, "topLeftSelectionHandle-HitArea")) {
        removeFromDragged.call(_this, "topLeft");
        _this.touchStartRange = void 0;
        event.preventDefault();
        return false;
      } else if (dom.hasClass(event.target, "bottomRightSelectionHandle-HitArea")) {
        removeFromDragged.call(_this, "bottomRight");
        _this.touchStartRange = void 0;
        event.preventDefault();
        return false;
      }
    });
    this.eventManager.addEventListener(this.hot.rootElement, 'touchmove', function(event) {
      var scrollTop = dom.getWindowScrollTop(),
          scrollLeft = dom.getWindowScrollLeft(),
          endTarget,
          targetCoords,
          selectedRange,
          rangeWidth,
          rangeHeight,
          rangeDirection,
          newRangeCoords;
      if (_this.dragged.length === 0) {
        return;
      }
      endTarget = document.elementFromPoint(event.touches[0].screenX - scrollLeft, event.touches[0].screenY - scrollTop);
      if (!endTarget || endTarget === _this.lastSetCell) {
        return;
      }
      if (endTarget.nodeName == "TD" || endTarget.nodeName == "TH") {
        targetCoords = _this.hot.getCoords(endTarget);
        if (targetCoords.col == -1) {
          targetCoords.col = 0;
        }
        selectedRange = _this.hot.getSelectedRange();
        rangeWidth = selectedRange.getWidth();
        rangeHeight = selectedRange.getHeight();
        rangeDirection = selectedRange.getDirection();
        if (rangeWidth == 1 && rangeHeight == 1) {
          _this.hot.selection.setRangeEnd(targetCoords);
        }
        newRangeCoords = _this.getCurrentRangeCoords(selectedRange, targetCoords, _this.touchStartRange.direction, rangeDirection, _this.dragged[0]);
        if (newRangeCoords.start !== null) {
          _this.hot.selection.setRangeStart(newRangeCoords.start);
        }
        _this.hot.selection.setRangeEnd(newRangeCoords.end);
        _this.lastSetCell = endTarget;
      }
      event.preventDefault();
    });
  },
  getCurrentRangeCoords: function(selectedRange, currentTouch, touchStartDirection, currentDirection, draggedHandle) {
    var topLeftCorner = selectedRange.getTopLeftCorner(),
        bottomRightCorner = selectedRange.getBottomRightCorner(),
        bottomLeftCorner = selectedRange.getBottomLeftCorner(),
        topRightCorner = selectedRange.getTopRightCorner();
    var newCoords = {
      start: null,
      end: null
    };
    switch (touchStartDirection) {
      case "NE-SW":
        switch (currentDirection) {
          case "NE-SW":
          case "NW-SE":
            if (draggedHandle == "topLeft") {
              newCoords = {
                start: new WalkontableCellCoords(currentTouch.row, selectedRange.highlight.col),
                end: new WalkontableCellCoords(bottomLeftCorner.row, currentTouch.col)
              };
            } else {
              newCoords = {
                start: new WalkontableCellCoords(selectedRange.highlight.row, currentTouch.col),
                end: new WalkontableCellCoords(currentTouch.row, topLeftCorner.col)
              };
            }
            break;
          case "SE-NW":
            if (draggedHandle == "bottomRight") {
              newCoords = {
                start: new WalkontableCellCoords(bottomRightCorner.row, currentTouch.col),
                end: new WalkontableCellCoords(currentTouch.row, topLeftCorner.col)
              };
            }
            break;
        }
        break;
      case "NW-SE":
        switch (currentDirection) {
          case "NE-SW":
            if (draggedHandle == "topLeft") {
              newCoords = {
                start: currentTouch,
                end: bottomLeftCorner
              };
            } else {
              newCoords.end = currentTouch;
            }
            break;
          case "NW-SE":
            if (draggedHandle == "topLeft") {
              newCoords = {
                start: currentTouch,
                end: bottomRightCorner
              };
            } else {
              newCoords.end = currentTouch;
            }
            break;
          case "SE-NW":
            if (draggedHandle == "topLeft") {
              newCoords = {
                start: currentTouch,
                end: topLeftCorner
              };
            } else {
              newCoords.end = currentTouch;
            }
            break;
          case "SW-NE":
            if (draggedHandle == "topLeft") {
              newCoords = {
                start: currentTouch,
                end: topRightCorner
              };
            } else {
              newCoords.end = currentTouch;
            }
            break;
        }
        break;
      case "SW-NE":
        switch (currentDirection) {
          case "NW-SE":
            if (draggedHandle == "bottomRight") {
              newCoords = {
                start: new WalkontableCellCoords(currentTouch.row, topLeftCorner.col),
                end: new WalkontableCellCoords(bottomLeftCorner.row, currentTouch.col)
              };
            } else {
              newCoords = {
                start: new WalkontableCellCoords(topLeftCorner.row, currentTouch.col),
                end: new WalkontableCellCoords(currentTouch.row, bottomRightCorner.col)
              };
            }
            break;
          case "SW-NE":
            if (draggedHandle == "topLeft") {
              newCoords = {
                start: new WalkontableCellCoords(selectedRange.highlight.row, currentTouch.col),
                end: new WalkontableCellCoords(currentTouch.row, bottomRightCorner.col)
              };
            } else {
              newCoords = {
                start: new WalkontableCellCoords(currentTouch.row, topLeftCorner.col),
                end: new WalkontableCellCoords(topLeftCorner.row, currentTouch.col)
              };
            }
            break;
          case "SE-NW":
            if (draggedHandle == "bottomRight") {
              newCoords = {
                start: new WalkontableCellCoords(currentTouch.row, topRightCorner.col),
                end: new WalkontableCellCoords(topLeftCorner.row, currentTouch.col)
              };
            } else if (draggedHandle == "topLeft") {
              newCoords = {
                start: bottomLeftCorner,
                end: currentTouch
              };
            }
            break;
        }
        break;
      case "SE-NW":
        switch (currentDirection) {
          case "NW-SE":
          case "NE-SW":
          case "SW-NE":
            if (draggedHandle == "topLeft") {
              newCoords.end = currentTouch;
            }
            break;
          case "SE-NW":
            if (draggedHandle == "topLeft") {
              newCoords.end = currentTouch;
            } else {
              newCoords = {
                start: currentTouch,
                end: topLeftCorner
              };
            }
            break;
        }
        break;
    }
    return newCoords;
  },
  isDragged: function() {
    return this.dragged.length > 0;
  }
}, {}, BasePlugin);
var $__default = MultipleSelectionHandles;
registerPlugin('multipleSelectionHandles', MultipleSelectionHandles);


//# 
},{"./../../dom.js":27,"./../../eventManager.js":41,"./../../plugins.js":45,"./../_base.js":46}],65:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  ObserveChanges: {get: function() {
      return ObserveChanges;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_plugins_46_js__,
    $__jsonpatch__;
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
var jsonpatch = ($__jsonpatch__ = require("jsonpatch"), $__jsonpatch__ && $__jsonpatch__.__esModule && $__jsonpatch__ || {default: $__jsonpatch__}).default;
;
function ObserveChanges() {}
Handsontable.hooks.add('afterLoadData', init);
Handsontable.hooks.add('afterUpdateSettings', init);
Handsontable.hooks.register('afterChangesObserved');
function init() {
  var instance = this;
  var pluginEnabled = instance.getSettings().observeChanges;
  if (pluginEnabled) {
    if (instance.observer) {
      destroy.call(instance);
    }
    createObserver.call(instance);
    bindEvents.call(instance);
  } else if (!pluginEnabled) {
    destroy.call(instance);
  }
}
function createObserver() {
  var instance = this;
  instance.observeChangesActive = true;
  instance.pauseObservingChanges = function() {
    instance.observeChangesActive = false;
  };
  instance.resumeObservingChanges = function() {
    instance.observeChangesActive = true;
  };
  instance.observedData = instance.getData();
  instance.observer = jsonpatch.observe(instance.observedData, function(patches) {
    if (instance.observeChangesActive) {
      runHookForOperation.call(instance, patches);
      instance.render();
    }
    instance.runHooks('afterChangesObserved');
  });
}
function runHookForOperation(rawPatches) {
  var instance = this;
  var patches = cleanPatches(rawPatches);
  for (var i = 0,
      len = patches.length; i < len; i++) {
    var patch = patches[i];
    var parsedPath = parsePath(patch.path);
    switch (patch.op) {
      case 'add':
        if (isNaN(parsedPath.col)) {
          instance.runHooks('afterCreateRow', parsedPath.row);
        } else {
          instance.runHooks('afterCreateCol', parsedPath.col);
        }
        break;
      case 'remove':
        if (isNaN(parsedPath.col)) {
          instance.runHooks('afterRemoveRow', parsedPath.row, 1);
        } else {
          instance.runHooks('afterRemoveCol', parsedPath.col, 1);
        }
        break;
      case 'replace':
        instance.runHooks('afterChange', [parsedPath.row, parsedPath.col, null, patch.value], 'external');
        break;
    }
  }
  function cleanPatches(rawPatches) {
    var patches;
    patches = removeLengthRelatedPatches(rawPatches);
    patches = removeMultipleAddOrRemoveColPatches(patches);
    return patches;
  }
  function removeMultipleAddOrRemoveColPatches(rawPatches) {
    var newOrRemovedColumns = [];
    return rawPatches.filter(function(patch) {
      var parsedPath = parsePath(patch.path);
      if (['add', 'remove'].indexOf(patch.op) != -1 && !isNaN(parsedPath.col)) {
        if (newOrRemovedColumns.indexOf(parsedPath.col) != -1) {
          return false;
        } else {
          newOrRemovedColumns.push(parsedPath.col);
        }
      }
      return true;
    });
  }
  function removeLengthRelatedPatches(rawPatches) {
    return rawPatches.filter(function(patch) {
      return !/[/]length/ig.test(patch.path);
    });
  }
  function parsePath(path) {
    var match = path.match(/^\/(\d+)\/?(.*)?$/);
    return {
      row: parseInt(match[1], 10),
      col: /^\d*$/.test(match[2]) ? parseInt(match[2], 10) : match[2]
    };
  }
}
function destroy() {
  var instance = this;
  if (instance.observer) {
    destroyObserver.call(instance);
    unbindEvents.call(instance);
  }
}
function destroyObserver() {
  var instance = this;
  jsonpatch.unobserve(instance.observedData, instance.observer);
  delete instance.observeChangesActive;
  delete instance.pauseObservingChanges;
  delete instance.resumeObservingChanges;
}
function bindEvents() {
  var instance = this;
  instance.addHook('afterDestroy', destroy);
  instance.addHook('afterCreateRow', afterTableAlter);
  instance.addHook('afterRemoveRow', afterTableAlter);
  instance.addHook('afterCreateCol', afterTableAlter);
  instance.addHook('afterRemoveCol', afterTableAlter);
  instance.addHook('afterChange', function(changes, source) {
    if (source != 'loadData') {
      afterTableAlter.call(this);
    }
  });
}
function unbindEvents() {
  var instance = this;
  instance.removeHook('afterDestroy', destroy);
  instance.removeHook('afterCreateRow', afterTableAlter);
  instance.removeHook('afterRemoveRow', afterTableAlter);
  instance.removeHook('afterCreateCol', afterTableAlter);
  instance.removeHook('afterRemoveCol', afterTableAlter);
  instance.removeHook('afterChange', afterTableAlter);
}
function afterTableAlter() {
  var instance = this;
  instance.pauseObservingChanges();
  instance.addHookOnce('afterChangesObserved', function() {
    instance.resumeObservingChanges();
  });
}


//# 
},{"./../../plugins.js":45,"jsonpatch":undefined}],66:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  HandsontablePersistentState: {get: function() {
      return HandsontablePersistentState;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_plugins_46_js__;
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
;
function Storage(prefix) {
  var savedKeys;
  var saveSavedKeys = function() {
    window.localStorage[prefix + '__' + 'persistentStateKeys'] = JSON.stringify(savedKeys);
  };
  var loadSavedKeys = function() {
    var keysJSON = window.localStorage[prefix + '__' + 'persistentStateKeys'];
    var keys = typeof keysJSON == 'string' ? JSON.parse(keysJSON) : void 0;
    savedKeys = keys ? keys : [];
  };
  var clearSavedKeys = function() {
    savedKeys = [];
    saveSavedKeys();
  };
  loadSavedKeys();
  this.saveValue = function(key, value) {
    window.localStorage[prefix + '_' + key] = JSON.stringify(value);
    if (savedKeys.indexOf(key) == -1) {
      savedKeys.push(key);
      saveSavedKeys();
    }
  };
  this.loadValue = function(key, defaultValue) {
    key = typeof key != 'undefined' ? key : defaultValue;
    var value = window.localStorage[prefix + '_' + key];
    return typeof value == "undefined" ? void 0 : JSON.parse(value);
  };
  this.reset = function(key) {
    window.localStorage.removeItem(prefix + '_' + key);
  };
  this.resetAll = function() {
    for (var index = 0; index < savedKeys.length; index++) {
      window.localStorage.removeItem(prefix + '_' + savedKeys[index]);
    }
    clearSavedKeys();
  };
}
function HandsontablePersistentState() {
  var plugin = this;
  this.init = function() {
    var instance = this,
        pluginSettings = instance.getSettings().persistentState;
    plugin.enabled = !!(pluginSettings);
    if (!plugin.enabled) {
      removeHooks.call(instance);
      return;
    }
    if (!instance.storage) {
      instance.storage = new Storage(instance.rootElement.id);
    }
    instance.resetState = plugin.resetValue;
    addHooks.call(instance);
  };
  this.saveValue = function(key, value) {
    var instance = this;
    instance.storage.saveValue(key, value);
  };
  this.loadValue = function(key, saveTo) {
    var instance = this;
    saveTo.value = instance.storage.loadValue(key);
  };
  this.resetValue = function(key) {
    var instance = this;
    if (typeof key != 'undefined') {
      instance.storage.reset(key);
    } else {
      instance.storage.resetAll();
    }
  };
  var hooks = {
    'persistentStateSave': plugin.saveValue,
    'persistentStateLoad': plugin.loadValue,
    'persistentStateReset': plugin.resetValue
  };
  for (var hookName in hooks) {
    if (hooks.hasOwnProperty(hookName)) {
      Handsontable.hooks.register(hookName);
    }
  }
  function addHooks() {
    var instance = this;
    for (var hookName in hooks) {
      if (hooks.hasOwnProperty(hookName)) {
        instance.addHook(hookName, hooks[hookName]);
      }
    }
  }
  function removeHooks() {
    var instance = this;
    for (var hookName in hooks) {
      if (hooks.hasOwnProperty(hookName)) {
        instance.removeHook(hookName, hooks[hookName]);
      }
    }
  }
}
var htPersistentState = new HandsontablePersistentState();
Handsontable.hooks.add('beforeInit', htPersistentState.init);
Handsontable.hooks.add('afterUpdateSettings', htPersistentState.init);


//# 
},{"./../../plugins.js":45}],67:[function(require,module,exports){
"use strict";
var $___46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__46__46__47_renderers_46_js__;
var dom = ($___46__46__47__46__46__47_dom_46_js__ = require("./../../dom.js"), $___46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47_dom_46_js__});
var $__0 = ($___46__46__47__46__46__47_renderers_46_js__ = require("./../../renderers.js"), $___46__46__47__46__46__47_renderers_46_js__ && $___46__46__47__46__46__47_renderers_46_js__.__esModule && $___46__46__47__46__46__47_renderers_46_js__ || {default: $___46__46__47__46__46__47_renderers_46_js__}),
    registerRenderer = $__0.registerRenderer,
    getRenderer = $__0.getRenderer;
Handsontable.Search = function Search(instance) {
  this.query = function(queryStr, callback, queryMethod) {
    var rowCount = instance.countRows();
    var colCount = instance.countCols();
    var queryResult = [];
    if (!callback) {
      callback = Handsontable.Search.global.getDefaultCallback();
    }
    if (!queryMethod) {
      queryMethod = Handsontable.Search.global.getDefaultQueryMethod();
    }
    for (var rowIndex = 0; rowIndex < rowCount; rowIndex++) {
      for (var colIndex = 0; colIndex < colCount; colIndex++) {
        var cellData = instance.getDataAtCell(rowIndex, colIndex);
        var cellProperties = instance.getCellMeta(rowIndex, colIndex);
        var cellCallback = cellProperties.search.callback || callback;
        var cellQueryMethod = cellProperties.search.queryMethod || queryMethod;
        var testResult = cellQueryMethod(queryStr, cellData);
        if (testResult) {
          var singleResult = {
            row: rowIndex,
            col: colIndex,
            data: cellData
          };
          queryResult.push(singleResult);
        }
        if (cellCallback) {
          cellCallback(instance, rowIndex, colIndex, cellData, testResult);
        }
      }
    }
    return queryResult;
  };
};
Handsontable.Search.DEFAULT_CALLBACK = function(instance, row, col, data, testResult) {
  instance.getCellMeta(row, col).isSearchResult = testResult;
};
Handsontable.Search.DEFAULT_QUERY_METHOD = function(query, value) {
  if (typeof query == 'undefined' || query == null || !query.toLowerCase || query.length === 0) {
    return false;
  }
  if (typeof value == 'undefined' || value == null) {
    return false;
  }
  return value.toString().toLowerCase().indexOf(query.toLowerCase()) != -1;
};
Handsontable.Search.DEFAULT_SEARCH_RESULT_CLASS = 'htSearchResult';
Handsontable.Search.global = (function() {
  var defaultCallback = Handsontable.Search.DEFAULT_CALLBACK;
  var defaultQueryMethod = Handsontable.Search.DEFAULT_QUERY_METHOD;
  var defaultSearchResultClass = Handsontable.Search.DEFAULT_SEARCH_RESULT_CLASS;
  return {
    getDefaultCallback: function() {
      return defaultCallback;
    },
    setDefaultCallback: function(newDefaultCallback) {
      defaultCallback = newDefaultCallback;
    },
    getDefaultQueryMethod: function() {
      return defaultQueryMethod;
    },
    setDefaultQueryMethod: function(newDefaultQueryMethod) {
      defaultQueryMethod = newDefaultQueryMethod;
    },
    getDefaultSearchResultClass: function() {
      return defaultSearchResultClass;
    },
    setDefaultSearchResultClass: function(newSearchResultClass) {
      defaultSearchResultClass = newSearchResultClass;
    }
  };
})();
Handsontable.SearchCellDecorator = function(instance, TD, row, col, prop, value, cellProperties) {
  var searchResultClass = (cellProperties.search !== null && typeof cellProperties.search == 'object' && cellProperties.search.searchResultClass) || Handsontable.Search.global.getDefaultSearchResultClass();
  if (cellProperties.isSearchResult) {
    dom.addClass(TD, searchResultClass);
  } else {
    dom.removeClass(TD, searchResultClass);
  }
};
var originalBaseRenderer = getRenderer('base');
registerRenderer('base', function(instance, TD, row, col, prop, value, cellProperties) {
  originalBaseRenderer.apply(this, arguments);
  Handsontable.SearchCellDecorator.apply(this, arguments);
});
function init() {
  var instance = this;
  var pluginEnabled = !!instance.getSettings().search;
  if (pluginEnabled) {
    instance.search = new Handsontable.Search(instance);
  } else {
    delete instance.search;
  }
}
Handsontable.hooks.add('afterInit', init);
Handsontable.hooks.add('afterUpdateSettings', init);


//# 
},{"./../../dom.js":27,"./../../renderers.js":70}],68:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  TouchScroll: {get: function() {
      return TouchScroll;
    }},
  __esModule: {value: true}
});
var $___46__46__47__46__46__47_dom_46_js__,
    $___46__46__47__95_base_46_js__,
    $___46__46__47__46__46__47_plugins_46_js__;
var dom = ($___46__46__47__46__46__47_dom_46_js__ = require("./../../dom.js"), $___46__46__47__46__46__47_dom_46_js__ && $___46__46__47__46__46__47_dom_46_js__.__esModule && $___46__46__47__46__46__47_dom_46_js__ || {default: $___46__46__47__46__46__47_dom_46_js__});
var BasePlugin = ($___46__46__47__95_base_46_js__ = require("./../_base.js"), $___46__46__47__95_base_46_js__ && $___46__46__47__95_base_46_js__.__esModule && $___46__46__47__95_base_46_js__ || {default: $___46__46__47__95_base_46_js__}).default;
var registerPlugin = ($___46__46__47__46__46__47_plugins_46_js__ = require("./../../plugins.js"), $___46__46__47__46__46__47_plugins_46_js__ && $___46__46__47__46__46__47_plugins_46_js__.__esModule && $___46__46__47__46__46__47_plugins_46_js__ || {default: $___46__46__47__46__46__47_plugins_46_js__}).registerPlugin;
var TouchScroll = function TouchScroll(hotInstance) {
  var $__2 = this;
  $traceurRuntime.superConstructor($TouchScroll).call(this, hotInstance);
  this.hot.addHook('afterInit', (function() {
    return $__2.init();
  }));
  this.hot.addHook('afterUpdateSettings', (function() {
    return $__2.onAfterUpdateSettings();
  }));
  this.scrollbars = [];
  this.clones = [];
};
var $TouchScroll = TouchScroll;
($traceurRuntime.createClass)(TouchScroll, {
  init: function() {
    this.registerEvents();
    this.onAfterUpdateSettings();
  },
  onAfterUpdateSettings: function() {
    var _this = this;
    this.hot.addHookOnce('afterRender', function() {
      var wtOverlays = _this.hot.view.wt.wtOverlays;
      _this.scrollbars = [];
      _this.scrollbars.push(wtOverlays.topOverlay);
      _this.scrollbars.push(wtOverlays.leftOverlay);
      if (wtOverlays.topLeftCornerOverlay) {
        _this.scrollbars.push(wtOverlays.topLeftCornerOverlay);
      }
      _this.clones = [];
      if (wtOverlays.topOverlay.needFullRender) {
        _this.clones.push(wtOverlays.topOverlay.clone.wtTable.holder.parentNode);
      }
      if (wtOverlays.leftOverlay.needFullRender) {
        _this.clones.push(wtOverlays.leftOverlay.clone.wtTable.holder.parentNode);
      }
      if (wtOverlays.topLeftCornerOverlay) {
        _this.clones.push(wtOverlays.topLeftCornerOverlay.clone.wtTable.holder.parentNode);
      }
    });
  },
  registerEvents: function() {
    var $__2 = this;
    this.hot.addHook('beforeTouchScroll', (function() {
      return $__2.onBeforeTouchScroll();
    }));
    this.hot.addHook('afterMomentumScroll', (function() {
      return $__2.onAfterMomentumScroll();
    }));
  },
  onBeforeTouchScroll: function() {
    Handsontable.freezeOverlays = true;
    for (var i = 0,
        cloneCount = this.clones.length; i < cloneCount; i++) {
      dom.addClass(this.clones[i], 'hide-tween');
    }
  },
  onAfterMomentumScroll: function() {
    Handsontable.freezeOverlays = false;
    var _that = this;
    for (var i = 0,
        cloneCount = this.clones.length; i < cloneCount; i++) {
      dom.removeClass(this.clones[i], 'hide-tween');
    }
    for (var i$__4 = 0,
        cloneCount$__5 = this.clones.length; i$__4 < cloneCount$__5; i$__4++) {
      dom.addClass(this.clones[i$__4], 'show-tween');
    }
    setTimeout(function() {
      for (var i = 0,
          cloneCount = _that.clones.length; i < cloneCount; i++) {
        dom.removeClass(_that.clones[i], 'show-tween');
      }
    }, 400);
    for (var i$__6 = 0,
        cloneCount$__7 = this.scrollbars.length; i$__6 < cloneCount$__7; i$__6++) {
      this.scrollbars[i$__6].refresh();
      this.scrollbars[i$__6].resetFixedPosition();
    }
    this.hot.view.wt.wtOverlays.syncScrollWithMaster();
  }
}, {}, BasePlugin);
;
registerPlugin('touchScroll', TouchScroll);


//# 
},{"./../../dom.js":27,"./../../plugins.js":45,"./../_base.js":46}],69:[function(require,module,exports){
"use strict";
var $___46__46__47__46__46__47_helpers_46_js__;
var helper = ($___46__46__47__46__46__47_helpers_46_js__ = require("./../../helpers.js"), $___46__46__47__46__46__47_helpers_46_js__ && $___46__46__47__46__46__47_helpers_46_js__.__esModule && $___46__46__47__46__46__47_helpers_46_js__ || {default: $___46__46__47__46__46__47_helpers_46_js__});
Handsontable.UndoRedo = function(instance) {
  var plugin = this;
  this.instance = instance;
  this.doneActions = [];
  this.undoneActions = [];
  this.ignoreNewActions = false;
  instance.addHook("afterChange", function(changes, origin) {
    if (changes) {
      var action = new Handsontable.UndoRedo.ChangeAction(changes);
      plugin.done(action);
    }
  });
  instance.addHook("afterCreateRow", function(index, amount, createdAutomatically) {
    if (createdAutomatically) {
      return;
    }
    var action = new Handsontable.UndoRedo.CreateRowAction(index, amount);
    plugin.done(action);
  });
  instance.addHook("beforeRemoveRow", function(index, amount) {
    var originalData = plugin.instance.getData();
    index = (originalData.length + index) % originalData.length;
    var removedData = originalData.slice(index, index + amount);
    var action = new Handsontable.UndoRedo.RemoveRowAction(index, removedData);
    plugin.done(action);
  });
  instance.addHook("afterCreateCol", function(index, amount, createdAutomatically) {
    if (createdAutomatically) {
      return;
    }
    var action = new Handsontable.UndoRedo.CreateColumnAction(index, amount);
    plugin.done(action);
  });
  instance.addHook("beforeRemoveCol", function(index, amount) {
    var originalData = plugin.instance.getData();
    index = (plugin.instance.countCols() + index) % plugin.instance.countCols();
    var removedData = [];
    for (var i = 0,
        len = originalData.length; i < len; i++) {
      removedData[i] = originalData[i].slice(index, index + amount);
    }
    var headers;
    if (Array.isArray(instance.getSettings().colHeaders)) {
      headers = instance.getSettings().colHeaders.slice(index, index + removedData.length);
    }
    var action = new Handsontable.UndoRedo.RemoveColumnAction(index, removedData, headers);
    plugin.done(action);
  });
  instance.addHook("beforeCellAlignment", function(stateBefore, range, type, alignment) {
    var action = new Handsontable.UndoRedo.CellAlignmentAction(stateBefore, range, type, alignment);
    plugin.done(action);
  });
};
Handsontable.UndoRedo.prototype.done = function(action) {
  if (!this.ignoreNewActions) {
    this.doneActions.push(action);
    this.undoneActions.length = 0;
  }
};
Handsontable.UndoRedo.prototype.undo = function() {
  if (this.isUndoAvailable()) {
    var action = this.doneActions.pop();
    this.ignoreNewActions = true;
    var that = this;
    action.undo(this.instance, function() {
      that.ignoreNewActions = false;
      that.undoneActions.push(action);
    });
  }
};
Handsontable.UndoRedo.prototype.redo = function() {
  if (this.isRedoAvailable()) {
    var action = this.undoneActions.pop();
    this.ignoreNewActions = true;
    var that = this;
    action.redo(this.instance, function() {
      that.ignoreNewActions = false;
      that.doneActions.push(action);
    });
  }
};
Handsontable.UndoRedo.prototype.isUndoAvailable = function() {
  return this.doneActions.length > 0;
};
Handsontable.UndoRedo.prototype.isRedoAvailable = function() {
  return this.undoneActions.length > 0;
};
Handsontable.UndoRedo.prototype.clear = function() {
  this.doneActions.length = 0;
  this.undoneActions.length = 0;
};
Handsontable.UndoRedo.Action = function() {};
Handsontable.UndoRedo.Action.prototype.undo = function() {};
Handsontable.UndoRedo.Action.prototype.redo = function() {};
Handsontable.UndoRedo.ChangeAction = function(changes) {
  this.changes = changes;
};
helper.inherit(Handsontable.UndoRedo.ChangeAction, Handsontable.UndoRedo.Action);
Handsontable.UndoRedo.ChangeAction.prototype.undo = function(instance, undoneCallback) {
  var data = helper.deepClone(this.changes),
      emptyRowsAtTheEnd = instance.countEmptyRows(true),
      emptyColsAtTheEnd = instance.countEmptyCols(true);
  for (var i = 0,
      len = data.length; i < len; i++) {
    data[i].splice(3, 1);
  }
  instance.addHookOnce('afterChange', undoneCallback);
  instance.setDataAtRowProp(data, null, null, 'undo');
  for (var i = 0,
      len = data.length; i < len; i++) {
    if (instance.getSettings().minSpareRows && data[i][0] + 1 + instance.getSettings().minSpareRows === instance.countRows() && emptyRowsAtTheEnd == instance.getSettings().minSpareRows) {
      instance.alter('remove_row', parseInt(data[i][0] + 1, 10), instance.getSettings().minSpareRows);
      instance.undoRedo.doneActions.pop();
    }
    if (instance.getSettings().minSpareCols && data[i][1] + 1 + instance.getSettings().minSpareCols === instance.countCols() && emptyColsAtTheEnd == instance.getSettings().minSpareCols) {
      instance.alter('remove_col', parseInt(data[i][1] + 1, 10), instance.getSettings().minSpareCols);
      instance.undoRedo.doneActions.pop();
    }
  }
};
Handsontable.UndoRedo.ChangeAction.prototype.redo = function(instance, onFinishCallback) {
  var data = helper.deepClone(this.changes);
  for (var i = 0,
      len = data.length; i < len; i++) {
    data[i].splice(2, 1);
  }
  instance.addHookOnce('afterChange', onFinishCallback);
  instance.setDataAtRowProp(data, null, null, 'redo');
};
Handsontable.UndoRedo.CreateRowAction = function(index, amount) {
  this.index = index;
  this.amount = amount;
};
helper.inherit(Handsontable.UndoRedo.CreateRowAction, Handsontable.UndoRedo.Action);
Handsontable.UndoRedo.CreateRowAction.prototype.undo = function(instance, undoneCallback) {
  var rowCount = instance.countRows(),
      minSpareRows = instance.getSettings().minSpareRows;
  if (this.index >= rowCount && this.index - minSpareRows < rowCount) {
    this.index -= minSpareRows;
  }
  instance.addHookOnce('afterRemoveRow', undoneCallback);
  instance.alter('remove_row', this.index, this.amount);
};
Handsontable.UndoRedo.CreateRowAction.prototype.redo = function(instance, redoneCallback) {
  instance.addHookOnce('afterCreateRow', redoneCallback);
  instance.alter('insert_row', this.index + 1, this.amount);
};
Handsontable.UndoRedo.RemoveRowAction = function(index, data) {
  this.index = index;
  this.data = data;
};
helper.inherit(Handsontable.UndoRedo.RemoveRowAction, Handsontable.UndoRedo.Action);
Handsontable.UndoRedo.RemoveRowAction.prototype.undo = function(instance, undoneCallback) {
  var spliceArgs = [this.index, 0];
  Array.prototype.push.apply(spliceArgs, this.data);
  Array.prototype.splice.apply(instance.getData(), spliceArgs);
  instance.addHookOnce('afterRender', undoneCallback);
  instance.render();
};
Handsontable.UndoRedo.RemoveRowAction.prototype.redo = function(instance, redoneCallback) {
  instance.addHookOnce('afterRemoveRow', redoneCallback);
  instance.alter('remove_row', this.index, this.data.length);
};
Handsontable.UndoRedo.CreateColumnAction = function(index, amount) {
  this.index = index;
  this.amount = amount;
};
helper.inherit(Handsontable.UndoRedo.CreateColumnAction, Handsontable.UndoRedo.Action);
Handsontable.UndoRedo.CreateColumnAction.prototype.undo = function(instance, undoneCallback) {
  instance.addHookOnce('afterRemoveCol', undoneCallback);
  instance.alter('remove_col', this.index, this.amount);
};
Handsontable.UndoRedo.CreateColumnAction.prototype.redo = function(instance, redoneCallback) {
  instance.addHookOnce('afterCreateCol', redoneCallback);
  instance.alter('insert_col', this.index + 1, this.amount);
};
Handsontable.UndoRedo.CellAlignmentAction = function(stateBefore, range, type, alignment) {
  this.stateBefore = stateBefore;
  this.range = range;
  this.type = type;
  this.alignment = alignment;
};
Handsontable.UndoRedo.CellAlignmentAction.prototype.undo = function(instance, undoneCallback) {
  if (!instance.contextMenu) {
    return;
  }
  for (var row = this.range.from.row; row <= this.range.to.row; row++) {
    for (var col = this.range.from.col; col <= this.range.to.col; col++) {
      instance.setCellMeta(row, col, 'className', this.stateBefore[row][col] || ' htLeft');
    }
  }
  instance.addHookOnce('afterRender', undoneCallback);
  instance.render();
};
Handsontable.UndoRedo.CellAlignmentAction.prototype.redo = function(instance, undoneCallback) {
  if (!instance.contextMenu) {
    return;
  }
  for (var row = this.range.from.row; row <= this.range.to.row; row++) {
    for (var col = this.range.from.col; col <= this.range.to.col; col++) {
      instance.contextMenu.align.call(instance, this.range, this.type, this.alignment);
    }
  }
  instance.addHookOnce('afterRender', undoneCallback);
  instance.render();
};
Handsontable.UndoRedo.RemoveColumnAction = function(index, data, headers) {
  this.index = index;
  this.data = data;
  this.amount = this.data[0].length;
  this.headers = headers;
};
helper.inherit(Handsontable.UndoRedo.RemoveColumnAction, Handsontable.UndoRedo.Action);
Handsontable.UndoRedo.RemoveColumnAction.prototype.undo = function(instance, undoneCallback) {
  var row,
      spliceArgs;
  for (var i = 0,
      len = instance.getData().length; i < len; i++) {
    row = instance.getSourceDataAtRow(i);
    spliceArgs = [this.index, 0];
    Array.prototype.push.apply(spliceArgs, this.data[i]);
    Array.prototype.splice.apply(row, spliceArgs);
  }
  if (typeof this.headers != 'undefined') {
    spliceArgs = [this.index, 0];
    Array.prototype.push.apply(spliceArgs, this.headers);
    Array.prototype.splice.apply(instance.getSettings().colHeaders, spliceArgs);
  }
  instance.addHookOnce('afterRender', undoneCallback);
  instance.render();
};
Handsontable.UndoRedo.RemoveColumnAction.prototype.redo = function(instance, redoneCallback) {
  instance.addHookOnce('afterRemoveCol', redoneCallback);
  instance.alter('remove_col', this.index, this.amount);
};
function init() {
  var instance = this;
  var pluginEnabled = typeof instance.getSettings().undo == 'undefined' || instance.getSettings().undo;
  if (pluginEnabled) {
    if (!instance.undoRedo) {
      instance.undoRedo = new Handsontable.UndoRedo(instance);
      exposeUndoRedoMethods(instance);
      instance.addHook('beforeKeyDown', onBeforeKeyDown);
      instance.addHook('afterChange', onAfterChange);
    }
  } else {
    if (instance.undoRedo) {
      delete instance.undoRedo;
      removeExposedUndoRedoMethods(instance);
      instance.removeHook('beforeKeyDown', onBeforeKeyDown);
      instance.removeHook('afterChange', onAfterChange);
    }
  }
}
function onBeforeKeyDown(event) {
  var instance = this;
  var ctrlDown = (event.ctrlKey || event.metaKey) && !event.altKey;
  if (ctrlDown) {
    if (event.keyCode === 89 || (event.shiftKey && event.keyCode === 90)) {
      instance.undoRedo.redo();
      event.stopImmediatePropagation();
    } else if (event.keyCode === 90) {
      instance.undoRedo.undo();
      event.stopImmediatePropagation();
    }
  }
}
function onAfterChange(changes, source) {
  var instance = this;
  if (source == 'loadData') {
    return instance.undoRedo.clear();
  }
}
function exposeUndoRedoMethods(instance) {
  instance.undo = function() {
    return instance.undoRedo.undo();
  };
  instance.redo = function() {
    return instance.undoRedo.redo();
  };
  instance.isUndoAvailable = function() {
    return instance.undoRedo.isUndoAvailable();
  };
  instance.isRedoAvailable = function() {
    return instance.undoRedo.isRedoAvailable();
  };
  instance.clearUndo = function() {
    return instance.undoRedo.clear();
  };
}
function removeExposedUndoRedoMethods(instance) {
  delete instance.undo;
  delete instance.redo;
  delete instance.isUndoAvailable;
  delete instance.isRedoAvailable;
  delete instance.clearUndo;
}
Handsontable.hooks.add('afterInit', init);
Handsontable.hooks.add('afterUpdateSettings', init);


//# 
},{"./../../helpers.js":42}],70:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  registerRenderer: {get: function() {
      return registerRenderer;
    }},
  getRenderer: {get: function() {
      return getRenderer;
    }},
  hasRenderer: {get: function() {
      return hasRenderer;
    }},
  __esModule: {value: true}
});
var $__helpers_46_js__;
var helper = ($__helpers_46_js__ = require("./helpers.js"), $__helpers_46_js__ && $__helpers_46_js__.__esModule && $__helpers_46_js__ || {default: $__helpers_46_js__});
;
var registeredRenderers = {};
Handsontable.renderers = Handsontable.renderers || {};
Handsontable.renderers.registerRenderer = registerRenderer;
Handsontable.renderers.getRenderer = getRenderer;
function registerRenderer(rendererName, rendererFunction) {
  var registerName;
  registeredRenderers[rendererName] = rendererFunction;
  registerName = helper.toUpperCaseFirst(rendererName) + 'Renderer';
  Handsontable.renderers[registerName] = rendererFunction;
  Handsontable[registerName] = rendererFunction;
}
function getRenderer(rendererName) {
  if (typeof rendererName == 'function') {
    return rendererName;
  }
  if (typeof rendererName != 'string') {
    throw Error('Only strings and functions can be passed as "renderer" parameter');
  }
  if (!(rendererName in registeredRenderers)) {
    throw Error('No editor registered under name "' + rendererName + '"');
  }
  return registeredRenderers[rendererName];
}
function hasRenderer(rendererName) {
  return rendererName in registeredRenderers;
}


//# 
},{"./helpers.js":42}],71:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  cellDecorator: {get: function() {
      return cellDecorator;
    }},
  __esModule: {value: true}
});
var $___46__46__47_dom_46_js__,
    $___46__46__47_renderers_46_js__;
var dom = ($___46__46__47_dom_46_js__ = require("./../dom.js"), $___46__46__47_dom_46_js__ && $___46__46__47_dom_46_js__.__esModule && $___46__46__47_dom_46_js__ || {default: $___46__46__47_dom_46_js__});
var registerRenderer = ($___46__46__47_renderers_46_js__ = require("./../renderers.js"), $___46__46__47_renderers_46_js__ && $___46__46__47_renderers_46_js__.__esModule && $___46__46__47_renderers_46_js__ || {default: $___46__46__47_renderers_46_js__}).registerRenderer;
;
registerRenderer('base', cellDecorator);
Handsontable.renderers.cellDecorator = cellDecorator;
function cellDecorator(instance, TD, row, col, prop, value, cellProperties) {
  if (cellProperties.className) {
    if (TD.className) {
      TD.className = TD.className + " " + cellProperties.className;
    } else {
      TD.className = cellProperties.className;
    }
  }
  if (cellProperties.readOnly) {
    dom.addClass(TD, cellProperties.readOnlyCellClassName);
  }
  if (cellProperties.valid === false && cellProperties.invalidCellClassName) {
    dom.addClass(TD, cellProperties.invalidCellClassName);
  } else {
    dom.removeClass(TD, cellProperties.invalidCellClassName);
  }
  if (cellProperties.wordWrap === false && cellProperties.noWordWrapClassName) {
    dom.addClass(TD, cellProperties.noWordWrapClassName);
  }
  if (!value && cellProperties.placeholder) {
    dom.addClass(TD, cellProperties.placeholderCellClassName);
  }
}


//# 
},{"./../dom.js":27,"./../renderers.js":70}],72:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  autocompleteRenderer: {get: function() {
      return autocompleteRenderer;
    }},
  __esModule: {value: true}
});
var $___46__46__47_dom_46_js__,
    $___46__46__47_eventManager_46_js__,
    $___46__46__47_renderers_46_js__,
    $___46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__;
var dom = ($___46__46__47_dom_46_js__ = require("./../dom.js"), $___46__46__47_dom_46_js__ && $___46__46__47_dom_46_js__.__esModule && $___46__46__47_dom_46_js__ || {default: $___46__46__47_dom_46_js__});
var eventManagerObject = ($___46__46__47_eventManager_46_js__ = require("./../eventManager.js"), $___46__46__47_eventManager_46_js__ && $___46__46__47_eventManager_46_js__.__esModule && $___46__46__47_eventManager_46_js__ || {default: $___46__46__47_eventManager_46_js__}).eventManager;
var $__1 = ($___46__46__47_renderers_46_js__ = require("./../renderers.js"), $___46__46__47_renderers_46_js__ && $___46__46__47_renderers_46_js__.__esModule && $___46__46__47_renderers_46_js__ || {default: $___46__46__47_renderers_46_js__}),
    getRenderer = $__1.getRenderer,
    registerRenderer = $__1.registerRenderer;
var WalkontableCellCoords = ($___46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ = require("./../3rdparty/walkontable/src/cell/coords.js"), $___46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ && $___46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__.__esModule && $___46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ || {default: $___46__46__47_3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__}).WalkontableCellCoords;
;
var clonableWRAPPER = document.createElement('DIV');
clonableWRAPPER.className = 'htAutocompleteWrapper';
var clonableARROW = document.createElement('DIV');
clonableARROW.className = 'htAutocompleteArrow';
clonableARROW.appendChild(document.createTextNode(String.fromCharCode(9660)));
var wrapTdContentWithWrapper = function(TD, WRAPPER) {
  WRAPPER.innerHTML = TD.innerHTML;
  dom.empty(TD);
  TD.appendChild(WRAPPER);
};
registerRenderer('autocomplete', autocompleteRenderer);
function autocompleteRenderer(instance, TD, row, col, prop, value, cellProperties) {
  var WRAPPER = clonableWRAPPER.cloneNode(true);
  var ARROW = clonableARROW.cloneNode(true);
  getRenderer('text')(instance, TD, row, col, prop, value, cellProperties);
  TD.appendChild(ARROW);
  dom.addClass(TD, 'htAutocomplete');
  if (!TD.firstChild) {
    TD.appendChild(document.createTextNode(String.fromCharCode(160)));
  }
  if (!instance.acArrowListener) {
    var eventManager = eventManagerObject(instance);
    instance.acArrowListener = function(event) {
      if (dom.hasClass(event.target, 'htAutocompleteArrow')) {
        instance.view.wt.getSetting('onCellDblClick', null, new WalkontableCellCoords(row, col), TD);
      }
    };
    eventManager.addEventListener(instance.rootElement, 'mousedown', instance.acArrowListener);
    instance.addHookOnce('afterDestroy', function() {
      eventManager.clear();
    });
  }
}


//# 
},{"./../3rdparty/walkontable/src/cell/coords.js":5,"./../dom.js":27,"./../eventManager.js":41,"./../renderers.js":70}],73:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  checkboxRenderer: {get: function() {
      return checkboxRenderer;
    }},
  __esModule: {value: true}
});
var $___46__46__47_dom_46_js__,
    $___46__46__47_helpers_46_js__,
    $___46__46__47_eventManager_46_js__,
    $___46__46__47_renderers_46_js__;
var dom = ($___46__46__47_dom_46_js__ = require("./../dom.js"), $___46__46__47_dom_46_js__ && $___46__46__47_dom_46_js__.__esModule && $___46__46__47_dom_46_js__ || {default: $___46__46__47_dom_46_js__});
var helper = ($___46__46__47_helpers_46_js__ = require("./../helpers.js"), $___46__46__47_helpers_46_js__ && $___46__46__47_helpers_46_js__.__esModule && $___46__46__47_helpers_46_js__ || {default: $___46__46__47_helpers_46_js__});
var EventManager = ($___46__46__47_eventManager_46_js__ = require("./../eventManager.js"), $___46__46__47_eventManager_46_js__ && $___46__46__47_eventManager_46_js__.__esModule && $___46__46__47_eventManager_46_js__ || {default: $___46__46__47_eventManager_46_js__}).EventManager;
var $__1 = ($___46__46__47_renderers_46_js__ = require("./../renderers.js"), $___46__46__47_renderers_46_js__ && $___46__46__47_renderers_46_js__.__esModule && $___46__46__47_renderers_46_js__ || {default: $___46__46__47_renderers_46_js__}),
    getRenderer = $__1.getRenderer,
    registerRenderer = $__1.registerRenderer;
var clonableINPUT = document.createElement('INPUT');
clonableINPUT.className = 'htCheckboxRendererInput';
clonableINPUT.type = 'checkbox';
clonableINPUT.setAttribute('autocomplete', 'off');
var isListeningKeyDownEvent = new WeakMap();
function checkboxRenderer(instance, TD, row, col, prop, value, cellProperties) {
  var eventManager = new EventManager(instance);
  var input = clonableINPUT.cloneNode(false);
  if (typeof cellProperties.checkedTemplate === 'undefined') {
    cellProperties.checkedTemplate = true;
  }
  if (typeof cellProperties.uncheckedTemplate === 'undefined') {
    cellProperties.uncheckedTemplate = false;
  }
  dom.empty(TD);
  if (value === cellProperties.checkedTemplate || value === helper.stringify(cellProperties.checkedTemplate)) {
    input.checked = true;
    TD.appendChild(input);
  } else if (value === cellProperties.uncheckedTemplate || value === helper.stringify(cellProperties.uncheckedTemplate)) {
    TD.appendChild(input);
  } else if (value === null) {
    dom.addClass(input, 'noValue');
    TD.appendChild(input);
  } else {
    dom.fastInnerText(TD, '#bad value#');
  }
  if (cellProperties.readOnly) {
    eventManager.addEventListener(input, 'click', preventDefault);
  } else {
    eventManager.addEventListener(input, 'mousedown', stopPropagation);
    eventManager.addEventListener(input, 'mouseup', stopPropagation);
    eventManager.addEventListener(input, 'change', (function(event) {
      instance.setDataAtRowProp(row, prop, event.target.checked ? cellProperties.checkedTemplate : cellProperties.uncheckedTemplate);
    }));
  }
  if (!isListeningKeyDownEvent.has(instance)) {
    isListeningKeyDownEvent.set(instance, true);
    instance.addHook('beforeKeyDown', onBeforeKeyDown);
  }
  function onBeforeKeyDown(event) {
    var allowedKeys = [helper.keyCode.SPACE, helper.keyCode.ENTER, helper.keyCode.DELETE, helper.keyCode.BACKSPACE];
    dom.enableImmediatePropagation(event);
    if (allowedKeys.indexOf(event.keyCode) !== -1 && !event.isImmediatePropagationStopped()) {
      eachSelectedCheckboxCell(function() {
        event.stopImmediatePropagation();
        event.preventDefault();
      });
    }
    if (event.keyCode == helper.keyCode.SPACE || event.keyCode == helper.keyCode.ENTER) {
      toggleSelected();
    }
    if (event.keyCode == helper.keyCode.DELETE || event.keyCode == helper.keyCode.BACKSPACE) {
      toggleSelected(false);
    }
  }
  function toggleSelected() {
    var checked = arguments[0] !== (void 0) ? arguments[0] : null;
    eachSelectedCheckboxCell(function(checkboxes) {
      for (var i = 0,
          len = checkboxes.length; i < len; i++) {
        toggleCheckbox(checkboxes[i], checked);
      }
    });
  }
  function toggleCheckbox(checkbox) {
    var checked = arguments[1] !== (void 0) ? arguments[1] : null;
    if (checked === null) {
      checkbox.checked = !checkbox.checked;
    } else {
      checkbox.checked = checked;
    }
    eventManager.fireEvent(checkbox, 'change');
  }
  function eachSelectedCheckboxCell(callback) {
    var selRange = instance.getSelectedRange();
    var topLeft = selRange.getTopLeftCorner();
    var bottomRight = selRange.getBottomRightCorner();
    for (var row = topLeft.row; row <= bottomRight.row; row++) {
      for (var col = topLeft.col; col <= bottomRight.col; col++) {
        var cell = instance.getCell(row, col);
        var cellProperties$__2 = instance.getCellMeta(row, col);
        var checkboxes = cell.querySelectorAll('input[type=checkbox]');
        if (checkboxes.length > 0 && !cellProperties$__2.readOnly) {
          callback(checkboxes);
        }
      }
    }
  }
  function preventDefault(event) {
    event.preventDefault();
  }
  function stopPropagation(event) {
    helper.stopPropagation(event);
  }
}
;
registerRenderer('checkbox', checkboxRenderer);


//# 
},{"./../dom.js":27,"./../eventManager.js":41,"./../helpers.js":42,"./../renderers.js":70}],74:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  htmlRenderer: {get: function() {
      return htmlRenderer;
    }},
  __esModule: {value: true}
});
var $___46__46__47_dom_46_js__,
    $___46__46__47_renderers_46_js__;
var dom = ($___46__46__47_dom_46_js__ = require("./../dom.js"), $___46__46__47_dom_46_js__ && $___46__46__47_dom_46_js__.__esModule && $___46__46__47_dom_46_js__ || {default: $___46__46__47_dom_46_js__});
var $__0 = ($___46__46__47_renderers_46_js__ = require("./../renderers.js"), $___46__46__47_renderers_46_js__ && $___46__46__47_renderers_46_js__.__esModule && $___46__46__47_renderers_46_js__ || {default: $___46__46__47_renderers_46_js__}),
    getRenderer = $__0.getRenderer,
    registerRenderer = $__0.registerRenderer;
;
registerRenderer('html', htmlRenderer);
function htmlRenderer(instance, TD, row, col, prop, value, cellProperties) {
  getRenderer('base').apply(this, arguments);
  dom.fastInnerHTML(TD, value);
}


//# 
},{"./../dom.js":27,"./../renderers.js":70}],75:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  numericRenderer: {get: function() {
      return numericRenderer;
    }},
  __esModule: {value: true}
});
var $___46__46__47_dom_46_js__,
    $___46__46__47_helpers_46_js__,
    $__numeral__,
    $___46__46__47_renderers_46_js__;
var dom = ($___46__46__47_dom_46_js__ = require("./../dom.js"), $___46__46__47_dom_46_js__ && $___46__46__47_dom_46_js__.__esModule && $___46__46__47_dom_46_js__ || {default: $___46__46__47_dom_46_js__});
var helper = ($___46__46__47_helpers_46_js__ = require("./../helpers.js"), $___46__46__47_helpers_46_js__ && $___46__46__47_helpers_46_js__.__esModule && $___46__46__47_helpers_46_js__ || {default: $___46__46__47_helpers_46_js__});
var numeral = ($__numeral__ = require("numeral"), $__numeral__ && $__numeral__.__esModule && $__numeral__ || {default: $__numeral__}).default;
var $__1 = ($___46__46__47_renderers_46_js__ = require("./../renderers.js"), $___46__46__47_renderers_46_js__ && $___46__46__47_renderers_46_js__.__esModule && $___46__46__47_renderers_46_js__ || {default: $___46__46__47_renderers_46_js__}),
    getRenderer = $__1.getRenderer,
    registerRenderer = $__1.registerRenderer;
;
registerRenderer('numeric', numericRenderer);
function numericRenderer(instance, TD, row, col, prop, value, cellProperties) {
  if (helper.isNumeric(value)) {
    if (typeof cellProperties.language !== 'undefined') {
      numeral.language(cellProperties.language);
    }
    value = numeral(value).format(cellProperties.format || '0');
    dom.addClass(TD, 'htNumeric');
  }
  getRenderer('text')(instance, TD, row, col, prop, value, cellProperties);
}


//# 
},{"./../dom.js":27,"./../helpers.js":42,"./../renderers.js":70,"numeral":"numeral"}],76:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  passwordRenderer: {get: function() {
      return passwordRenderer;
    }},
  __esModule: {value: true}
});
var $___46__46__47_dom_46_js__,
    $___46__46__47_renderers_46_js__;
var dom = ($___46__46__47_dom_46_js__ = require("./../dom.js"), $___46__46__47_dom_46_js__ && $___46__46__47_dom_46_js__.__esModule && $___46__46__47_dom_46_js__ || {default: $___46__46__47_dom_46_js__});
var $__0 = ($___46__46__47_renderers_46_js__ = require("./../renderers.js"), $___46__46__47_renderers_46_js__ && $___46__46__47_renderers_46_js__.__esModule && $___46__46__47_renderers_46_js__ || {default: $___46__46__47_renderers_46_js__}),
    getRenderer = $__0.getRenderer,
    registerRenderer = $__0.registerRenderer;
;
registerRenderer('password', passwordRenderer);
function passwordRenderer(instance, TD, row, col, prop, value, cellProperties) {
  getRenderer('text').apply(this, arguments);
  value = TD.innerHTML;
  var hash;
  var hashLength = cellProperties.hashLength || value.length;
  var hashSymbol = cellProperties.hashSymbol || '*';
  for (hash = ''; hash.split(hashSymbol).length - 1 < hashLength; hash += hashSymbol) {}
  dom.fastInnerHTML(TD, hash);
}


//# 
},{"./../dom.js":27,"./../renderers.js":70}],77:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  textRenderer: {get: function() {
      return textRenderer;
    }},
  __esModule: {value: true}
});
var $___46__46__47_dom_46_js__,
    $___46__46__47_helpers_46_js__,
    $___46__46__47_renderers_46_js__;
var dom = ($___46__46__47_dom_46_js__ = require("./../dom.js"), $___46__46__47_dom_46_js__ && $___46__46__47_dom_46_js__.__esModule && $___46__46__47_dom_46_js__ || {default: $___46__46__47_dom_46_js__});
var helper = ($___46__46__47_helpers_46_js__ = require("./../helpers.js"), $___46__46__47_helpers_46_js__ && $___46__46__47_helpers_46_js__.__esModule && $___46__46__47_helpers_46_js__ || {default: $___46__46__47_helpers_46_js__});
var $__0 = ($___46__46__47_renderers_46_js__ = require("./../renderers.js"), $___46__46__47_renderers_46_js__ && $___46__46__47_renderers_46_js__.__esModule && $___46__46__47_renderers_46_js__ || {default: $___46__46__47_renderers_46_js__}),
    getRenderer = $__0.getRenderer,
    registerRenderer = $__0.registerRenderer;
;
registerRenderer('text', textRenderer);
function textRenderer(instance, TD, row, col, prop, value, cellProperties) {
  getRenderer('base').apply(this, arguments);
  if (!value && cellProperties.placeholder) {
    value = cellProperties.placeholder;
  }
  var escaped = helper.stringify(value);
  if (!instance.getSettings().trimWhitespace) {
    escaped = escaped.replace(/ /g, String.fromCharCode(160));
  }
  if (cellProperties.rendererTemplate) {
    dom.empty(TD);
    var TEMPLATE = document.createElement('TEMPLATE');
    TEMPLATE.setAttribute('bind', '{{}}');
    TEMPLATE.innerHTML = cellProperties.rendererTemplate;
    HTMLTemplateElement.decorate(TEMPLATE);
    TEMPLATE.model = instance.getSourceDataAtRow(row);
    TD.appendChild(TEMPLATE);
  } else {
    dom.fastInnerText(TD, escaped);
  }
}


//# 
},{"./../dom.js":27,"./../helpers.js":42,"./../renderers.js":70}],78:[function(require,module,exports){
"use strict";
if (!Array.prototype.filter) {
  Array.prototype.filter = function(fun, thisp) {
    "use strict";
    if (typeof this === "undefined" || this === null) {
      throw new TypeError();
    }
    if (typeof fun !== "function") {
      throw new TypeError();
    }
    thisp = thisp || this;
    if (isNodeList(thisp)) {
      thisp = convertNodeListToArray(thisp);
    }
    var len = thisp.length,
        res = [],
        i,
        val;
    for (i = 0; i < len; i += 1) {
      if (thisp.hasOwnProperty(i)) {
        val = thisp[i];
        if (fun.call(thisp, val, i, thisp)) {
          res.push(val);
        }
      }
    }
    return res;
    function isNodeList(object) {
      return /NodeList/i.test(object.item);
    }
    function convertNodeListToArray(nodeList) {
      var array = [];
      for (var i = 0,
          len = nodeList.length; i < len; i++) {
        array[i] = nodeList[i];
      }
      return array;
    }
  };
}


//# 
},{}],79:[function(require,module,exports){
"use strict";
if (!Array.prototype.indexOf) {
  Array.prototype.indexOf = function(elt) {
    var len = this.length >>> 0;
    var from = Number(arguments[1]) || 0;
    from = (from < 0) ? Math.ceil(from) : Math.floor(from);
    if (from < 0) {
      from += len;
    }
    for (; from < len; from++) {
      if (from in this && this[from] === elt) {
        return from;
      }
    }
    return -1;
  };
}


//# 
},{}],80:[function(require,module,exports){
"use strict";
if (!Array.isArray) {
  Array.isArray = function(obj) {
    return Object.prototype.toString.call(obj) == '[object Array]';
  };
}


//# 
},{}],81:[function(require,module,exports){
"use strict";
(function(global) {
  'use strict';
  if (global.$traceurRuntime) {
    return;
  }
  var $Object = Object;
  var $TypeError = TypeError;
  var $create = $Object.create;
  var $defineProperties = $Object.defineProperties;
  var $defineProperty = $Object.defineProperty;
  var $freeze = $Object.freeze;
  var $getOwnPropertyDescriptor = $Object.getOwnPropertyDescriptor;
  var $getOwnPropertyNames = $Object.getOwnPropertyNames;
  var $keys = $Object.keys;
  var $hasOwnProperty = $Object.prototype.hasOwnProperty;
  var $toString = $Object.prototype.toString;
  var $preventExtensions = Object.preventExtensions;
  var $seal = Object.seal;
  var $isExtensible = Object.isExtensible;
  function nonEnum(value) {
    return {
      configurable: true,
      enumerable: false,
      value: value,
      writable: true
    };
  }
  var method = nonEnum;
  var counter = 0;
  function newUniqueString() {
    return '__$' + Math.floor(Math.random() * 1e9) + '$' + ++counter + '$__';
  }
  var symbolInternalProperty = newUniqueString();
  var symbolDescriptionProperty = newUniqueString();
  var symbolDataProperty = newUniqueString();
  var symbolValues = $create(null);
  var privateNames = $create(null);
  function isPrivateName(s) {
    return privateNames[s];
  }
  function createPrivateName() {
    var s = newUniqueString();
    privateNames[s] = true;
    return s;
  }
  function isShimSymbol(symbol) {
    return typeof symbol === 'object' && symbol instanceof SymbolValue;
  }
  function typeOf(v) {
    if (isShimSymbol(v))
      return 'symbol';
    return typeof v;
  }
  function Symbol(description) {
    var value = new SymbolValue(description);
    if (!(this instanceof Symbol))
      return value;
    throw new TypeError('Symbol cannot be new\'ed');
  }
  $defineProperty(Symbol.prototype, 'constructor', nonEnum(Symbol));
  $defineProperty(Symbol.prototype, 'toString', method(function() {
    var symbolValue = this[symbolDataProperty];
    if (!getOption('symbols'))
      return symbolValue[symbolInternalProperty];
    if (!symbolValue)
      throw TypeError('Conversion from symbol to string');
    var desc = symbolValue[symbolDescriptionProperty];
    if (desc === undefined)
      desc = '';
    return 'Symbol(' + desc + ')';
  }));
  $defineProperty(Symbol.prototype, 'valueOf', method(function() {
    var symbolValue = this[symbolDataProperty];
    if (!symbolValue)
      throw TypeError('Conversion from symbol to string');
    if (!getOption('symbols'))
      return symbolValue[symbolInternalProperty];
    return symbolValue;
  }));
  function SymbolValue(description) {
    var key = newUniqueString();
    $defineProperty(this, symbolDataProperty, {value: this});
    $defineProperty(this, symbolInternalProperty, {value: key});
    $defineProperty(this, symbolDescriptionProperty, {value: description});
    freeze(this);
    symbolValues[key] = this;
  }
  $defineProperty(SymbolValue.prototype, 'constructor', nonEnum(Symbol));
  $defineProperty(SymbolValue.prototype, 'toString', {
    value: Symbol.prototype.toString,
    enumerable: false
  });
  $defineProperty(SymbolValue.prototype, 'valueOf', {
    value: Symbol.prototype.valueOf,
    enumerable: false
  });
  var hashProperty = createPrivateName();
  var hashPropertyDescriptor = {value: undefined};
  var hashObjectProperties = {
    hash: {value: undefined},
    self: {value: undefined}
  };
  var hashCounter = 0;
  function getOwnHashObject(object) {
    var hashObject = object[hashProperty];
    if (hashObject && hashObject.self === object)
      return hashObject;
    if ($isExtensible(object)) {
      hashObjectProperties.hash.value = hashCounter++;
      hashObjectProperties.self.value = object;
      hashPropertyDescriptor.value = $create(null, hashObjectProperties);
      $defineProperty(object, hashProperty, hashPropertyDescriptor);
      return hashPropertyDescriptor.value;
    }
    return undefined;
  }
  function freeze(object) {
    getOwnHashObject(object);
    return $freeze.apply(this, arguments);
  }
  function preventExtensions(object) {
    getOwnHashObject(object);
    return $preventExtensions.apply(this, arguments);
  }
  function seal(object) {
    getOwnHashObject(object);
    return $seal.apply(this, arguments);
  }
  freeze(SymbolValue.prototype);
  function isSymbolString(s) {
    return symbolValues[s] || privateNames[s];
  }
  function toProperty(name) {
    if (isShimSymbol(name))
      return name[symbolInternalProperty];
    return name;
  }
  function removeSymbolKeys(array) {
    var rv = [];
    for (var i = 0; i < array.length; i++) {
      if (!isSymbolString(array[i])) {
        rv.push(array[i]);
      }
    }
    return rv;
  }
  function getOwnPropertyNames(object) {
    return removeSymbolKeys($getOwnPropertyNames(object));
  }
  function keys(object) {
    return removeSymbolKeys($keys(object));
  }
  function getOwnPropertySymbols(object) {
    var rv = [];
    var names = $getOwnPropertyNames(object);
    for (var i = 0; i < names.length; i++) {
      var symbol = symbolValues[names[i]];
      if (symbol) {
        rv.push(symbol);
      }
    }
    return rv;
  }
  function getOwnPropertyDescriptor(object, name) {
    return $getOwnPropertyDescriptor(object, toProperty(name));
  }
  function hasOwnProperty(name) {
    return $hasOwnProperty.call(this, toProperty(name));
  }
  function getOption(name) {
    return global.traceur && global.traceur.options[name];
  }
  function defineProperty(object, name, descriptor) {
    if (isShimSymbol(name)) {
      name = name[symbolInternalProperty];
    }
    $defineProperty(object, name, descriptor);
    return object;
  }
  function polyfillObject(Object) {
    $defineProperty(Object, 'defineProperty', {value: defineProperty});
    $defineProperty(Object, 'getOwnPropertyNames', {value: getOwnPropertyNames});
    $defineProperty(Object, 'getOwnPropertyDescriptor', {value: getOwnPropertyDescriptor});
    $defineProperty(Object.prototype, 'hasOwnProperty', {value: hasOwnProperty});
    $defineProperty(Object, 'freeze', {value: freeze});
    $defineProperty(Object, 'preventExtensions', {value: preventExtensions});
    $defineProperty(Object, 'seal', {value: seal});
    $defineProperty(Object, 'keys', {value: keys});
  }
  function exportStar(object) {
    for (var i = 1; i < arguments.length; i++) {
      var names = $getOwnPropertyNames(arguments[i]);
      for (var j = 0; j < names.length; j++) {
        var name = names[j];
        if (isSymbolString(name))
          continue;
        (function(mod, name) {
          $defineProperty(object, name, {
            get: function() {
              return mod[name];
            },
            enumerable: true
          });
        })(arguments[i], names[j]);
      }
    }
    return object;
  }
  function isObject(x) {
    return x != null && (typeof x === 'object' || typeof x === 'function');
  }
  function toObject(x) {
    if (x == null)
      throw $TypeError();
    return $Object(x);
  }
  function checkObjectCoercible(argument) {
    if (argument == null) {
      throw new TypeError('Value cannot be converted to an Object');
    }
    return argument;
  }
  function polyfillSymbol(global, Symbol) {
    if (!global.Symbol) {
      global.Symbol = Symbol;
      Object.getOwnPropertySymbols = getOwnPropertySymbols;
    }
    if (!global.Symbol.iterator) {
      global.Symbol.iterator = Symbol('Symbol.iterator');
    }
  }
  function setupGlobals(global) {
    polyfillSymbol(global, Symbol);
    global.Reflect = global.Reflect || {};
    global.Reflect.global = global.Reflect.global || global;
    polyfillObject(global.Object);
  }
  setupGlobals(global);
  global.$traceurRuntime = {
    checkObjectCoercible: checkObjectCoercible,
    createPrivateName: createPrivateName,
    defineProperties: $defineProperties,
    defineProperty: $defineProperty,
    exportStar: exportStar,
    getOwnHashObject: getOwnHashObject,
    getOwnPropertyDescriptor: $getOwnPropertyDescriptor,
    getOwnPropertyNames: $getOwnPropertyNames,
    isObject: isObject,
    isPrivateName: isPrivateName,
    isSymbolString: isSymbolString,
    keys: $keys,
    setupGlobals: setupGlobals,
    toObject: toObject,
    toProperty: toProperty,
    typeof: typeOf
  };
})(window);
(function() {
  'use strict';
  var path;
  function relativeRequire(callerPath, requiredPath) {
    path = path || typeof require !== 'undefined' && require('path');
    function isDirectory(path) {
      return path.slice(-1) === '/';
    }
    function isAbsolute(path) {
      return path[0] === '/';
    }
    function isRelative(path) {
      return path[0] === '.';
    }
    if (isDirectory(requiredPath) || isAbsolute(requiredPath))
      return;
    return isRelative(requiredPath) ? require(path.resolve(path.dirname(callerPath), requiredPath)) : require(requiredPath);
  }
  $traceurRuntime.require = relativeRequire;
})();
(function() {
  'use strict';
  function spread() {
    var rv = [],
        j = 0,
        iterResult;
    for (var i = 0; i < arguments.length; i++) {
      var valueToSpread = $traceurRuntime.checkObjectCoercible(arguments[i]);
      if (typeof valueToSpread[$traceurRuntime.toProperty(Symbol.iterator)] !== 'function') {
        throw new TypeError('Cannot spread non-iterable object.');
      }
      var iter = valueToSpread[$traceurRuntime.toProperty(Symbol.iterator)]();
      while (!(iterResult = iter.next()).done) {
        rv[j++] = iterResult.value;
      }
    }
    return rv;
  }
  $traceurRuntime.spread = spread;
})();
(function() {
  'use strict';
  var $Object = Object;
  var $TypeError = TypeError;
  var $create = $Object.create;
  var $defineProperties = $traceurRuntime.defineProperties;
  var $defineProperty = $traceurRuntime.defineProperty;
  var $getOwnPropertyDescriptor = $traceurRuntime.getOwnPropertyDescriptor;
  var $getOwnPropertyNames = $traceurRuntime.getOwnPropertyNames;
  var $getPrototypeOf = Object.getPrototypeOf;
  var $__0 = Object,
      getOwnPropertyNames = $__0.getOwnPropertyNames,
      getOwnPropertySymbols = $__0.getOwnPropertySymbols;
  function superDescriptor(homeObject, name) {
    var proto = $getPrototypeOf(homeObject);
    do {
      var result = $getOwnPropertyDescriptor(proto, name);
      if (result)
        return result;
      proto = $getPrototypeOf(proto);
    } while (proto);
    return undefined;
  }
  function superConstructor(ctor) {
    return ctor.__proto__;
  }
  function superCall(self, homeObject, name, args) {
    return superGet(self, homeObject, name).apply(self, args);
  }
  function superGet(self, homeObject, name) {
    var descriptor = superDescriptor(homeObject, name);
    if (descriptor) {
      if (!descriptor.get)
        return descriptor.value;
      return descriptor.get.call(self);
    }
    return undefined;
  }
  function superSet(self, homeObject, name, value) {
    var descriptor = superDescriptor(homeObject, name);
    if (descriptor && descriptor.set) {
      descriptor.set.call(self, value);
      return value;
    }
    throw $TypeError(("super has no setter '" + name + "'."));
  }
  function getDescriptors(object) {
    var descriptors = {};
    var names = getOwnPropertyNames(object);
    for (var i = 0; i < names.length; i++) {
      var name = names[i];
      descriptors[name] = $getOwnPropertyDescriptor(object, name);
    }
    var symbols = getOwnPropertySymbols(object);
    for (var i = 0; i < symbols.length; i++) {
      var symbol = symbols[i];
      descriptors[$traceurRuntime.toProperty(symbol)] = $getOwnPropertyDescriptor(object, $traceurRuntime.toProperty(symbol));
    }
    return descriptors;
  }
  function createClass(ctor, object, staticObject, superClass) {
    $defineProperty(object, 'constructor', {
      value: ctor,
      configurable: true,
      enumerable: false,
      writable: true
    });
    if (arguments.length > 3) {
      if (typeof superClass === 'function')
        ctor.__proto__ = superClass;
      ctor.prototype = $create(getProtoParent(superClass), getDescriptors(object));
    } else {
      ctor.prototype = object;
    }
    $defineProperty(ctor, 'prototype', {
      configurable: false,
      writable: false
    });
    return $defineProperties(ctor, getDescriptors(staticObject));
  }
  function getProtoParent(superClass) {
    if (typeof superClass === 'function') {
      var prototype = superClass.prototype;
      if ($Object(prototype) === prototype || prototype === null)
        return superClass.prototype;
      throw new $TypeError('super prototype must be an Object or null');
    }
    if (superClass === null)
      return null;
    throw new $TypeError(("Super expression must either be null or a function, not " + typeof superClass + "."));
  }
  function defaultSuperCall(self, homeObject, args) {
    if ($getPrototypeOf(homeObject) !== null)
      superCall(self, homeObject, 'constructor', args);
  }
  $traceurRuntime.createClass = createClass;
  $traceurRuntime.defaultSuperCall = defaultSuperCall;
  $traceurRuntime.superCall = superCall;
  $traceurRuntime.superConstructor = superConstructor;
  $traceurRuntime.superGet = superGet;
  $traceurRuntime.superSet = superSet;
})();


//# 
},{"path":undefined}],82:[function(require,module,exports){
"use strict";
if (!Object.keys) {
  Object.keys = (function() {
    'use strict';
    var hasOwnProperty = Object.prototype.hasOwnProperty,
        hasDontEnumBug = !({toString: null}).propertyIsEnumerable('toString'),
        dontEnums = ['toString', 'toLocaleString', 'valueOf', 'hasOwnProperty', 'isPrototypeOf', 'propertyIsEnumerable', 'constructor'],
        dontEnumsLength = dontEnums.length;
    return function(obj) {
      if (typeof obj !== 'object' && (typeof obj !== 'function' || obj === null)) {
        throw new TypeError('Object.keys called on non-object');
      }
      var result = [],
          prop,
          i;
      for (prop in obj) {
        if (hasOwnProperty.call(obj, prop)) {
          result.push(prop);
        }
      }
      if (hasDontEnumBug) {
        for (i = 0; i < dontEnumsLength; i++) {
          if (hasOwnProperty.call(obj, dontEnums[i])) {
            result.push(dontEnums[i]);
          }
        }
      }
      return result;
    };
  }());
}


//# 
},{}],83:[function(require,module,exports){
"use strict";
if (!String.prototype.trim) {
  var trimRegex = /^\s+|\s+$/g;
  String.prototype.trim = function() {
    return this.replace(trimRegex, '');
  };
}


//# 
},{}],84:[function(require,module,exports){
"use strict";
if (typeof WeakMap === 'undefined') {
  (function() {
    var defineProperty = Object.defineProperty;
    try {
      var properDefineProperty = true;
      defineProperty(function() {}, 'foo', {});
    } catch (e) {
      properDefineProperty = false;
    }
    var counter = +(new Date) % 1e9;
    var WeakMap = function() {
      this.name = '__st' + (Math.random() * 1e9 >>> 0) + (counter++ + '__');
      if (!properDefineProperty) {
        this._wmCache = [];
      }
    };
    if (properDefineProperty) {
      WeakMap.prototype = {
        set: function(key, value) {
          var entry = key[this.name];
          if (entry && entry[0] === key)
            entry[1] = value;
          else
            defineProperty(key, this.name, {
              value: [key, value],
              writable: true
            });
        },
        get: function(key) {
          var entry;
          return (entry = key[this.name]) && entry[0] === key ? entry[1] : undefined;
        },
        has: function(key) {
          return this.get(key) ? true : false;
        },
        'delete': function(key) {
          this.set(key, undefined);
        }
      };
    } else {
      WeakMap.prototype = {
        set: function(key, value) {
          if (typeof key == 'undefined' || typeof value == 'undefined')
            return;
          for (var i = 0,
              len = this._wmCache.length; i < len; i++) {
            if (this._wmCache[i].key == key) {
              this._wmCache[i].value = value;
              return;
            }
          }
          this._wmCache.push({
            key: key,
            value: value
          });
        },
        get: function(key) {
          if (typeof key == 'undefined')
            return;
          for (var i = 0,
              len = this._wmCache.length; i < len; i++) {
            if (this._wmCache[i].key == key) {
              return this._wmCache[i].value;
            }
          }
          return void 0;
        },
        has: function(key) {
          return this.get(key) ? true : false;
        },
        'delete': function(key) {
          if (typeof key == 'undefined')
            return;
          for (var i = 0,
              len = this._wmCache.length; i < len; i++) {
            if (this._wmCache[i].key == key) {
              Array.prototype.slice.call(this._wmCache, i, 1);
            }
          }
        }
      };
    }
    window.WeakMap = WeakMap;
  })();
}


//# 
},{}],85:[function(require,module,exports){
"use strict";
Object.defineProperties(exports, {
  TableView: {get: function() {
      return TableView;
    }},
  __esModule: {value: true}
});
var $__dom_46_js__,
    $__helpers_46_js__,
    $__eventManager_46_js__,
    $__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__,
    $__3rdparty_47_walkontable_47_src_47_selection_46_js__,
    $__3rdparty_47_walkontable_47_src_47_core_46_js__;
var dom = ($__dom_46_js__ = require("./dom.js"), $__dom_46_js__ && $__dom_46_js__.__esModule && $__dom_46_js__ || {default: $__dom_46_js__});
var helper = ($__helpers_46_js__ = require("./helpers.js"), $__helpers_46_js__ && $__helpers_46_js__.__esModule && $__helpers_46_js__ || {default: $__helpers_46_js__});
var eventManagerObject = ($__eventManager_46_js__ = require("./eventManager.js"), $__eventManager_46_js__ && $__eventManager_46_js__.__esModule && $__eventManager_46_js__ || {default: $__eventManager_46_js__}).eventManager;
var WalkontableCellCoords = ($__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ = require("./3rdparty/walkontable/src/cell/coords.js"), $__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ && $__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__.__esModule && $__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__ || {default: $__3rdparty_47_walkontable_47_src_47_cell_47_coords_46_js__}).WalkontableCellCoords;
var WalkontableSelection = ($__3rdparty_47_walkontable_47_src_47_selection_46_js__ = require("./3rdparty/walkontable/src/selection.js"), $__3rdparty_47_walkontable_47_src_47_selection_46_js__ && $__3rdparty_47_walkontable_47_src_47_selection_46_js__.__esModule && $__3rdparty_47_walkontable_47_src_47_selection_46_js__ || {default: $__3rdparty_47_walkontable_47_src_47_selection_46_js__}).WalkontableSelection;
var Walkontable = ($__3rdparty_47_walkontable_47_src_47_core_46_js__ = require("./3rdparty/walkontable/src/core.js"), $__3rdparty_47_walkontable_47_src_47_core_46_js__ && $__3rdparty_47_walkontable_47_src_47_core_46_js__.__esModule && $__3rdparty_47_walkontable_47_src_47_core_46_js__ || {default: $__3rdparty_47_walkontable_47_src_47_core_46_js__}).Walkontable;
Handsontable.TableView = TableView;
function TableView(instance) {
  var that = this;
  this.eventManager = eventManagerObject(instance);
  this.instance = instance;
  this.settings = instance.getSettings();
  var originalStyle = instance.rootElement.getAttribute('style');
  if (originalStyle) {
    instance.rootElement.setAttribute('data-originalstyle', originalStyle);
  }
  dom.addClass(instance.rootElement, 'handsontable');
  var table = document.createElement('TABLE');
  table.className = 'htCore';
  this.THEAD = document.createElement('THEAD');
  table.appendChild(this.THEAD);
  this.TBODY = document.createElement('TBODY');
  table.appendChild(this.TBODY);
  instance.table = table;
  instance.container.insertBefore(table, instance.container.firstChild);
  this.eventManager.addEventListener(instance.rootElement, 'mousedown', function(event) {
    if (!that.isTextSelectionAllowed(event.target)) {
      clearTextSelection();
      event.preventDefault();
      window.focus();
    }
  });
  this.eventManager.addEventListener(document.documentElement, 'keyup', function(event) {
    if (instance.selection.isInProgress() && !event.shiftKey) {
      instance.selection.finish();
    }
  });
  var isMouseDown;
  this.isMouseDown = function() {
    return isMouseDown;
  };
  this.eventManager.addEventListener(document.documentElement, 'mouseup', function(event) {
    if (instance.selection.isInProgress() && event.which === 1) {
      instance.selection.finish();
    }
    isMouseDown = false;
    if (helper.isOutsideInput(document.activeElement)) {
      instance.unlisten();
    }
  });
  this.eventManager.addEventListener(document.documentElement, 'mousedown', function(event) {
    var next = event.target;
    if (isMouseDown) {
      return;
    }
    if (next !== instance.view.wt.wtTable.holder) {
      while (next !== document.documentElement) {
        if (next === null) {
          if (event.isTargetWebComponent) {
            break;
          }
          return;
        }
        if (next === instance.rootElement) {
          return;
        }
        next = next.parentNode;
      }
    } else {
      var scrollbarWidth = Handsontable.Dom.getScrollbarWidth();
      if (document.elementFromPoint(event.x + scrollbarWidth, event.y) !== instance.view.wt.wtTable.holder || document.elementFromPoint(event.x, event.y + scrollbarWidth) !== instance.view.wt.wtTable.holder) {
        return;
      }
    }
    if (that.settings.outsideClickDeselects) {
      instance.deselectCell();
    } else {
      instance.destroyEditor();
    }
  });
  this.eventManager.addEventListener(table, 'selectstart', function(event) {
    if (that.settings.fragmentSelection) {
      return;
    }
    event.preventDefault();
  });
  var clearTextSelection = function() {
    if (window.getSelection) {
      if (window.getSelection().empty) {
        window.getSelection().empty();
      } else if (window.getSelection().removeAllRanges) {
        window.getSelection().removeAllRanges();
      }
    } else if (document.selection) {
      document.selection.empty();
    }
  };
  var selections = [new WalkontableSelection({
    className: 'current',
    border: {
      width: 2,
      color: '#5292F7',
      cornerVisible: function() {
        return that.settings.fillHandle && !that.isCellEdited() && !instance.selection.isMultiple();
      },
      multipleSelectionHandlesVisible: function() {
        return !that.isCellEdited() && !instance.selection.isMultiple();
      }
    }
  }), new WalkontableSelection({
    className: 'area',
    border: {
      width: 1,
      color: '#89AFF9',
      cornerVisible: function() {
        return that.settings.fillHandle && !that.isCellEdited() && instance.selection.isMultiple();
      },
      multipleSelectionHandlesVisible: function() {
        return !that.isCellEdited() && instance.selection.isMultiple();
      }
    }
  }), new WalkontableSelection({
    className: 'highlight',
    highlightRowClassName: that.settings.currentRowClassName,
    highlightColumnClassName: that.settings.currentColClassName
  }), new WalkontableSelection({
    className: 'fill',
    border: {
      width: 1,
      color: 'red'
    }
  })];
  selections.current = selections[0];
  selections.area = selections[1];
  selections.highlight = selections[2];
  selections.fill = selections[3];
  var walkontableConfig = {
    debug: function() {
      return that.settings.debug;
    },
    table: table,
    stretchH: this.settings.stretchH,
    data: instance.getDataAtCell,
    totalRows: instance.countRows,
    totalColumns: instance.countCols,
    fixedColumnsLeft: function() {
      return that.settings.fixedColumnsLeft;
    },
    fixedRowsTop: function() {
      return that.settings.fixedRowsTop;
    },
    renderAllRows: that.settings.renderAllRows,
    rowHeaders: function() {
      var arr = [];
      if (instance.hasRowHeaders()) {
        arr.push(function(index, TH) {
          that.appendRowHeader(index, TH);
        });
      }
      Handsontable.hooks.run(instance, 'afterGetRowHeaderRenderers', arr);
      return arr;
    },
    columnHeaders: function() {
      var arr = [];
      if (instance.hasColHeaders()) {
        arr.push(function(index, TH) {
          that.appendColHeader(index, TH);
        });
      }
      Handsontable.hooks.run(instance, 'afterGetColumnHeaderRenderers', arr);
      return arr;
    },
    columnWidth: instance.getColWidth,
    rowHeight: instance.getRowHeight,
    cellRenderer: function(row, col, TD) {
      var prop = that.instance.colToProp(col),
          cellProperties = that.instance.getCellMeta(row, col),
          renderer = that.instance.getCellRenderer(cellProperties);
      var value = that.instance.getDataAtRowProp(row, prop);
      renderer(that.instance, TD, row, col, prop, value, cellProperties);
      Handsontable.hooks.run(that.instance, 'afterRenderer', TD, row, col, prop, value, cellProperties);
    },
    selections: selections,
    hideBorderOnMouseDownOver: function() {
      return that.settings.fragmentSelection;
    },
    onCellMouseDown: function(event, coords, TD, wt) {
      instance.listen();
      that.activeWt = wt;
      isMouseDown = true;
      dom.enableImmediatePropagation(event);
      Handsontable.hooks.run(instance, 'beforeOnCellMouseDown', event, coords, TD);
      if (!event.isImmediatePropagationStopped()) {
        if (event.button === 2 && instance.selection.inInSelection(coords)) {} else if (event.shiftKey) {
          if (coords.row >= 0 && coords.col >= 0) {
            instance.selection.setRangeEnd(coords);
          }
        } else {
          if ((coords.row < 0 || coords.col < 0) && (coords.row >= 0 || coords.col >= 0)) {
            if (coords.row < 0) {
              instance.selectCell(0, coords.col, instance.countRows() - 1, coords.col);
              instance.selection.setSelectedHeaders(false, true);
            }
            if (coords.col < 0) {
              instance.selectCell(coords.row, 0, coords.row, instance.countCols() - 1);
              instance.selection.setSelectedHeaders(true, false);
            }
          } else {
            coords.row = coords.row < 0 ? 0 : coords.row;
            coords.col = coords.col < 0 ? 0 : coords.col;
            instance.selection.setRangeStart(coords);
          }
        }
        Handsontable.hooks.run(instance, 'afterOnCellMouseDown', event, coords, TD);
        that.activeWt = that.wt;
      }
    },
    onCellMouseOver: function(event, coords, TD, wt) {
      that.activeWt = wt;
      if (coords.row >= 0 && coords.col >= 0) {
        if (isMouseDown) {
          instance.selection.setRangeEnd(coords);
        }
      } else {
        if (isMouseDown) {
          if (coords.row < 0) {
            instance.selection.setRangeEnd(new WalkontableCellCoords(instance.countRows() - 1, coords.col));
            instance.selection.setSelectedHeaders(false, true);
          }
          if (coords.col < 0) {
            instance.selection.setRangeEnd(new WalkontableCellCoords(coords.row, instance.countCols() - 1));
            instance.selection.setSelectedHeaders(true, false);
          }
        }
      }
      Handsontable.hooks.run(instance, 'afterOnCellMouseOver', event, coords, TD);
      that.activeWt = that.wt;
    },
    onCellCornerMouseDown: function(event) {
      event.preventDefault();
      Handsontable.hooks.run(instance, 'afterOnCellCornerMouseDown', event);
    },
    beforeDraw: function(force) {
      that.beforeRender(force);
    },
    onDraw: function(force) {
      that.onDraw(force);
    },
    onScrollVertically: function() {
      instance.runHooks('afterScrollVertically');
    },
    onScrollHorizontally: function() {
      instance.runHooks('afterScrollHorizontally');
    },
    onBeforeDrawBorders: function(corners, borderClassName) {
      instance.runHooks('beforeDrawBorders', corners, borderClassName);
    },
    onBeforeTouchScroll: function() {
      instance.runHooks('beforeTouchScroll');
    },
    onAfterMomentumScroll: function() {
      instance.runHooks('afterMomentumScroll');
    },
    viewportRowCalculatorOverride: function(calc) {
      if (that.settings.viewportRowRenderingOffset) {
        calc.startRow = Math.max(calc.startRow - that.settings.viewportRowRenderingOffset, 0);
        calc.endRow = Math.min(calc.endRow + that.settings.viewportRowRenderingOffset, instance.countRows() - 1);
      }
      instance.runHooks('afterViewportRowCalculatorOverride', calc);
    },
    viewportColumnCalculatorOverride: function(calc) {
      if (that.settings.viewportColumnRenderingOffset) {
        calc.startColumn = Math.max(calc.startColumn - that.settings.viewportColumnRenderingOffset, 0);
        calc.endColumn = Math.min(calc.endColumn + that.settings.viewportColumnRenderingOffset, instance.countCols() - 1);
      }
      instance.runHooks('afterViewportColumnCalculatorOverride', calc);
    }
  };
  Handsontable.hooks.run(instance, 'beforeInitWalkontable', walkontableConfig);
  this.wt = new Walkontable(walkontableConfig);
  this.activeWt = this.wt;
  this.eventManager.addEventListener(that.wt.wtTable.spreader, 'mousedown', function(event) {
    if (event.target === that.wt.wtTable.spreader && event.which === 3) {
      helper.stopPropagation(event);
    }
  });
  this.eventManager.addEventListener(that.wt.wtTable.spreader, 'contextmenu', function(event) {
    if (event.target === that.wt.wtTable.spreader && event.which === 3) {
      helper.stopPropagation(event);
    }
  });
  this.eventManager.addEventListener(document.documentElement, 'click', function() {
    if (that.settings.observeDOMVisibility) {
      if (that.wt.drawInterrupted) {
        that.instance.forceFullRender = true;
        that.render();
      }
    }
  });
}
TableView.prototype.isTextSelectionAllowed = function(el) {
  if (helper.isInput(el)) {
    return true;
  }
  if (this.settings.fragmentSelection && dom.isChildOf(el, this.TBODY)) {
    return true;
  }
  return false;
};
TableView.prototype.isCellEdited = function() {
  var activeEditor = this.instance.getActiveEditor();
  return activeEditor && activeEditor.isOpened();
};
TableView.prototype.beforeRender = function(force) {
  if (force) {
    Handsontable.hooks.run(this.instance, 'beforeRender', this.instance.forceFullRender);
  }
};
TableView.prototype.onDraw = function(force) {
  if (force) {
    Handsontable.hooks.run(this.instance, 'afterRender', this.instance.forceFullRender);
  }
};
TableView.prototype.render = function() {
  this.wt.draw(!this.instance.forceFullRender);
  this.instance.forceFullRender = false;
};
TableView.prototype.getCellAtCoords = function(coords, topmost) {
  var td = this.wt.getCell(coords, topmost);
  if (td < 0) {
    return null;
  } else {
    return td;
  }
};
TableView.prototype.scrollViewport = function(coords) {
  this.wt.scrollViewport(coords);
};
TableView.prototype.appendRowHeader = function(row, TH) {
  if (TH.firstChild) {
    var container = TH.firstChild;
    if (!dom.hasClass(container, 'relative')) {
      dom.empty(TH);
      this.appendRowHeader(row, TH);
      return;
    }
    this.updateCellHeader(container.firstChild, row, this.instance.getRowHeader);
  } else {
    var div = document.createElement('div');
    var span = document.createElement('span');
    div.className = 'relative';
    span.className = 'colHeader';
    this.updateCellHeader(span, row, this.instance.getRowHeader);
    div.appendChild(span);
    TH.appendChild(div);
  }
  Handsontable.hooks.run(this.instance, 'afterGetRowHeader', row, TH);
};
TableView.prototype.appendColHeader = function(col, TH) {
  if (TH.firstChild) {
    var container = TH.firstChild;
    if (!dom.hasClass(container, 'relative')) {
      dom.empty(TH);
      this.appendRowHeader(col, TH);
      return;
    }
    this.updateCellHeader(container.firstChild, col, this.instance.getColHeader);
  } else {
    var div = document.createElement('div');
    var span = document.createElement('span');
    div.className = 'relative';
    span.className = 'colHeader';
    this.updateCellHeader(span, col, this.instance.getColHeader);
    div.appendChild(span);
    TH.appendChild(div);
  }
  Handsontable.hooks.run(this.instance, 'afterGetColHeader', col, TH);
};
TableView.prototype.updateCellHeader = function(element, index, content) {
  if (index > -1) {
    dom.fastInnerHTML(element, content(index));
  } else {
    dom.fastInnerText(element, String.fromCharCode(160));
    dom.addClass(element, 'cornerHeader');
  }
};
TableView.prototype.maximumVisibleElementWidth = function(leftOffset) {
  var workspaceWidth = this.wt.wtViewport.getWorkspaceWidth();
  var maxWidth = workspaceWidth - leftOffset;
  return maxWidth > 0 ? maxWidth : 0;
};
TableView.prototype.maximumVisibleElementHeight = function(topOffset) {
  var workspaceHeight = this.wt.wtViewport.getWorkspaceHeight();
  var maxHeight = workspaceHeight - topOffset;
  return maxHeight > 0 ? maxHeight : 0;
};
TableView.prototype.mainViewIsActive = function() {
  return this.wt === this.activeWt;
};
TableView.prototype.destroy = function() {
  this.wt.destroy();
  this.eventManager.clear();
};
;


//# 
},{"./3rdparty/walkontable/src/cell/coords.js":5,"./3rdparty/walkontable/src/core.js":7,"./3rdparty/walkontable/src/selection.js":18,"./dom.js":27,"./eventManager.js":41,"./helpers.js":42}],86:[function(require,module,exports){
"use strict";
var process = function(value, callback) {
  var originalVal = value;
  var lowercaseVal = typeof originalVal === 'string' ? originalVal.toLowerCase() : null;
  return function(source) {
    var found = false;
    for (var s = 0,
        slen = source.length; s < slen; s++) {
      if (originalVal === source[s]) {
        found = true;
        break;
      } else if (lowercaseVal === Handsontable.helper.stringify(source[s]).toLowerCase()) {
        found = true;
        break;
      }
    }
    callback(found);
  };
};
Handsontable.AutocompleteValidator = function(value, callback) {
  if (this.strict && this.source) {
    if (typeof this.source === 'function') {
      this.source(value, process(value, callback));
    } else {
      process(value, callback)(this.source);
    }
  } else {
    callback(true);
  }
};


//# 
},{}],87:[function(require,module,exports){
"use strict";
var $__moment__;
var moment = ($__moment__ = require("moment"), $__moment__ && $__moment__.__esModule && $__moment__ || {default: $__moment__}).default;
Handsontable.DateValidator = function(value, callback) {
  var correctedValue = null,
      valid = true,
      dateEditor = Handsontable.editors.getEditor('date', this.instance);
  if (value === null) {
    value = '';
  }
  var isValidDate = moment(new Date(value)).isValid(),
      isValidFormat = moment(value, this.dateFormat || dateEditor.defaultDateFormat, true).isValid();
  if (!isValidDate) {
    valid = false;
  }
  if (!isValidDate && isValidFormat) {
    valid = true;
  }
  if (isValidDate && !isValidFormat) {
    if (this.correctFormat === true) {
      correctedValue = correctFormat(value, this.dateFormat);
      this.instance.setDataAtCell(this.row, this.col, correctedValue, 'dateValidator');
      valid = true;
    } else {
      valid = false;
    }
  }
  callback(valid);
};
var correctFormat = function(value, dateFormat) {
  value = moment(new Date(value)).format(dateFormat);
  return value;
};


//# 
},{"moment":undefined}],88:[function(require,module,exports){
"use strict";
Handsontable.NumericValidator = function(value, callback) {
  if (value === null) {
    value = '';
  }
  callback(/^-?\d*(\.|\,)?\d*$/.test(value));
};


//# 
},{}],"numeral":[function(require,module,exports){
"use strict";
(function() {
  var numeral,
      VERSION = '1.5.3',
      languages = {},
      currentLanguage = 'en',
      zeroFormat = null,
      defaultFormat = '0,0',
      hasModule = (typeof module !== 'undefined' && module.exports);
  function Numeral(number) {
    this._value = number;
  }
  function toFixed(value, precision, roundingFunction, optionals) {
    var power = Math.pow(10, precision),
        optionalsRegExp,
        output;
    output = (roundingFunction(value * power) / power).toFixed(precision);
    if (optionals) {
      optionalsRegExp = new RegExp('0{1,' + optionals + '}$');
      output = output.replace(optionalsRegExp, '');
    }
    return output;
  }
  function formatNumeral(n, format, roundingFunction) {
    var output;
    if (format.indexOf('$') > -1) {
      output = formatCurrency(n, format, roundingFunction);
    } else if (format.indexOf('%') > -1) {
      output = formatPercentage(n, format, roundingFunction);
    } else if (format.indexOf(':') > -1) {
      output = formatTime(n, format);
    } else {
      output = formatNumber(n._value, format, roundingFunction);
    }
    return output;
  }
  function unformatNumeral(n, string) {
    var stringOriginal = string,
        thousandRegExp,
        millionRegExp,
        billionRegExp,
        trillionRegExp,
        suffixes = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
        bytesMultiplier = false,
        power;
    if (string.indexOf(':') > -1) {
      n._value = unformatTime(string);
    } else {
      if (string === zeroFormat) {
        n._value = 0;
      } else {
        if (languages[currentLanguage].delimiters.decimal !== '.') {
          string = string.replace(/\./g, '').replace(languages[currentLanguage].delimiters.decimal, '.');
        }
        thousandRegExp = new RegExp('[^a-zA-Z]' + languages[currentLanguage].abbreviations.thousand + '(?:\\)|(\\' + languages[currentLanguage].currency.symbol + ')?(?:\\))?)?$');
        millionRegExp = new RegExp('[^a-zA-Z]' + languages[currentLanguage].abbreviations.million + '(?:\\)|(\\' + languages[currentLanguage].currency.symbol + ')?(?:\\))?)?$');
        billionRegExp = new RegExp('[^a-zA-Z]' + languages[currentLanguage].abbreviations.billion + '(?:\\)|(\\' + languages[currentLanguage].currency.symbol + ')?(?:\\))?)?$');
        trillionRegExp = new RegExp('[^a-zA-Z]' + languages[currentLanguage].abbreviations.trillion + '(?:\\)|(\\' + languages[currentLanguage].currency.symbol + ')?(?:\\))?)?$');
        for (power = 0; power <= suffixes.length; power++) {
          bytesMultiplier = (string.indexOf(suffixes[power]) > -1) ? Math.pow(1024, power + 1) : false;
          if (bytesMultiplier) {
            break;
          }
        }
        n._value = ((bytesMultiplier) ? bytesMultiplier : 1) * ((stringOriginal.match(thousandRegExp)) ? Math.pow(10, 3) : 1) * ((stringOriginal.match(millionRegExp)) ? Math.pow(10, 6) : 1) * ((stringOriginal.match(billionRegExp)) ? Math.pow(10, 9) : 1) * ((stringOriginal.match(trillionRegExp)) ? Math.pow(10, 12) : 1) * ((string.indexOf('%') > -1) ? 0.01 : 1) * (((string.split('-').length + Math.min(string.split('(').length - 1, string.split(')').length - 1)) % 2) ? 1 : -1) * Number(string.replace(/[^0-9\.]+/g, ''));
        n._value = (bytesMultiplier) ? Math.ceil(n._value) : n._value;
      }
    }
    return n._value;
  }
  function formatCurrency(n, format, roundingFunction) {
    var symbolIndex = format.indexOf('$'),
        openParenIndex = format.indexOf('('),
        minusSignIndex = format.indexOf('-'),
        space = '',
        spliceIndex,
        output;
    if (format.indexOf(' $') > -1) {
      space = ' ';
      format = format.replace(' $', '');
    } else if (format.indexOf('$ ') > -1) {
      space = ' ';
      format = format.replace('$ ', '');
    } else {
      format = format.replace('$', '');
    }
    output = formatNumber(n._value, format, roundingFunction);
    if (symbolIndex <= 1) {
      if (output.indexOf('(') > -1 || output.indexOf('-') > -1) {
        output = output.split('');
        spliceIndex = 1;
        if (symbolIndex < openParenIndex || symbolIndex < minusSignIndex) {
          spliceIndex = 0;
        }
        output.splice(spliceIndex, 0, languages[currentLanguage].currency.symbol + space);
        output = output.join('');
      } else {
        output = languages[currentLanguage].currency.symbol + space + output;
      }
    } else {
      if (output.indexOf(')') > -1) {
        output = output.split('');
        output.splice(-1, 0, space + languages[currentLanguage].currency.symbol);
        output = output.join('');
      } else {
        output = output + space + languages[currentLanguage].currency.symbol;
      }
    }
    return output;
  }
  function formatPercentage(n, format, roundingFunction) {
    var space = '',
        output,
        value = n._value * 100;
    if (format.indexOf(' %') > -1) {
      space = ' ';
      format = format.replace(' %', '');
    } else {
      format = format.replace('%', '');
    }
    output = formatNumber(value, format, roundingFunction);
    if (output.indexOf(')') > -1) {
      output = output.split('');
      output.splice(-1, 0, space + '%');
      output = output.join('');
    } else {
      output = output + space + '%';
    }
    return output;
  }
  function formatTime(n) {
    var hours = Math.floor(n._value / 60 / 60),
        minutes = Math.floor((n._value - (hours * 60 * 60)) / 60),
        seconds = Math.round(n._value - (hours * 60 * 60) - (minutes * 60));
    return hours + ':' + ((minutes < 10) ? '0' + minutes : minutes) + ':' + ((seconds < 10) ? '0' + seconds : seconds);
  }
  function unformatTime(string) {
    var timeArray = string.split(':'),
        seconds = 0;
    if (timeArray.length === 3) {
      seconds = seconds + (Number(timeArray[0]) * 60 * 60);
      seconds = seconds + (Number(timeArray[1]) * 60);
      seconds = seconds + Number(timeArray[2]);
    } else if (timeArray.length === 2) {
      seconds = seconds + (Number(timeArray[0]) * 60);
      seconds = seconds + Number(timeArray[1]);
    }
    return Number(seconds);
  }
  function formatNumber(value, format, roundingFunction) {
    var negP = false,
        signed = false,
        optDec = false,
        abbr = '',
        abbrK = false,
        abbrM = false,
        abbrB = false,
        abbrT = false,
        abbrForce = false,
        bytes = '',
        ord = '',
        abs = Math.abs(value),
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
        min,
        max,
        power,
        w,
        precision,
        thousands,
        d = '',
        neg = false;
    if (value === 0 && zeroFormat !== null) {
      return zeroFormat;
    } else {
      if (format.indexOf('(') > -1) {
        negP = true;
        format = format.slice(1, -1);
      } else if (format.indexOf('+') > -1) {
        signed = true;
        format = format.replace(/\+/g, '');
      }
      if (format.indexOf('a') > -1) {
        abbrK = format.indexOf('aK') >= 0;
        abbrM = format.indexOf('aM') >= 0;
        abbrB = format.indexOf('aB') >= 0;
        abbrT = format.indexOf('aT') >= 0;
        abbrForce = abbrK || abbrM || abbrB || abbrT;
        if (format.indexOf(' a') > -1) {
          abbr = ' ';
          format = format.replace(' a', '');
        } else {
          format = format.replace('a', '');
        }
        if (abs >= Math.pow(10, 12) && !abbrForce || abbrT) {
          abbr = abbr + languages[currentLanguage].abbreviations.trillion;
          value = value / Math.pow(10, 12);
        } else if (abs < Math.pow(10, 12) && abs >= Math.pow(10, 9) && !abbrForce || abbrB) {
          abbr = abbr + languages[currentLanguage].abbreviations.billion;
          value = value / Math.pow(10, 9);
        } else if (abs < Math.pow(10, 9) && abs >= Math.pow(10, 6) && !abbrForce || abbrM) {
          abbr = abbr + languages[currentLanguage].abbreviations.million;
          value = value / Math.pow(10, 6);
        } else if (abs < Math.pow(10, 6) && abs >= Math.pow(10, 3) && !abbrForce || abbrK) {
          abbr = abbr + languages[currentLanguage].abbreviations.thousand;
          value = value / Math.pow(10, 3);
        }
      }
      if (format.indexOf('b') > -1) {
        if (format.indexOf(' b') > -1) {
          bytes = ' ';
          format = format.replace(' b', '');
        } else {
          format = format.replace('b', '');
        }
        for (power = 0; power <= suffixes.length; power++) {
          min = Math.pow(1024, power);
          max = Math.pow(1024, power + 1);
          if (value >= min && value < max) {
            bytes = bytes + suffixes[power];
            if (min > 0) {
              value = value / min;
            }
            break;
          }
        }
      }
      if (format.indexOf('o') > -1) {
        if (format.indexOf(' o') > -1) {
          ord = ' ';
          format = format.replace(' o', '');
        } else {
          format = format.replace('o', '');
        }
        ord = ord + languages[currentLanguage].ordinal(value);
      }
      if (format.indexOf('[.]') > -1) {
        optDec = true;
        format = format.replace('[.]', '.');
      }
      w = value.toString().split('.')[0];
      precision = format.split('.')[1];
      thousands = format.indexOf(',');
      if (precision) {
        if (precision.indexOf('[') > -1) {
          precision = precision.replace(']', '');
          precision = precision.split('[');
          d = toFixed(value, (precision[0].length + precision[1].length), roundingFunction, precision[1].length);
        } else {
          d = toFixed(value, precision.length, roundingFunction);
        }
        w = d.split('.')[0];
        if (d.split('.')[1].length) {
          d = languages[currentLanguage].delimiters.decimal + d.split('.')[1];
        } else {
          d = '';
        }
        if (optDec && Number(d.slice(1)) === 0) {
          d = '';
        }
      } else {
        w = toFixed(value, null, roundingFunction);
      }
      if (w.indexOf('-') > -1) {
        w = w.slice(1);
        neg = true;
      }
      if (thousands > -1) {
        w = w.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1' + languages[currentLanguage].delimiters.thousands);
      }
      if (format.indexOf('.') === 0) {
        w = '';
      }
      return ((negP && neg) ? '(' : '') + ((!negP && neg) ? '-' : '') + ((!neg && signed) ? '+' : '') + w + d + ((ord) ? ord : '') + ((abbr) ? abbr : '') + ((bytes) ? bytes : '') + ((negP && neg) ? ')' : '');
    }
  }
  numeral = function(input) {
    if (numeral.isNumeral(input)) {
      input = input.value();
    } else if (input === 0 || typeof input === 'undefined') {
      input = 0;
    } else if (!Number(input)) {
      input = numeral.fn.unformat(input);
    }
    return new Numeral(Number(input));
  };
  numeral.version = VERSION;
  numeral.isNumeral = function(obj) {
    return obj instanceof Numeral;
  };
  numeral.language = function(key, values) {
    if (!key) {
      return currentLanguage;
    }
    if (key && !values) {
      if (!languages[key]) {
        throw new Error('Unknown language : ' + key);
      }
      currentLanguage = key;
    }
    if (values || !languages[key]) {
      loadLanguage(key, values);
    }
    return numeral;
  };
  numeral.languageData = function(key) {
    if (!key) {
      return languages[currentLanguage];
    }
    if (!languages[key]) {
      throw new Error('Unknown language : ' + key);
    }
    return languages[key];
  };
  numeral.language('en', {
    delimiters: {
      thousands: ',',
      decimal: '.'
    },
    abbreviations: {
      thousand: 'k',
      million: 'm',
      billion: 'b',
      trillion: 't'
    },
    ordinal: function(number) {
      var b = number % 10;
      return (~~(number % 100 / 10) === 1) ? 'th' : (b === 1) ? 'st' : (b === 2) ? 'nd' : (b === 3) ? 'rd' : 'th';
    },
    currency: {symbol: '$'}
  });
  numeral.zeroFormat = function(format) {
    zeroFormat = typeof(format) === 'string' ? format : null;
  };
  numeral.defaultFormat = function(format) {
    defaultFormat = typeof(format) === 'string' ? format : '0.0';
  };
  numeral.validate = function(val, culture) {
    var _decimalSep,
        _thousandSep,
        _currSymbol,
        _valArray,
        _abbrObj,
        _thousandRegEx,
        languageData,
        temp;
    if (typeof val !== 'string') {
      val += '';
      if (console.warn) {
        console.warn('Numeral.js: Value is not string. It has been co-erced to: ', val);
      }
    }
    val = val.trim();
    if (val === '') {
      return false;
    }
    val = val.replace(/^[+-]?/, '');
    try {
      languageData = numeral.languageData(culture);
    } catch (e) {
      languageData = numeral.languageData(numeral.language());
    }
    _currSymbol = languageData.currency.symbol;
    _abbrObj = languageData.abbreviations;
    _decimalSep = languageData.delimiters.decimal;
    if (languageData.delimiters.thousands === '.') {
      _thousandSep = '\\.';
    } else {
      _thousandSep = languageData.delimiters.thousands;
    }
    temp = val.match(/^[^\d]+/);
    if (temp !== null) {
      val = val.substr(1);
      if (temp[0] !== _currSymbol) {
        return false;
      }
    }
    temp = val.match(/[^\d]+$/);
    if (temp !== null) {
      val = val.slice(0, -1);
      if (temp[0] !== _abbrObj.thousand && temp[0] !== _abbrObj.million && temp[0] !== _abbrObj.billion && temp[0] !== _abbrObj.trillion) {
        return false;
      }
    }
    if (!!val.match(/^\d+$/)) {
      return true;
    }
    _thousandRegEx = new RegExp(_thousandSep + '{2}');
    if (!val.match(/[^\d.,]/g)) {
      _valArray = val.split(_decimalSep);
      if (_valArray.length > 2) {
        return false;
      } else {
        if (_valArray.length < 2) {
          return (!!_valArray[0].match(/^\d+.*\d$/) && !_valArray[0].match(_thousandRegEx));
        } else {
          if (_valArray[0].length === 1) {
            return (!!_valArray[0].match(/^\d+$/) && !_valArray[0].match(_thousandRegEx) && !!_valArray[1].match(/^\d+$/));
          } else {
            return (!!_valArray[0].match(/^\d+.*\d$/) && !_valArray[0].match(_thousandRegEx) && !!_valArray[1].match(/^\d+$/));
          }
        }
      }
    }
    return false;
  };
  function loadLanguage(key, values) {
    languages[key] = values;
  }
  if ('function' !== typeof Array.prototype.reduce) {
    Array.prototype.reduce = function(callback, opt_initialValue) {
      'use strict';
      if (null === this || 'undefined' === typeof this) {
        throw new TypeError('Array.prototype.reduce called on null or undefined');
      }
      if ('function' !== typeof callback) {
        throw new TypeError(callback + ' is not a function');
      }
      var index,
          value,
          length = this.length >>> 0,
          isValueSet = false;
      if (1 < arguments.length) {
        value = opt_initialValue;
        isValueSet = true;
      }
      for (index = 0; length > index; ++index) {
        if (this.hasOwnProperty(index)) {
          if (isValueSet) {
            value = callback(value, this[index], index, this);
          } else {
            value = this[index];
            isValueSet = true;
          }
        }
      }
      if (!isValueSet) {
        throw new TypeError('Reduce of empty array with no initial value');
      }
      return value;
    };
  }
  function multiplier(x) {
    var parts = x.toString().split('.');
    if (parts.length < 2) {
      return 1;
    }
    return Math.pow(10, parts[1].length);
  }
  function correctionFactor() {
    var args = Array.prototype.slice.call(arguments);
    return args.reduce(function(prev, next) {
      var mp = multiplier(prev),
          mn = multiplier(next);
      return mp > mn ? mp : mn;
    }, -Infinity);
  }
  numeral.fn = Numeral.prototype = {
    clone: function() {
      return numeral(this);
    },
    format: function(inputString, roundingFunction) {
      return formatNumeral(this, inputString ? inputString : defaultFormat, (roundingFunction !== undefined) ? roundingFunction : Math.round);
    },
    unformat: function(inputString) {
      if (Object.prototype.toString.call(inputString) === '[object Number]') {
        return inputString;
      }
      return unformatNumeral(this, inputString ? inputString : defaultFormat);
    },
    value: function() {
      return this._value;
    },
    valueOf: function() {
      return this._value;
    },
    set: function(value) {
      this._value = Number(value);
      return this;
    },
    add: function(value) {
      var corrFactor = correctionFactor.call(null, this._value, value);
      function cback(accum, curr, currI, O) {
        return accum + corrFactor * curr;
      }
      this._value = [this._value, value].reduce(cback, 0) / corrFactor;
      return this;
    },
    subtract: function(value) {
      var corrFactor = correctionFactor.call(null, this._value, value);
      function cback(accum, curr, currI, O) {
        return accum - corrFactor * curr;
      }
      this._value = [value].reduce(cback, this._value * corrFactor) / corrFactor;
      return this;
    },
    multiply: function(value) {
      function cback(accum, curr, currI, O) {
        var corrFactor = correctionFactor(accum, curr);
        return (accum * corrFactor) * (curr * corrFactor) / (corrFactor * corrFactor);
      }
      this._value = [this._value, value].reduce(cback, 1);
      return this;
    },
    divide: function(value) {
      function cback(accum, curr, currI, O) {
        var corrFactor = correctionFactor(accum, curr);
        return (accum * corrFactor) / (curr * corrFactor);
      }
      this._value = [this._value, value].reduce(cback);
      return this;
    },
    difference: function(value) {
      return Math.abs(numeral(this._value).subtract(value).value());
    }
  };
  if (hasModule) {
    module.exports = numeral;
  }
  if (typeof ender === 'undefined') {
    this['numeral'] = numeral;
  }
  if (typeof define === 'function' && define.amd) {
    define([], function() {
      return numeral;
    });
  }
}).call(window);


//# 
},{}]},{},[23,47,48,49,65,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,67,68,69,86,87,88,72,73,74,75,76,77,31,35,40,32,33,34,36,37,38,39]);
