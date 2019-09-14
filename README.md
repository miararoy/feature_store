# feature store



## Design

Feature store encapsules data query and feature extraction and exposes APIs for both data scientists and backend engineers.

## main features

1. Data extration (queries):
   1. query warehouse for training DS models
   2. query in app (real time) data for real time predictions (serving
   3. save and load queries to catalog for re-querying
2. Feature extractions:
   1. load feature extraction (etl) transformations from git (/web)
   2. run feature exraction against query
   3. save and load feature extraction (etl) to catalog


# API DOCUMENTATION
## extract/realtime
## POST
### app.extract_realtime
runs a query against training database
### Expected Response Types
| Response | Reason |
| -------- | ------ |
| 200      | OK     |
| 500      | Failed |

### Parameters
| Name  | In   | Description      | Required? | Type                                 |
| ----- | ---- | ---------------- | --------- | ------------------------------------ |
| query | body | the query to run | true      | [extract_rt](#extract_rt-definition) |

| Produces          |
| ----------------- |
| application/json; |

| Consumes         |
| ---------------- |
| application/json |


## extract/train
## POST
### app.extract_train
runs a query against training database
### Expected Response Types
| Response | Reason |
| -------- | ------ |
| 200      | OK     |
| 500      | Failed |

### Parameters
| Name  | In    | Description                      | Required? | Type                           |
| ----- | ----- | -------------------------------- | --------- | ------------------------------ |
| query | body  | the query to run                 | true      | [extract](#extract-definition) |

| Produces          |
| ----------------- |
| application/json; |

| Consumes         |
| ---------------- |
| application/json |


## publish
## PUT
### app.publish
creates flows and save to db, emulate user flow

### Expected Response Types
| Response | Reason |
| -------- | ------ |
| 200      | OK     |
| 500      | Failed |

### Parameters
| Name    | In    | Description     | Required? | Type    |
| ------- | ----- | --------------- | --------- | ------- |
| n_flows | query | number of flows | true      | integer |

| Produces          |
| ----------------- |
| application/json; |


## query/realtime
## POST
### app.query_realtime
runs a query against training database
updates database with hf
### Expected Response Types
| Response | Reason |
| -------- | ------ |
| 200      | OK     |
| 500      | Failed |

### Parameters
| Name  | In   | Description      | Required? | Type                             |
| ----- | ---- | ---------------- | --------- | -------------------------------- |
| query | body | the query to run | true      | [query_rt](#query_rt-definition) |

| Produces         |
| ---------------- |
| application/json |

| Consumes         |
| ---------------- |
| application/json |


## query/train
## POST
### app.query_train
runs a query against training database
updates database with hf
### Expected Response Types
| Response | Reason |
| -------- | ------ |
| 200      | OK     |
| 500      | Failed |

### Parameters
| Name  | In    | Description                      | Required? | Type                       |
| ----- | ----- | -------------------------------- | --------- | -------------------------- |
| query | body  | the query to run                 | true      | [query](#query-definition) |

### Content Types Produced
| Produces          |
| ----------------- |
| application/json; |

### Content Types Consumed
| Consumes         |
| ---------------- |
| application/json |


## Definitions
### extract Definition
| Property | Type   | Format |
| -------- | ------ | ------ |
| query_id | string |        |
| etl_path | string |        |
### extract_rt Definition
| Property    | Type   | Format |
| ----------- | ------ | ------ |
| query_id    | string |        |
| etl_path    | string |        |
| index_key   | string |        |
| index_value | string |        |
### query Definition
| Property   | Type   | Format |
| ---------- | ------ | ------ |
| query      | string |        |
| query_name | string |        |
### query_rt Definition
| Property    | Type   | Format |
| ----------- | ------ | ------ |
|             |        |        |
| query_id    | string |        |
| index_key   | string |        |
| index_value | string |        |