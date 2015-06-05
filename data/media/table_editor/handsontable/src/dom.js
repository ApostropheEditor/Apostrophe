/**
 * DOM helper optimized for maximum performance
 * It is recommended for Handsontable plugins and renderers, because it is much faster than jQuery
 * @type {Object}
 */


export function enableImmediatePropagation(event) {
  if (event != null && event.isImmediatePropagationEnabled == null) {
    event.stopImmediatePropagation = function () {
      this.isImmediatePropagationEnabled = false;
      this.cancelBubble = true;
    };
    event.isImmediatePropagationEnabled = true;
    event.isImmediatePropagationStopped = function () {
      return !this.isImmediatePropagationEnabled;
    };
  }
}

/**
 * Goes up the DOM tree (including given element) until it finds an element that matches the nodes or nodes name.
 * This method goes up through web components.
 *
 * @param {HTMLElement} element Element from which traversing is started
 * @param {Array} nodes Array of elements or Array of elements name
 * @param {HTMLElement} [until]
 * @returns {HTMLElement|null}
 */
export function closest(element, nodes, until) {
  while (element != null && element !== until) {
    if (element.nodeType === Node.ELEMENT_NODE &&
      (nodes.indexOf(element.nodeName) > -1 || nodes.indexOf(element) > -1)) {
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

/**
 * Goes up the DOM tree and checks if element is child of another element
 * @param child Child element
 * @param {Object|string} parent Parent element OR selector of the parent element. If classname provided, function returns true for the first occurance of element with that class.
 * @returns {boolean}
 */
export function isChildOf(child, parent) {
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

/**
 * Check if an element is part of `hot-table` web component.
 *
 * @param {Element} element
 * @returns {Boolean}
 */
export function isChildOfWebComponentTable(element) {
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
    }
    else if (parentNode.host && parentNode.nodeType === Node.DOCUMENT_FRAGMENT_NODE) {
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

/**
 * Wrap element into polymer/webcomponent container if exists
 *
 * @param element
 * @returns {*}
 */
export function polymerWrap(element) {
  /* global Polymer */
  return typeof Polymer !== 'undefined' && typeof wrap === 'function' ? wrap(element) : element;
}

/**
 * Unwrap element from polymer/webcomponent container if exists
 *
 * @param element
 * @returns {*}
 */
export function polymerUnwrap(element) {
  /* global Polymer */
  return typeof Polymer !== 'undefined' && typeof unwrap === 'function' ? unwrap(element) : element;
}

/**
 * Checks if browser is support web components natively
 *
 * @returns {Boolean}
 */
export function isWebComponentSupportedNatively() {
  var test = document.createElement('div');

  return test.createShadowRoot && test.createShadowRoot.toString().match(/\[native code\]/) ? true : false;
}

/**
 * Counts index of element within its parent
 * WARNING: for performance reasons, assumes there are only element nodes (no text nodes). This is true for Walkotnable
 * Otherwise would need to check for nodeType or use previousElementSibling
 * @see http://jsperf.com/sibling-index/10
 * @param {Element} elem
 * @return {Number}
 */
export function index(elem) {
  var i = 0;
  if (elem.previousSibling) {
    /* jshint ignore:start */
    while (elem = elem.previousSibling) {
      ++i;
    }
    /* jshint ignore:end */
  }
  return i;
}

var classListSupport = document.documentElement.classList ? true : false;
var _hasClass, _addClass, _removeClass;

function filterEmptyClassNames(classNames) {
  var len = 0, result = [];

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
  var isSupportMultipleClassesArg = (function () {
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
    // http://snipplr.com/view/3561/addclass-removeclass-hasclass/
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
      // String.prototype.trim is defined in polyfill.js
      _className = _className.replace(createClassNameRegExp(className[len]), ' ').trim();
      len++;
    }
    if (element.className !== _className) {
      element.className = _className;
    }
  };
}

/**
 * Checks if element has class name
 *
 * @param {HTMLElement} element
 * @param {String} className Class name to check
 * @returns {Boolean}
 */
export function hasClass(element, className) {
  return _hasClass(element, className);
}

/**
 * Add class name to an element
 *
 * @param {HTMLElement} element
 * @param {String|Array} className Class name as string or array of strings
 */
export function addClass(element, className) {
  return _addClass(element, className);
}

/**
 * Remove class name from an element
 *
 * @param {HTMLElement} element
 * @param {String|Array} className Class name as string or array of strings
 */
export function removeClass(element, className) {
  return _removeClass(element, className);
}

export function removeTextNodes(elem, parent) {
  if (elem.nodeType === 3) {
    parent.removeChild(elem); //bye text nodes!
  }
  else if (['TABLE', 'THEAD', 'TBODY', 'TFOOT', 'TR'].indexOf(elem.nodeName) > -1) {
    var childs = elem.childNodes;
    for (var i = childs.length - 1; i >= 0; i--) {
      removeTextNodes(childs[i], elem);
    }
  }
}

/**
 * Remove childs function
 * WARNING - this doesn't unload events and data attached by jQuery
 * http://jsperf.com/jquery-html-vs-empty-vs-innerhtml/9
 * http://jsperf.com/jquery-html-vs-empty-vs-innerhtml/11 - no siginificant improvement with Chrome remove() method
 * @param element
 * @returns {void}
 */
//
export function empty(element) {
  var child;
  /* jshint ignore:start */
  while (child = element.lastChild) {
    element.removeChild(child);
  }
  /* jshint ignore:end */
}

export var HTML_CHARACTERS = /(<(.*)>|&(.*);)/;

/**
 * Insert content into element trying avoid innerHTML method.
 * @return {void}
 */
export function fastInnerHTML(element, content) {
  if (HTML_CHARACTERS.test(content)) {
    element.innerHTML = content;
  }
  else {
    fastInnerText(element, content);
  }
}

/**
 * Insert text content into element
 * @return {void}
 */

var textContextSupport = document.createTextNode('test').textContent ? true : false;

export function fastInnerText(element, content) {
  var child = element.firstChild;

  if (child && child.nodeType === 3 && child.nextSibling === null) {
    // fast lane - replace existing text node

    if (textContextSupport) {
      // http://jsperf.com/replace-text-vs-reuse
      child.textContent = content;
    } else {
      // http://jsperf.com/replace-text-vs-reuse
      child.data = content;
    }
  }
  else {
    //slow lane - empty element and insert a text node
    empty(element);
    element.appendChild(document.createTextNode(content));
  }
}

/**
 * Returns true if element is attached to the DOM and visible, false otherwise
 * @param elem
 * @returns {boolean}
 */
export function isVisible(elem) {
  var next = elem;

  while (polymerUnwrap(next) !== document.documentElement) { //until <html> reached
    if (next === null) { //parent detached from DOM
      return false;
    }
    else if (next.nodeType === Node.DOCUMENT_FRAGMENT_NODE) {
      if (next.host) { //this is Web Components Shadow DOM
        //see: http://w3c.github.io/webcomponents/spec/shadow/#encapsulation
        //according to spec, should be if (next.ownerDocument !== window.document), but that doesn't work yet
        if (next.host.impl) { //Chrome 33.0.1723.0 canary (2013-11-29) Web Platform features disabled
          return isVisible(next.host.impl);
        }
        else if (next.host) { //Chrome 33.0.1723.0 canary (2013-11-29) Web Platform features enabled
          return isVisible(next.host);
        }
        else {
          throw new Error("Lost in Web Components world");
        }
      }
      else {
        return false; //this is a node detached from document in IE8
      }
    }
    else if (next.style.display === 'none') {
      return false;
    }
    next = next.parentNode;
  }

  return true;
}

/**
 * Returns elements top and left offset relative to the document. Function is not compatible with jQuery offset.
 *
 * @param {HTMLElement} elem
 * @return {Object} Returns object with `top` and `left` props
 */
export function offset(elem) {
  var offsetLeft,
    offsetTop,
    lastElem,
    docElem,
    box;

  docElem = document.documentElement;

  if (hasCaptionProblem() && elem.firstChild && elem.firstChild.nodeName === 'CAPTION') {
    // fixes problem with Firefox ignoring <caption> in TABLE offset (see also export outerHeight)
    // http://jsperf.com/offset-vs-getboundingclientrect/8
    box = elem.getBoundingClientRect();

    return {
      top: box.top + (window.pageYOffset || docElem.scrollTop) - (docElem.clientTop || 0),
      left: box.left + (window.pageXOffset || docElem.scrollLeft) - (docElem.clientLeft || 0)
    };
  }
  offsetLeft = elem.offsetLeft;
  offsetTop = elem.offsetTop;
  lastElem = elem;

  /* jshint ignore:start */
  while (elem = elem.offsetParent) {
    // from my observation, document.body always has scrollLeft/scrollTop == 0
    if (elem === document.body) {
      break;
    }
    offsetLeft += elem.offsetLeft;
    offsetTop += elem.offsetTop;
    lastElem = elem;
  }
  /* jshint ignore:end */

  //slow - http://jsperf.com/offset-vs-getboundingclientrect/6
  if (lastElem && lastElem.style.position === 'fixed') {
    //if(lastElem !== document.body) { //faster but does gives false positive in Firefox
    offsetLeft += window.pageXOffset || docElem.scrollLeft;
    offsetTop += window.pageYOffset || docElem.scrollTop;
  }

  return {
    left: offsetLeft,
    top: offsetTop
  };
}

/**
 * Returns the document's scrollTop property
 * @returns {Number}
 */
export function getWindowScrollTop() {
  var res = window.scrollY;
  if (res == void 0) { //IE8-11
    res = document.documentElement.scrollTop;
  }
  return res;
}

/**
 * Returns the document's scrollLeft property
 * @returns {Number}
 */
export function getWindowScrollLeft() {
  var res = window.scrollX;
  if (res == void 0) { //IE8-11
    res = document.documentElement.scrollLeft;
  }
  return res;
}

/**
 * Returns the provided element's scrollTop property
 * @param elem
 * @returns {Number}
 */
export function getScrollTop(elem) {
  if (elem === window) {
    return getWindowScrollTop(elem);
  }
  else {
    return elem.scrollTop;
  }
}

/**
 * Returns the provided element's scrollLeft property
 * @param elem
 * @returns {Number}
 */
export function getScrollLeft(elem) {
  if (elem === window) {
    return getWindowScrollLeft(elem);
  }
  else {
    return elem.scrollLeft;
  }
}

/**
 * Returns a DOM element responsible for scrolling of the provided element
 * @param {HTMLElement} element
 * @returns {HTMLElement} Element's scrollable parent
 */
export function getScrollableElement(element) {
  var el = element.parentNode,
    props = ['auto', 'scroll'],
    overflow, overflowX, overflowY,
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

    if (el.clientHeight <= el.scrollHeight && (props.indexOf(overflowY) !== -1 || props.indexOf(overflow) !== -1 ||
      props.indexOf(computedOverflow) !== -1 || props.indexOf(computedOverflowY) !== -1)) {
      return el;
    }
    if (el.clientWidth <= el.scrollWidth && (props.indexOf(overflowX) !== -1 || props.indexOf(overflow) !== -1 ||
      props.indexOf(computedOverflow) !== -1 || props.indexOf(computedOverflowX) !== -1)) {
      return el;
    }
    el = el.parentNode;
  }

  return window;
}

/**
 * Returns a DOM element responsible for trimming the provided element
 * @param {HTMLElement} base Base element
 * @returns {HTMLElement} Base element's trimming parent
 */
export function getTrimmingContainer(base) {
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

/**
 * Returns a style property for the provided element. (Be it an inline or external style)
 * @param {HTMLElement} elem
 * @param {string} prop Wanted property
 * @returns {string} Element's style property
 */
export function getStyle(elem, prop) {
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

/**
 * Returns a computed style object for the provided element. (Needed if style is declared in external stylesheet)
 * @param elem
 * @returns {IEElementStyle|CssStyle} Elements computed style object
 */
export function getComputedStyle(elem) {
  return elem.currentStyle || document.defaultView.getComputedStyle(elem);
}

/**
 * Returns the element's outer width
 * @param elem
 * @returns {number} Element's outer width
 */
export function outerWidth(elem) {
  return elem.offsetWidth;
}

/**
 * Returns the element's outer height
 * @param elem
 * @returns {number} Element's outer height
 */
export function outerHeight(elem) {
  if (hasCaptionProblem() && elem.firstChild && elem.firstChild.nodeName === 'CAPTION') {
    //fixes problem with Firefox ignoring <caption> in TABLE.offsetHeight
    //jQuery (1.10.1) still has this unsolved
    //may be better to just switch to getBoundingClientRect
    //http://bililite.com/blog/2009/03/27/finding-the-size-of-a-table/
    //http://lists.w3.org/Archives/Public/www-style/2009Oct/0089.html
    //http://bugs.jquery.com/ticket/2196
    //http://lists.w3.org/Archives/Public/www-style/2009Oct/0140.html#start140
    return elem.offsetHeight + elem.firstChild.offsetHeight;
  }
  else {
    return elem.offsetHeight;
  }
}

/**
 * Returns the element's inner height
 * @param elem
 * @returns {number} Element's inner height
 */
export function innerHeight(elem) {
  return elem.clientHeight || elem.innerHeight;
}

/**
 * Returns the element's inner width
 * @param elem
 * @returns {number} Element's inner width
 */
export function innerWidth(elem) {
  return elem.clientWidth || elem.innerWidth;
}

export function addEvent(element, event, callback) {
  if (window.addEventListener) {
    element.addEventListener(event, callback, false);
  } else {
    element.attachEvent('on' + event, callback);
  }
}

export function removeEvent(element, event, callback) {
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
  _hasCaptionProblem = (TABLE.offsetHeight < 2 * TABLE.lastChild.offsetHeight); //boolean
  document.body.removeChild(TABLE);
}

export function hasCaptionProblem() {
  if (_hasCaptionProblem === void 0) {
    detectCaptionProblem();
  }
  return _hasCaptionProblem;
}

/**
 * Returns caret position in text input
 * @author http://stackoverflow.com/questions/263743/how-to-get-caret-position-in-textarea
 * @return {Number}
 */
export function getCaretPosition(el) {
  if (el.selectionStart) {
    return el.selectionStart;
  }
  else if (document.selection) { //IE8
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

/**
 * Returns end of the selection in text input
 * @return {Number}
 */
export function getSelectionEndPosition(el) {
  if (el.selectionEnd) {
    return el.selectionEnd;
  } else if (document.selection) { //IE8
    var r = document.selection.createRange();
    if (r == null) {
      return 0;
    }
    var re = el.createTextRange();

    return re.text.indexOf(r.text) + r.text.length;
  }
}

/**
 * Sets caret position in text input
 * @author http://blog.vishalon.net/index.php/javascript-getting-and-setting-caret-position-in-textarea/
 * @param {Element} el
 * @param {Number} pos
 * @param {Number} endPos
 */
export function setCaretPosition(el, pos, endPos) {
  if (endPos === void 0) {
    endPos = pos;
  }
  if (el.setSelectionRange) {
    el.focus();
    el.setSelectionRange(pos, endPos);
  }
  else if (el.createTextRange) { //IE8
    var range = el.createTextRange();
    range.collapse(true);
    range.moveEnd('character', endPos);
    range.moveStart('character', pos);
    range.select();
  }
}

var cachedScrollbarWidth;

//http://stackoverflow.com/questions/986937/how-can-i-get-the-browsers-scrollbar-sizes
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

/**
 * Returns the computed width of the native browser scroll bar
 * @return {Number} width
 */
export function getScrollbarWidth() {
  if (cachedScrollbarWidth === void 0) {
    cachedScrollbarWidth = walkontableCalculateScrollbarWidth();
  }
  return cachedScrollbarWidth;
}

var _isIE8 = !(document.createTextNode('test').textContent);

export function isIE8() {
  return isIE8;
}

var _isIE9 = !!(document.documentMode);

export function isIE9() {
  return _isIE9;
}

var _isSafari = (/Safari/.test(navigator.userAgent) && /Apple Computer/.test(navigator.vendor));

export function isSafari() {
  return _isSafari;
}

/**
 * Sets overlay position depending on it's type and used browser
 */
export function setOverlayPosition(overlayElem, left, top) {
  if (_isIE8 || _isIE9) {
    overlayElem.style.top = top;
    overlayElem.style.left = left;
  } else if (_isSafari) {
    /* jshint sub:true */
    overlayElem.style['-webkit-transform'] = 'translate3d(' + left + ',' + top + ',0)';
  } else {
    overlayElem.style.transform = 'translate3d(' + left + ',' + top + ',0)';
  }
}

export function getCssTransform(elem) {
  var transform;

  /* jshint sub:true */
  if (elem.style['transform'] && (transform = elem.style['transform']) !== '') {
    return ['transform', transform];

  } else if (elem.style['-webkit-transform'] && (transform = elem.style['-webkit-transform']) !== '') {

    return ['-webkit-transform', transform];
  }

  return -1;
}

export function resetCssTransform(elem) {
  /* jshint sub:true */
  if (elem['transform'] && elem['transform'] !== '') {
    elem['transform'] = '';
  } else if (elem['-webkit-transform'] && elem['-webkit-transform'] !== '') {
    elem['-webkit-transform'] = '';
  }
}

window.Handsontable = window.Handsontable || {};
Handsontable.Dom = {
  addClass,
  addEvent,
  closest,
  empty,
  enableImmediatePropagation,
  fastInnerHTML,
  fastInnerText,
  getCaretPosition,
  getComputedStyle,
  getCssTransform,
  getScrollableElement,
  getScrollbarWidth,
  getScrollLeft,
  getScrollTop,
  getStyle,
  getSelectionEndPosition,
  getTrimmingContainer,
  getWindowScrollLeft,
  getWindowScrollTop,
  hasCaptionProblem,
  hasClass,
  HTML_CHARACTERS,
  index,
  innerHeight,
  innerWidth,
  isChildOf,
  isChildOfWebComponentTable,
  isIE8,
  isIE9,
  isSafari,
  isVisible,
  isWebComponentSupportedNatively,
  offset,
  outerHeight,
  outerWidth,
  polymerUnwrap,
  polymerWrap,
  removeClass,
  removeEvent,
  removeTextNodes,
  resetCssTransform,
  setCaretPosition,
  setOverlayPosition
};
