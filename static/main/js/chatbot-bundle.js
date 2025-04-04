/*! For license information please see chatbot-bundle.js.LICENSE.txt */
(()=>{"use strict";var e={221:(e,t,n)=>{var r=n(540);function o(e){var t="https://react.dev/errors/"+e;if(1<arguments.length){t+="?args[]="+encodeURIComponent(arguments[1]);for(var n=2;n<arguments.length;n++)t+="&args[]="+encodeURIComponent(arguments[n])}return"Minified React error #"+e+"; visit "+t+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}function i(){}var a={d:{f:i,r:function(){throw Error(o(522))},D:i,C:i,L:i,m:i,X:i,S:i,M:i},p:0,findDOMNode:null},s=Symbol.for("react.portal"),c=r.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;function u(e,t){return"font"===e?"":"string"==typeof t?"use-credentials"===t?t:"":void 0}t.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE=a,t.createPortal=function(e,t){var n=2<arguments.length&&void 0!==arguments[2]?arguments[2]:null;if(!t||1!==t.nodeType&&9!==t.nodeType&&11!==t.nodeType)throw Error(o(299));return function(e,t,n){var r=3<arguments.length&&void 0!==arguments[3]?arguments[3]:null;return{$$typeof:s,key:null==r?null:""+r,children:e,containerInfo:t,implementation:n}}(e,t,null,n)},t.flushSync=function(e){var t=c.T,n=a.p;try{if(c.T=null,a.p=2,e)return e()}finally{c.T=t,a.p=n,a.d.f()}},t.preconnect=function(e,t){"string"==typeof e&&(t=t?"string"==typeof(t=t.crossOrigin)?"use-credentials"===t?t:"":void 0:null,a.d.C(e,t))},t.prefetchDNS=function(e){"string"==typeof e&&a.d.D(e)},t.preinit=function(e,t){if("string"==typeof e&&t&&"string"==typeof t.as){var n=t.as,r=u(n,t.crossOrigin),o="string"==typeof t.integrity?t.integrity:void 0,i="string"==typeof t.fetchPriority?t.fetchPriority:void 0;"style"===n?a.d.S(e,"string"==typeof t.precedence?t.precedence:void 0,{crossOrigin:r,integrity:o,fetchPriority:i}):"script"===n&&a.d.X(e,{crossOrigin:r,integrity:o,fetchPriority:i,nonce:"string"==typeof t.nonce?t.nonce:void 0})}},t.preinitModule=function(e,t){if("string"==typeof e)if("object"==typeof t&&null!==t){if(null==t.as||"script"===t.as){var n=u(t.as,t.crossOrigin);a.d.M(e,{crossOrigin:n,integrity:"string"==typeof t.integrity?t.integrity:void 0,nonce:"string"==typeof t.nonce?t.nonce:void 0})}}else null==t&&a.d.M(e)},t.preload=function(e,t){if("string"==typeof e&&"object"==typeof t&&null!==t&&"string"==typeof t.as){var n=t.as,r=u(n,t.crossOrigin);a.d.L(e,n,{crossOrigin:r,integrity:"string"==typeof t.integrity?t.integrity:void 0,nonce:"string"==typeof t.nonce?t.nonce:void 0,type:"string"==typeof t.type?t.type:void 0,fetchPriority:"string"==typeof t.fetchPriority?t.fetchPriority:void 0,referrerPolicy:"string"==typeof t.referrerPolicy?t.referrerPolicy:void 0,imageSrcSet:"string"==typeof t.imageSrcSet?t.imageSrcSet:void 0,imageSizes:"string"==typeof t.imageSizes?t.imageSizes:void 0,media:"string"==typeof t.media?t.media:void 0})}},t.preloadModule=function(e,t){if("string"==typeof e)if(t){var n=u(t.as,t.crossOrigin);a.d.m(e,{as:"string"==typeof t.as&&"script"!==t.as?t.as:void 0,crossOrigin:n,integrity:"string"==typeof t.integrity?t.integrity:void 0})}else a.d.m(e)},t.requestFormReset=function(e){a.d.r(e)},t.unstable_batchedUpdates=function(e,t){return e(t)},t.useFormState=function(e,t,n){return c.H.useFormState(e,t,n)},t.useFormStatus=function(){return c.H.useHostTransitionStatus()},t.version="19.1.0"},540:(e,t,n)=>{e.exports=n(869)},869:(e,t)=>{var n=Symbol.for("react.transitional.element"),r=Symbol.for("react.portal"),o=Symbol.for("react.fragment"),i=Symbol.for("react.strict_mode"),a=Symbol.for("react.profiler"),s=Symbol.for("react.consumer"),c=Symbol.for("react.context"),u=Symbol.for("react.forward_ref"),l=Symbol.for("react.suspense"),f=Symbol.for("react.memo"),p=Symbol.for("react.lazy"),d=Symbol.iterator,y={isMounted:function(){return!1},enqueueForceUpdate:function(){},enqueueReplaceState:function(){},enqueueSetState:function(){}},m=Object.assign,h={};function g(e,t,n){this.props=e,this.context=t,this.refs=h,this.updater=n||y}function v(){}function b(e,t,n){this.props=e,this.context=t,this.refs=h,this.updater=n||y}g.prototype.isReactComponent={},g.prototype.setState=function(e,t){if("object"!=typeof e&&"function"!=typeof e&&null!=e)throw Error("takes an object of state variables to update or a function which returns an object of state variables.");this.updater.enqueueSetState(this,e,t,"setState")},g.prototype.forceUpdate=function(e){this.updater.enqueueForceUpdate(this,e,"forceUpdate")},v.prototype=g.prototype;var _=b.prototype=new v;_.constructor=b,m(_,g.prototype),_.isPureReactComponent=!0;var S=Array.isArray,k={H:null,A:null,T:null,S:null,V:null},E=Object.prototype.hasOwnProperty;function w(e,t,r,o,i,a){return r=a.ref,{$$typeof:n,type:e,key:t,ref:void 0!==r?r:null,props:a}}function x(e){return"object"==typeof e&&null!==e&&e.$$typeof===n}var T=/\/+/g;function O(e,t){return"object"==typeof e&&null!==e&&null!=e.key?(n=""+e.key,r={"=":"=0",":":"=2"},"$"+n.replace(/[=:]/g,(function(e){return r[e]}))):t.toString(36);var n,r}function C(){}function A(e,t,o,i,a){var s=typeof e;"undefined"!==s&&"boolean"!==s||(e=null);var c,u,l=!1;if(null===e)l=!0;else switch(s){case"bigint":case"string":case"number":l=!0;break;case"object":switch(e.$$typeof){case n:case r:l=!0;break;case p:return A((l=e._init)(e._payload),t,o,i,a)}}if(l)return a=a(e),l=""===i?"."+O(e,0):i,S(a)?(o="",null!=l&&(o=l.replace(T,"$&/")+"/"),A(a,t,o,"",(function(e){return e}))):null!=a&&(x(a)&&(c=a,u=o+(null==a.key||e&&e.key===a.key?"":(""+a.key).replace(T,"$&/")+"/")+l,a=w(c.type,u,void 0,0,0,c.props)),t.push(a)),1;l=0;var f,y=""===i?".":i+":";if(S(e))for(var m=0;m<e.length;m++)l+=A(i=e[m],t,o,s=y+O(i,m),a);else if("function"==typeof(m=null===(f=e)||"object"!=typeof f?null:"function"==typeof(f=d&&f[d]||f["@@iterator"])?f:null))for(e=m.call(e),m=0;!(i=e.next()).done;)l+=A(i=i.value,t,o,s=y+O(i,m++),a);else if("object"===s){if("function"==typeof e.then)return A(function(e){switch(e.status){case"fulfilled":return e.value;case"rejected":throw e.reason;default:switch("string"==typeof e.status?e.then(C,C):(e.status="pending",e.then((function(t){"pending"===e.status&&(e.status="fulfilled",e.value=t)}),(function(t){"pending"===e.status&&(e.status="rejected",e.reason=t)}))),e.status){case"fulfilled":return e.value;case"rejected":throw e.reason}}throw e}(e),t,o,i,a);throw t=String(e),Error("Objects are not valid as a React child (found: "+("[object Object]"===t?"object with keys {"+Object.keys(e).join(", ")+"}":t)+"). If you meant to render a collection of children, use an array instead.")}return l}function N(e,t,n){if(null==e)return e;var r=[],o=0;return A(e,r,"","",(function(e){return t.call(n,e,o++)})),r}function R(e){if(-1===e._status){var t=e._result;(t=t()).then((function(t){0!==e._status&&-1!==e._status||(e._status=1,e._result=t)}),(function(t){0!==e._status&&-1!==e._status||(e._status=2,e._result=t)})),-1===e._status&&(e._status=0,e._result=t)}if(1===e._status)return e._result.default;throw e._result}var H="function"==typeof reportError?reportError:function(e){if("object"==typeof window&&"function"==typeof window.ErrorEvent){var t=new window.ErrorEvent("error",{bubbles:!0,cancelable:!0,message:"object"==typeof e&&null!==e&&"string"==typeof e.message?String(e.message):String(e),error:e});if(!window.dispatchEvent(t))return}else if("object"==typeof process&&"function"==typeof process.emit)return void process.emit("uncaughtException",e);console.error(e)};function j(){}t.Children={map:N,forEach:function(e,t,n){N(e,(function(){t.apply(this,arguments)}),n)},count:function(e){var t=0;return N(e,(function(){t++})),t},toArray:function(e){return N(e,(function(e){return e}))||[]},only:function(e){if(!x(e))throw Error("React.Children.only expected to receive a single React element child.");return e}},t.Component=g,t.Fragment=o,t.Profiler=a,t.PureComponent=b,t.StrictMode=i,t.Suspense=l,t.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE=k,t.__COMPILER_RUNTIME={__proto__:null,c:function(e){return k.H.useMemoCache(e)}},t.cache=function(e){return function(){return e.apply(null,arguments)}},t.cloneElement=function(e,t,n){if(null==e)throw Error("The argument must be a React element, but you passed "+e+".");var r=m({},e.props),o=e.key;if(null!=t)for(i in t.ref,void 0!==t.key&&(o=""+t.key),t)!E.call(t,i)||"key"===i||"__self"===i||"__source"===i||"ref"===i&&void 0===t.ref||(r[i]=t[i]);var i=arguments.length-2;if(1===i)r.children=n;else if(1<i){for(var a=Array(i),s=0;s<i;s++)a[s]=arguments[s+2];r.children=a}return w(e.type,o,void 0,0,0,r)},t.createContext=function(e){return(e={$$typeof:c,_currentValue:e,_currentValue2:e,_threadCount:0,Provider:null,Consumer:null}).Provider=e,e.Consumer={$$typeof:s,_context:e},e},t.createElement=function(e,t,n){var r,o={},i=null;if(null!=t)for(r in void 0!==t.key&&(i=""+t.key),t)E.call(t,r)&&"key"!==r&&"__self"!==r&&"__source"!==r&&(o[r]=t[r]);var a=arguments.length-2;if(1===a)o.children=n;else if(1<a){for(var s=Array(a),c=0;c<a;c++)s[c]=arguments[c+2];o.children=s}if(e&&e.defaultProps)for(r in a=e.defaultProps)void 0===o[r]&&(o[r]=a[r]);return w(e,i,void 0,0,0,o)},t.createRef=function(){return{current:null}},t.forwardRef=function(e){return{$$typeof:u,render:e}},t.isValidElement=x,t.lazy=function(e){return{$$typeof:p,_payload:{_status:-1,_result:e},_init:R}},t.memo=function(e,t){return{$$typeof:f,type:e,compare:void 0===t?null:t}},t.startTransition=function(e){var t=k.T,n={};k.T=n;try{var r=e(),o=k.S;null!==o&&o(n,r),"object"==typeof r&&null!==r&&"function"==typeof r.then&&r.then(j,H)}catch(e){H(e)}finally{k.T=t}},t.unstable_useCacheRefresh=function(){return k.H.useCacheRefresh()},t.use=function(e){return k.H.use(e)},t.useActionState=function(e,t,n){return k.H.useActionState(e,t,n)},t.useCallback=function(e,t){return k.H.useCallback(e,t)},t.useContext=function(e){return k.H.useContext(e)},t.useDebugValue=function(){},t.useDeferredValue=function(e,t){return k.H.useDeferredValue(e,t)},t.useEffect=function(e,t,n){var r=k.H;if("function"==typeof n)throw Error("useEffect CRUD overload is not enabled in this build of React.");return r.useEffect(e,t)},t.useId=function(){return k.H.useId()},t.useImperativeHandle=function(e,t,n){return k.H.useImperativeHandle(e,t,n)},t.useInsertionEffect=function(e,t){return k.H.useInsertionEffect(e,t)},t.useLayoutEffect=function(e,t){return k.H.useLayoutEffect(e,t)},t.useMemo=function(e,t){return k.H.useMemo(e,t)},t.useOptimistic=function(e,t){return k.H.useOptimistic(e,t)},t.useReducer=function(e,t,n){return k.H.useReducer(e,t,n)},t.useRef=function(e){return k.H.useRef(e)},t.useState=function(e){return k.H.useState(e)},t.useSyncExternalStore=function(e,t,n){return k.H.useSyncExternalStore(e,t,n)},t.useTransition=function(){return k.H.useTransition()},t.version="19.1.0"},961:(e,t,n)=>{!function e(){if("undefined"!=typeof __REACT_DEVTOOLS_GLOBAL_HOOK__&&"function"==typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE)try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(e)}catch(e){console.error(e)}}(),e.exports=n(221)}},t={};function n(r){var o=t[r];if(void 0!==o)return o.exports;var i=t[r]={exports:{}};return e[r](i,i.exports,n),i.exports}var r=n(540),o=n(961);const i=e=>{const t=(e=>e.replace(/^([A-Z])|[\s-_]+(\w)/g,((e,t,n)=>n?n.toUpperCase():t.toLowerCase())))(e);return t.charAt(0).toUpperCase()+t.slice(1)},a=(...e)=>e.filter(((e,t,n)=>Boolean(e)&&""!==e.trim()&&n.indexOf(e)===t)).join(" ").trim();var s={xmlns:"http://www.w3.org/2000/svg",width:24,height:24,viewBox:"0 0 24 24",fill:"none",stroke:"currentColor",strokeWidth:2,strokeLinecap:"round",strokeLinejoin:"round"};const c=(0,r.forwardRef)((({color:e="currentColor",size:t=24,strokeWidth:n=2,absoluteStrokeWidth:o,className:i="",children:c,iconNode:u,...l},f)=>(0,r.createElement)("svg",{ref:f,...s,width:t,height:t,stroke:e,strokeWidth:o?24*Number(n)/Number(t):n,className:a("lucide",i),...l},[...u.map((([e,t])=>(0,r.createElement)(e,t))),...Array.isArray(c)?c:[c]]))),u=(e,t)=>{const n=(0,r.forwardRef)((({className:n,...o},s)=>{return(0,r.createElement)(c,{ref:s,iconNode:t,className:a(`lucide-${u=i(e),u.replace(/([a-z0-9])([A-Z])/g,"$1-$2").toLowerCase()}`,`lucide-${e}`,n),...o});var u}));return n.displayName=i(e),n},l=u("message-circle",[["path",{d:"M7.9 20A9 9 0 1 0 4 16.1L2 22Z",key:"vv11sd"}]]),f=u("x",[["path",{d:"M18 6 6 18",key:"1bl5f8"}],["path",{d:"m6 6 12 12",key:"d8bk6v"}]]);function p(e){return function(e){if(Array.isArray(e))return m(e)}(e)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(e)||y(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function d(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=n){var r,o,i,a,s=[],c=!0,u=!1;try{if(i=(n=n.call(e)).next,0===t){if(Object(n)!==n)return;c=!1}else for(;!(c=(r=i.call(n)).done)&&(s.push(r.value),s.length!==t);c=!0);}catch(e){u=!0,o=e}finally{try{if(!c&&null!=n.return&&(a=n.return(),Object(a)!==a))return}finally{if(u)throw o}}return s}}(e,t)||y(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function y(e,t){if(e){if("string"==typeof e)return m(e,t);var n={}.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?m(e,t):void 0}}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=Array(t);n<t;n++)r[n]=e[n];return r}const h=function(){var e=d((0,r.useState)(!1),2),t=e[0],n=e[1],o=d((0,r.useState)([{text:"Hi there! I'm your GTJGo travel assistant. How can I help you today?",sender:"bot",options:["Transportation options","Safety information","Destination ideas","Travel planning"]}]),2),i=o[0],a=o[1],s=(0,r.useRef)(null),c=d((0,r.useState)(!1),2),u=c[0],y=c[1],m=function(e){switch(e){case"Transportation options":return{text:"What kind of transportation information are you looking for?",options:["Public transit in a city","Airport transfers","Car rentals"]};case"Public transit in a city":return{text:"Our Transport section can help you find subway stations, bus stops, and train stations in your destination city. Which city are you visiting?",options:["Paris","London","Tokyo","New York","Ask about another city"]};case"Airport transfers":return{text:"In the Rentals section, you can book transportation from airports to your hotel. Just enter your airport, date, and hotel to see available options.",options:["How does it work?","View popular airports","Back to main menu"]};case"Car rentals":return{text:"While we don't offer direct car rental bookings, our Rentals section focuses on airport transfers and local transportation options.",options:["Airport transfers","Public transit options","Back to main menu"]};case"Safety information":return{text:"What kind of safety information are you looking for?",options:["General safety ratings","Women/Solo traveler safety","Common scams and crimes","Emergency contacts"]};case"General safety ratings":return{text:"Our Safety section provides comprehensive safety ratings for destinations worldwide. We rate overall safety, crime rates, and provide specific advice for travelers.",options:["How are ratings calculated?","Check a specific destination","Back to safety menu"]};case"Women/Solo traveler safety":return{text:"We offer dedicated safety information for women and solo travelers, including safe neighborhoods, transportation tips, and cultural considerations.",options:["Safest destinations for women","Solo travel tips","Back to safety menu"]};case"Common scams and crimes":return{text:"Our safety guides include information about common tourist scams and crimes in different destinations, along with tips to stay safe.",options:["Popular scams to watch for","Check specific destination","Back to safety menu"]};case"Emergency contacts":return{text:"Our safety information includes emergency phone numbers and helpful contacts for different countries. You can find police, ambulance, and embassy contacts.",options:["Back to safety menu","Back to main menu"]};case"Destination ideas":return{text:"What kind of destination are you interested in?",options:["Beach destinations","City breaks","Adventure travel","Family-friendly places","Cultural experiences"]};case"Beach destinations":return{text:"Some popular beach destinations include Bali, Cancun, the Greek Islands, and Thailand. Each offers different experiences from relaxation to water sports.",options:["Safety in beach destinations","Transportation tips","More destination types","Back to main menu"]};case"City breaks":return{text:"Popular city destinations include Paris, London, Tokyo, New York, and Barcelona. Each offers unique cultural experiences, cuisine, and attractions.",options:["City safety information","Public transportation","More destination types","Back to main menu"]};case"Travel planning":return{text:"How can I help with your travel planning?",options:["Best time to visit destinations","Saving favorite places","Packing tips","Travel preparation checklist"]};case"Best time to visit destinations":return{text:"The best time to visit depends on your destination. Would you like general seasonal advice or information about a specific region?",options:["Europe seasons","Asia seasons","Americas seasons","Back to planning menu"]};case"Saving favorite places":return{text:"You can save your favorite destinations to your account by clicking the 'Add to Favorites' button. You'll need to be logged in to use this feature.",options:["How to create an account","Managing favorites","Back to planning menu"]};case"Paris":case"London":case"Tokyo":case"New York":return{text:"You can find detailed transportation information for ".concat(e," in our Transport section. There you'll see subway/metro stations, bus stops, and train connections."),options:["Safety information","Other cities","Back to main menu"]};case"Back to safety menu":return m("Safety information");case"Back to planning menu":return m("Travel planning");case"Back to main menu":return{text:"What else would you like to know about?",options:["Transportation options","Safety information","Destination ideas","Travel planning"]};default:return{text:"I'm here to help with your travel plans! What would you like to know about?",options:["Transportation options","Safety information","Destination ideas","Travel planning"]}}};return(0,r.useEffect)((function(){var e;null===(e=s.current)||void 0===e||e.scrollIntoView({behavior:"smooth"})}),[i]),r.createElement("div",{className:"fixed bottom-6 right-6 z-50"},!t&&r.createElement("button",{onClick:function(){return n(!0)},className:"bg-pink-200 hover:bg-pink-300 text-gray-800 rounded-full p-4 shadow-lg flex items-center"},r.createElement(l,{size:24}),r.createElement("span",{className:"ml-2 font-medium"},"Travel Assistant")),t&&r.createElement("div",{className:"bg-white rounded-lg shadow-xl flex flex-col w-80 sm:w-96 h-96 border border-gray-200"},r.createElement("div",{className:"bg-pink-200 text-gray-800 p-4 rounded-t-lg flex justify-between items-center"},r.createElement("h3",{className:"font-bold"},"GTJGo Travel Assistant"),r.createElement("button",{onClick:function(){return n(!1)},className:"text-gray-700 hover:text-gray-900"},r.createElement(f,{size:20}))),r.createElement("div",{className:"flex-1 p-4 overflow-y-auto"},i.map((function(e,t){return r.createElement("div",{key:t,className:"mb-3 ".concat("user"===e.sender?"text-right":"")},r.createElement("div",{className:"inline-block p-3 rounded-lg ".concat("user"===e.sender?"bg-pink-100 text-gray-800":"bg-gray-100 text-gray-800")},e.text),"bot"===e.sender&&e.options&&r.createElement("div",{className:"mt-2 flex flex-col gap-2"},e.options.map((function(e,t){return r.createElement("button",{key:t,onClick:function(){return function(e){var t={text:e,sender:"user"};a([].concat(p(i),[t])),y(!0),setTimeout((function(){var t=m(e),n={text:t.text,sender:"bot",options:t.options};a((function(e){return[].concat(p(e),[n])})),y(!1)}),700)}(e)},className:"text-left text-sm bg-white border border-gray-300 hover:bg-gray-50 text-gray-800 py-2 px-3 rounded-lg transition-colors"},e)}))))})),u&&r.createElement("div",{className:"mb-3"},r.createElement("div",{className:"inline-block bg-gray-100 p-3 rounded-lg text-gray-800"},r.createElement("div",{className:"typing-animation"},r.createElement("span",null),r.createElement("span",null),r.createElement("span",null)))),r.createElement("div",{ref:s}))),r.createElement("style",{jsx:!0},"\n        .typing-animation {\n          display: flex;\n          align-items: center;\n          column-gap: 6px;\n          padding: 0 3px;\n        }\n        .typing-animation span {\n          background-color: #9CA3AF;\n          border-radius: 50%;\n          height: 6px;\n          width: 6px;\n          display: block;\n          opacity: 0.4;\n        }\n        .typing-animation span:nth-child(1) {\n          animation: pulse 1s infinite ease-in-out;\n        }\n        .typing-animation span:nth-child(2) {\n          animation: pulse 1s infinite ease-in-out .2s;\n        }\n        .typing-animation span:nth-child(3) {\n          animation: pulse 1s infinite ease-in-out .4s;\n        }\n        @keyframes pulse {\n          0%, 100% {\n            opacity: 0.4;\n            transform: scale(1);\n          }\n          50% {\n            opacity: 1;\n            transform: scale(1.2);\n          }\n        }\n      "))};document.addEventListener("DOMContentLoaded",(function(){var e=document.getElementById("chatbot-root");e||((e=document.createElement("div")).id="chatbot-root",document.body.appendChild(e)),o.render(r.createElement(h,null),e)}))})();