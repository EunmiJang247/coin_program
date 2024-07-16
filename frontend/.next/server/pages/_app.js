(() => {
var exports = {};
exports.id = 888;
exports.ids = [888];
exports.modules = {

/***/ 7526:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": () => (/* binding */ _app)
});

// EXTERNAL MODULE: external "react/jsx-runtime"
var jsx_runtime_ = __webpack_require__(997);
// EXTERNAL MODULE: ./styles/globals.css
var globals = __webpack_require__(6764);
// EXTERNAL MODULE: external "react"
var external_react_ = __webpack_require__(6689);
;// CONCATENATED MODULE: ./contexts/sub-categories.ts

// TODO 에러를 감지할 수 없는 undefined를 여기에서 쓰는게 맞을까?
const SubCategoriesContext = (0,external_react_.createContext)(undefined);
/* harmony default export */ const sub_categories = (SubCategoriesContext);

;// CONCATENATED MODULE: ./services/read-sub-categories/index.ts
const useReadSubCategories = ()=>{
    return async ()=>{
        // TODO 원래는 서버로부터 가져와야 함.
        return [
            {
                id: "1",
                name: "육개장",
                slug: "yukgaejang"
            },
            {
                id: "2",
                name: "치킨",
                slug: "chicken"
            },
            {
                id: "3",
                name: "한솥",
                slug: "hansot"
            },
            {
                id: "4",
                name: "에그드랍",
                slug: "eggdrop"
            },
            {
                id: "5",
                name: "으아니 차",
                slug: "uanicha"
            }
        ];
    };
};
/* harmony default export */ const read_sub_categories = (useReadSubCategories);

;// CONCATENATED MODULE: ./providers/sub-categories.tsx




const SubCategoriesProvider = ({ children  })=>{
    const readSubCategories = read_sub_categories();
    const [categories, setCategories] = (0,external_react_.useState)(undefined);
    const init = async ()=>{
        // eslint-disable-next-line no-underscore-dangle
        const categories_ = await readSubCategories();
        setCategories(categories_);
    };
    (0,external_react_.useEffect)(()=>{
        init();
    }, []);
    return /*#__PURE__*/ jsx_runtime_.jsx(sub_categories.Provider, {
        value: categories,
        children: children
    });
};
/* harmony default export */ const providers_sub_categories = (SubCategoriesProvider);

;// CONCATENATED MODULE: ./pages/_app.tsx



const App = ({ Component , pageProps  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx(providers_sub_categories, {
        children: /*#__PURE__*/ jsx_runtime_.jsx(Component, {
            ...pageProps
        })
    });
};
/* harmony default export */ const _app = (App);


/***/ }),

/***/ 6764:
/***/ (() => {



/***/ }),

/***/ 6689:
/***/ ((module) => {

"use strict";
module.exports = require("react");

/***/ }),

/***/ 997:
/***/ ((module) => {

"use strict";
module.exports = require("react/jsx-runtime");

/***/ })

};
;

// load runtime
var __webpack_require__ = require("../webpack-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = (__webpack_exec__(7526));
module.exports = __webpack_exports__;

})();