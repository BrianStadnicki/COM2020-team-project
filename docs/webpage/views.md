# Views & URLs

Django uses view functions (also referred to as views) to take web requests and return a web response. For this web application, the response consists of the following options: a HTML page, a redirect, or an HTTP error. To utilise these views, URLs are used to execute them whenever the corresponding web address is visited.

The structure of the web application will be abstracted as follows:

main/
├── seller/
│   ├── profile/
│   ├── reports/
│   ├── response/
│   ├── accessibility/
│   ├── bundles/
│   │   ├── create/
│   │   └── finalise/
│   ├── reservations/
│   ├── analytics/
│   └── activity/
│
├── consumer/
│   ├── profile/
│   ├── accessibility/
│   ├── impact/
│   ├── details/
│   ├── bundles/
│   ├── reservations/
│   └── reports/
│
└── developer/
    ├── reports/
    ├── company/
    └── developer_company/