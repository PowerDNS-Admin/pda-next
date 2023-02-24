/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
var SiteJS;
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./assets/javascript/app.js":
/*!**********************************!*\
  !*** ./assets/javascript/app.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"Cookies\": () => (/* binding */ Cookies),\n/* harmony export */   \"Modals\": () => (/* reexport safe */ _web_modals__WEBPACK_IMPORTED_MODULE_2__.Modals),\n/* harmony export */   \"Payments\": () => (/* reexport safe */ _payments__WEBPACK_IMPORTED_MODULE_1__.Payments)\n/* harmony export */ });\n/* harmony import */ var js_cookie__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! js-cookie */ \"./node_modules/js-cookie/dist/js.cookie.mjs\");\n/* harmony import */ var _payments__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./payments */ \"./assets/javascript/payments.js\");\n/* harmony import */ var _web_modals__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./web/modals */ \"./assets/javascript/web/modals.js\");\n // generated\n\n\n\n\n// pass-through for Cookies API\nvar Cookies = js_cookie__WEBPACK_IMPORTED_MODULE_0__[\"default\"];\n\n//# sourceURL=webpack://SiteJS/./assets/javascript/app.js?");

/***/ }),

/***/ "./assets/javascript/payments.js":
/*!***************************************!*\
  !*** ./assets/javascript/payments.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"Payments\": () => (/* binding */ Payments),\n/* harmony export */   \"addInputToForm\": () => (/* binding */ addInputToForm),\n/* harmony export */   \"createCardElement\": () => (/* binding */ createCardElement),\n/* harmony export */   \"createPaymentIntent\": () => (/* binding */ createPaymentIntent),\n/* harmony export */   \"showOrClearError\": () => (/* binding */ showOrClearError)\n/* harmony export */ });\n/* harmony import */ var js_cookie__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! js-cookie */ \"./node_modules/js-cookie/dist/js.cookie.mjs\");\n\n\n\nfunction addInputToForm(form, name, value) {\n  var hiddenInput = document.createElement('input');\n  hiddenInput.setAttribute('type', 'hidden');\n  hiddenInput.setAttribute('name', name);\n  hiddenInput.setAttribute('value', value);\n  form.appendChild(hiddenInput);\n}\nfunction showOrClearError(errorMessage) {\n  var displayError = document.getElementById('card-errors');\n  if (errorMessage) {\n    displayError.textContent = errorMessage;\n  } else {\n    displayError.textContent = '';\n  }\n}\nfunction createCardElement(stripe) {\n  var elements = stripe.elements();\n  var classes = {\n    base: 'stripe-element',\n    focus: 'focused-stripe-element',\n    invalid: 'invalid-stripe-element',\n    complete: 'complete-stripe-element'\n  };\n  var style = {\n    base: {\n      fontSize: '16px'\n    }\n  };\n  // Create an instance of the card Element.\n  var cardElement = elements.create('card', {\n    classes: classes,\n    style: style\n  });\n  cardElement.mount(\"#card-element\");\n  cardElement.addEventListener('change', function (event) {\n    var errorMessage = event.error ? event.error.message : '';\n    showOrClearError(errorMessage);\n  });\n  return cardElement;\n}\nvar createPaymentIntent = function createPaymentIntent(createPaymentIntentUrl, paymentData) {\n  // creates a payment intent in stripe and populates the result in the passed in clientSecrets dictionary\n  // (potentially overwriting what was previous there, in the case of a coupon changing the price)\n  // returns a promise\n  return new Promise(function (resolve, reject) {\n    var csrfToken = js_cookie__WEBPACK_IMPORTED_MODULE_0__[\"default\"].get('csrftoken');\n    paymentData = paymentData || {};\n    fetch(createPaymentIntentUrl, {\n      method: \"POST\",\n      headers: {\n        \"Content-Type\": \"application/json\",\n        'X-CSRFToken': csrfToken\n      },\n      credentials: 'same-origin',\n      body: JSON.stringify(paymentData)\n    }).then(function (result) {\n      return result.json();\n    }).then(function (data) {\n      resolve(data.client_secret);\n    })[\"catch\"](function (error) {\n      reject(error);\n    });\n  });\n};\nvar Payments = {\n  addInputToForm: addInputToForm,\n  createCardElement: createCardElement,\n  createPaymentIntent: createPaymentIntent,\n  showOrClearError: showOrClearError\n};\n\n//# sourceURL=webpack://SiteJS/./assets/javascript/payments.js?");

/***/ }),

/***/ "./assets/javascript/web/modals.js":
/*!*****************************************!*\
  !*** ./assets/javascript/web/modals.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"Modals\": () => (/* binding */ Modals),\n/* harmony export */   \"initializeModal\": () => (/* binding */ initializeModal)\n/* harmony export */ });\nfunction initializeModal(modalId) {\n  var openSelector = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : '.modal-opener';\n  var closeSelector = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : '.modal-closer';\n  var modal = document.getElementById(modalId);\n  (document.querySelectorAll(openSelector) || []).forEach(function (modalOpener) {\n    modalOpener.addEventListener('click', function () {\n      modal.classList.add('is-active');\n    });\n  });\n  (document.querySelectorAll(closeSelector) || []).forEach(function (modalCloser) {\n    modalCloser.addEventListener('click', function () {\n      modal.classList.remove('is-active');\n    });\n  });\n}\nvar Modals = {\n  initializeModal: initializeModal\n};\n\n//# sourceURL=webpack://SiteJS/./assets/javascript/web/modals.js?");

/***/ }),

/***/ "./node_modules/js-cookie/dist/js.cookie.mjs":
/*!***************************************************!*\
  !*** ./node_modules/js-cookie/dist/js.cookie.mjs ***!
  \***************************************************/
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (__WEBPACK_DEFAULT_EXPORT__)\n/* harmony export */ });\n/*! js-cookie v3.0.1 | MIT */\n/* eslint-disable no-var */\nfunction assign (target) {\n  for (var i = 1; i < arguments.length; i++) {\n    var source = arguments[i];\n    for (var key in source) {\n      target[key] = source[key];\n    }\n  }\n  return target\n}\n/* eslint-enable no-var */\n\n/* eslint-disable no-var */\nvar defaultConverter = {\n  read: function (value) {\n    if (value[0] === '\"') {\n      value = value.slice(1, -1);\n    }\n    return value.replace(/(%[\\dA-F]{2})+/gi, decodeURIComponent)\n  },\n  write: function (value) {\n    return encodeURIComponent(value).replace(\n      /%(2[346BF]|3[AC-F]|40|5[BDE]|60|7[BCD])/g,\n      decodeURIComponent\n    )\n  }\n};\n/* eslint-enable no-var */\n\n/* eslint-disable no-var */\n\nfunction init (converter, defaultAttributes) {\n  function set (key, value, attributes) {\n    if (typeof document === 'undefined') {\n      return\n    }\n\n    attributes = assign({}, defaultAttributes, attributes);\n\n    if (typeof attributes.expires === 'number') {\n      attributes.expires = new Date(Date.now() + attributes.expires * 864e5);\n    }\n    if (attributes.expires) {\n      attributes.expires = attributes.expires.toUTCString();\n    }\n\n    key = encodeURIComponent(key)\n      .replace(/%(2[346B]|5E|60|7C)/g, decodeURIComponent)\n      .replace(/[()]/g, escape);\n\n    var stringifiedAttributes = '';\n    for (var attributeName in attributes) {\n      if (!attributes[attributeName]) {\n        continue\n      }\n\n      stringifiedAttributes += '; ' + attributeName;\n\n      if (attributes[attributeName] === true) {\n        continue\n      }\n\n      // Considers RFC 6265 section 5.2:\n      // ...\n      // 3.  If the remaining unparsed-attributes contains a %x3B (\";\")\n      //     character:\n      // Consume the characters of the unparsed-attributes up to,\n      // not including, the first %x3B (\";\") character.\n      // ...\n      stringifiedAttributes += '=' + attributes[attributeName].split(';')[0];\n    }\n\n    return (document.cookie =\n      key + '=' + converter.write(value, key) + stringifiedAttributes)\n  }\n\n  function get (key) {\n    if (typeof document === 'undefined' || (arguments.length && !key)) {\n      return\n    }\n\n    // To prevent the for loop in the first place assign an empty array\n    // in case there are no cookies at all.\n    var cookies = document.cookie ? document.cookie.split('; ') : [];\n    var jar = {};\n    for (var i = 0; i < cookies.length; i++) {\n      var parts = cookies[i].split('=');\n      var value = parts.slice(1).join('=');\n\n      try {\n        var foundKey = decodeURIComponent(parts[0]);\n        jar[foundKey] = converter.read(value, foundKey);\n\n        if (key === foundKey) {\n          break\n        }\n      } catch (e) {}\n    }\n\n    return key ? jar[key] : jar\n  }\n\n  return Object.create(\n    {\n      set: set,\n      get: get,\n      remove: function (key, attributes) {\n        set(\n          key,\n          '',\n          assign({}, attributes, {\n            expires: -1\n          })\n        );\n      },\n      withAttributes: function (attributes) {\n        return init(this.converter, assign({}, this.attributes, attributes))\n      },\n      withConverter: function (converter) {\n        return init(assign({}, this.converter, converter), this.attributes)\n      }\n    },\n    {\n      attributes: { value: Object.freeze(defaultAttributes) },\n      converter: { value: Object.freeze(converter) }\n    }\n  )\n}\n\nvar api = init(defaultConverter, { path: '/' });\n/* eslint-enable no-var */\n\n/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (api);\n\n\n//# sourceURL=webpack://SiteJS/./node_modules/js-cookie/dist/js.cookie.mjs?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./assets/javascript/app.js");
/******/ 	(SiteJS = typeof SiteJS === "undefined" ? {} : SiteJS).app = __webpack_exports__;
/******/ 	
/******/ })()
;